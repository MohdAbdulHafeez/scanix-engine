class ComplianceReport:

    @staticmethod
    def build(

        validation

    ):

        violation_count = len(

            validation[
                "violations"
            ]

        )

        warning_count = len(

            validation[
                "warnings"
            ]

        )

        compliance_score = 100

        compliance_score -= (
            violation_count * 25
        )

        compliance_score -= (
            warning_count * 5
        )

        compliance_score = max(
            0,
            compliance_score
        )

        if compliance_score >= 90:

            verdict = (
                "FULLY_COMPLIANT"
            )

        elif compliance_score >= 70:

            verdict = (
                "COMPLIANT_WITH_WARNINGS"
            )

        elif compliance_score >= 50:

            verdict = (
                "QUESTIONABLE"
            )

        else:

            verdict = (
                "NON_COMPLIANT"
            )

        return {

            "verdict":
            verdict,

            "compliance_score":
            compliance_score,

            "violation_count":
            violation_count,

            "warning_count":
            warning_count,

            "violations":
            validation[
                "violations"
            ],

            "warnings":
            validation[
                "warnings"
            ],

            "passed_checks":
            validation[
                "passed_checks"
            ],

            "consumer_summary":

            f"{violation_count} violations and {warning_count} warnings detected.",

            "regulatory_summary":

            f"Compliance score: {compliance_score}/100"

        }