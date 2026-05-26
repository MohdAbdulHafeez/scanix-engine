async def lookup_external(
    barcode,
):

    if not barcode:

        return None

    return {

        "product_name":
        "Sample Product",

        "brand":
        "OpenFoodFacts",

        "nutriscore":
        "C",

        "nova":
        4,

        "calories":
        210,

    }