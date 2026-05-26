PRODUCT_IMAGES = {

    "Lays": (
        "https://images.openfoodfacts.org/images/products/"
        "8901491101837/front_en.5.full.jpg"
    ),

    "Doritos": (
        "https://images.openfoodfacts.org/images/products/"
        "8410199018438/front_en.5.full.jpg"
    ),

    "Pringles": (
        "https://images.openfoodfacts.org/images/products/"
        "5053990156000/front_en.3.full.jpg"
    ),

}


def get_product_image(
    product,
):

    brand = product.get(
        "brand"
    )

    return PRODUCT_IMAGES.get(

        brand,

        "https://images.openfoodfacts.org/images/products/default.png",

    )