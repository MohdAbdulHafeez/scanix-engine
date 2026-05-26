def calculate_confidence(
    ocr,
    product,
):

    avg = 0

    values = ocr.get(
        "confidence",
        [],
    )

    if values:

        avg = sum(
            values
        ) / len(
            values
        )

    score = round(
        avg * 100
    )

    if product["brand"]:

        score += 10

    score = min(
        score,
        100,
    )

    return {

        "overall": score,

    }