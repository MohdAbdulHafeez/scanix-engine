import re


def extract_barcode(
    text: str,
):

    match = re.search(

        r"\b\d{8,14}\b",

        text,

    )

    if match:

        return match.group()

    return None