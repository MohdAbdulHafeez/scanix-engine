from PIL import Image

import easyocr

import tempfile


reader = easyocr.Reader(

    ["en"],

    gpu=False,

)


async def extract_text(

    file,

):

    with tempfile.NamedTemporaryFile(

        delete=False,

        suffix=".jpg",

    ) as temp:

        content = await file.read()

        temp.write(content)

        path = temp.name

    await file.seek(0)

    result = reader.readtext(

        path,

    )

    blocks = []

    confidence = []

    text = []

    for item in result:

        blocks.append(

            item[1]

        )

        confidence.append(

            round(

                item[2],

                2,

            )
        )

        text.append(

            item[1]

        )

    return {

        "text": " ".join(
            text
        ),

        "blocks": blocks,

        "confidence": confidence,

    }