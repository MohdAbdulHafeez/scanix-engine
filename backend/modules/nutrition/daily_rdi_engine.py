from modules.nutrition.nutrition_registry import (
    DAILY_RDI
)


class DailyRDIEngine:

    @staticmethod
    def analyze(
        nutrition
    ):

        analysis = {}

        for nutrient, rdi in DAILY_RDI.items():

            value = nutrition.get(
                nutrient,
                0
            )

            percentage = round(
                (value / rdi) * 100,
                1
            )

            analysis[nutrient] = {

                "value":
                value,

                "daily_requirement":
                rdi,

                "percentage":
                percentage,

                "status":

                "HIGH"

                if percentage >= 70

                else

                "MODERATE"

                if percentage >= 30

                else

                "LOW"

            }

        return analysis