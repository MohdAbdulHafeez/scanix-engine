ALLERGENS = [

    "milk",

    "egg",

    "soy",

    "gluten",

    "nuts",

    "peanut",

]


def detect_allergens(
    text: str,
):

    text = text.lower()

    found = []

    for item in ALLERGENS:

        if item in text:

            found.append(
                item
            )

    return found