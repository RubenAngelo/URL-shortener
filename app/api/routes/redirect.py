from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from app.CRUD.url import fetch_url_by_md5

router = APIRouter()

@router.get("/{url_md5}", response_class=RedirectResponse)
def redirect_short_url(url_md5: str):
    """
    Redireciona para a URL original a partir da URL curta.
    Se não existir URL para o hash MD5, retorna um erro 404.
    """

    url = fetch_url_by_md5(url_md5)

    if not url:
        raise HTTPException(status_code=404, detail="URL não encontrada.")

    return RedirectResponse(url=url, status_code=302)
