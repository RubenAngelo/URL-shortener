"""
Módulo de rotas para encurtamento de URLs utilizando FastAPI.

Este módulo define a rota responsável por receber uma URL original,
gerar um hash MD5 para identificá-la de forma única, armazenar o mapeamento
no banco de dados e retornar uma URL encurtada para o usuário.
"""

from fastapi import APIRouter, Request

from app.core.logging_config import setup_logging
from app.models.url_shortener_models import UrlRequest, UrlResponse
from app.utils.utils import md5_url_encode, build_short_url
from app.CRUD.url_crud import create_url_mapping, fetch_md5_hash_by_url

logger = setup_logging("url_shortener")

router = APIRouter()

@router.post("/shorten", response_model=UrlResponse)
def create_short_url(request: UrlRequest, fastapi_request: Request) -> UrlResponse:
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
    url_md5_hash = fetch_md5_hash_by_url(url)

    if not url_md5_hash:
        # Gera o hash MD5 da URL
        url_md5_hash = md5_url_encode(url)

        # Insere a URL e o hash MD5 na tabela
        create_url_mapping(url, url_md5_hash)

    # Gera a URL encurtada
    short_url = build_short_url(fastapi_request, "redirect_short_url", url_md5_hash)

    logger.info("Retornando URL encurtada...")

    return UrlResponse(short_url=short_url)
