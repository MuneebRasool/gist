from .service import NylasService
from fastapi import HTTPException


def get_nylas_service() -> NylasService:
    """Dependency to get Nylas service instance."""
    try:
        return NylasService()
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
