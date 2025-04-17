"""
Global exception handlers
"""

from typing import Any, Dict
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError as PydanticValidationError
from starlette.exceptions import HTTPException
from src.utils.common import format_error


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Handle HTTP exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content=format_error(message=exc.detail, data=getattr(exc, "details", {})),
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handle request validation errors
    """
    detail = []
    for error in exc.errors():
        error_message = {
            "loc": error["loc"],
            "msg": error["msg"],
            "type": error["type"],
        }
        detail.append(error_message)

    # Log the error for debugging purposes
    if detail:
        print(f"Validation error: {detail[0]}")

    return JSONResponse(status_code=422, content={"detail": detail})


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle any unhandled exceptions"""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=format_error(message="Internal server error", data=str(exc)),
    )
