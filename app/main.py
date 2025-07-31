from fastapi import FastAPI
from app.schema.init_db import create_tables
from app.api.routers import all_routers

create_tables()

app = FastAPI()

for router, prefix in all_routers:
    app.include_router(router, prefix=prefix)
