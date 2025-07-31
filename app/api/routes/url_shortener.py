from fastapi import APIRouter,Request
from app.CRUD.url import insert_url
from app.utils.utils import md5_url_encode
from app.models.url_shortener import UrlRequests, UrlResponses

router = APIRouter()

@router.post("/url/shortener", response_model=UrlResponses)
def create_short_url(request_body: UrlRequests, request: Request):
    url = str(request_body.url)

    md5_code = md5_url_encode(url)
    insert_url(url, md5_code)

    short_url = str(request.url_for("redirect_short_url", md5_code=md5_code))

    return {
        "short_url": short_url
    }
