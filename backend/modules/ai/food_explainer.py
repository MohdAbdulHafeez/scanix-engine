from pathlib import Path

from modules.ai.providers.gemini_provider import (
    GeminiProvider
)

from modules.ai.rag_engine import (
    RAGEngine
)

from modules.ai.exceptions import (
    RAGError
)


class FoodExplainer:

    def __init__(self):

        self.llm = (
            GeminiProvider()
        )

        self.rag = (
            RAGEngine()
        )

        prompt_path = (

            Path(__file__).parent
            /
            "prompts"
            /
            "food_explainer.txt"

        )

        self.system_prompt = (

            prompt_path.read_text(
                encoding="utf-8"
            )
        )

    def explain(

        self,

        ingredients_result,
        nutrition_result,
        trust_result

    ):

        try:

            ingredients = []

            for ingredient in (

                ingredients_result.get(
                    "ingredients",
                    []
                )

            ):

                if isinstance(
                    ingredient,
                    dict
                ):
                    ingredients.append(
                        ingredient
                    )

                else:
                    ingredients.append({
                        "name":
                        ingredient
                    })

            ranked_ingredients = []

            for index, ingredient in enumerate(

                ingredients,

                start=1

            ):

                if isinstance(
                    ingredient,
                    dict
                ):

                    ranked_ingredients.append({

                        "name":

                        ingredient.get(
                            "name",
                            ""
                        ),

                        "position":
                        index

                    })

            additives = [

                item.get(
                    "name",
                    ""
                )

                for item in

                ingredients_result.get(
                    "additives",
                    []
                )

            ]

            rag_result = (

                self.rag.retrieve(

                    ingredients=
                    ingredients,

                    additives=
                    additives

                )

            )

            prompt = self._build_prompt(

                ingredients_result=
                ingredients_result,

                ranked_ingredients=
                ranked_ingredients,

                nutrition_result=
                nutrition_result,

                trust_result=
                trust_result,

                rag_result=
                rag_result

            )

            explanation = (

                self.llm.generate(
                    prompt
                )

            )

            return {

                "success":
                True,

                "explanation":
                explanation,

                "confidence":

                self._calculate_confidence(

                    rag_result

                ),

                "citations":

                rag_result[
                    "citations"
                ],

                "documents_found":

                rag_result[
                    "documents_found"
                ]

            }

        except Exception as e:

            raise RAGError(

                f"Food explanation failed: {str(e)}"

            )

    def _build_prompt(

        self,

        ingredients_result,
        ranked_ingredients,
        nutrition_result,
        trust_result,
        rag_result

    ):

        return f"""

{self.system_prompt}

========================================================

SCANIX INGREDIENT INTELLIGENCE

========================================================

{ingredients_result}

========================================================

INGREDIENT ORDER INFORMATION

========================================================

{ranked_ingredients}

Ingredients appearing earlier in the list
typically exist in higher quantities.

Ingredients appearing later in the list
typically exist in smaller quantities.

Use ingredient order while reasoning about:

- Health impact
- Ingredient quality
- Risk assessment
- Final verdict

========================================================

SCANIX NUTRITION INTELLIGENCE

========================================================

{nutrition_result}

========================================================

SCANIX TRUST INTELLIGENCE

========================================================

{trust_result}

========================================================

SCIENTIFIC EVIDENCE

========================================================

{rag_result["scientific_context"]}

========================================================

NUTRITION EVIDENCE

========================================================

{rag_result["nutrition_context"]}

========================================================

SAFETY EVIDENCE

========================================================

{rag_result["safety_context"]}

========================================================

SCIENTIFIC CONSENSUS

========================================================

{rag_result["scientific_consensus"]}

========================================================

EVIDENCE RULES

========================================================

Tier 1 sources are strongest.

Tier 2 sources are supporting evidence.

Tier 3 sources are weakest evidence.

If evidence conflicts:

state that evidence is mixed.

Never overstate causation.

Prefer:

"associated with"

"may increase risk"

"evidence suggests"

instead of:

"causes"

"proves"

"results in"

========================================================

INSTRUCTIONS

========================================================

Create a complete consumer report.

Include:

1. Executive Summary

2. Product Pros

3. Product Cons

4. Ingredient Analysis

5. Additive Analysis

6. Nutrition Analysis

7. Scientific Findings

8. Regulatory / Safety Findings

9. Long-Term Consumption Impact

10. Who Should Consume

11. Who Should Avoid

12. Final Verdict

Rules:

- Use supplied evidence only.
- Never invent scientific facts.
- Mention uncertainty if evidence is limited.
- Be consumer friendly.
- Explain complex science simply.
- Prioritize health and safety.
- Mention high-risk additives separately.
- Mention sugar, sodium and calorie concerns separately.
- Mention compliance concerns separately.

"""

    def _calculate_confidence(

        self,
        rag_result

    ):

        citations = (

            rag_result.get(
                "citations",
                []
            )
        )

        documents = (

            rag_result.get(
                "documents_found",
                0
            )
        )

        trusted = 0

        for citation in citations:

            if (

                citation.get(
                    "trust",
                    0
                ) >= 8

            ):

                trusted += 1

        score = 60

        score += min(
            trusted * 4,
            24
        )

        score += min(
            documents,
            16
        )

        return min(
            score,
            99
        )