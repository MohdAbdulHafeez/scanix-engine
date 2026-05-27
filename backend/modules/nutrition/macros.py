class MacroAnalyzer:

    @staticmethod
    def analyze(nutrition):

        protein = nutrition.get(
            "protein",
            0
        )

        carbs = nutrition.get(
            "carbs",
            0
        )

        fats = nutrition.get(
            "fat",
            0
        )

        fiber = nutrition.get(
            "fiber",
            0
        )

        calories = nutrition.get(
            "calories",
            0
        )

        return {

            "protein":
            protein,

            "carbs":
            carbs,

            "fat":
            fats,

            "fiber":
            fiber,

            "calories":
            calories,

            "high_protein":
            protein >= 15,

            "high_fiber":
            fiber >= 5,

            "low_calorie":
            calories <= 120

        }