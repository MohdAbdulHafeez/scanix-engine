class EvidenceRanker:

    WEIGHTS = {

        "TIER_1": 100,

        "TIER_2": 75,

        "TIER_3": 50,

        "UNKNOWN": 25
    }

    @staticmethod
    def rank(

        citations

    ):

        ranked = []

        for citation in citations:

            tier = (

                citation.get(
                    "tier",
                    "UNKNOWN"
                )
            )

            citation[

                "evidence_score"

            ] = (

                EvidenceRanker.WEIGHTS.get(

                    tier,

                    25

                )

            )

            ranked.append(
                citation
            )

        ranked.sort(

            key=lambda item:

            item[
                "evidence_score"
            ],

            reverse=True

        )

        return ranked