from modules.ingredients.parser import (
    IngredientParser
)

from modules.ingredients.claim_verifier import (
    verify_claims
)

from modules.ingredients.additives_engine import (
    AdditivesEngine
)

from modules.ingredients.risk import (
    RiskEngine
)

from modules.ingredients.sugar_detector import (
    SugarDetector
)

from modules.ingredients.synergy import (
    SynergyEngine
)

from modules.ingredients.score_engine import (
    IngredientScoreEngine
)

from modules.ingredients.scientific_reasoner import (
    ScientificReasoner
)


class IngredientService:

    @staticmethod
    def analyze(

        raw_ingredients,
        claims=[]

    ):

        ingredients = IngredientParser.parse(
            raw_ingredients
        )

        structured_ingredients = [

            {
                "text": ingredient,
                "id": f"en:{ingredient.lower().replace(' ', '-')}"
            }

            for ingredient in ingredients

        ]

        additives = AdditivesEngine.detect(
            ingredients
        )

        risk = RiskEngine.analyze(
            additives
        )

        sugar = SugarDetector.detect(
            ingredients
        )

        synergy = SynergyEngine.analyze(
            ingredients
        )

        verifier = verify_claims(

            claims=claims,

            ingredients=structured_ingredients,

            ingredients_text=", ".join(
                ingredients
            )

        )

        score = IngredientScoreEngine.compute(

            additive_risk=
            risk["risk_score"],

            sugar_score=
            sugar["sugar_score"],

            synergy_count=
            synergy["count"],

            verifier_summary=
            verifier["summary"]

        )

        reasoning = [

            ScientificReasoner.explain(
                additive
            )

            for additive in additives

        ]

        return {

            "ingredients":
            ingredients,

            "structured_ingredients":
            structured_ingredients,

            "additives":
            additives,

            "risk":
            risk,

            "sugar":
            sugar,

            "synergy":
            synergy,

            "claims":
            verifier,

            "score":
            score,

            "scientific_reasoning":
            reasoning

        }