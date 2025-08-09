"""
Módulo de rotas para encurtamento de URLs utilizando FastAPI.

Este módulo define a rota responsável por receber uma URL original,
gerar um hash para identificá-la de forma única, armazenar o mapeamento
no banco de dados e retornar uma URL encurtada para o usuário.
"""

from fastapi import APIRouter, Request, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.models.user_db_model import User
from app.core.database_config import get_db
from app.core.logging_config import setup_logging
from app.schema.url_shortener_schema import UrlRequest, UrlResponse
from app.utils.utils import generate_url_hash, build_short_url
from app.CRUD.url_crud import create_url_mapping, get_url_hash_by_url
from app.core.security_config import get_current_user

logger = setup_logging("url_shortener")

router = APIRouter()


@router.post("/shorten", response_model=UrlResponse)
def create_short_url(
    request: UrlRequest,
    fastapi_request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> UrlResponse:
    """
    Cria uma URL encurtada a partir de uma URL original.
    Retorna a URL encurtada.
    """

    logger.info("Nova requisição.")

    url = str(request.url)
    base_url = str(fastapi_request.base_url)

    logger.info("Verificando se é uma URL já encurtada...")

    # Verifica se a URL já é uma URL encurtada
    if url.startswith(base_url):
        logger.info("A URL ja foi encurtada. Devolvendo URL encurtada...")

        return UrlResponse(short_url=url)

    # Verifica se a URL ja existe no banco
    url_hash = get_url_hash_by_url(db=db, url=url)

    if not url_hash:
        # Gera o hash da URL
        url_hash = generate_url_hash(url=url)

    try:
        # Insere a URL e o hash na tabela
        create_url_mapping(db=db, url=url, url_hash=url_hash, user_id=user.id)

    except Exception as e:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao registrar usuário: {e}",
        ) from e

    # Gera a URL encurtada
    short_url = build_short_url(
        fastapi_request=fastapi_request,
        endpoint_func_name="redirect_short_url",
        url_hash=url_hash,
    )

    logger.info("Retornando URL encurtada...")

    return UrlResponse(short_url=short_url)
