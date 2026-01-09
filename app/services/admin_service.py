"""
Servicio para operaciones administrativas
Queries, filtros, métricas y estadísticas
"""
import logging
from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import func, desc

from app.models.waitlist import Waitlist
from app.schemas.admin import (
    MetricsByCategory,
    TopEmail,
    LatestByType
)

logger = logging.getLogger(__name__)


class AdminService:
    """Servicio para operaciones del dashboard administrativo"""

    @staticmethod
    def get_waitlist_paginated(
        db: Session,
        page: int = 1,
        limit: int = 20,
        user_type: Optional[str] = None,
        product_of_interest: Optional[str] = None,
        source: Optional[str] = None,
        country: Optional[str] = None,
        email: Optional[str] = None,
        order_by: str = "created_at_desc"
    ) -> Tuple[List[Waitlist], int]:
        """
        Obtiene lista paginada de waitlist con filtros

        Args:
            page: Número de página (1-indexed)
            limit: Registros por página (max 100)
            user_type: Filtro por tipo de usuario
            product_of_interest: Filtro por producto (búsqueda parcial)
            source: Filtro por fuente de tráfico
            country: Filtro por país
            email: Búsqueda parcial por email
            order_by: Ordenamiento (created_at_desc | registration_count_desc)

        Returns:
            Tuple con (lista de registros, total de registros)
        """
        # Límite máximo
        limit = min(limit, 100)

        # Query base
        query = db.query(Waitlist)

        # Aplicar filtros
        if user_type:
            query = query.filter(Waitlist.user_type == user_type)

        if product_of_interest:
            query = query.filter(Waitlist.product_of_interest.ilike(f"%{product_of_interest}%"))

        if source:
            query = query.filter(Waitlist.source.ilike(f"%{source}%"))

        if country:
            query = query.filter(Waitlist.country.ilike(f"%{country}%"))

        if email:
            query = query.filter(Waitlist.email.ilike(f"%{email}%"))

        # Total antes de paginar
        total = query.count()

        # Ordenamiento
        if order_by == "registration_count_desc":
            query = query.order_by(desc(Waitlist.registration_count))
        else:  # created_at_desc por defecto
            query = query.order_by(desc(Waitlist.created_at))

        # Paginación
        offset = (page - 1) * limit
        items = query.offset(offset).limit(limit).all()

        logger.info(f"Fetched {len(items)} waitlist items (page {page}, total {total})")
        return items, total

    @staticmethod
    def get_metrics_by_user_type(db: Session) -> List[MetricsByCategory]:
        """Obtiene cantidad de registros por tipo de usuario"""
        results = (
            db.query(
                Waitlist.user_type.label("category"),
                func.count(Waitlist.id).label("count")
            )
            .group_by(Waitlist.user_type)
            .order_by(desc("count"))
            .all()
        )

        return [
            MetricsByCategory(category=str(r.category), count=r.count)
            for r in results
        ]

    @staticmethod
    def get_metrics_by_source(db: Session) -> List[MetricsByCategory]:
        """Obtiene cantidad de registros por fuente de tráfico"""
        results = (
            db.query(
                func.coalesce(Waitlist.source, "Unknown").label("category"),
                func.count(Waitlist.id).label("count")
            )
            .group_by("category")
            .order_by(desc("count"))
            .all()
        )

        return [
            MetricsByCategory(category=r.category, count=r.count)
            for r in results
        ]

    @staticmethod
    def get_metrics_by_country(db: Session) -> List[MetricsByCategory]:
        """Obtiene cantidad de registros por país"""
        results = (
            db.query(
                func.coalesce(Waitlist.country, "Unknown").label("category"),
                func.count(Waitlist.id).label("count")
            )
            .group_by("category")
            .order_by(desc("count"))
            .limit(10)  # Top 10 países
            .all()
        )

        return [
            MetricsByCategory(category=r.category, count=r.count)
            for r in results
        ]

    @staticmethod
    def get_top_emails(db: Session, limit: int = 10) -> List[TopEmail]:
        """Obtiene los emails con más intentos de registro"""
        results = (
            db.query(
                Waitlist.email,
                Waitlist.registration_count
            )
            .filter(Waitlist.registration_count > 1)
            .order_by(desc(Waitlist.registration_count))
            .limit(limit)
            .all()
        )

        return [
            TopEmail(email=r.email, registration_count=r.registration_count)
            for r in results
        ]

    @staticmethod
    def get_latest_by_type(db: Session) -> List[LatestByType]:
        """Obtiene el último registro de cada tipo de usuario"""
        # Subquery para obtener el ID del más reciente por tipo
        subquery = (
            db.query(
                Waitlist.user_type,
                func.max(Waitlist.id).label("max_id")
            )
            .group_by(Waitlist.user_type)
            .subquery()
        )

        results = (
            db.query(Waitlist)
            .join(
                subquery,
                (Waitlist.user_type == subquery.c.user_type) &
                (Waitlist.id == subquery.c.max_id)
            )
            .all()
        )

        return [
            LatestByType(
                user_type=str(r.user_type),
                email=r.email,
                created_at=r.created_at,
                registration_count=r.registration_count
            )
            for r in results
        ]

    @staticmethod
    def get_total_attempts(db: Session) -> int:
        """Obtiene el total de intentos de registro (suma de registration_count)"""
        result = db.query(func.sum(Waitlist.registration_count)).scalar()
        return result or 0

