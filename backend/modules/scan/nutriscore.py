def compute_nutriscore(
    negatives,
):

    count = len(
        negatives
    )

    if count == 0:
        return "A"

    if count <= 2:
        return "B"

    if count <= 4:
        return "C"

    return "D"