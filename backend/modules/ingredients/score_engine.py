class IngredientScoreEngine:

    @staticmethod
    def compute(

        additive_risk,
        sugar_score,
        synergy_count,
        verifier_summary

    ):

        score = 100

        # additive penalties
        score -= (
            additive_risk * 4
        )

        # sugar penalties
        score -= (
            sugar_score * 0.15
        )

        # dangerous combinations
        score -= (
            synergy_count * 8
        )

        # failed claims
        score -= (
            verifier_summary.get(
                "fail",
                0
            ) * 5
        )

        # unverifiable claims
        score -= (
            verifier_summary.get(
                "unverifiable",
                0
            ) * 1
        )

        score = max(
            0,
            min(
                100,
                round(score)
            )
        )

        if score >= 90:

            grade = "A+"

        elif score >= 80:

            grade = "A"

        elif score >= 70:

            grade = "B"

        elif score >= 55:

            grade = "C"

        elif score >= 40:

            grade = "D"

        else:

            grade = "F"

        return {

            "score":
            score,

            "grade":
            grade,

            "rating": {

                "A+":
                "Excellent",

                "A":
                "Healthy",

                "B":
                "Acceptable",

                "C":
                "Moderate",

                "D":
                "Poor",

                "F":
                "Harmful"

            }[grade]

        }