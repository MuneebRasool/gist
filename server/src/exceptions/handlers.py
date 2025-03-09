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


async def validation_exception_handler(
    request: Request, exc: RequestValidationError | PydanticValidationError
) -> JSONResponse:
    """Handle request validation errors"""
    print("\n---------------------------------------")
    print("❌ VALIDATION ERROR:")
    
    errors: Dict[str, Any] = {}
    for error in exc.errors():
        # For logging purposes
        location = " -> ".join([str(loc) for loc in error["loc"]])
        print(f"  Field: {location}")
        print(f"  Error: {error['msg']}")
        print(f"  Type: {error['type']}")
        print("---")
        
        # Original functionality
        loc = ".".join(str(x) for x in error["loc"])
        errors[loc] = error["msg"]
    
    print("---------------------------------------\n")

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=format_error(message="Validation error", data=errors),
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle any unhandled exceptions"""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=format_error(message="Internal server error", data=str(exc)),
    )
