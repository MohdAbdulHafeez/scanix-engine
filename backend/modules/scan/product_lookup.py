import re


BRANDS = {

    "Lays": [
        "lays",
        "iays",
    ],

    "Doritos": [
        "doritos",
    ],

    "Pringles": [
        "pringles",
    ],

    "Cheetos": [
        "cheetos",
    ],

}


def clean_text(
    text: str,
):

    text = text.lower()

    text = re.sub(
        r"[^a-z0-9\s]",
        " ",
        text,
    )

    text = re.sub(
        r"\s+",
        " ",
        text,
    )

    return text.strip()


def lookup_product(
    text: str,
):

    cleaned = clean_text(
        text
    )

    brand = None

    category = "unknown"

    for product, aliases in BRANDS.items():

        if any(

            alias in cleaned

            for alias in aliases

        ):

            brand = product

            category = "chips"

            break

    if category == "unknown":

        chips_keywords = [

            "chips",

            "potato",

            "onion",

            "cream",

            "flavour",

        ]

        if any(

            word in cleaned

            for word in chips_keywords

        ):

            category = "chips"

    return {

        "brand": brand,

        "category": category,

    }