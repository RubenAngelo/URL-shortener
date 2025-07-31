from app.config.database import get_db

def create_tables():
    """
    Cria a tabela url_lookup no banco de dados, se ela não existir.
    """

    try:
        with get_db() as conn:
            cursor = conn.cursor()

            cursor.execute(
                """--sql
                CREATE TABLE IF NOT EXISTS url_lookup (
                    url_md5 VARCHAR(32) PRIMARY KEY,
                    url TEXT NOT NULL
                )
                """
            )

        print("Tabela url_lookup criada ou já existente!")

    except Exception as e:
        print(f"[ERRO][DB] Falha ao criar tabela: {e}")
        raise
