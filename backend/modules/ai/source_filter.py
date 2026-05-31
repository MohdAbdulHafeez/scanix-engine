TIER_1 = {

    "who.int",

    "fda.gov",

    "nih.gov",

    "ncbi.nlm.nih.gov",

    "pubmed.ncbi.nlm.nih.gov"
}

TIER_2 = {

    "efsa.europa.eu",

    "openfoodfacts.org"
}

TIER_3 = {

    "healthline.com",

    "webmd.com"
}


class SourceFilter:

    @staticmethod
    def classify(

        citation

    ):

        domain = (

            citation.get(
                "domain",
                ""
            )
        )

        if domain in TIER_1:

            return "TIER_1"

        if domain in TIER_2:

            return "TIER_2"

        if domain in TIER_3:

            return "TIER_3"

        return "UNKNOWN"

    @staticmethod
    def filter(

        citations

    ):

        filtered = []

        for citation in citations:

            citation["tier"] = (

                SourceFilter.classify(
                    citation
                )
            )

            filtered.append(
                citation
            )

        return filtered