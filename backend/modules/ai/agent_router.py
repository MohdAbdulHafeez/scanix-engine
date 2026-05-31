import os
import uuid

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Form
)

from pydantic import (
    BaseModel
)

from typing import (
    Dict,
    Optional
)

from modules.ai.agent_service import (
    AgentService
)


router = APIRouter()


# =====================================
# Chat Request
# =====================================

class AgentChatRequest(
    BaseModel
):

    question: str

    ingredients_result: Dict

    nutrition_result: Dict

    trust_result: Dict

    food_explainer: Optional[
        Dict
    ] = None


# =====================================
# Text Chat
# =====================================

@router.post(
    "/chat"
)

async def chat(

    request: AgentChatRequest

):

    return (

        AgentService.chat(

            question=
            request.question,

            ingredients_result=
            request.ingredients_result,

            nutrition_result=
            request.nutrition_result,

            trust_result=
            request.trust_result,

            food_explainer=
            request.food_explainer

        )

    )


# =====================================
# Image Chat
# =====================================

@router.post(
    "/image"
)

async def image_chat(

    image: UploadFile = File(...)

):

    temp_path = (

        f"temp_{uuid.uuid4()}.jpg"

    )

    with open(

        temp_path,

        "wb"

    ) as f:

        f.write(

            await image.read()

        )

    result = (

        AgentService.image_chat(

            image_path=
            temp_path,

            ingredients_result=
            {},

            nutrition_result=
            {},

            trust_result=
            {}

        )

    )

    os.remove(
        temp_path
    )

    return result


# =====================================
# Voice Chat
# =====================================

@router.post(
    "/voice"
)

async def voice_chat(

    audio: UploadFile = File(...)

):

    temp_path = (

        f"temp_{uuid.uuid4()}.wav"

    )

    with open(

        temp_path,

        "wb"

    ) as f:

        f.write(

            await audio.read()

        )

    result = (

        AgentService.voice_chat(

            audio_path=
            temp_path,

            ingredients_result=
            {},

            nutrition_result=
            {},

            trust_result=
            {}

        )

    )

    os.remove(
        temp_path
    )

    return result


# =====================================
# Multimodal
# =====================================

@router.post(
    "/multimodal"
)

async def multimodal_chat(

    question: str = Form(...),

    image: UploadFile = File(...)

):

    temp_path = (

        f"temp_{uuid.uuid4()}.jpg"

    )

    try:

        with open(

            temp_path,

            "wb"

        ) as f:

            f.write(

                await image.read()

            )

        result = (

            AgentService.multimodal_chat(

                question=
                question,

                image_path=
                temp_path,

                ingredients_result=
                {},

                nutrition_result=
                {},

                trust_result=
                {}

            )

        )

    finally:

        if os.path.exists(
            temp_path
        ):

            os.remove(
                temp_path
            )

    return result

def save_upload_file(
    file,
    suffix
):

    pass