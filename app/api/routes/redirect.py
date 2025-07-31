from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from app.CRUD.url import get_url_by_url_code
from app.models.redirect import RedirectResponses

router = APIRouter()

@router.get("/{md5_code}", response_model=RedirectResponses)
def redirect_short_url(md5_code: str):
    url = get_url_by_url_code(md5_code)

    return RedirectResponse(url=url, status_code=302)
