BAD = {

    "maltodextrin":
    "Highly processed additive",

    "color":
    "Food coloring",

    "citric acid":
    "Artificial stabilizer",

    "chips":
    "Ultra processed carbohydrate",

}


def get_negatives(
    text: str,
):

    text = text.lower()

    result = []

    for item, label in BAD.items():

        if item in text:

            result.append(
                label
            )

    return list(
        set(result)
    )