from datetime import (
    datetime
)


class MultimodalContext:

    @staticmethod
    def build(

        question=None,

        image_analysis=None,

        voice_transcript=None,

        memory=None,

        ingredients_result=None,

        nutrition_result=None,

        trust_result=None,

        food_explainer=None,

        goal_result=None,

        risk_result=None,

        recommendation_result=None

    ):

        context = {

            "timestamp":

            datetime.utcnow()

            .isoformat(),

            "user_input": {

                "question":
                question,

                "voice_transcript":
                voice_transcript

            },

            "image_analysis":

            image_analysis

            or

            {},

            "memory":

            memory.build_context()

            if memory

            else

            "",

            "ingredients":

            ingredients_result

            or

            {},

            "nutrition":

            nutrition_result

            or

            {},

            "trust":

            trust_result

            or

            {},

            "food_explainer":

            food_explainer

            or

            {},

            "goal_analysis":

            goal_result

            or

            {},

            "risk_forecast":

            risk_result

            or

            {},

            "recommendations":

            recommendation_result

            or

            {}

        }

        return context

    # =====================================
    # Prompt Builder
    # =====================================

    @staticmethod
    def build_prompt(

        context

    ):

        return f"""

========================================================

SCANIX MULTIMODAL CONTEXT

========================================================

QUESTION

{context['user_input'].get('question')}

========================================================

VOICE TRANSCRIPT

{context['user_input'].get('voice_transcript')}

========================================================

IMAGE ANALYSIS

{context['image_analysis']}

========================================================

MEMORY

{context['memory']}

========================================================

INGREDIENT INTELLIGENCE

{context['ingredients']}

========================================================

NUTRITION INTELLIGENCE

{context['nutrition']}

========================================================

TRUST INTELLIGENCE

{context['trust']}

========================================================

FOOD EXPLAINER

{context['food_explainer']}

========================================================

GOAL ANALYSIS

{context['goal_analysis']}

========================================================

RISK FORECAST

{context['risk_forecast']}

========================================================

RECOMMENDATIONS

{context['recommendations']}

========================================================

Provide the best possible nutrition guidance.

Use all available intelligence.

Be evidence-based.

Be personalized.

Be actionable.

"""