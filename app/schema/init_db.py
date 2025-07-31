from app.config.database import get_db

def create_tables():
    with get_db() as conn:
        cursor = conn.cursor()

        cursor.execute("""--sql
            CREATE TABLE IF NOT EXISTS url_lookup (
                url_md5 TEXT PRIMARY KEY,
                url TEXT NOT NULL
        )
        """)
