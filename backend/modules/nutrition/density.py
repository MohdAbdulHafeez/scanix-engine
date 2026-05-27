class HealthDensity:

    @staticmethod
    def analyze(

        nutrition

    ):

        nutrients = (

            nutrition.get(
                "protein",
                0
            )

            +

            nutrition.get(
                "fiber",
                0
            )

            +

            nutrition.get(
                "vitamin_c",
                0
            )

        )

        calories = max(

            nutrition.get(
                "calories",
                1
            ),

            1

        )

        density = round(
            nutrients / calories,
            2
        )

        return {

            "density":
            density,

            "status":

            "HIGH"

        if density >= 0.35

            else

                "MODERATE"

        if density >= 0.18

            else

                "LOW"
        }