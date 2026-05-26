from functools import lru_cache

from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class Settings(BaseSettings):

    APP_NAME: str = "SCANIX AI"

    APP_ENV: str = "development"

    APP_VERSION: str = "1.0.0"

    HOST: str = "0.0.0.0"

    PORT: int = 8000

    API_PREFIX: str = "/api/v1"

    DEBUG: bool = True

    model_config = SettingsConfigDict(

        env_file=".env",

        case_sensitive=True,

        extra="ignore",   # ← IMPORTANT FIX

    )


@lru_cache
def get_settings():

    return Settings()


settings = get_settings()