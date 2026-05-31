import os
import requests

from tavily import (
    TavilyClient
)


class WebRetriever:

    def __init__(self):

        self.tavily = TavilyClient(

            api_key=os.getenv(
                "TAVILY_API_KEY"
            )

        )

        self.timeout = int(

            os.getenv(

                "RAG_SEARCH_TIMEOUT",

                15

            )

        )

    # =====================================
    # Query Classification
    # =====================================

    def classify_query(

        self,
        term

    ):

        term = term.lower()

        additive_keywords = [

            "e100",
            "e102",
            "e110",
            "e211",
            "e250",
            "e621",

            "msg",

            "tartrazine",

            "benzoate",

            "preservative",

            "lecithin",

            "sodium bicarbonate",

            "sodium benzoate",

            "tartrazine",

            "monosodium glutamate",

            "artificial color"

        ]

        for keyword in additive_keywords:

            if keyword in term:

                return "additive"

        return "ingredient"

    # =====================================
    # Smart Query Builder
    # =====================================

    def build_query(

        self,
        term

    ):

        category = (

            self.classify_query(
                term
            )

        )

        if category == "additive":

            return (

                f"{term} food additive safety "
                f"FDA WHO EFSA PubMed "
                f"health effects"

            )

        return (

            f"{term} nutrition "
            f"health benefits "
            f"health risks "
            f"scientific evidence"

        )

    # =====================================
    # Tavily Search
    # =====================================

    def search_web(

        self,
        query,
        max_results=5

    ):

        try:

            response = (

                self.tavily.search(

                    query=query,

                    max_results=max_results,

                    search_depth="advanced"

                )

            )

            return response.get(
                "results",
                []
            )

        except Exception:

            return []

    # =====================================
    # OpenFoodFacts
    # =====================================

    def search_openfoodfacts(

        self,
        term

    ):

        try:

            response = requests.get(

                "https://world.openfoodfacts.org/cgi/search.pl",

                params={

                    "search_terms":
                    term,

                    "json":
                    1

                },

                timeout=self.timeout

            )

            data = response.json()

            return {

                "source":
                "OpenFoodFacts",

                "products":
                data.get(
                    "products",
                    []
                )[:5]

            }

        except Exception:

            return {}

    # =====================================
    # PubMed
    # =====================================

    def search_pubmed(

        self,
        query

    ):

        try:

            response = requests.get(

                "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi",

                params={

                    "db":
                    "pubmed",

                    "retmode":
                    "json",

                    "term":
                    query,

                    "retmax":
                    10

                },

                timeout=self.timeout

            )

            data = response.json()

            ids = (

                data

                .get(
                    "esearchresult",
                    {}
                )

                .get(
                    "idlist",
                    []
                )

            )

            return {

                "source":
                "PubMed",

                "ids":
                ids[:10]

            }

        except Exception:

            return {}

    # =====================================
    # OpenFDA
    # =====================================

    def search_fda(

        self,
        query

    ):

        try:

            response = requests.get(

                "https://api.fda.gov/food/enforcement.json",

                params={

                    "search":
                    query,

                    "limit":
                    5

                },

                timeout=self.timeout

            )

            return {

                "source":
                "FDA",

                "results":
                response.json()

            }

        except Exception:

            return {}

    # =====================================
    # Unified Scientific Retrieval
    # =====================================

    def retrieve_scientific_bundle(

        self,
        ingredient

    ):

        query = (

            self.build_query(
                ingredient
            )

        )

        return {

            "query":
            query,

            "category":
            self.classify_query(
                ingredient
            ),

            "web":

            self.search_web(

                query

            ),

            "pubmed":

            self.search_pubmed(

                ingredient

            ),

            "fda":

            self.search_fda(

                ingredient

            ),

            "openfoodfacts":

            self.search_openfoodfacts(

                ingredient

            )

        }