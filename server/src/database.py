"""
Database configuration and initialization.
"""

from tortoise import Tortoise
from src.config import settings


async def init_db():
    """Initialize database and create schemas."""
    await Tortoise.init(config=settings.TORTOISE_ORM)
    # Generate schemas if not in production
    if settings.ENV != "production":
        await Tortoise.generate_schemas()


async def close_db():
    """Close database connections."""
    await Tortoise.close_connections()
