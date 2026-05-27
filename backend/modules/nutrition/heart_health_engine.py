class HeartHealthEngine:

    @staticmethod
    def analyze(
        nutrition
    ):

        sodium = nutrition.get(
            "sodium",
            0
        )

        saturated_fat = nutrition.get(
            "saturated_fat",
            0
        )

        cholesterol = nutrition.get(
            "cholesterol",
            0
        )

        risk_score = 0

        if sodium > 500:
            risk_score += 1

        if saturated_fat > 6:
            risk_score += 1

        if cholesterol > 60:
            risk_score += 1

        if risk_score >= 3:

            status = "HIGH"

        elif risk_score >= 1:

            status = "MODERATE"

        else:

            status = "LOW"

        return {

            "risk_score":
            risk_score,

            "status":
            status

        }