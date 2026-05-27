DANGEROUS_COMBINATIONS=[

[
"sodium benzoate",
"ascorbic acid"
],

[
"msg",
"disodium inosinate"
],

[
"aspartame",
"acesulfame k"
]

]


class SynergyEngine:

    @staticmethod
    def analyze(
        ingredients
    ):

        detected=[]

        normalized=[
            i.lower()
            for i in ingredients
        ]

        for combo in DANGEROUS_COMBINATIONS:

            if all(
                item in " ".join(
                    normalized
                )
                for item in combo
            ):

                detected.append(
                    combo
                )

        return {

            "detected":
            detected,

            "count":
            len(detected),

            "risk":
            (
                "HIGH"
                if detected
                else "LOW"
            )

        }