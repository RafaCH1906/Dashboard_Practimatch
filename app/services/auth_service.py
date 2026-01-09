"""
Servicio de autenticación y JWT
Maneja login, tokens y verificación
"""
import logging
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.config import settings
from app.models.admin_user import AdminUser
from app.schemas.auth import TokenData

logger = logging.getLogger(__name__)

# Configuración de hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    """Servicio para autenticación y manejo de JWT"""

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verifica que el password coincida con el hash"""
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        """Genera hash de password"""
        return pwd_context.hash(password)

    @staticmethod
    def authenticate_admin(db: Session, email: str, password: str) -> Optional[AdminUser]:
        """
        Autentica un administrador

        Returns:
            AdminUser si las credenciales son válidas, None si no
        """
        admin = db.query(AdminUser).filter(AdminUser.email == email).first()

        if not admin:
            logger.warning(f"Login attempt with non-existent email: {email}")
            return None

        if not admin.is_active:
            logger.warning(f"Login attempt with inactive account: {email}")
            return None

        if not AuthService.verify_password(password, admin.hashed_password):
            logger.warning(f"Failed login attempt for: {email}")
            return None

        # Actualizar last_login
        admin.last_login = datetime.utcnow()
        db.commit()

        logger.info(f"Successful login: {email}")
        return admin

    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """
        Crea un JWT token

        Args:
            data: Datos a encodear en el token
            expires_delta: Tiempo de expiración personalizado

        Returns:
            JWT token string
        """
        to_encode = data.copy()

        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

        return encoded_jwt

    @staticmethod
    def decode_token(token: str) -> Optional[TokenData]:
        """
        Decodifica y valida un JWT token

        Returns:
            TokenData si el token es válido, None si no
        """
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
            email: str = payload.get("sub")
            user_id: int = payload.get("user_id")

            if email is None:
                return None

            return TokenData(email=email, user_id=user_id)

        except JWTError as e:
            logger.error(f"JWT decode error: {str(e)}")
            return None

    @staticmethod
    def create_admin_user(db: Session, email: str, password: str, full_name: Optional[str] = None) -> AdminUser:
        """
        Crea un nuevo usuario administrador

        SOLO para uso en scripts de setup, NO exponer como endpoint
        """
        hashed_password = AuthService.get_password_hash(password)

        admin = AdminUser(
            email=email,
            hashed_password=hashed_password,
            full_name=full_name,
            is_active=True
        )

        db.add(admin)
        db.commit()
        db.refresh(admin)

        logger.info(f"Admin user created: {email}")
        return admin
