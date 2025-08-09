from app.core.logging_config import setup_logging
from app.core.database_config import base, engine, session_local
from app.CRUD.partners_crud import create_initial_api_key

logger = setup_logging("init_db")


def create_all_tables() -> None:
    """
    Cria todas as tabelas no banco de dados definidas pelos modelos SQLAlchemy.
    """

    logger.info("Validando e criando tabelas (se não existirem)...")

    base.metadata.create_all(bind=engine)

    logger.info("Todas as tabelas estão prontas!")

    logger.info("Criando chave de API inicial...")

    db = session_local()

    try:
        create_initial_api_key(db)

    finally:
        db.close()

    logger.info("Chave de API inicial criada com sucesso!")
