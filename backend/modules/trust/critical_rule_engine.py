class CriticalRuleEngine:

    @staticmethod
    def analyze(

        validation,
        marketing,
        organic

    ):

        critical = []

        for violation in (

            validation[
                "violations"
            ]

        ):

            rule = violation.get(
                "rule",
                ""
            )

            if rule in [

                "NO_PRESERVATIVES",
                "NO_ARTIFICIAL_COLORS",
                "VEGAN",
                "GLUTEN_FREE"

            ]:

                critical.append({

                    "type":
                    "REGULATORY",

                    "rule":
                    rule,

                    "reason":
                    violation[
                        "reason"
                    ]

                })

        if (

            organic[
                "organic_claim"
            ]

            and

            not organic[
                "organic_valid"
            ]

        ):

            critical.append({

                "type":
                "ORGANIC_FRAUD",

                "rule":
                "ORGANIC",

                "reason":
                "Organic claim conflicts with detected artificial ingredients."

            })

        for finding in (

            marketing[
                "findings"
            ]

        ):

            if (

                finding[
                    "category"
                ]

                ==

                "MEDICAL"

            ):

                critical.append({

                    "type":
                    "MEDICAL_MARKETING",

                    "rule":
                    "HEALTH_CLAIM",

                    "reason":
                    finding[
                        "phrase"
                    ]

                })

        return {

            "count":
            len(
                critical
            ),

            "critical_violations":
            critical

        }