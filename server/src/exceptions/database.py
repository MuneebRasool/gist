"""
Database exceptions and handlers
"""

from typing import Any, Dict, Optional
from fastapi import Request, status
from fastapi.responses import JSONResponse
from tortoise.exceptions import (
    DoesNotExist,
    IntegrityError,
    ValidationError,
    OperationalError,
)
from src.utils.common import format_error


class DatabaseException(Exception):
    """Base exception for database errors"""

    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        details: Optional[Dict[str, Any]] = None,
    ):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


async def database_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle database exceptions and return appropriate responses"""

    if isinstance(exc, DoesNotExist):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=format_error(data=str(exc), message="Resource not found"),
        )

    if isinstance(exc, IntegrityError):
        # Handle unique constraint violations
        if "unique constraint" in str(exc).lower():
            return JSONResponse(
                status_code=status.HTTP_409_CONFLICT,
                content=format_error(data=str(exc), message="Resource already exists"),
            )
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=format_error(data=str(exc), message="Database integrity error"),
        )

    if isinstance(exc, ValidationError):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=format_error(data=str(exc), message="Validation error"),
        )

    if isinstance(exc, OperationalError):
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content=format_error(data=str(exc), message="Database operation error"),
        )

    if isinstance(exc, DatabaseException):
        return JSONResponse(
            status_code=exc.status_code,
            content=format_error(message=exc.message, data=exc.details),
        )

    # Handle any other database-related exceptions
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=format_error(
            message="An unexpected database error occurred", data=str(exc)
        ),
    )
