GOOD = {

    "protein":
    "Protein source",

    "fiber":
    "High fiber",

    "milk":
    "Natural dairy",

    "potatoes":
    "Whole food",

}


def get_positives(
    text: str,
):

    text = text.lower()

    result = []

    for item, label in GOOD.items():

        if item in text:

            result.append(
                label
            )

    return list(
        set(result)
    )