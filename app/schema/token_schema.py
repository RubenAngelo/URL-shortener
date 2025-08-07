from pydantic import BaseModel


class Token(BaseModel):
    """
    Modelo Pydantic para o token de acesso e tipo de token.
    """

    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """
    Modelo Pydantic para os dados contidos no token (payload).
    """

    username: str | None = None
