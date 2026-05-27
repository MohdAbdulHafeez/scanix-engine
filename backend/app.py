from fastapi import FastAPI

from config.settings import (
    settings,
)

from core.logging import (
    logger,
)

from api.v1.router import (
    router,
)

from modules.ingredients.router import (
    router as ingredients_router
)

from modules.nutrition.router import (
    router as nutrition_router
)


app = FastAPI(

    title=settings.APP_NAME,

    version=settings.APP_VERSION,

)


@app.get("/")
async def root():

    return {

        "success": True,

        "app": settings.APP_NAME,

        "version": settings.APP_VERSION,

        "status": "running",

    }


@app.get("/health")
async def health():

    return {

        "status": "healthy",

    }


# SYSTEM 1
app.include_router(

    router,

    prefix=settings.API_PREFIX,

)


# SYSTEM 2
app.include_router(

    ingredients_router,

    prefix="/api/v1",

    tags=["System 2 • Ingredients"]

)


logger.info(
    "SCANIX started"
)


# SYSTEM 3
app.include_router(

    nutrition_router,

    prefix="/api/v1",

    tags=["System 3 • Nutrition"]

)