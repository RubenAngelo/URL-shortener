"""
Este módulo é o principal da aplicação URL Shortener.

O módulo inicializa a aplicação FastAPI, configura os parâmetros principais
utilizando as definições do arquivo de configuração, registra os roteadores da API
e garante a criação da tabela de armazenamento de URLs no banco de dados durante
o evento de inicialização.

A aplicação permite o encurtamento de URLs e o gerenciamento dos redirecionamentos,
utilizando rotas registradas dinamicamente.
"""

from fastapi import FastAPI, HTTPException

from app.core.env_config import settings
from app.core.exception_handlers import (
    http_exception_handler,
    generic_exception_handler,
)
from app.database.init_db import create_all_tables
from app.api.routers import api_registered_routers

# Cria a aplicação FastAPI
app = FastAPI(title=settings.APP_NAME, debug=settings.APP_DEBUG)

# Configura o tratamento de exceções das requisições
app.add_exception_handler(HTTPException, http_exception_handler)

# Configura o tratamento de exceções geral
app.add_exception_handler(Exception, generic_exception_handler)


# Ao iniciar a aplicação, cria a tabela do banco de dados
@app.on_event("startup")
def on_startup() -> None:
    """
    Evento de inicialização da aplicação.
    Cria a tabela do banco de dados, se necessário.
    """

    # Cria a tabela do banco de dados
    create_all_tables()


# Registra as rotas da API
for router, prefix in api_registered_routers:
    app.include_router(router, prefix=prefix)
