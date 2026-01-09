"""
Middleware y dependencies para autenticación JWT
"""
import logging
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.auth_service import AuthService
from app.models.admin_user import AdminUser

logger = logging.getLogger(__name__)

# Security scheme para Swagger
security = HTTPBearer()


async def get_current_admin(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> AdminUser:
    """
    Dependency para obtener el admin actual desde el JWT token

    Uso:
        @router.get("/protected")
        async def protected_route(admin: AdminUser = Depends(get_current_admin)):
            return {"admin_email": admin.email}

    Raises:
        HTTPException 401: Si el token es inválido o el usuario no existe
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decodificar token
        token_data = AuthService.decode_token(credentials.credentials)

        if token_data is None or token_data.email is None:
            raise credentials_exception

        # Buscar admin en DB
        admin = db.query(AdminUser).filter(AdminUser.email == token_data.email).first()

        if admin is None:
            logger.warning(f"Token valid but user not found: {token_data.email}")
            raise credentials_exception

        if not admin.is_active:
            logger.warning(f"Inactive user attempted access: {token_data.email}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Inactive user"
            )

        return admin

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Auth middleware error: {str(e)}")
        raise credentials_exception

