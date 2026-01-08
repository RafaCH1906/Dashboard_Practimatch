"""
Health check endpoint
Verifica que la API y la base de datos estén funcionando
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.db.database import get_db
from app.schemas.waitlist import HealthResponse
from app.config import settings

router = APIRouter()


@router.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check(db: Session = Depends(get_db)):
    """
    Health check endpoint

    Verifica:
    - La API está respondiendo
    - La conexión a PostgreSQL funciona
    """
    try:
        # Test de conexión a DB
        db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"

    return HealthResponse(
        status="healthy" if db_status == "connected" else "unhealthy",
        app_name=settings.APP_NAME,
        version=settings.VERSION,
        database=db_status
    )

