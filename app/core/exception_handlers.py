from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

from app.core.logging_config import setup_logging

logger = setup_logging("exception_handlers")

async def http_exception_handler(request: Request, exception: HTTPException):
    logger.error("HTTP error: %s - Path: %s", exception, request)

    return JSONResponse(
        status_code=exception.status_code,
        content={"detail": exception.detail},
    )

async def generic_exception_handler(request: Request, exception: HTTPException):
    logger.error("Unhandled error: %s - Path: %s", exception, request, exc_info=True)

    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )
