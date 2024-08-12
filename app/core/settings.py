import os
from pathlib import Path

from pydantic_settings import BaseSettings
from dotenv import load_dotenv


env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)


class Settings(BaseSettings):
    POSTGRE_USER: str = os.environ.get("POSTGRE_USER", "postgres")
    POSTGRE_PASSWORD: str = os.environ.get("POSTGRE_PASSWORD", "portgasDace")
    POSTGRE_HOST: str = os.environ.get("POSTGRE_HOST", "localhost")
    POSTGRE_PORT: str = os.environ.get("POSTGRE_PORT", 5432)
    POSTGRE_DB: str = os.environ.get("POSTGRE_DB", "olympic_paris")

    @property
    def DATABASE_URI(self):
        return f"postgresql+asyncpg://{self.POSTGRE_USER}:{self.POSTGRE_PASSWORD}@{self.POSTGRE_HOST}:{self.POSTGRE_PORT}/{self.POSTGRE_DB}"


settings = Settings()
