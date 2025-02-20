"""
FastAPI Template Application
This is a template for FastAPI applications following best practices.
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from starlette.responses import RedirectResponse
from tortoise.exceptions import BaseORMException
from contextlib import asynccontextmanager
from dotenv import load_dotenv

load_dotenv('.env')

from src.config import  settings
from src.database import init_db, close_db
from src.modules.auth.router import router as user_router
from src.exceptions import (
    http_exception_handler,
    validation_exception_handler,
    generic_exception_handler,
    database_exception_handler,
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan events."""
    await init_db()
    yield
    await close_db()

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="A template FastAPI application with best practices",
    lifespan=lifespan
)

# Register exception handlers
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(BaseORMException, database_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers with API versioning
app.include_router(user_router, prefix=settings.API_V1_PREFIX)


@app.get("/")
async def root():
    """
    Root endpoint that redirects to the API documentation.
    Returns:
        RedirectResponse: Redirects to the /docs endpoint
    """
    return RedirectResponse(url="/docs")


@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify the API is running.
    Returns:
        dict: A simple message indicating the API is healthy
    """
    return {"version": settings.VERSION, "status": "healthy"}
