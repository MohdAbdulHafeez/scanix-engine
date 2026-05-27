class BodyGoalEngine:

    @staticmethod
    def analyze(
        nutrition
    ):

        protein = nutrition.get(
            "protein",
            0
        )

        calories = nutrition.get(
            "calories",
            0
        )

        sugar = nutrition.get(
            "sugar",
            0
        )

        muscle_gain = (
            protein >= 20
        )

        fat_loss = (

            calories <= 220

            and

            sugar <= 10

        )

        return {

            "muscle_gain_friendly":
            muscle_gain,

            "fat_loss_friendly":
            fat_loss

        }