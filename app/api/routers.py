from app.api.routes.url_shortener import router as url_shortener_router
from app.api.routes.redirect import router as redirect_router

all_routers = [
    (url_shortener_router, "/api"),
    (redirect_router, "/r"),
]
