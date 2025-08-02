"""
Este módulo contém a função responsável por criar as tabelas necessárias no banco de dados. 

Cria a tabela 'url_lookup', que armazena o hash MD5 da URL original e a própria URL.
"""

from app.core.logging_config import setup_logging
from app.core.database_config import get_db_connection

logger = setup_logging("create_tables")

def create_table_url_lookup() -> None:
    """
    Cria a tabela url_lookup no banco de dados, se ela não existir.
    """

    logger.info("Validando tabelas...")

    with get_db_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            """--sql
            CREATE TABLE IF NOT EXISTS url_lookup (
                url_md5_hash VARCHAR(10) PRIMARY KEY,
                url TEXT NOT NULL
            )
            """
        )

    logger.info("Tabela url_lookup pronta!")
