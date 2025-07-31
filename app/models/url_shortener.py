from pydantic import BaseModel, HttpUrl

class UrlRequests(BaseModel):
    url: HttpUrl

class UrlResponses(BaseModel):
    short_url: str
