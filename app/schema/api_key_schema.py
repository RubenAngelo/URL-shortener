from pydantic import BaseModel


class ApiKeyResponse(BaseModel):
    client_name: str
    is_active: bool

    class Config:
        from_attributes = True
