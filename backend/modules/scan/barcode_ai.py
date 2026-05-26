async def analyze_barcode(
    barcode,
    product,
):

    if not barcode:

        return {

            "available": False,

            "message":
            "Barcode required",

        }

    brand = product.get(
        "brand"
    )

    category = product.get(
        "category"
    )

    return {

        "available": True,

        "summary": (
            f"{brand or 'This product'} "
            f"belongs to "
            f"{category} category."
        ),

        "health_score": 72,

        "recommendation": (
            "Consume in moderation"
        ),

        "alternative": (
            "Lower processed option"
        ),

    }