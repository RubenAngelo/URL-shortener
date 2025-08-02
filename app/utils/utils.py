"""
Módulo utilitário para geração de hash MD5 de URLs.

Este módulo fornece funções auxiliares para codificar URLs utilizando o algoritmo MD5,
permitindo a obtenção de identificadores curtos a partir de URLs completas.
"""

import hashlib

from app.core.logging_config import setup_logging

logger = setup_logging("utils")

def md5_url_encode(url: str, length: int = 10) -> str:
    """
    Gera um hash MD5 da URL e retorna os primeiros 'length' caracteres.
    """

    url_md5_hash = hashlib.md5(url.encode('utf-8')).hexdigest()[:length]

    logger.info("Hash MD5 gerado com sucesso!")

    return url_md5_hash
