import json

from pathlib import Path

from modules.trust.fssai_rules import (
    FSSAI_RULES
)


BASE_DIR = Path(__file__).parent


class TrustValidator:

    def __init__(self):

        with open(
            BASE_DIR / "ontology.json",
            "r",
            encoding="utf-8"
        ) as f:

            self.ontology = json.load(f)

        with open(
            BASE_DIR / "fssai_thresholds.json",
            "r",
            encoding="utf-8"
        ) as f:

            self.thresholds = json.load(f)

    def _evaluate_threshold(

        self,
        threshold_rule,
        nutrition

    ):

        nutrient = threshold_rule[
            "nutrient"
        ]

        operator = threshold_rule[
            "operator"
        ]

        threshold = threshold_rule[
            "threshold"
        ]

        value = nutrition.get(
            nutrient,
            0
        )

        if operator == ">=":

            return value >= threshold

        if operator == "<=":

            return value <= threshold

        return False

    def validate(

        self,
        ingredients,
        nutrition,
        claims

    ):

        ingredients_lower = [

            x.lower()

            for x in ingredients

        ]

        claims_lower = [

            x.lower()

            for x in claims

        ]

        violations = []

        passed_checks = []

        warnings = []

        for rule_name, rule in (
            FSSAI_RULES.items()
        ):

            # --------------------
            # CLAIM ABSENCE RULES
            # --------------------

            if rule["type"] == (
                "ingredient_absence"
            ):

                claim = rule[
                    "claim"
                ]

                if claim not in (
                    claims_lower
                ):

                    continue

                ontology_items = (
                    self.ontology[
                        rule[
                            "ontology_key"
                        ]
                    ]
                )

                detected = [

                    item

                    for item in (
                        ontology_items
                    )

                    if item in (
                        ingredients_lower
                    )

                ]

                if detected:

                    violations.append({

                        "rule":
                        rule_name,

                        "claim":
                        claim,

                        "severity":
                        "HIGH",

                        "reason":

                        f"Detected prohibited ingredients: {detected}"

                    })

                else:

                    passed_checks.append({

                        "rule":
                        rule_name,

                        "claim":
                        claim

                    })

            # --------------------
            # THRESHOLD RULES
            # --------------------

            elif rule["type"] == (
                "threshold"
            ):

                threshold_name = (
                    rule[
                        "threshold_key"
                    ]
                )

                if threshold_name not in (
                    claims_lower
                ):

                    continue

                threshold_rule = (
                    self.thresholds[
                        threshold_name
                    ]
                )

                passed = (
                    self._evaluate_threshold(

                        threshold_rule,

                        nutrition

                    )
                )

                if not passed:

                    nutrient = (
                        threshold_rule[
                            "nutrient"
                        ]
                    )

                    actual = nutrition.get(
                        nutrient,
                        0
                    )

                    violations.append({

                        "rule":
                        rule_name,

                        "claim":
                        threshold_name,

                        "severity":
                        "HIGH",

                        "reason":

                        f"{nutrient} value ({actual}) violates threshold"

                    })

                else:

                    passed_checks.append({

                        "rule":
                        rule_name,

                        "claim":
                        threshold_name

                    })

        # --------------------
        # WARNING ENGINE
        # --------------------

        sugar = nutrition.get(
            "sugar",
            0
        )

        sodium = nutrition.get(
            "sodium",
            0
        )

        fat = nutrition.get(
            "fat",
            0
        )

        if sugar >= 22:

            warnings.append(

                "High sugar product"

            )

        if sodium >= 600:

            warnings.append(

                "High sodium product"

            )

        if fat >= 20:

            warnings.append(

                "High fat product"

            )

        return {

            "compliant":
            len(
                violations
            ) == 0,

            "violations":
            violations,

            "warnings":
            warnings,

            "passed_checks":
            passed_checks

        }