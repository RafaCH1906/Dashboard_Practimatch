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

    # Tracking avanzado (inferido desde backend)
    city = Column(String(100), nullable=True)  # Ciudad detectada desde IP
    device_type = Column(String(20), nullable=True)  # mobile | desktop | tablet
    traffic_source = Column(String(100), nullable=True)  # Origen inferido desde Referer O explícito desde frontend
    traffic_source_type = Column(String(20), nullable=True)  # "explicit" | "detected" (indica el origen del traffic_source)
    user_agent = Column(String(500), nullable=True)  # User-Agent completo (para debugging)
    ip_address = Column(String(45), nullable=True)  # IPv4 o IPv6

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Índices compuestos para mejorar performance de queries
    __table_args__ = (
        Index('idx_waitlist_filters', 'user_type', 'created_at'),
        Index('idx_waitlist_source', 'source'),
        Index('idx_waitlist_country', 'country'),
        Index('idx_waitlist_city', 'city'),
        Index('idx_waitlist_device', 'device_type'),
        Index('idx_waitlist_traffic', 'traffic_source'),
        Index('idx_waitlist_traffic_type', 'traffic_source_type'),
    )

    def __repr__(self):
        return f"<Waitlist(email={self.email}, user_type={self.user_type}, count={self.registration_count})>"

