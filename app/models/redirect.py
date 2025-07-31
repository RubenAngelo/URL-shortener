from pydantic import BaseModel, HttpUrl

class RedirectResponses(BaseModel):
    url: HttpUrl
