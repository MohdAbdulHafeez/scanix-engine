from fastapi import APIRouter
from pydantic import BaseModel

from modules.ai.diet_planner import (
    DietPlanner
)

router = APIRouter()


class PlannerRequest(
    BaseModel
):

    age: int

    gender: str

    weight: float

    height: float

    activity_level: str

    goal: str

    diet_type: str

    budget: str = "medium"


@router.post("/generate")
async def generate_plan(

    request: PlannerRequest

):

    return DietPlanner.build(

        age=request.age,

        gender=request.gender,

        weight=request.weight,

        height=request.height,

        activity_level=request.activity_level,

        goal=request.goal,

        diet_type=request.diet_type,

        budget=request.budget

    )