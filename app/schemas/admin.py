"""
Schemas Pydantic para endpoints administrativos
"""
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class UserTypeFilter(str, Enum):
    """Enum para filtrar por tipo de usuario"""
    STUDENT = "student"
    COMPANY = "company"
    UNIVERSITY = "university"


class WaitlistItemAdmin(BaseModel):
    """Schema para un item de waitlist (admin view)"""
    id: int
    email: str
    user_type: str
    product_of_interest: str
    registration_count: int
    source: Optional[str] = None
    country: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class PaginatedWaitlistResponse(BaseModel):
    """Schema para respuesta paginada de waitlist"""
    total: int = Field(..., description="Total de registros")
    page: int = Field(..., description="Página actual")
    limit: int = Field(..., description="Registros por página")
    pages: int = Field(..., description="Total de páginas")
    items: List[WaitlistItemAdmin] = Field(..., description="Lista de registros")

    class Config:
        json_schema_extra = {
            "example": {
                "total": 150,
                "page": 1,
                "limit": 20,
                "pages": 8,
                "items": [
                    {
                        "id": 1,
                        "email": "student@example.com",
                        "user_type": "student",
                        "product_of_interest": "PractiMatch Platform",
                        "registration_count": 2,
                        "source": "Instagram",
                        "country": "Mexico",
                        "created_at": "2026-01-08T10:00:00Z",
                        "updated_at": "2026-01-08T11:00:00Z"
                    }
                ]
            }
        }


class MetricsByCategory(BaseModel):
    """Schema para métricas por categoría"""
    category: str
    count: int


class TopEmail(BaseModel):
    """Schema para top emails"""
    email: str
    registration_count: int


class LatestByType(BaseModel):
    """Schema para último registro por tipo"""
    user_type: str
    email: str
    created_at: datetime
    registration_count: int


class MetricsResponse(BaseModel):
    """Schema para respuesta de métricas agregadas"""
    total_registrations: int = Field(..., description="Total de registros únicos")
    total_attempts: int = Field(..., description="Total de intentos de registro")

    by_user_type: List[MetricsByCategory] = Field(..., description="Registros por tipo de usuario")
    by_source: List[MetricsByCategory] = Field(..., description="Registros por fuente")
    by_country: List[MetricsByCategory] = Field(..., description="Registros por país")

    top_emails: List[TopEmail] = Field(..., description="Top 10 emails con más intentos")
    latest_by_type: List[LatestByType] = Field(..., description="Último registro por tipo")

    class Config:
        json_schema_extra = {
            "example": {
                "total_registrations": 150,
                "total_attempts": 285,
                "by_user_type": [
                    {"category": "student", "count": 100},
                    {"category": "company", "count": 30},
                    {"category": "university", "count": 20}
                ],
                "by_source": [
                    {"category": "Instagram", "count": 80},
                    {"category": "Facebook", "count": 40},
                    {"category": "Direct", "count": 30}
                ],
                "by_country": [
                    {"category": "Mexico", "count": 90},
                    {"category": "Colombia", "count": 35},
                    {"category": "Unknown", "count": 25}
                ],
                "top_emails": [
                    {"email": "user@example.com", "registration_count": 5}
                ],
                "latest_by_type": [
                    {
                        "user_type": "student",
                        "email": "recent@example.com",
                        "created_at": "2026-01-08T14:30:00Z",
                        "registration_count": 1
                    }
                ]
            }
        }

