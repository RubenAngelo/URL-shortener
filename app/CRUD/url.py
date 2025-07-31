from app.config.database import get_db

def insert_url(url: str, url_code: str):
    with get_db() as conn:
        cursor = conn.cursor()

        cursor.execute("""--sql
            INSERT INTO url_lookup (
                url_md5, 
                url
            ) 

            VALUES (
                %s, 
                %s
            )

            """,
            (#VALUES
                url_code,
                url
            )
        )

def get_url_by_url_code(url_code: str):
    with get_db() as conn:
        cursor = conn.cursor()

        cursor.execute("""--sql
            SELECT 
                url 

            FROM 
                url_lookup

            WHERE 
                url_md5 = %s

            """,
            (#VALUES
                url_code,
            )
        )

        return cursor.fetchone()["url"]
