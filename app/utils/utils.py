"""
Módulo utilitário para geração de hash MD5 de URLs.

Este módulo fornece funções auxiliares para o gerenciamento de URLs e hashes MD5.
"""

import hashlib
from datetime import datetime

from fastapi import Request

from app.core.logging_config import setup_logging

logger = setup_logging("utils")

def md5_url_encode(url: str, length: int = 10) -> str:
    """
    Gera um hash MD5 da URL e retorna os primeiros 'length' caracteres.
    """

    logger.info("Gerando hash MD5 da URL...")

    url_md5_hash = hashlib.md5(url.encode('utf-8')).hexdigest()[:length]

    logger.info("Hash MD5 gerado com sucesso!")

    return url_md5_hash

def build_short_url(fastapi_request: Request, endpoint_func_name: str, url_md5_hash: str) -> str:
    """
    Gera uma URL curta a partir da URL original e do hash MD5.
    """

    logger.info("Gerando URL curta...")

    short_url = str(fastapi_request.url_for(endpoint_func_name, url_md5_hash=url_md5_hash))

    logger.info("URL curta gerada com sucesso!")

    return short_url

def current_timestamp() -> str:
    """
    Retorna o timestamp atual.
    """

    return datetime.utcnow().isoformat() + "Z"
