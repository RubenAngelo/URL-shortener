"""
Módulo de rotas para redirecionamento de URLs curtas.

Este módulo define a rota responsável por redirecionar o usuário para a URL original
a partir de um hash fornecido na URL.
"""

from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.core.database_config import get_db
from app.core.logging_config import setup_logging
from app.CRUD.url_crud import get_url_by_url_hash

logger = setup_logging("redirect_url")

router = APIRouter()


@router.get("/r/{url_hash}", response_class=RedirectResponse)
def redirect_short_url(
    url_hash: str, db: Session = Depends(get_db)
) -> RedirectResponse:
    """
    Redireciona para a URL original a partir da URL curta.
    """

    # Busca a URL original a partir do hash
    url = get_url_by_url_hash(db=db, url_hash=url_hash)

    logger.info("Redirecionando para %s...", url)

    # Redireciona para a URL original
    return RedirectResponse(url=url, status_code=307)
