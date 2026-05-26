FAVORITES = []


def add_favorite(
    product,
):

    brand = product.get(
        "brand"
    )

    if not brand:

        return

    exists = any(

        x["brand"]

        == brand

        for x in FAVORITES

    )

    if not exists:

        FAVORITES.append(
            product
        )


def get_favorites():

    return FAVORITES