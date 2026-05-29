from fastapi import (
    APIRouter
)

from pydantic import (
    BaseModel,
    Field
)

from typing import (
    List,
    Dict,
    Any
)

from modules.trust.service import (
    TrustService
)


router = APIRouter()


class TrustRequest(
    BaseModel
):

    ingredients: List[str] = Field(
        default_factory=list
    )

    nutrition: Dict[str, Any] = Field(
        default_factory=dict
    )

    claims: List[str] = Field(
        default_factory=list
    )

    marketing_text: str = ""


@router.post(

    "/trust/analyze",

    summary=
    "Trust & Compliance Analysis",

    description=
    "Runs FSSAI compliance, claim validation, organic verification, marketing analysis and trust scoring."

)
async def analyze_trust(

    request: TrustRequest

):

    result = (

        TrustService.analyze(

            ingredients=
            request.ingredients,

            nutrition=
            request.nutrition,

            claims=
            request.claims,

            marketing_text=
            request.marketing_text

        )

    )

    return {

        "success":
        True,

        "system":
        "System 4 - Trust & Compliance",

        "data":
        result

    }