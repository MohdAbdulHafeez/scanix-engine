from modules.ingredients.data.additives_registry import (
ADDITIVES
)


class RiskEngine:

    @staticmethod
    def analyze(
        detected_additives
    ):

        hazardous=[]
        moderate=[]
        safe=[]

        total_score=0

        for additive in detected_additives:

            risk=additive.get(
                "risk",
                0
            )

            total_score+=risk

            if risk>=3:
                hazardous.append(
                    additive
                )

            elif risk>=2:
                moderate.append(
                    additive
                )

            else:
                safe.append(
                    additive
                )

        if total_score<=2:

            verdict="SAFE"

        elif total_score<=5:

            verdict="MODERATE"

        else:

            verdict="HIGH RISK"

        return {

            "verdict":
            verdict,

            "risk_score":
            total_score,

            "hazardous":
            hazardous,

            "moderate":
            moderate,

            "safe":
            safe,

            "hazardous_count":
            len(hazardous),

            "moderate_count":
            len(moderate),

            "safe_count":
            len(safe)

        }