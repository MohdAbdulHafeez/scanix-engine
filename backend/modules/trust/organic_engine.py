import json

from pathlib import Path

from modules.trust.evidence_engine import (
    EvidenceEngine
)

from modules.trust.confidence_engine import (
    ConfidenceEngine
)


BASE_DIR = Path(__file__).parent


class OrganicEngine:

    def __init__(self):

        with open(
            BASE_DIR / "ontology.json",
            "r",
            encoding="utf-8"
        ) as f:

            self.ontology = json.load(f)

    def analyze(

        self,
        ingredients,
        claims

    ):

        ingredients_lower = [

            i.lower()

            for i in ingredients

        ]

        organic_claim = any(

            "organic"

            in claim.lower()

            for claim

            in claims

        )

        if not organic_claim:

            return {

                "organic_claim":
                False,

                "organic_valid":
                None,

                "confidence":
                None,

                "conflicts":
                [],

                "reasoning":
                []

            }

        artificial_pool = (

            self.ontology[
                "artificial_colors"
            ]

            +

            self.ontology[
                "artificial_sweeteners"
            ]

            +

            self.ontology[
                "flavour_enhancers"
            ]

            +

            self.ontology[
                "preservatives"
            ]

        )

        evidence = (

            EvidenceEngine.collect(

                claim=
                "organic",

                ingredients=
                ingredients,

                ontology_items=
                artificial_pool

            )

        )

        conflicts = evidence[
            "matches"
        ]

        confidence = (

            ConfidenceEngine.score(

                evidence_count=
                evidence[
                    "evidence_count"
                ],

                passed=
                len(
                    conflicts
                ) == 0

            )
        )

        reasoning = []

        for item in conflicts:

            if item in (

                self.ontology[
                    "artificial_colors"
                ]

            ):

                reasoning.append(

                    f"Artificial color detected: {item}"

                )

            elif item in (

                self.ontology[
                    "artificial_sweeteners"
                ]

            ):

                reasoning.append(

                    f"Artificial sweetener detected: {item}"

                )

            elif item in (

                self.ontology[
                    "flavour_enhancers"
                ]

            ):

                reasoning.append(

                    f"Flavour enhancer detected: {item}"

                )

            elif item in (

                self.ontology[
                    "preservatives"
                ]

            ):

                reasoning.append(

                    f"Preservative detected: {item}"

                )

        return {

            "organic_claim":
            True,

            "organic_valid":
            len(
                conflicts
            ) == 0,

            "confidence":
            confidence,

            "conflicts":
            conflicts,

            "reasoning":
            reasoning

        }