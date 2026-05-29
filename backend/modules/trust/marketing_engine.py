from modules.trust.confidence_engine import (
    ConfidenceEngine
)


class MarketingEngine:

    MEDICAL_CLAIMS = [

        "cures",

        "treats",

        "prevents disease",

        "heals",

        "doctor recommended",

        "clinically proven",

        "medical grade"

    ]

    WEIGHT_LOSS_CLAIMS = [

        "fat burning",

        "instant weight loss",

        "rapid weight loss",

        "lose weight fast",

        "melt fat"

    ]

    ABSOLUTE_CLAIMS = [

        "100% healthy",

        "completely safe",

        "zero risk",

        "guaranteed results",

        "best in the world"

    ]

    FEAR_CLAIMS = [

        "toxin",

        "toxic",

        "poison",

        "dangerous chemicals",

        "deadly ingredients"

    ]

    @staticmethod
    def analyze(

        marketing_text

    ):

        text = (
            marketing_text
            .lower()
        )

        findings = []

        categories = {

            "MEDICAL":
            MarketingEngine.MEDICAL_CLAIMS,

            "WEIGHT_LOSS":
            MarketingEngine.WEIGHT_LOSS_CLAIMS,

            "ABSOLUTE":
            MarketingEngine.ABSOLUTE_CLAIMS,

            "FEAR":
            MarketingEngine.FEAR_CLAIMS

        }

        for category, phrases in (
            categories.items()
        ):

            for phrase in phrases:

                if phrase in text:

                    findings.append({

                        "category":
                        category,

                        "phrase":
                        phrase,

                        "severity":

                        "HIGH"

                        if category in [

                            "MEDICAL",

                            "WEIGHT_LOSS"

                        ]

                        else

                        "MEDIUM"

                    })

        evidence_count = len(
            findings
        )

        deceptive = (
            evidence_count > 0
        )

        confidence = (
            ConfidenceEngine.score(

                evidence_count=
                evidence_count,

                passed=
                not deceptive

            )
        )

        risk_score = max(

            0,

            100 -

            (
                evidence_count * 15
            )

        )

        if risk_score >= 85:

            risk_level = "LOW"

        elif risk_score >= 60:

            risk_level = "MODERATE"

        else:

            risk_level = "HIGH"

        return {

            "deceptive":
            deceptive,

            "confidence":
            confidence,

            "risk_score":
            risk_score,

            "risk_level":
            risk_level,

            "findings":
            findings

        }