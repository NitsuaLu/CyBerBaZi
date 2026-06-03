"""Application configuration."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "BaZi API"
    version: str = "0.1.0"
    debug: bool = False
    allowed_origins: list[str] = ["*"]

    model_config = {"env_prefix": "BAZI_"}


settings = Settings()
