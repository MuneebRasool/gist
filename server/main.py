"""
FastAPI Template Application
This is a template for FastAPI applications following best practices.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from starlette.responses import RedirectResponse
from tortoise.exceptions import BaseORMException
from contextlib import asynccontextmanager
from src.config import  settings
from src.database import init_db, close_db
from src.modules.auth.router import router as user_router
from src.modules.nylas.router import router as nylas_router
from src.modules.nylas.email_router import router as nylas_email_router
from src.modules.agent.router import router as agent_router
from src.modules.tasks.router import router as tasks_router
from src.modules.feedback.router import router as feedback_router
from src.modules.user.router import router as users_router
from src.exceptions import (
    http_exception_handler,
    validation_exception_handler,
    generic_exception_handler,
    database_exception_handler,
)
from neomodel import config as neo_config

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan events."""
    await init_db()
    neo_config.DATABASE_URL = settings.NEO4J_URL
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
app.include_router(nylas_router, prefix=settings.API_V1_PREFIX)
app.include_router(nylas_email_router, prefix=settings.API_V1_PREFIX)
app.include_router(agent_router, prefix=settings.API_V1_PREFIX)
app.include_router(tasks_router, prefix=settings.API_V1_PREFIX)
app.include_router(feedback_router, prefix=settings.API_V1_PREFIX)
app.include_router(users_router, prefix=settings.API_V1_PREFIX)

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
