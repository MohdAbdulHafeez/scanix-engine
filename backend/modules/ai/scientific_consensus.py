class ScientificConsensus:

    POSITIVE = [

        "benefit",
        "improve",
        "protect",
        "support",
        "reduce risk",
        "healthy"
    ]

    NEGATIVE = [

        "risk",
        "harm",
        "disease",
        "obesity",
        "cancer",
        "cholesterol",
        "diabetes"
    ]

    @staticmethod
    def analyze(

        citations

    ):

        positive = 0

        negative = 0

        neutral = 0

        for citation in citations:

            text = (

                citation.get(
                    "snippet",
                    ""
                )

                .lower()

            )

            pos = any(

                word in text

                for word in

                ScientificConsensus.POSITIVE

            )

            neg = any(

                word in text

                for word in

                ScientificConsensus.NEGATIVE

            )

            if pos and not neg:

                positive += 1

            elif neg and not pos:

                negative += 1

            else:

                neutral += 1

        if positive > negative * 2:

            consensus = (

                "MOSTLY_POSITIVE"
            )

        elif negative > positive * 2:

            consensus = (

                "MOSTLY_NEGATIVE"
            )

        else:

            consensus = (

                "MIXED_EVIDENCE"
            )

        return {

            "consensus":
            consensus,

            "positive":
            positive,

            "negative":
            negative,

            "neutral":
            neutral
        }