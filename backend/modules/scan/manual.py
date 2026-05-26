def parse_manual_input(
    value: str,
):

    value = value.strip()

    return {

        "query": value,

        "mode": "manual",

    }