"""
Modelo ORM para la tabla Waitlist
Representa registros de usuarios en la waitlist
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLEnum, Index
from sqlalchemy.sql import func
import enum

from app.db.database import Base


class UserTypeEnum(str, enum.Enum):
    """Tipos de usuario permitidos"""
    STUDENT = "student"
    COMPANY = "company"
    UNIVERSITY = "university"


class Waitlist(Base):
    """
    Tabla de waitlist
    - email único como identificador principal
    - registration_count: cuántas veces intentó registrarse
    - source: origen del tráfico (Instagram, Facebook, etc.)
    - country: país del usuario (opcional, enviado desde frontend)
    """
    __tablename__ = "waitlist"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    user_type = Column(SQLEnum(UserTypeEnum), nullable=False)
    product_of_interest = Column(String(255), nullable=False)
    registration_count = Column(Integer, default=1, nullable=False)

    # Tracking de tráfico
    source = Column(String(100), nullable=True)  # Instagram, Facebook, TikTok, Direct
    country = Column(String(100), nullable=True)  # Opcional desde frontend

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Índices compuestos para mejorar performance de queries
    __table_args__ = (
        Index('idx_waitlist_filters', 'user_type', 'created_at'),
        Index('idx_waitlist_source', 'source'),
        Index('idx_waitlist_country', 'country'),
    )

    def __repr__(self):
        return f"<Waitlist(email={self.email}, user_type={self.user_type}, count={self.registration_count})>"

