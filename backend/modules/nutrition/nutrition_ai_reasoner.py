class NutritionAIReasoner:

    @staticmethod
    def explain(

        score,
        glycemic,
        heart,
        goals

    ):

        explanations = []

        if score >= 85:

            explanations.append(
                "Excellent nutritional profile."
            )

        elif score >= 70:

            explanations.append(
                "Balanced nutrition with moderate health benefits."
            )

        else:

            explanations.append(
                "Nutritional quality is below optimal."
            )

        if glycemic["risk"] == "HIGH":

            explanations.append(
                "High glycemic load may spike blood sugar."
            )

        if heart["status"] == "HIGH":

            explanations.append(
                "Potential cardiovascular risk due to sodium/fats."
            )

        if goals["muscle_gain_friendly"]:

            explanations.append(
                "Suitable for muscle building goals."
            )

        if goals["fat_loss_friendly"]:

            explanations.append(
                "Supports calorie deficit and fat loss."
            )

        return explanations