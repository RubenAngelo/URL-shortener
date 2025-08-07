from pydantic import BaseModel, EmailStr
from typing import Optional


class UserBase(BaseModel):
    """
    Modelo base para um usuário, contendo campos comuns.
    """

    username: str
    email: Optional[EmailStr] = None
    disabled: Optional[bool] = None


class UserCreate(UserBase):
    """
    Modelo para criação de um novo usuário.
    Inclui o campo de senha.
    """

    password: str


class UserResponse(UserBase):
    """
    Modelo de usuário para ser retornado pela API.
    Não inclui a senha.
    """

    id: int

    class Config:
        from_attributes = True
