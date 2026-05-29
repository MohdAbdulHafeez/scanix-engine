class TrustScore:

    @staticmethod
    def compute(

        validation,
        marketing,
        organic,
        critical

    ):

        score = 100

        regulatory_penalty = (

            len(
                validation[
                    "violations"
                ]
            ) * 10

        )

        marketing_penalty = (

            len(
                marketing[
                    "findings"
                ]
            ) * 8

        )

        organic_penalty = (

            25

            if (

                organic[
                    "organic_claim"
                ]

                and

                not organic[
                    "organic_valid"
                ]

            )

            else

            0

        )

        critical_penalty = (

            critical[
                "count"
            ] * 12

        )

        total_penalty = (

            regulatory_penalty
            +
            marketing_penalty
            +
            organic_penalty
            +
            critical_penalty

        )

        score -= total_penalty

        score = max(
            10,
            min(
                100,
                score
            )
        )

        if score >= 90:

            verdict = "TRUSTED"

        elif score >= 75:

            verdict = "GOOD"

        elif score >= 60:

            verdict = "QUESTIONABLE"

        else:

            verdict = "HIGH_RISK"

        explanation = []

        if regulatory_penalty > 0:

            explanation.append(

                f"{len(validation['violations'])} regulatory violation(s) detected."

            )

        if marketing_penalty > 0:

            explanation.append(

                f"{len(marketing['findings'])} deceptive marketing indicator(s) detected."

            )

        if organic_penalty > 0:

            explanation.append(

                "Organic claim conflict detected."

            )

        if critical_penalty > 0:

            explanation.append(

                f"{critical['count']} critical compliance violation(s) detected."

            )

        if not explanation:

            explanation.append(

                "No significant trust concerns detected."

            )

        return {

            "trust_score":
            score,

            "verdict":
            verdict,

            "components": {

                "regulatory_penalty":
                regulatory_penalty,

                "marketing_penalty":
                marketing_penalty,

                "organic_penalty":
                organic_penalty,

                "critical_penalty":
                critical_penalty,

                "total_penalty":
                total_penalty

            },

            "explanation":
            explanation

        }