from sqlalchemy import Column, Integer, String, Boolean
from app.core.database_config import base


class ApiKey(base):
    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    key = Column(String, unique=True, index=True, nullable=False)
    client_name = Column(String, unique=True, nullable=False)
    is_active = Column(Boolean, default=True)
