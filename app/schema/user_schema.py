from pydantic import BaseModel

class UserBase(BaseModel):
    """
    Modelo base para um usuário, contendo campos comuns.
    """

    email: str

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
