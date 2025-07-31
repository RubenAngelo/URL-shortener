import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
from app.core.config import settings

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
def get_db():
    """
    Context manager para conexão com o banco de dados.
    Garante commit, rollback e fechamento da conexão.
    """

    conn = get_postgres_connection()

    try:
        yield conn
        conn.commit()

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()
