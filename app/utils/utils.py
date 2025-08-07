"""
Módulo utilitário para geração de hash de URLs.

Este módulo fornece funções auxiliares para o gerenciamento de URLs e hashes.
"""

import hashlib
from datetime import datetime

from fastapi import Request
from passlib.context import CryptContext

from app.core.logging_config import setup_logging

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

logger = setup_logging("utils")


def generate_url_hash(url: str, length: int = 10) -> str:
    """
    Gera um hash MD5 da URL e retorna os primeiros 'length' caracteres.
    """

    logger.info("Gerando hash da URL...")

    url_hash = hashlib.md5(url.encode("utf-8")).hexdigest()[:length]

    logger.info("Hash gerado com sucesso!")

    return url_hash


def build_short_url(
    fastapi_request: Request, endpoint_func_name: str, url_hash: str
) -> str:
    """
    Gera uma URL curta a partir da URL original e do hash.
    """

    logger.info("Gerando URL curta...")

    short_url = str(fastapi_request.url_for(endpoint_func_name, url_hash=url_hash))

    logger.info("URL curta gerada com sucesso!")

    return short_url


def current_timestamp() -> str:
    """
    Retorna o timestamp atual.
    """

    return datetime.utcnow().isoformat() + "Z"


def get_password_hash(password: str) -> str:
    """
    Gera o hash de uma senha usando bcrypt.
    """
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verifica se uma senha em texto puro corresponde a um hash.
    """
    return pwd_context.verify(password, hashed_password)
