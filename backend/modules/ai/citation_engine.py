from urllib.parse import (
    urlparse
)


TRUSTED_DOMAINS = {

    "who.int": 10,
    "fda.gov": 10,

    "nih.gov": 10,

    "ncbi.nlm.nih.gov": 10,

    "pubmed.ncbi.nlm.nih.gov": 10,

    "efsa.europa.eu": 9,

    "openfoodfacts.org": 8,

    "healthline.com": 7,

    "webmd.com": 7
}


DOMAIN_TYPES = {

    "who.int":
    "Government",

    "fda.gov":
    "Government",

    "nih.gov":
    "Research",

    "ncbi.nlm.nih.gov":
    "Research",

    "pubmed.ncbi.nlm.nih.gov":
    "Research",

    "efsa.europa.eu":
    "Regulatory",

    "openfoodfacts.org":
    "Food Database",

    "healthline.com":
    "Health Media",

    "webmd.com":
    "Health Media"
}


class CitationEngine:

    @staticmethod
    def build(

        documents

    ):

        citations = []

        seen = set()

        for doc in documents:

            url = doc.get(
                "url",
                ""
            )

            if not url:

                continue

            if url in seen:

                continue

            seen.add(
                url
            )

            domain = (

                urlparse(
                    url
                ).netloc.lower()

            )

            domain = (

                domain.replace(
                    "www.",
                    ""
                )

            )

            trust = (

                TRUSTED_DOMAINS.get(

                    domain,

                    5

                )

            )

            source_type = (

                DOMAIN_TYPES.get(

                    domain,

                    "General Web"

                )

            )

            title = doc.get(
                "title",
                ""
            )

            snippet = doc.get(
                "content",
                ""
            )

            citations.append({

                "title":
                title,

                "url":
                url,

                "domain":
                domain,

                "source_type":
                source_type,

                "trust":
                trust,

                "snippet":

                snippet[:300]

                if snippet

                else ""

            })

        citations.sort(

            key=lambda item: (

                item["trust"]

            ),

            reverse=True

        )

        return citations

    @staticmethod
    def summarize(

        citations

    ):

        if not citations:

            return {

                "trusted_sources":
                0,

                "research_sources":
                0,

                "government_sources":
                0
            }

        trusted_sources = sum(

            1

            for citation in citations

            if citation[
                "trust"
            ] >= 8

        )

        research_sources = sum(

            1

            for citation in citations

            if citation[
                "source_type"
            ] == "Research"

        )

        government_sources = sum(

            1

            for citation in citations

            if citation[
                "source_type"
            ] == "Government"

        )

        return {

            "trusted_sources":
            trusted_sources,

            "research_sources":
            research_sources,

            "government_sources":
            government_sources

        }