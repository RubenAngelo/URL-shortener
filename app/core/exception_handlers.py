"""
Módulo de manipuladores de exceções para a aplicação FastAPI.

Este módulo define funções assíncronas para lidar com exceções HTTP e genéricas,
registrando os erros e retornando respostas JSON apropriadas.
"""

from http import HTTPStatus

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

from app.core.logging_config import setup_logging
from app.utils.utils import current_timestamp

logger = setup_logging("exception_handlers")

async def http_exception_handler(request: Request, exception: HTTPException) -> JSONResponse:
    """
    Manipula exceções HTTP lançadas durante o processamento de requisições.
    Este manipulador registra o erro ocorrido e retorna uma resposta JSON contendo detalhes sobre a exceção,
    incluindo o código de status, mensagem de erro, descrição da exceção e o timestamp do momento em que ocorreu.
    """

    logger.error("HTTP error: %s - Path: %s", exception, request.url.path)

    status_code = exception.status_code
    status_phrase = HTTPStatus(status_code).phrase

    return JSONResponse(
        status_code=status_code,
        content={
            "error": status_phrase,
            'status_code': status_code,
            "description": exception.detail,
            'timestamp': current_timestamp()
        },
    )

async def generic_exception_handler(request: Request, exception: Exception) -> JSONResponse:
    """
    Manipula exceções genéricas não tratadas durante o processamento de requisições HTTP.
    Este manipulador registra o erro ocorrido, incluindo informações sobre a exceção e o caminho da requisição,
    e retorna uma resposta JSON padronizada com o status HTTP 500 (Erro Interno do Servidor).
    """

    logger.error("Unhandled error: %s - Path: %s", exception, request.url.path, exc_info=True)

    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            'status_code': 500,
            'description': str(exception),
            'timestamp': current_timestamp()
        },
    )
