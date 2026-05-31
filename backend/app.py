from dotenv import load_dotenv

load_dotenv()

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

from modules.trust.router import (
    router as trust_router
)

from modules.ai.router import (
    router as ai_router
)

from modules.ai.agent_router import (
    router as agent_router
)

from modules.ai.nutrition_planner_router import (
    router as planner_router
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


# SYSTEM 4
app.include_router(

    trust_router,

    prefix="/api/v1",

    tags=[
        "System 4 • Trust & Compliance"
    ]

)


# SYSTEM 5
app.include_router(

    ai_router,

    prefix="/api/v1/ai",

    tags=[
        "System 5 - AI Intelligence"
    ]

)


app.include_router(

    agent_router,

    prefix="/api/v1/agent",

    tags=[
        "System 5 - AI Nutritionist"
    ]

)


app.include_router(

    planner_router,

    prefix="/api/v1/planner",

    tags=["Nutrition Planner"]

)