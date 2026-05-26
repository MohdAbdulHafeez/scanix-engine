SCAN_HISTORY = []


def save_scan(
    data,
):

    SCAN_HISTORY.insert(

        0,

        data,

    )

    SCAN_HISTORY[:] = (

        SCAN_HISTORY[:20]

    )

    return True


def get_history():

    return SCAN_HISTORY