from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.env_config import settings

SQLALCHEMY_DATABASE_URL = (
    f"{settings.DB_DIALECT}://{settings.DB_USER}:{settings.DB_PASSWORD}@"
    f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=settings.APP_DEBUG)

session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

base = declarative_base()


def get_db() -> Generator:
    """
    Context manager para conexão com o banco de dados.
    Garante commit, rollback e fechamento da conexão.
    """

    db = session_local()

    try:
        yield db

    finally:
        db.close()
