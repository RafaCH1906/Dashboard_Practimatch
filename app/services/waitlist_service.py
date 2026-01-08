"""
Lógica de negocio para la waitlist
Separa la lógica de los endpoints para mejor testabilidad
"""
from sqlalchemy.orm import Session

from app.models.waitlist import Waitlist, UserTypeEnum
from app.schemas.waitlist import WaitlistCreate


class WaitlistService:
    """Servicio para gestionar operaciones de waitlist"""

    @staticmethod
    def get_by_email(db: Session, email: str) -> Waitlist | None:
        """Busca un registro por email"""
        return db.query(Waitlist).filter(Waitlist.email == email).first()

    @staticmethod
    def create_or_increment(db: Session, waitlist_data: WaitlistCreate) -> tuple[Waitlist, bool]:
        """
        Crea un nuevo registro o incrementa el contador si ya existe

        Returns:
            tuple: (Waitlist object, is_new: bool)
            - is_new=True: registro nuevo creado
            - is_new=False: registro existente actualizado
        """
        # Verificar si el email ya existe
        existing = WaitlistService.get_by_email(db, waitlist_data.email)

        if existing:
            # Email duplicado: incrementar contador
            existing.registration_count += 1
            existing.source = waitlist_data.source or existing.source
            existing.country = waitlist_data.country or existing.country
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
            country=waitlist_data.country
        )
        db.add(new_waitlist)
        db.commit()
        db.refresh(new_waitlist)
        return new_waitlist, True

    @staticmethod
    def count_total_registrations(db: Session) -> int:
        """Cuenta total de registros únicos"""
        return db.query(Waitlist).count()


