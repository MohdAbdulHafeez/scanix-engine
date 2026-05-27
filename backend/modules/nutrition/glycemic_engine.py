from modules.nutrition.nutrition_registry import (
    NUTRITION_THRESHOLDS
)


class GlycemicEngine:

    @staticmethod
    def analyze(
        nutrition
    ):

        sugar = nutrition.get(
            "sugar",
            0
        )

        carbs = nutrition.get(
            "carbs",
            0
        )

        glycemic_load = round(

            (
                sugar * 0.6
            )

            +

            (
                carbs * 0.4
            ),

            2

        )

        if glycemic_load >= 25:

            risk = "HIGH"

        elif glycemic_load >= 12:

            risk = "MODERATE"

        else:

            risk = "LOW"

        return {

            "glycemic_load":
            glycemic_load,

            "risk":
            risk

        }