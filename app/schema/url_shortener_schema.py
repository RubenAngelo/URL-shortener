"""
Este módulo define os modelos de dados utilizados para o serviço de encurtamento de URLs.

Utiliza Pydantic para validação dos dados.
"""

from pydantic import BaseModel, HttpUrl


class UrlRequest(BaseModel):
    """
    Modelo para requisição de encurtamento de URL.
    """

    url: HttpUrl


class UrlResponse(BaseModel):
    """
    Modelo de resposta contendo a URL encurtada.
    """

    short_url: HttpUrl
