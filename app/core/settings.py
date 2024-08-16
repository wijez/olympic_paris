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
    SECRET_KEY: str = os.environ.get("SECRET_KEY", "009e6d3e8b942fddc8389892badbfeee663e7b37e27786d8e8b1f5def70af3e8")
    ALGORITHM: str = os.environ.get("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

    class Config:
        env_file = ".env"

    @property
    def DATABASE_URI(self):
        return f"postgresql+asyncpg://{self.POSTGRE_USER}:{self.POSTGRE_PASSWORD}@{self.POSTGRE_HOST}:{self.POSTGRE_PORT}/{self.POSTGRE_DB}"


settings = Settings()
