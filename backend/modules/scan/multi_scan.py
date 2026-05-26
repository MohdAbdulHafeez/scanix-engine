async def build_multi_response(
    results,
):

    return {

        "total": len(
            results
        ),

        "results": results,

    }