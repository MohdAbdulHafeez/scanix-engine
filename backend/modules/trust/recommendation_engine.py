class RecommendationEngine:

    @staticmethod
    def generate(

        validation,
        marketing,
        organic

    ):

        recommendations = []

        if validation[
            "violations"
        ]:

            recommendations.append(

                "Review FSSAI claim compliance before product release."

            )

        if marketing[
            "deceptive"
        ]:

            recommendations.append(

                "Remove unsupported marketing and medical claims."

            )

        if (

            organic[
                "organic_claim"
            ]

            and

            not organic[
                "organic_valid"
            ]

        ):

            recommendations.append(

                "Remove organic claim or reformulate product."

            )

        if len(
            recommendations
        ) == 0:

            recommendations.append(

                "No major compliance concerns detected."

            )

        return recommendations