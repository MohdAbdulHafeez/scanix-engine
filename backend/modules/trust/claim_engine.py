import json

from pathlib import Path

from modules.trust.fssai_rules import (
    FSSAI_RULES
)

from modules.trust.evidence_engine import (
    EvidenceEngine
)

from modules.trust.confidence_engine import (
    ConfidenceEngine
)


BASE_DIR = Path(__file__).parent


class ClaimEngine:

    def __init__(self):

        with open(
            BASE_DIR / "ontology.json",
            "r",
            encoding="utf-8"
        ) as f:

            self.ontology = json.load(f)

    def analyze(

        self,
        claims,
        ingredients

    ):

        results = []

        for claim in claims:

            claim_lower = (
                claim.lower()
            )

            if claim_lower == "organic":

                results.append({

                    "claim":
                    claim,

                    "verdict":
                    "EVALUATED",

                    "confidence":
                    100,

                    "reason":
                    "Organic claim evaluated by Organic Engine.",

                    "evidence":
                    []

                })

                continue

            matched_rule = None

            for _, rule in (
                FSSAI_RULES.items()
            ):

                if (

                    rule.get(
                        "claim",
                        ""
                    ).lower().replace(
                        "_",
                        " "
                    ) == claim_lower
                ):

                    matched_rule = (
                        rule
                    )

                    break

            if not matched_rule:

                results.append({

                    "claim":
                    claim,

                    "verdict":
                    "UNVERIFIABLE",

                    "confidence":
                    0,

                    "reason":
                    "No regulatory rule available.",

                    "evidence":
                    []

                })

                continue

            if (

                matched_rule[
                    "type"
                ]

                ==

                "threshold"

            ):

                results.append({

                    "claim":
                    claim,

                    "verdict":
                    "EVALUATED",

                    "confidence":
                    100,

                    "reason":
                    "Claim evaluated through FSSAI threshold validator.",

                    "evidence":
                    []

                })

                continue

            ontology_key = (

                matched_rule[
                    "ontology_key"
                ]

            )

            ontology_items = (

                self.ontology[
                    ontology_key
                ]

            )

            evidence = (

                EvidenceEngine.collect(

                    claim=
                    claim,

                    ingredients=
                    ingredients,

                    ontology_items=
                    ontology_items

                )

            )

            passed = not (

                evidence[
                    "has_evidence"
                ]

            )

            confidence = (

                ConfidenceEngine.score(

                    evidence_count=
                    evidence[
                        "evidence_count"
                    ],

                    passed=
                    passed

                )

            )

            if passed:

                verdict = "PASS"

                reason = (

                    f"No prohibited ingredients detected for '{claim}'."

                )

            else:

                verdict = "FAIL"

                reason = (

                    f"Detected conflicting ingredients: {evidence['matches']}"

                )

            results.append({

                "claim":
                claim,

                "verdict":
                verdict,

                "confidence":
                confidence,

                "reason":
                reason,

                "evidence":
                evidence[
                    "matches"
                ]

            })

        summary = {

            "pass":

            len(

                [

                    x

                    for x

                    in results

                    if x[
                        "verdict"
                    ] == "PASS"

                ]

            ),

            "fail":

            len(

                [

                    x

                    for x

                    in results

                    if x[
                        "verdict"
                    ] == "FAIL"

                ]

            ),

            "evaluated":

            len(

                [

                    x

                    for x

                    in results

                    if x[
                        "verdict"
                    ] == "EVALUATED"

                ]

            ),

            "unverifiable":

            len(

                [

                    x

                    for x

                    in results

                    if x[
                        "verdict"
                    ] == "UNVERIFIABLE"

                ]

            )

        }

        return {

            "results":
            results,

            "summary":
            summary

        }