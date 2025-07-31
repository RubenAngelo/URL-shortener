from fastapi import FastAPI
from app.schema.init_db import create_tables
from app.api.routers import registered_routers
from app.core.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.APP_DEBUG
)

@app.on_event("startup")
def on_startup():
    """
    Evento de inicialização da aplicação.
    Cria as tabelas do banco de dados, se necessário.
    """

    create_tables()

for router, prefix in registered_routers:
    app.include_router(router, prefix=prefix)
