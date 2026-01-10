"""
Rutas administrativas protegidas
Dashboard, métricas y gestión de waitlist
"""
import logging
import math
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from sqlalchemy.orm import Session
from sqlalchemy import func
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.db.database import get_db
from app.middleware.auth import get_current_admin
from app.models.admin_user import AdminUser
from app.models.waitlist import Waitlist
from app.services.admin_service import AdminService
from app.schemas.admin import (
    PaginatedWaitlistResponse,
    WaitlistItemAdmin,
    MetricsResponse,
    UserTypeFilter
)
router = APIRouter()
limiter = Limiter(key_func=get_remote_address)
logger = logging.getLogger(__name__)
@router.get(
    "/waitlist",
    response_model=PaginatedWaitlistResponse,
    tags=["Admin"],
    summary="Lista paginada de waitlist V2 (UNLIMITED)"
)
@limiter.limit("60/minute")  # Máximo 60 requests por minuto por IP
async def get_waitlist(
    request: Request,
    page: int = Query(1, ge=1, description="Número de página"),
    limit: int = Query(20, ge=1, description="Registros por página"),
    user_type: Optional[UserTypeFilter] = Query(None, description="Filtrar por tipo de usuario"),
    product_of_interest: Optional[str] = Query(None, description="Búsqueda parcial en producto"),
    source: Optional[str] = Query(None, description="Filtrar por fuente de tráfico"),
    country: Optional[str] = Query(None, description="Filtrar por país"),
    email: Optional[str] = Query(None, description="Búsqueda parcial por email"),
    # Nuevos filtros de tracking
    city: Optional[str] = Query(None, description="Filtrar por ciudad"),
    device_type: Optional[str] = Query(None, description="Filtrar por dispositivo (mobile/desktop/tablet)"),
    traffic_source: Optional[str] = Query(None, description="Filtrar por origen de tráfico"),
    order_by: str = Query("created_at_desc", regex="^(created_at_desc|registration_count_desc)$"),
    admin: AdminUser = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    **Obtiene lista paginada de registros de waitlist**
    - Requiere autenticación (Bearer token)
    - Soporta filtros múltiples
    - Ordenamiento configurable
    - Registros por página personalizable
    **Filtros disponibles:**
    - `user_type`: student | company | university
    - `product_of_interest`: búsqueda parcial (case-insensitive)
    - `source`: fuente de tráfico (Instagram, Facebook, etc.)
    - `country`: país del usuario
    - `email`: búsqueda parcial por email
    - `city`: ciudad del usuario (NUEVO)
    - `device_type`: tipo de dispositivo (NUEVO)
    - `traffic_source`: origen de tráfico inferido (NUEVO)
    **Ordenamiento:**
    - `created_at_desc`: Más recientes primero (default)
    - `registration_count_desc`: Más intentos primero
    """
    try:
        # Obtener datos paginados
        items, total = AdminService.get_waitlist_paginated(
            db=db,
            page=page,
            limit=limit,
            user_type=user_type.value if user_type else None,
            product_of_interest=product_of_interest,
            source=source,
            country=country,
            email=email,
            # Nuevos filtros
            city=city,
            device_type=device_type,
            traffic_source=traffic_source,
            order_by=order_by
        )
        # Calcular total de páginas
        pages = math.ceil(total / limit) if total > 0 else 1
        # Convertir a schemas
        items_response = [WaitlistItemAdmin.model_validate(item) for item in items]
        logger.info(f"Admin {admin.email} fetched waitlist page {page}")
        return PaginatedWaitlistResponse(
            total=total,
            page=page,
            limit=limit,
            pages=pages,
            items=items_response
        )
    except Exception as e:
        logger.error(f"Error fetching waitlist: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving waitlist data"
        )
@router.get(
    "/metrics",
    response_model=MetricsResponse,
    tags=["Admin"],
    summary="Métricas agregadas de waitlist"
)
@limiter.limit("30/minute")  # Máximo 30 requests por minuto por IP
async def get_metrics(
    request: Request,
    admin: AdminUser = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    **Obtiene métricas y estadísticas agregadas**
    - Requiere autenticación (Bearer token)
    - Datos calculados en tiempo real
    - Útil para dashboards y reportes
    **Métricas incluidas:**
    - Total de registros únicos
    - Total de intentos de registro
    - Distribución por tipo de usuario
    - Distribución por fuente de tráfico
    - Top 10 países
    - Top 10 emails con más intentos
    - Último registro por tipo de usuario
    """
    try:
        # Calcular métricas
        total_registrations = db.query(func.count(Waitlist.id)).scalar() or 0
        total_attempts = AdminService.get_total_attempts(db)
        by_user_type = AdminService.get_metrics_by_user_type(db)
        by_source = AdminService.get_metrics_by_source(db)
        by_country = AdminService.get_metrics_by_country(db)

        # NUEVAS MÉTRICAS DE TRACKING
        by_city = AdminService.get_metrics_by_city(db, limit=10)
        by_device = AdminService.get_metrics_by_device(db)
        by_traffic_source = AdminService.get_metrics_by_traffic_source(db, limit=10)
        by_traffic_source_type = AdminService.get_metrics_by_traffic_source_type(db)
        top_explicit_sources = AdminService.get_top_explicit_sources(db, limit=10)
        top_detected_sources = AdminService.get_top_detected_sources(db, limit=10)

        top_emails = AdminService.get_top_emails(db, limit=10)
        latest_by_type = AdminService.get_latest_by_type(db)
        logger.info(f"Admin {admin.email} fetched metrics")
        return MetricsResponse(
            total_registrations=total_registrations,
            total_attempts=total_attempts,
            by_user_type=by_user_type,
            by_source=by_source,
            by_country=by_country,
            # Nuevas métricas
            by_city=by_city,
            by_device=by_device,
            by_traffic_source=by_traffic_source,
            by_traffic_source_type=by_traffic_source_type,
            top_explicit_sources=top_explicit_sources,
            top_detected_sources=top_detected_sources,
            top_emails=top_emails,
            latest_by_type=latest_by_type
        )
    except Exception as e:
        logger.error(f"Error fetching metrics: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error calculating metrics"
        )
