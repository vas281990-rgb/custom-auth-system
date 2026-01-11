from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # Database connection string
    DATABASE_URL: str = Field(..., env="DATABASE_URL")

    # JWT Security settings
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        # Automatically load variables from .env file
        env_file = ".env"
        env_file_encoding = "utf-8"


# Singleton instance of settings to be used throughout the app
settings = Settings()
