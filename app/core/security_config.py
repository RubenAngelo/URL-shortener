from datetime import datetime, timedelta, timezone
from typing import Union

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.env_config import settings
from app.schema.token_schema import TokenData
from app.CRUD.user_crud import get_user_by_username
from app.core.database_config import get_db
from app.core.logging_config import setup_logging

logger = setup_logging("security_config")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

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
        username: str = payload.get("sub")

        if username is None:
            raise credentials_exception

        token_data = TokenData(username=username)

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
    user = get_user_by_username(db, username=token_data.username)

    if user is None:
        raise credentials_exception

    return user
