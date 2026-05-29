from modules.trust.critical_rule_engine import (
    CriticalRuleEngine
)

from modules.trust.recommendation_engine import (
    RecommendationEngine
)


class ComplianceEngine:

    @staticmethod
    def build(

        validation,
        claims,
        marketing,
        organic

    ):

        critical = (

            CriticalRuleEngine.analyze(

                validation=
                validation,

                marketing=
                marketing,

                organic=
                organic

            )
        )

        recommendations = (

            RecommendationEngine.generate(

                validation=
                validation,

                marketing=
                marketing,

                organic=
                organic

            )
        )

        if (

            critical[
                "count"
            ] >= 3

        ):

            severity = "HIGH"

        elif (

            critical[
                "count"
            ] >= 1

        ):

            severity = "MODERATE"

        else:

            severity = "LOW"

        return {

            "compliant":

            validation[
                "compliant"
            ]

            and

            critical[
                "count"
            ] == 0,

            "severity":
            severity,

            "regulatory_risk":

            "HIGH"

            if critical[
                "count"
            ] >= 2

            else

            "LOW",

            "consumer_risk":

            "HIGH"

            if marketing[
                "deceptive"
            ]

            else

            "LOW",

            "fraud_risk":

            "HIGH"

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

            "LOW",

            "critical":
            critical,

            "recommendations":
            recommendations,

            "violations":
            validation[
                "violations"
            ],

            "warnings":
            validation[
                "warnings"
            ],

            "claims":
            claims,

            "marketing":
            marketing,

            "organic":
            organic

        }