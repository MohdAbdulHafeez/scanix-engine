class ScientificReasoner:

    @staticmethod
    def explain(
        additive
    ):

        name=additive.get(
            "name",
            "Unknown"
        )

        risk=additive.get(
            "risk",
            0
        )

        if risk>=3:

            summary=(
                f"{name} is classified "
                f"as a high-risk additive "
                f"based on current "
                f"food safety references."
            )

        elif risk>=2:

            summary=(
                f"{name} should be "
                f"consumed in moderation."
            )

        else:

            summary=(
                f"{name} is generally "
                f"considered safe."
            )

        return {

            "additive":
            name,

            "scientific_summary":
            summary,

            "risk":
            risk

        }