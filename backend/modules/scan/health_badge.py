def generate_badge(
    product,
):

    category = product.get(
        "category"
    )

    if category == "chips":

        return {

            "grade": "C",

            "color": "yellow",

            "message": (
                "Consume in moderation"
            ),

        }

    if category == "dairy":

        return {

            "grade": "B",

            "color": "green",

            "message": (
                "Generally balanced"
            ),

        }

    return {

        "grade": "N/A",

        "color": "gray",

        "message": (
            "Insufficient data"
        ),

    }