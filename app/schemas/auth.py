"""
Schemas Pydantic para autenticación
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class AdminLogin(BaseModel):
    """Schema para login de admin"""
    email: EmailStr = Field(..., description="Email del administrador")
    password: str = Field(..., min_length=6, description="Password del administrador")

    class Config:
        json_schema_extra = {
            "example": {
                "email": "admin@practimatch.com",
                "password": "secure_password123"
            }
        }


class Token(BaseModel):
    """Schema para respuesta de token JWT"""
    access_token: str
    token_type: str = "bearer"

    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer"
            }
        }


class TokenData(BaseModel):
    """Schema para datos dentro del token"""
    email: Optional[str] = None
    user_id: Optional[int] = None


class AdminUser(BaseModel):
    """Schema para usuario admin (sin password)"""
    id: int
    email: str
    full_name: Optional[str] = None
    is_active: bool
    created_at: datetime
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True

