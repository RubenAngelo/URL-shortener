from app.core.logging_config import setup_logging
from app.core.database_config import base, engine

logger = setup_logging("init_db")


def create_all_tables() -> None:
    """
    Cria todas as tabelas no banco de dados definidas pelos modelos SQLAlchemy.
    """

    logger.info("Validando e criando tabelas (se não existirem)...")

    base.metadata.create_all(bind=engine)

    logger.info("Todas as tabelas estão prontas!")
