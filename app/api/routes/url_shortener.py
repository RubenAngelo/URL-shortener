from fastapi import APIRouter,Request
from app.CRUD.url import insert_url_mapping
from app.utils.utils import md5_url_encode
from app.models.url_shortener_models import UrlRequest, UrlResponse

router = APIRouter()

@router.post("/shorten", response_model=UrlResponse)
def create_short_url(request: UrlRequest, fastapi_request: Request):
    """
    Cria uma URL encurtada a partir de uma URL original.
    Retorna a URL encurtada.
    """

    url = str(request.url)

    url_md5 = md5_url_encode(url)
    insert_url_mapping(url, url_md5)

    short_url = str(fastapi_request.url_for("redirect_short_url", url_md5=url_md5))

    return UrlResponse(short_url=short_url)
