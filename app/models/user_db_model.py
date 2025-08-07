from sqlalchemy import Column, Integer, String, Boolean

from app.core.database_config import base


class User(base):
    """
    Modelo de usuário para armazenamento no banco de dados.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True, nullable=True)
    password = Column(String)
    disabled = Column(Boolean, default=False)
