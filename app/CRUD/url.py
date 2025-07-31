from app.config.database import get_db

def fetch_url_by_md5(url_md5: str):
    """
    Busca a URL original a partir do hash MD5.
    Retorna a URL se encontrada, ou None.
    """

    try:
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
                (url_md5,)
            )

            result = cursor.fetchone()

            return result["url"] if result else None

    except Exception as e:
        return None

def insert_url_mapping(url: str, url_md5: str):
    """
    Insere uma nova URL e seu hash MD5 na tabela url_lookup.
    Retorna True se inserção for bem-sucedida, False caso contrário.
    """

    exist_url = fetch_url_by_md5(url_md5)

    if exist_url:
        return True

    try:
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
                (url_md5, url)
            )
        return True

    except Exception as e:
        return False
