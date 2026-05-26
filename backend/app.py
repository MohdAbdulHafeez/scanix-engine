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


app.include_router(

    router,

    prefix=settings.API_PREFIX,

)


logger.info(
    "SCANIX started"
)