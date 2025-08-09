from datetime import datetime, timedelta, timezone
from typing import Union

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from fastapi.security.api_key import APIKeyHeader

from app.core.env_config import settings
from app.schema.token_schema import TokenData
from app.CRUD.user_crud import get_user_by_email
from app.core.database_config import get_db
from app.core.logging_config import setup_logging
from app.models.api_key_model import ApiKey

logger = setup_logging("security_config")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=True)

AUTH_SECRET_KEY = settings.AUTH_SECRET_KEY
AUTH_ALGORITHM = settings.AUTH_ALGORITHM
AUTH_ACCESS_TOKEN_EXPIRE_MINUTES = settings.AUTH_ACCESS_TOKEN_EXPIRE_MINUTES


def create_access_token(
    data: dict, expires_delta: Union[timedelta, None] = None
) -> str:
    """
    Cria um token de acesso JWT.
    """

    logger.info("Criando token de acesso...")

    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta

    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=AUTH_ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, AUTH_SECRET_KEY, algorithm=AUTH_ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception) -> TokenData:
    """
    Verifica e decodifica um token de acesso JWT.
    Levanta uma exceção se o token for inválido ou expirado.
    """

    try:
        payload = jwt.decode(token, AUTH_SECRET_KEY, algorithms=[AUTH_ALGORITHM])
        email: str = payload.get("sub")

        if email is None:
            raise credentials_exception

        token_data = TokenData(email=email)

    except jwt.PyJWTError as exc:
        raise credentials_exception from exc

    return token_data


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    """
    Dependência para obter o usuário logado a partir do token.
    """

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data = verify_access_token(token, credentials_exception)
    user = get_user_by_email(db, email=token_data.email)

    if user is None:
        raise credentials_exception

    return user


async def get_api_key(
    api_key: str = Depends(api_key_header), db: Session = Depends(get_db)
):
    """
    Dependência para validar uma API Key.
    Espera a API Key no cabeçalho X-API-Key.
    """
    # Lógica para buscar a API Key no banco de dados
    db_api_key = (
        db.query(ApiKey).filter(ApiKey.key == api_key, ApiKey.is_active == True).first()
    )

    if not db_api_key:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="API Key inválida ou inativa. Acesso negado.",
        )
    return db_api_key  # Retorna o objeto ApiKey validado
