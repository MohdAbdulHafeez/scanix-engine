from fastapi import (
    APIRouter
)

from pydantic import (
    BaseModel
)

from typing import Dict

from modules.nutrition.service import (
    NutritionService
)

router = APIRouter()


class NutritionRequest(
    BaseModel
):

    nutrition: Dict

    bmi: float = 22


@router.post(
    "/nutrition/analyze"
)

async def analyze_nutrition(
    request: NutritionRequest
):

    return NutritionService.analyze(

        nutrition=
        request.nutrition,

        bmi=
        request.bmi

    )