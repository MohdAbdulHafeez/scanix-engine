from fastapi import (
    APIRouter
)

from pydantic import (
    BaseModel
)

from typing import (
    Dict
)

from modules.ai.service import (
    AIService
)

router = APIRouter()


class AIRequest(
    BaseModel
):

    ingredients_result: Dict

    nutrition_result: Dict

    trust_result: Dict


@router.post(
        "/explain"
)

async def explain_product(

    request: AIRequest

):
    try:

        return AIService.explain_product(

            ingredients_result= 
            request.ingredients_result,
            nutrition_result=
            request.nutrition_result,
            trust_result=
            request.trust_result
        )

    except Exception as e:

        return {
            "error": str(e)
        }