from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.logging_config import setup_logging
from app.models.url_db_model import UrlLookup

logger = setup_logging("url_crud")


def get_url_hash_by_url(db: Session, url: str) -> Optional[str]:
    """
    Verifica se uma URL já existe no banco de dados e retorna o hash associado.
    """

    logger.info("Verificando se a URL já existe no banco...")

    url_obj = db.query(UrlLookup).filter_by(url=url).first()

    if not url_obj:
        logger.info("A URL não existe no banco.")
        return None

    logger.info("A URL já existe no banco.")
    return url_obj.url_hash


def get_url_by_url_hash(db: Session, url_hash: str) -> Optional[str]:
    """
    Busca a URL original a partir do hash.
    Retorna a URL se encontrada.
    """
    logger.info("Buscando URL pelo hash ...")

    url_obj = db.query(UrlLookup).get(url_hash)

    if not url_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="URL não encontrada."
        )

    logger.info("URL encontrada com sucesso!")
    return url_obj.url


def create_url_mapping(db: Session, url: str, url_hash: str) -> None:
    """
    Insere uma nova URL e seu hash na tabela url_lookup.
    """
    logger.info("Inserindo URL no banco...")

    new_url = UrlLookup(url_hash=url_hash, url=url)

    db.add(new_url)
    db.commit()
    db.refresh(new_url)

    logger.info("URL inserida com sucesso!")
