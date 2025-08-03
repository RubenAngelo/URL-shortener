"""
Módulo de configuração de conexão com o banco de dados PostgreSQL.

Este módulo fornece funções para criar e gerenciar conexões com o banco de dados,
utilizando o pacote psycopg2. Inclui um gerenciador de contexto para garantir
commit, rollback e fechamento adequado da conexão.
"""

from contextlib import contextmanager
from typing import Generator

import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi import HTTPException

from app.core.env_config import settings

def get_postgres_connection() -> psycopg2.extensions.connection:
    """
    Cria e retorna uma conexão com o banco de dados PostgreSQL.
    """

    return psycopg2.connect(
        dbname=settings.DB_NAME,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        cursor_factory=RealDictCursor
    )

@contextmanager
def get_db_connection() -> Generator[psycopg2.extensions.connection, None, None]:
    """
    Context manager para conexão com o banco de dados.
    Garante commit, rollback e fechamento da conexão.
    """

    conn = get_postgres_connection()

    try:
        yield conn
        conn.commit()

    except psycopg2.DatabaseError as e:
        conn.rollback()

        raise HTTPException(status_code=500, detail="Erro no banco de dados") from e

    finally:
        conn.close()
