from modules.ai.web_retriever import (
    WebRetriever
)

from modules.ai.citation_engine import (
    CitationEngine
)

from modules.ingredients.additive_mapper import (
    AdditiveMapper
)

from modules.ai.source_filter import (
    SourceFilter
)

from modules.ai.evidence_ranker import (
    EvidenceRanker
)

from modules.ai.scientific_consensus import (
    ScientificConsensus
)


class RAGEngine:

    def __init__(self):

        self.retriever = (
            WebRetriever()
        )

    def _rank_citations(

        self,
        citations

    ):

        return sorted(

            citations,

            key=lambda item:

            item.get(
                "trust",
                0
            ),

            reverse=True

        )

    def _evidence_strength(

        self,

        citations

    ):

        high = len([

            c

            for c in citations

            if c.get(
                "trust",
                0
            ) >= 8

        ])

        if high >= 6:

            return "HIGH"

        if high >= 3:

            return "MODERATE"

        return "LOW"

    def retrieve(

        self,
        ingredients,
        additives

    ):

        scientific_context = []

        nutrition_context = []

        safety_context = []

        all_documents = []

        processed = set()

        targets = []

        targets.extend(
            ingredients
        )

        resolved_additives = []

        for additive in additives:

            resolved_additives.append(

                AdditiveMapper.resolve(
                    additive
                )

            )

        targets.extend(
            resolved_additives
        )

        unique_targets = []

        seen = set()

        for target in targets:

            if isinstance(target, dict):

                name = str(
                    target.get(
                        "name",
                        ""
                    )
                ).lower()

            else:

                name = str(
                    target
                ).lower()

            if name in seen:

                continue

            seen.add(
                name
            )

            unique_targets.append(
                target
            )

        targets = unique_targets

        for item in targets[:10]:

            # ==========================
            # Handle Dict Ingredients
            # ==========================

            if isinstance(

                item,

                dict

            ):

                item_name = (

                    item.get(
                        "name",
                        ""
                    )

                )

            else:

                item_name = item

            item_name = str(

                item_name

            ).strip()

            if not item_name:

                continue

            key = item_name.lower()

            if key in processed:

                continue

            processed.add(
                key
            )

            bundle = (

                self.retriever
                .retrieve_scientific_bundle(

                    item_name

                )

            )

            category = (

                bundle.get(

                    "category",

                    "ingredient"

                )

            )

            query = (

                bundle.get(

                    "query",

                    item_name

                )

            )

            # =====================================
            # Tavily Documents
            # =====================================

            for doc in bundle.get(
                "web",
                []
            ):

                all_documents.append(
                    doc
                )

                title = doc.get(
                    "title",
                    ""
                )

                content = doc.get(
                    "content",
                    ""
                )

                evidence = f"""
QUERY:
{query}

SOURCE:
{title}

CONTENT:
{content}
"""

                scientific_context.append(
                    evidence
                )

            # =====================================
            # PubMed
            # =====================================

            pubmed = bundle.get(
                "pubmed",
                {}
            )

            ids = pubmed.get(
                "ids",
                []
            )

            if ids:

                safety_context.append(

                    f"""
SCIENTIFIC STUDIES

Target:
{item_name}

Category:
{category}

PubMed IDs:
{', '.join(ids)}
"""

                )

            # =====================================
            # FDA
            # =====================================

            fda = bundle.get(
                "fda",
                {}
            )

            if fda:

                safety_context.append(

                    f"""
FDA DATA FOUND

Target:
{item_name}

Category:
{category}
"""

                )

            # =====================================
            # OpenFoodFacts
            # =====================================

            off = bundle.get(
                "openfoodfacts",
                {}
            )

            products = off.get(
                "products",
                []
            )

            if products:

                nutrition_context.append(

                    f"""
OPENFOODFACTS DATA

Target:
{item_name}

Category:
{category}

Occurrences:
{len(products)}
"""

                )

                all_documents.append({

                    "title":
                    f"OpenFoodFacts - {item_name}",

                    "url":
                    "https://world.openfoodfacts.org",

                    "content":
                    str(products[:3])

                })

        citations = (

            CitationEngine.build(

                all_documents

            )

        )

        citations = (

            SourceFilter.filter(

                citations

            )

        )

        citations = (

            EvidenceRanker.rank(

                citations

            )

        )

        consensus = (

            ScientificConsensus.analyze(

                citations

            )

        )

        citations = (

            self._rank_citations(
                citations
            )

        )

        citation_summary = (

            CitationEngine.summarize(
                citations
            )

        )

        domains = set()

        for citation in citations:

            domains.add(

                citation.get(
                    "domain",
                    ""
                )

            )

        return {

            "scientific_context":

            "\n\n".join(

                scientific_context[:30]

            ),

            "nutrition_context":

            "\n\n".join(

                nutrition_context[:20]

            ),

            "safety_context":

            "\n\n".join(

                safety_context[:20]

            ),

            "citations":

            citations[:8],

            "citation_summary":

            citation_summary,

            "documents_found":

            len(
                all_documents
            ),

            "scientific_consensus":
            consensus,

            "evidence_strength":

            self._evidence_strength(
                citations
            ),

            "source_diversity":

            len(domains),

            "research_coverage": {

                "pubmed":
                bool(
                    safety_context
                ),

                "fda":
                "FDA DATA FOUND"
                in
                "\n".join(
                    safety_context
                ),

                "openfoodfacts":
                bool(
                    nutrition_context
                )

            }

        }