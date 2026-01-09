"""
Rutas de autenticación
Login y gestión de tokens JWT
"""
import logging
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.config import settings
from app.db.database import get_db
from app.services.auth_service import AuthService
from app.schemas.auth import AdminLogin, Token, AdminUser as AdminUserSchema
from app.middleware.auth import get_current_admin
from app.models.admin_user import AdminUser

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post(
    "/login",
    response_model=Token,
    tags=["Auth"],
    summary="Login de administrador"
)
async def login(
    login_data: AdminLogin,
    db: Session = Depends(get_db)
):
    """
    **Login para administradores**

    - Autentica con email y password
    - Retorna JWT token para acceder a rutas protegidas
    - Token válido por 8 horas (configurable)

    **Uso del token:**
    ```
    Headers: {
        "Authorization": "Bearer <access_token>"
    }
    ```

    **Códigos de error:**
    - 401: Credenciales inválidas o usuario inactivo
    """
    # Autenticar admin
    admin = AuthService.authenticate_admin(
        db=db,
        email=login_data.email,
        password=login_data.password
    )

    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Crear token JWT
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = AuthService.create_access_token(
        data={"sub": admin.email, "user_id": admin.id},
        expires_delta=access_token_expires
    )

    logger.info(f"Token generated for admin: {admin.email}")

    return Token(access_token=access_token, token_type="bearer")


@router.get(
    "/me",
    response_model=AdminUserSchema,
    tags=["Auth"],
    summary="Obtener información del admin actual"
)
async def get_current_user_info(
    admin: AdminUser = Depends(get_current_admin)
):
    """
    **Obtiene información del administrador autenticado**

    - Requiere token JWT válido
    - Útil para verificar autenticación
    - Retorna datos del perfil (sin password)
    """
    return admin


@router.post(
    "/refresh",
    response_model=Token,
    tags=["Auth"],
    summary="Renovar token JWT"
)
async def refresh_token(
    admin: AdminUser = Depends(get_current_admin)
):
    """
    **Renueva el token JWT antes de expiración**

    - Requiere token JWT válido actual
    - Genera un nuevo token con tiempo completo de expiración
    - Útil para mantener sesiones largas sin interrupciones

    **Uso recomendado**:
    - Frontend debe llamar este endpoint periódicamente (ej: cada 7 horas)
    - O cuando detecte que el token está próximo a expirar

    **Ejemplo**:
    ```javascript
    // Renovar token cada 7 horas
    setInterval(async () => {
        const newToken = await fetch('/api/auth/refresh', {
            headers: { Authorization: `Bearer ${currentToken}` }
        });
    }, 7 * 60 * 60 * 1000);
    ```
    """
    # Generar nuevo token con tiempo completo
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = AuthService.create_access_token(
        data={"sub": admin.email, "user_id": admin.id},
        expires_delta=access_token_expires
    )

    logger.info(f"Token refreshed for admin: {admin.email}")

    return Token(access_token=access_token, token_type="bearer")



