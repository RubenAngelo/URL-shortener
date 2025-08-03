"""
Módulo de operações CRUD para o encurtador de URLs.

Este módulo fornece funções para buscar e inserir mapeamentos de URLs e seus respectivos hashes MD5
no banco de dados.
"""

from typing import Optional

from fastapi import HTTPException

from app.core.logging_config import setup_logging
from app.core.database_config import get_db_connection

logger = setup_logging("url_crud")

def fetch_md5_hash_by_url(url: str) -> Optional[str]:
    """
    Verifica se uma URL já existe no banco de dados e retorna o hash MD5 associado.
    """

    logger.info("Verificando se a URL ja existe no banco...")

    with get_db_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""--sql
            SELECT
                url_md5_hash

            FROM
                url_lookup

            WHERE
                url = %s

            """,
            (url,)
        )

        result = cursor.fetchone()

        if not result:
            logger.info("A URL não existe no banco.")
            return None

        logger.info("A URL ja existe no banco.")

        return result["url_md5_hash"]

def fetch_url_by_md5_hash(url_md5_hash: str) -> Optional[str]:
    """
    Busca a URL original a partir do hash MD5.
    Retorna a URL se encontrada.
    """

    logger.info("Buscando URL pelo hash MD5...")

    with get_db_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""--sql
            SELECT
                url

            FROM
                url_lookup

            WHERE
                url_md5_hash = %s

            """,
            (url_md5_hash,)
        )

        result = cursor.fetchone()

        if not result:
            raise HTTPException(status_code=404, detail="URL não encontrada.")

        logger.info("URL encontrada com sucesso!")

        return result["url"]

def create_url_mapping(url: str, url_md5_hash: str) -> None:
    """
    Insere uma nova URL e seu hash MD5 na tabela url_lookup.
    Retorna True se inserção for bem-sucedida, False caso contrário.
    """

    logger.info("Inserindo URL no banco...")

    with get_db_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""--sql
            INSERT INTO url_lookup (
                url_md5_hash, 
                url
            ) 

            VALUES (
                %s, 
                %s
            )

            """,
            (url_md5_hash, url)
        )

    logger.info("URL inserida com sucesso!")
