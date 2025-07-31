from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    """
    Configurações principais da aplicação, lidas de variáveis de ambiente ou arquivo .env.
    """

    # Database
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "testdb"
    DB_USER: str = "usuario"
    DB_PASSWORD: str = "1234"

    # App
    APP_NAME: str = "URL Shortener"
    APP_DEBUG: bool = True

    class Config:
        env_file = os.getenv("ENV_FILE", ".env")

settings = Settings()
