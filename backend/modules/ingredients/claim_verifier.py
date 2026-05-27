"""
ingredient_verifier.py  ·  Ingredient-Based Claim Verification Engine
=====================================================================
Verifies consumer label claims purely from the structured ingredients
list returned by Open Food Facts (barcode-content endpoint).

Each claim defines:
- What ingredient taxonomy IDs or text patterns are FORBIDDEN
- What vegan/vegetarian flags to check
- A human-readable verdict with reason

Supported claims (verifiable from ingredients):
 - Vegan
 - Vegetarian
 - Dairy Free
 - No Added Sugar
 - No Artificial Additives (no E-codes)
 - No Preservatives (no E200-E299)
 - No Artificial Colors (no E100-E199)
 - No Artificial Emulsifiers (no E400-E499)
 - No Flavour Enhancers (no E600-E699)
 - No Artificial Flavours
 - No Palm Oil
 - Gluten Free
 - No Soy
 - No Nuts
"""

from __future__ import annotations

import re
import time
import logging
from functools import lru_cache
from typing import List, Dict, Any

logger = logging.getLogger(__name__)


# ── Supported Claims Registry ─────────────────────────────────────────────────

SUPPORTED_CLAIMS: Dict[str, Dict[str, str]] = {
    "Vegan": {
        "description": "All ingredients must be of plant/non-animal origin.",
        "icon": "leaf",
    },
    "Vegetarian": {
        "description": "No meat, poultry, or seafood ingredients.",
        "icon": "salad",
    },
    "Dairy Free": {
        "description": "No milk, cream, cheese, butter, or whey ingredients.",
        "icon": "milk-off",
    },
    "No Added Sugar": {
        "description": "No sugar, sweeteners, or sugar-derived ingredients.",
        "icon": "candy-slash",
    },
    "No Palm Oil": {
        "description": "No palm oil or ingredients derived from palm.",
        "icon": "tree-palm",
    },
    "No Artificial Additives": {
        "description": "No E-number food additives (all categories).",
        "icon": "flask",
    },
    "No Preservatives": {
        "description": "No preservative additives (E200–E299).",
        "icon": "shield",
    },
    "No Artificial Colors": {
        "description": "No artificial colour additives (E100–E199).",
        "icon": "palette",
    },
    "No Artificial Emulsifiers": {
        "description": "No emulsifier additives (E400–E499).",
        "icon": "microscope",
    },
    "No Flavour Enhancers": {
        "description": "No flavour-enhancer additives (E600–E699).",
        "icon": "tongue",
    },
    "No Artificial Flavours": {
        "description": "No artificial or synthetic flavouring ingredients.",
        "icon": "herb",
    },
    "Gluten Free": {
        "description": "No wheat, barley, rye, or gluten-containing ingredients.",
        "icon": "wheat-slash",
    },
    "No Soy": {
        "description": "No soy, soya, or soybean-derived ingredients.",
        "icon": "bean-off",
    },
    "No Nuts": {
        "description": "No tree nuts or peanut ingredients.",
        "icon": "peanut-slash",
    },
}


# ── Regex helpers ─────────────────────────────────────────────────────────────

_E_CODE_RE = re.compile(
    r"\ben?[-\s]?\d{3,4}[a-z]?\b",
    re.IGNORECASE
)


@lru_cache(maxsize=500)
def _is_e_code(text: str) -> bool:
    return bool(_E_CODE_RE.search(text))


@lru_cache(maxsize=500)
def _e_code_in_range(text: str, lo: int, hi: int) -> bool:
    """Return True if any E-number in text falls in [lo, hi]."""
    for m in _E_CODE_RE.finditer(text):
        digits = re.search(r"\d+", m.group())
        if digits and lo <= int(digits.group()) <= hi:
            return True
    return False


# ── Flat ingredient extractor ─────────────────────────────────────────────────

def flatten_ingredients(ingredients: List[Dict]) -> List[Dict]:
    """Recursively flatten nested ingredient lists into a single list."""
    flat: List[Dict] = []
    for ing in ingredients:
        flat.append(ing)
        if "ingredients" in ing and isinstance(ing["ingredients"], list):
            flat.extend(flatten_ingredients(ing["ingredients"]))
    return flat


# ── Taxonomy IDs & Regex Patterns ─────────────────────────────────────────────

_DAIRY_IDS = {
    "en:milk",
    "en:whole-milk",
    "en:skim-milk",
    "en:low-fat-milk",
    "en:whole-milk-powder",
    "en:skim-milk-powder",
    "en:milk-powder",
    "en:cream",
    "en:butter",
    "en:cheese",
    "en:whey",
    "en:whey-permeate",
    "en:whey-protein",
    "en:casein",
    "en:lactose",
    "en:cow-s-milk",
    "en:ghee",
    "en:buttermilk",
    "en:condensed-milk",
}

_DAIRY_TEXT = re.compile(
    r"\b(milk|cream|butter|cheese|whey|casein|lactose|ghee|buttermilk|curd|paneer)\b",
    re.IGNORECASE,
)

_SUGAR_IDS = {
    "en:sugar",
    "en:added-sugars",
    "en:cane-sugar",
    "en:brown-sugar",
    "en:glucose",
    "en:fructose",
    "en:sucrose",
    "en:dextrose",
    "en:corn-syrup",
    "en:high-fructose-corn-syrup",
    "en:maltose",
    "en:honey",
    "en:maple-syrup",
    "en:molasses",
    "en:treacle",
    "en:invert-sugar",
    "en:golden-syrup",
    "en:agave",
    "en:fruit-juice-concentrate",
}

_SUGAR_TEXT = re.compile(
    r"\b(sugar|syrup|honey|dextrose|fructose|maltose|molasses|treacle|agave)\b",
    re.IGNORECASE,
)

_FLAVOUR_IDS = {
    "en:flavouring",
    "en:artificial-flavouring",
    "en:flavour"
}

_FLAVOUR_TEXT = re.compile(
    r"\b(flavouring|flavoring|artificial flavou?r)\b",
    re.IGNORECASE
)

_GLUTEN_IDS = {
    "en:wheat",
    "en:barley",
    "en:rye",
    "en:spelt",
    "en:kamut",
    "en:gluten",
    "en:wheat-gluten",
    "en:wheat-flour",
    "en:wheat-starch",
}

_GLUTEN_TEXT = re.compile(
    r"\b(wheat|barley|rye|spelt|gluten|kamut)\b",
    re.IGNORECASE
)

_SOY_IDS = {
    "en:soy",
    "en:soya",
    "en:soybean",
    "en:soy-protein",
    "en:soy-lecithin",
    "en:soya-lecithin",
}

_SOY_TEXT = re.compile(
    r"\b(soy|soya|soybean)\b",
    re.IGNORECASE
)

_NUT_IDS = {
    "en:tree-nut",
    "en:almond",
    "en:cashew",
    "en:walnut",
    "en:hazelnut",
    "en:pistachio",
    "en:pecan",
    "en:macadamia",
    "en:brazil-nut",
    "en:peanut",
    "en:groundnut",
}

_NUT_TEXT = re.compile(
    r"\b(almond|cashew|walnut|hazelnut|pistachio|pecan|macadamia|peanut|groundnut|tree nut)\b",
    re.IGNORECASE,
)


# ── Individual claim checkers ─────────────────────────────────────────────────

def _check_vegan(flat_ings: List[Dict], _text: str) -> Dict:
    non_vegan = [
        i.get("text", i.get("id", "?"))
        for i in flat_ings
        if i.get("vegan") in ("no",)
    ]
    if non_vegan:
        return {
            "verdict": "FAIL",
            "confidence": 99,
            "severity": "HIGH",
            "reason": f"Non-vegan ingredient(s) detected: {', '.join(non_vegan[:5])}",
            "found": non_vegan,
        }
    maybe = [
        i.get("text", i.get("id", "?"))
        for i in flat_ings
        if i.get("vegan") == "maybe"
    ]
    if maybe:
        return {
            "verdict": "UNVERIFIABLE",
            "confidence": 60,
            "severity": "MEDIUM",
            "reason": f"Some ingredients have uncertain vegan status: {', '.join(maybe[:5])}",
            "found": maybe,
        }
    return {
        "verdict": "PASS",
        "confidence": 95,
        "severity": "LOW",
        "reason": "No non-vegan ingredients detected.",
        "found": []
    }


def _check_vegetarian(flat_ings: List[Dict], _text: str) -> Dict:
    non_veg = [
        i.get("text", i.get("id", "?"))
        for i in flat_ings
        if i.get("vegetarian") == "no"
    ]
    if non_veg:
        return {
            "verdict": "FAIL",
            "confidence": 99,
            "severity": "HIGH",
            "reason": f"Non-vegetarian ingredient(s) found: {', '.join(non_veg[:5])}",
            "found": non_veg,
        }
    return {
        "verdict": "PASS",
        "confidence": 95,
        "severity": "LOW",
        "reason": "All ingredients are vegetarian-safe.",
        "found": []
    }


def _check_dairy_free(flat_ings: List[Dict], text: str) -> Dict:
    found = [
        i.get("text", i.get("id", "?"))
        for i in flat_ings
        if i.get("id") in _DAIRY_IDS
        or _DAIRY_TEXT.search(i.get("text", ""))
    ]
    found = list(dict.fromkeys(found))
    if found:
        return {
            "verdict": "FAIL",
            "confidence": 99,
            "severity": "CRITICAL",
            "reason": f"Dairy ingredient(s) found: {', '.join(found[:5])}",
            "found": found,
        }
    return {
        "verdict": "PASS",
        "confidence": 95,
        "severity": "LOW",
        "reason": "No dairy ingredients detected.",
        "found": []
    }


def _check_no_added_sugar(flat_ings: List[Dict], text: str) -> Dict:
    found = [
        i.get("text", i.get("id", "?"))
        for i in flat_ings
        if i.get("id") in _SUGAR_IDS
        or _SUGAR_TEXT.search(i.get("text", ""))
    ]
    found = list(dict.fromkeys(found))
    if found:
        return {
            "verdict": "FAIL",
            "confidence": 98,
            "severity": "MEDIUM",
            "reason": f"Added sugar/sweetener ingredient(s) detected: {', '.join(found[:5])}",
            "found": found,
        }
    return {
        "verdict": "PASS",
        "confidence": 90,
        "severity": "LOW",
        "reason": "No added sugar or sweetener ingredients found.",
        "found": []
    }


def _check_no_palm_oil(flat_ings: List[Dict], text: str) -> Dict:
    palm = [
        i.get("text", i.get("id", "?"))
        for i in flat_ings
        if i.get("from_palm_oil") in ("yes", "maybe")
        or "palm" in i.get("id", "").lower()
        or "palm" in i.get("text", "").lower()
    ]
    palm = list(dict.fromkeys(palm))
    if any(i.get("from_palm_oil") == "maybe" for i in flat_ings):
        return {
            "verdict": "UNVERIFIABLE",
            "confidence": 50,
            "severity": "MEDIUM",
            "reason": f"Some fats may be palm-derived: {', '.join(palm[:5])}",
            "found": palm,
        }
    if palm:
        return {
            "verdict": "FAIL",
            "confidence": 98,
            "severity": "MEDIUM",
            "reason": f"Palm oil/palm-derived fat detected: {', '.join(palm[:5])}",
            "found": palm,
        }
    return {
        "verdict": "PASS",
        "confidence": 90,
        "severity": "LOW",
        "reason": "No palm oil detected in ingredients.",
        "found": []
    }


def _check_no_artificial_additives(
    flat_ings: List[Dict],
    text: str
) -> Dict:

    ADDITIVE_NAMES = {

        "sodium benzoate",
        "tartrazine",
        "msg",
        "monosodium glutamate",
        "aspartame",
        "acesulfame",
        "saccharin",

    }

    found = []

    for i in flat_ings:

        ingredient_text = (
            i.get("text", "")
            .lower()
        )

        ingredient_id = (
            i.get("id", "")
            .lower()
        )

        if (

            _is_e_code(
                ingredient_text
            )

            or

            _is_e_code(
                ingredient_id
            )

        ):

            found.append(
                ingredient_text
            )

        for additive in ADDITIVE_NAMES:

            if additive in ingredient_text:

                found.append(
                    ingredient_text
                )

    found = list(
        dict.fromkeys(found)
    )

    if found:

        return {

            "verdict": "FAIL",

            "confidence": 99,

            "severity": "HIGH",

            "reason":
            f"Artificial additive(s) detected: {', '.join(found[:6])}",

            "found": found,

        }

    return {

        "verdict": "PASS",

        "confidence": 95,

        "severity": "LOW",

        "reason":
        "No artificial additives detected.",

        "found": []

    }


def _check_no_preservatives(
    flat_ings: List[Dict],
    text: str
) -> Dict:

    PRESERVATIVE_NAMES = {
        "sodium benzoate",
        "potassium sorbate",
        "calcium propionate",
        "sulphur dioxide",
        "nitrite",
        "nitrate",
    }

    found = []

    for i in flat_ings:

        ingredient_text = (
            i.get("text", "")
            .lower()
        )

        ingredient_id = (
            i.get("id", "")
            .lower()
        )

        if (

            _e_code_in_range(
                ingredient_text,
                200,
                299
            )

            or

            _e_code_in_range(
                ingredient_id,
                200,
                299
            )

        ):

            found.append(
                ingredient_text
            )

        for preservative in PRESERVATIVE_NAMES:

            if preservative in ingredient_text:

                found.append(
                    ingredient_text
                )

    found = list(
        dict.fromkeys(found)
    )

    if found:

        return {

            "verdict": "FAIL",

            "confidence": 99,

            "severity": "HIGH",

            "reason":
            f"Preservative(s) detected: {', '.join(found[:5])}",

            "found": found,

        }

    return {

        "verdict": "PASS",

        "confidence": 95,

        "severity": "LOW",

        "reason":
        "No preservatives detected.",

        "found": []

    }


def _check_no_artificial_colors(flat_ings: List[Dict], text: str) -> Dict:
    found = [
        i.get("text", i.get("id", "?"))
        for i in flat_ings
        if _e_code_in_range(i.get("text", ""), 100, 199)
        or _e_code_in_range(i.get("id", ""), 100, 199)
    ]
    found = list(dict.fromkeys(found))
    if found:
        return {
            "verdict": "FAIL",
            "confidence": 99,
            "severity": "MEDIUM",
            "reason": f"Artificial colour(s) detected: {', '.join(found[:5])}",
            "found": found,
        }
    return {
        "verdict": "PASS",
        "confidence": 95,
        "severity": "LOW",
        "reason": "No artificial colours (E100–E199) found.",
        "found": []
    }


def _check_no_emulsifiers(flat_ings: List[Dict], text: str) -> Dict:
    found = [
        i.get("text", i.get("id", "?"))
        for i in flat_ings
        if _e_code_in_range(i.get("text", ""), 400, 499)
        or _e_code_in_range(i.get("id", ""), 400, 499)
        or i.get("id") == "en:emulsifier"
    ]
    found = list(dict.fromkeys(found))
    if found:
        return {
            "verdict": "FAIL",
            "confidence": 99,
            "severity": "MEDIUM",
            "reason": f"Emulsifier(s) detected: {', '.join(found[:5])}",
            "found": found,
        }
    return {
        "verdict": "PASS",
        "confidence": 95,
        "severity": "LOW",
        "reason": "No emulsifiers (E400–E499) found.",
        "found": []
    }


def _check_no_flavour_enhancers(flat_ings: List[Dict], text: str) -> Dict:
    found = [
        i.get("text", i.get("id", "?"))
        for i in flat_ings
        if _e_code_in_range(i.get("text", ""), 600, 699)
        or _e_code_in_range(i.get("id", ""), 600, 699)
    ]
    found = list(dict.fromkeys(found))
    if found:
        return {
            "verdict": "FAIL",
            "confidence": 99,
            "severity": "MEDIUM",
            "reason": f"Flavour enhancer(s) detected: {', '.join(found[:5])}",
            "found": found,
        }
    return {
        "verdict": "PASS",
        "confidence": 95,
        "severity": "LOW",
        "reason": "No flavour enhancers (E600–E699) found.",
        "found": []
    }


def _check_no_artificial_flavours(flat_ings: List[Dict], text: str) -> Dict:
    found = [
        i.get("text", i.get("id", "?"))
        for i in flat_ings
        if i.get("id") in _FLAVOUR_IDS
        or _FLAVOUR_TEXT.search(i.get("text", ""))
    ]
    found = list(dict.fromkeys(found))
    if found:
        return {
            "verdict": "FAIL",
            "confidence": 95,
            "severity": "MEDIUM",
            "reason": f"Flavouring ingredient(s) present: {', '.join(found[:5])}",
            "found": found,
        }
    return {
        "verdict": "PASS",
        "confidence": 90,
        "severity": "LOW",
        "reason": "No artificial flavouring detected.",
        "found": []
    }


def _check_gluten_free(flat_ings: List[Dict], text: str) -> Dict:
    found = [
        i.get("text", i.get("id", "?"))
        for i in flat_ings
        if i.get("id") in _GLUTEN_IDS
        or _GLUTEN_TEXT.search(i.get("text", ""))
        or _GLUTEN_TEXT.search(i.get("id", ""))
    ]
    
    # Also check raw text for "may contain" warnings
    if _GLUTEN_TEXT.search(text or ""):
        if not found:
            return {
                "verdict": "UNVERIFIABLE",
                "confidence": 80,
                "severity": "HIGH",
                "reason": "Gluten warning found in product description ('may contain wheat/gluten').",
                "found": [],
            }
            
    found = list(dict.fromkeys(found))
    if found:
        return {
            "verdict": "FAIL",
            "confidence": 99,
            "severity": "CRITICAL",
            "reason": f"Gluten-containing ingredient(s) detected: {', '.join(found[:5])}",
            "found": found,
        }
    return {
        "verdict": "PASS",
        "confidence": 95,
        "severity": "LOW",
        "reason": "No gluten-containing ingredients found.",
        "found": []
    }


def _check_no_soy(flat_ings: List[Dict], text: str) -> Dict:
    found = [
        i.get("text", i.get("id", "?"))
        for i in flat_ings
        if i.get("id") in _SOY_IDS
        or _SOY_TEXT.search(i.get("text", ""))
        or _SOY_TEXT.search(i.get("id", ""))
    ]
    found = list(dict.fromkeys(found))
    if found:
        return {
            "verdict": "FAIL",
            "confidence": 99,
            "severity": "CRITICAL",
            "reason": f"Soy ingredient(s) detected: {', '.join(found[:5])}",
            "found": found,
        }
    return {
        "verdict": "PASS",
        "confidence": 95,
        "severity": "LOW",
        "reason": "No soy or soya ingredients detected.",
        "found": []
    }


def _check_no_nuts(flat_ings: List[Dict], text: str) -> Dict:
    found = [
        i.get("text", i.get("id", "?"))
        for i in flat_ings
        if i.get("id") in _NUT_IDS
        or _NUT_TEXT.search(i.get("text", ""))
        or _NUT_TEXT.search(i.get("id", ""))
    ]
    found = list(dict.fromkeys(found))
    if found:
        return {
            "verdict": "FAIL",
            "confidence": 99,
            "severity": "CRITICAL",
            "reason": f"Nut ingredient(s) detected: {', '.join(found[:5])}",
            "found": found,
        }
    return {
        "verdict": "PASS",
        "confidence": 95,
        "severity": "LOW",
        "reason": "No nut ingredients detected.",
        "found": []
    }


# ── Dispatcher ─────────────────────────────────────────────────────────────────

_HANDLERS = {
    "vegan": _check_vegan,
    "vegetarian": _check_vegetarian,
    "dairy free": _check_dairy_free,
    "no added sugar": _check_no_added_sugar,
    "no palm oil": _check_no_palm_oil,
    "no artificial additives": _check_no_artificial_additives,
    "no preservatives": _check_no_preservatives,
    "no artificial colors": _check_no_artificial_colors,
    "no artificial emulsifiers": _check_no_emulsifiers,
    "no flavour enhancers": _check_no_flavour_enhancers,
    "no artificial flavours": _check_no_artificial_flavours,
    "gluten free": _check_gluten_free,
    "no soy": _check_no_soy,
    "no nuts": _check_no_nuts,
}


def verify_claims(
    claims: List[str],
    ingredients: List[Dict[str, Any]],
    ingredients_text: str = "",
) -> Dict[str, Any]:
    """
    Verify a list of claims against structured ingredient data.

    Args:
        claims: List of claim strings (e.g. ["Vegan", "No Palm Oil"])
        ingredients: Nested ingredient list from Open Food Facts
        ingredients_text: Raw ingredients text (for fallback/context)

    Returns:
        Dict containing version, health_score, "results" list, "summary" counts, and "execution_ms".
    """
    start = time.perf_counter()
    flat = flatten_ingredients(ingredients or [])
    results = []
    
    summary = {
        "pass": 0,
        "fail": 0,
        "unverifiable": 0
    }

    VERDICT_MAP = {
        "PASS": "pass",
        "FAIL": "fail",
        "UNVERIFIABLE": "unverifiable",
    }

    for claim in claims:
        key = claim.strip().lower()
        handler = _HANDLERS.get(key)
        meta = SUPPORTED_CLAIMS.get(claim.strip().title(), SUPPORTED_CLAIMS.get(claim.strip(), {}))

        if handler is None:
            results.append({
                "claim": claim,
                "verdict": "UNVERIFIABLE",
                "confidence": 0,
                "severity": "LOW",
                "reason": f"No rule defined for claim '{claim}'. Cannot verify from ingredients list.",
                "found": [],
                "icon": "help-circle",
                "description": "This claim cannot be verified from ingredient data alone.",
            })
            
            summary[VERDICT_MAP.get("UNVERIFIABLE", "unverifiable")] += 1
            
            continue

        try:
            result = handler(flat, ingredients_text or "")
            # Normalize claim name to title case for display
            display_claim = claim.strip().title()
            verdict = result["verdict"]
            
            results.append({
                "claim": display_claim,
                "verdict": verdict,
                "confidence": result.get("confidence", 0),
                "severity": result.get("severity", "LOW"),
                "reason": result["reason"],
                "found": result.get("found", []),
                "icon": meta.get("icon", "search"),
                "description": meta.get("description", ""),
            })
            
            summary[VERDICT_MAP.get(verdict, "unverifiable")] += 1
            
        except Exception as e:
            logger.exception("Error checking claim '%s': %s", claim, e)
            results.append({
                "claim": claim,
                "verdict": "UNVERIFIABLE",
                "confidence": 0,
                "severity": "LOW",
                "reason": f"Error during verification: {str(e)}",
                "found": [],
                "icon": "alert-circle",
                "description": "",
            })
            
            summary[VERDICT_MAP.get("UNVERIFIABLE", "unverifiable")] += 1

    return {
        "version": "scanix_v1",
        "health_score":
min(

    100,

    max(

        0,

        100
        -
        summary["fail"] * 15
        -
        summary["unverifiable"] * 5

    )

),
        "results": results,
        "summary": summary,
        "execution_ms": round(
            (
                time.perf_counter() 
                - 
                start
            ) 
            * 1000, 
            2
        )
    }


def get_supported_claims() -> List[Dict[str, str]]:
    """Return list of all supported claims with metadata."""
    return [
        {
            "claim": name,
            "description": meta["description"],
            "icon": meta["icon"],
        }
        for name, meta in SUPPORTED_CLAIMS.items()
    ]