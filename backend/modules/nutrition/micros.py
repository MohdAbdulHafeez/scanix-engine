class MicroAnalyzer:

    @staticmethod
    def analyze(nutrition):

        vitamins = {

            "vitamin_a":
            nutrition.get(
                "vitamin_a",
                0
            ),

            "vitamin_c":
            nutrition.get(
                "vitamin_c",
                0
            ),

            "vitamin_d":
            nutrition.get(
                "vitamin_d",
                0
            ),

            "iron":
            nutrition.get(
                "iron",
                0
            ),

            "calcium":
            nutrition.get(
                "calcium",
                0
            )

        }

        richness = sum(
            1
            for v in vitamins.values()
            if v > 10
        )

        return {

            "vitamins":
            vitamins,

            "micronutrient_richness":
            richness,

            "status":
            "HIGH"
            if richness >= 4
            else "MODERATE"

        }