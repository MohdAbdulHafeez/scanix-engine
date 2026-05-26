from fastapi import APIRouter

from api.v1.scan import (
    router as scan_router,
)


router = APIRouter()


router.include_router(

    scan_router,

    prefix="/scan",

    tags=["System 1 • Scan"],

)