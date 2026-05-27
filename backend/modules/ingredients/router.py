from fastapi import APIRouter

from pydantic import BaseModel

from modules.ingredients.service import (
IngredientService
)

router=APIRouter()


class IngredientRequest(
BaseModel
):

    ingredients:str

    claims:list[str]=[]


@router.post(
"/ingredients/analyze"
)

def analyze_ingredients(
    body:IngredientRequest
):

    return IngredientService.analyze(

        raw_ingredients=
        body.ingredients,

        claims=
        body.claims

    )