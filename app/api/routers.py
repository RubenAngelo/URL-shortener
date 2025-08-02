"""
Este módulo registra e organiza os roteadores (routers) da aplicação FastAPI.

Ele importa e agrupa os roteadores responsáveis pelas funcionalidades de encurtamento de URLs e redirecionamento,
definindo os caminhos base para cada um. Novas rotas devem ser adicionadas à lista `api_registered_routers` conforme necessário.
A lista `api_registered_routers` contém tuplas com o roteador e seu respectivo prefixo de rota.
"""

from typing import List, Tuple

from fastapi import APIRouter

from app.api.routes.url_shortener import router as url_shortener_router
from app.api.routes.redirect_url import router as redirect_router

#Novas rotas devem ser adicionadas aqui
api_registered_routers: List[Tuple[APIRouter, str]] = [
    (url_shortener_router, "/api"),
    (redirect_router, "/r"),
]
