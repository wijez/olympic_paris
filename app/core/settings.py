import os
from pathlib import Path
from fastapi_mail import ConnectionConfig
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)


class Settings(BaseSettings):
    # Database configuration
    POSTGRE_USER: str = os.environ.get("POSTGRE_USER")
    POSTGRE_PASSWORD: str = os.environ.get("POSTGRE_PASSWORD")
    POSTGRE_HOST: str = os.environ.get("POSTGRE_HOST", "localhost")
    POSTGRE_PORT: int = int(os.environ.get("POSTGRE_PORT", 5432))
    POSTGRE_DB: str = os.environ.get("POSTGRE_DB", "olympic_paris")

    # JWT configuration
    SECRET_KEY: str = os.environ.get("SECRET_KEY", "009e6d3e8b942fddc8389892badbfeee663e7b37e27786d8e8b1f5def70af3e8")
    ALGORITHM: str = os.environ.get("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.environ.get("REFRESH_TOKEN_EXPIRE_DAYS", 3))

    # Email configurationa
    MAIL_USER: str = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD: str = os.environ.get("MAIL_PASSWORD")
    MAIL_FROM: str = os.environ.get("MAIL_FROM")
    MAIL_PORT: int = int(os.environ.get("MAIL_PORT"))
    MAIL_SERVER: str = os.environ.get("MAIL_SERVER", "smtp.gmail.com")
    MAIL_STARTTLS: bool = os.environ.get("MAIL_STARTTLS", "True").lower() in ("true", "1", "yes")
    MAIL_SSL_TLS: bool = os.environ.get("MAIL_SSL_TLS", "False").lower() in ("true", "1", "yes")
    VALIDATE_CERTS: bool = os.environ.get("VALIDATE_CERTS", "True").lower() in ("true", "1", "yes")
    TEMPLATE_FOLDER: Path = Path("D:/project/olympic_paris/email_templates").resolve()

    REDIS_HOST: str = os.environ.get("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.environ.get("REDIS_PORT", 6379))
    REDIS_URL: str = os.environ.get("REDIS_URL", 'redis://localhost:6379/0')
    CELERY_BROKER_URL: str = os.environ.get("CELERY_BROKER_URL")
    CELERY_RESULT_BACKEND: str = os.environ.get("CELERY_RESULT_BACKEND")

    class Config:
        env_file = ".env"

    @property
    def DATABASE_URI(self):
        return f"postgresql+asyncpg://{self.POSTGRE_USER}:{self.POSTGRE_PASSWORD}@{self.POSTGRE_HOST}:{self.POSTGRE_PORT}/{self.POSTGRE_DB}"

    @staticmethod
    def get_email_config() -> ConnectionConfig:
        return ConnectionConfig(
            MAIL_USERNAME=settings.MAIL_USER,
            MAIL_PASSWORD=settings.MAIL_PASSWORD,
            MAIL_FROM=settings.MAIL_FROM,
            MAIL_PORT=settings.MAIL_PORT,
            MAIL_SERVER=settings.MAIL_SERVER,
            MAIL_STARTTLS=settings.MAIL_STARTTLS,
            MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
            VALIDATE_CERTS=settings.VALIDATE_CERTS,
            TEMPLATE_FOLDER=settings.TEMPLATE_FOLDER
        )


settings = Settings()
