"""
Schemas Pydantic para validación de datos
- WaitlistCreate: entrada del endpoint POST
- WaitlistResponse: respuesta exitosa
- HealthResponse: respuesta del health check
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from enum import Enum


class UserType(str, Enum):
    """Tipos de usuario (mirror del modelo)"""
    STUDENT = "student"
    COMPANY = "company"
    UNIVERSITY = "university"


class TrafficSourceExplicit(str, Enum):
    """Fuentes de tráfico explícitas permitidas desde frontend"""
    INSTAGRAM = "instagram"
    FACEBOOK = "facebook"
    TIKTOK = "tiktok"
    LINKEDIN = "linkedin"
    GOOGLE = "google"
    WHATSAPP = "whatsapp"
    OTHER = "other"


class WaitlistCreate(BaseModel):
    """Schema para crear registro en waitlist"""
    email: EmailStr = Field(..., description="Email del usuario")
    user_type: UserType = Field(..., description="Tipo de usuario")
    product_of_interest: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Producto de interés",
        pattern="^[a-zA-Z0-9 áéíóúÁÉÍÓÚñÑ,.'-]+$"  # Prevenir XSS/SQL injection
    )
    source: Optional[str] = Field(
        None,
        max_length=100,
        description="Origen del tráfico (legacy, usar traffic_source_explicit)",
        pattern="^[a-zA-Z0-9 _-]+$"  # Solo alfanumérico
    )
    traffic_source_explicit: Optional[TrafficSourceExplicit] = Field(
        None,
        description="Fuente de tráfico explícita desde frontend (prioridad sobre detección automática)"
    )
    country: Optional[str] = Field(
        None,
        max_length=100,
        description="País del usuario",
        pattern="^[a-zA-Z ]+$"  # Solo letras
    )

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "user_type": "student",
                "product_of_interest": "PractiMatch Platform",
                "traffic_source_explicit": "instagram",  # Nuevo campo opcional
                "country": "Mexico"
            }
        }


class WaitlistResponse(BaseModel):
    """Schema para respuesta de registro"""
    success: bool
    message: str
    data: Optional[dict] = None

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Thank you for registering for this product of interest. We will notify you when it is ready.",
                "data": {
                    "email": "user@example.com",
                    "user_type": "student",
                    "registration_count": 1
                }
            }
        }


class HealthResponse(BaseModel):
    """Schema para health check"""
    status: str
    app_name: str
    version: str
    database: str

