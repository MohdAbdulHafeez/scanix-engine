class EvidenceEngine:

    @staticmethod
    def collect(

        claim,
        ingredients,
        ontology_items

    ):

        ingredients_lower = [

            x.lower()

            for x in ingredients

        ]

        matches = [

            item

            for item

            in ontology_items

            if item in (
                ingredients_lower
            )

        ]

        return {

            "claim":
            claim,

            "matches":
            matches,

            "evidence_count":
            len(
                matches
            ),

            "has_evidence":
            len(
                matches
            ) > 0

        }