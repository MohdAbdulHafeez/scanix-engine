from modules.trust.validator import (
    TrustValidator
)

from modules.trust.report import (
    ComplianceReport
)

from modules.trust.claim_engine import (
    ClaimEngine
)

from modules.trust.marketing_engine import (
    MarketingEngine
)

from modules.trust.organic_engine import (
    OrganicEngine
)

from modules.trust.compliance_engine import (
    ComplianceEngine
)

from modules.trust.trust_score import (
    TrustScore
)


class TrustService:

    @staticmethod
    def analyze(

        ingredients,
        nutrition,
        claims,
        marketing_text

    ):

        validator = (
            TrustValidator()
        )

        validation = (

            validator.validate(

                ingredients=
                ingredients,

                nutrition=
                nutrition,

                claims=
                claims

            )

        )

        claim_results = (

            ClaimEngine().analyze(

                claims=
                claims,

                ingredients=
                ingredients

            )

        )

        marketing = (

            MarketingEngine.analyze(

                marketing_text

            )

        )

        organic = (

            OrganicEngine().analyze(

                ingredients=
                ingredients,

                claims=
                claims

            )

        )

        compliance = (

            ComplianceEngine.build(

                validation=
                validation,

                claims=
                claim_results,

                marketing=
                marketing,

                organic=
                organic

            )

        )

        critical = (

            compliance[
                "critical"
            ]

        )

        trust_score = (

            TrustScore.compute(

                validation=
                validation,

                marketing=
                marketing,

                organic=
                organic,

                critical=
                critical

            )

        )

        report = (

            ComplianceReport.build(

                validation

            )

        )

        return {

            "claims":
            claim_results,

            "marketing":
            marketing,

            "organic":
            organic,

            "compliance":
            compliance,

            "trust_score":
            trust_score,

            "report":
            report

        }