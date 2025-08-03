"""
Módulo de configuração principal da aplicação URL Shortener.

Este módulo define a classe Settings, responsável por carregar e validar as configurações
da aplicação a partir de variáveis de ambiente ou de um arquivo .env. Inclui parâmetros
de conexão com o banco de dados, configurações gerais da aplicação e validações para
garantir a integridade dos dados fornecidos.
"""

import os

from pydantic import field_validator
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Configurações principais da aplicação, lidas de variáveis de ambiente ou arquivo .env.
    """

    # Database
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "testdb"
    DB_USER: str = "admin"
    DB_PASSWORD: str = "senhaParaADM321*"

    @classmethod
    @field_validator("DB_PORT")
    def port_must_be_valid(cls, v: int) -> int:
        """
        Faz validação da porta do banco de dados.
        """

        if not (1024 <= v <= 65535):
            raise ValueError("DB_PORT deve estar entre 1024 e 65535!")

        return v

    # App
    APP_NAME: str = "URL Shortener"
    APP_DEBUG: bool = True

    class Config:
        env_file = os.getenv("ENV_FILE", ".env")

settings = Settings()
