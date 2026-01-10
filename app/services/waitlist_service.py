"""
Lógica de negocio para la waitlist
Separa la lógica de los endpoints para mejor testabilidad
"""
from sqlalchemy.orm import Session
from typing import Optional

from app.models.waitlist import Waitlist, UserTypeEnum
from app.schemas.waitlist import WaitlistCreate


class WaitlistService:
    """Servicio para gestionar operaciones de waitlist"""

    @staticmethod
    def get_by_email(db: Session, email: str) -> Waitlist | None:
        """Busca un registro por email"""
        return db.query(Waitlist).filter(Waitlist.email == email).first()

    @staticmethod
    def create_or_increment(
        db: Session,
        waitlist_data: WaitlistCreate,
        # Nuevos parámetros opcionales para tracking
        device_type: Optional[str] = None,
        city: Optional[str] = None,
        traffic_source: Optional[str] = None,
        traffic_source_type: Optional[str] = None,  # "explicit" | "detected"
        user_agent: Optional[str] = None,
        ip_address: Optional[str] = None
    ) -> tuple[Waitlist, bool]:
        """
        Crea un nuevo registro o incrementa el contador si ya existe

        Args:
            db: Sesión de base de datos
            waitlist_data: Datos del formulario
            device_type: Tipo de dispositivo (mobile/desktop/tablet)
            city: Ciudad detectada
            traffic_source: Origen de tráfico (final, ya con prioridad aplicada)
            traffic_source_type: "explicit" si viene de frontend, "detected" si es automático
            user_agent: User-Agent completo
            ip_address: IP del cliente

        Returns:
            tuple: (Waitlist object, is_new: bool)
            - is_new=True: registro nuevo creado
            - is_new=False: registro existente actualizado
        """
        # Verificar si el email ya existe
        existing = WaitlistService.get_by_email(db, waitlist_data.email)

        if existing:
            # Email duplicado: incrementar contador y actualizar datos
            existing.registration_count += 1
            existing.source = waitlist_data.source or existing.source
            existing.country = waitlist_data.country or existing.country

            # Actualizar tracking avanzado (si viene info nueva)
            if device_type:
                existing.device_type = device_type
            if city:
                existing.city = city
            if traffic_source:
                existing.traffic_source = traffic_source
            if traffic_source_type:
                existing.traffic_source_type = traffic_source_type
            if user_agent:
                existing.user_agent = user_agent
            if ip_address:
                existing.ip_address = ip_address

            db.commit()
            db.refresh(existing)
            return existing, False

        # Nuevo registro
        new_waitlist = Waitlist(
            email=waitlist_data.email,
            user_type=UserTypeEnum(waitlist_data.user_type.value),
            product_of_interest=waitlist_data.product_of_interest,
            registration_count=1,
            source=waitlist_data.source,
            country=waitlist_data.country,
            # Tracking avanzado
            device_type=device_type,
            city=city,
            traffic_source=traffic_source,
            traffic_source_type=traffic_source_type,
            user_agent=user_agent,
            ip_address=ip_address
        )
        db.add(new_waitlist)
        db.commit()
        db.refresh(new_waitlist)
        return new_waitlist, True

    @staticmethod
    def count_total_registrations(db: Session) -> int:
        """Cuenta total de registros únicos"""
        return db.query(Waitlist).count()


