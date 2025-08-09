from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.database_config import get_db
from app.core.security_config import (
    create_access_token,
    AUTH_ACCESS_TOKEN_EXPIRE_MINUTES,
    get_api_key,
)
from app.models.api_key_model import ApiKey
from app.CRUD.user_crud import get_user_by_email, create_user
from app.utils.utils import verify_password, decode_auth
from app.schema.token_schema import Token
from app.schema.user_schema import UserCreate, UserResponse
from app.core.logging_config import setup_logging

logger = setup_logging("auth")

router = APIRouter()


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """
    Endpoint para login de usuário e obtenção de token de acesso.
    """

    email, password = decode_auth(form_data.password)

    user = get_user_by_email(db=db, email=email)

    if not user or not verify_password(
        password=password, hashed_password=user.password
    ):

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nome de usuário ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=AUTH_ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    logger.info("Usuário autenticado com sucesso!")

    return Token(access_token=access_token, token_type="bearer")


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
def register_user(
    user: UserCreate, db: Session = Depends(get_db), _: ApiKey = Depends(get_api_key)
):
    """
    Endpoint para registro de um novo usuário.
    """

    db_user = get_user_by_email(db, email=user.email)

    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nome de usuário já registrado",
        )

    try:
        new_user = create_user(db=db, user=user)
        return UserResponse(id=new_user.id, email=new_user.email)

    except Exception as e:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao registrar usuário: {e}",
        ) from e
