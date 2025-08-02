"""
Módulo de rotas para redirecionamento de URLs curtas.

Este módulo define a rota responsável por redirecionar o usuário para a URL original
a partir de um hash MD5 fornecido na URL. Caso o hash não corresponda a nenhuma URL
cadastrada, retorna um erro 404.
"""

from fastapi import APIRouter
from fastapi.responses import RedirectResponse

from app.core.logging_config import setup_logging
from app.CRUD.url_crud import fetch_url_by_md5_hash

logger = setup_logging("redirect")

router = APIRouter()

@router.get("/{url_md5_hash}", response_class=RedirectResponse)
def redirect_short_url(url_md5_hash: str) -> RedirectResponse:
    """
    Redireciona para a URL original a partir da URL curta.
    Se não existir URL para o hash MD5, retorna um erro 404.
    """

    # Busca a URL original a partir do hash MD5
    url = fetch_url_by_md5_hash(url_md5_hash)

    logger.info("Redirecionando para %s...", url)

    # Redireciona para a URL original
    return RedirectResponse(url=url, status_code=307)
