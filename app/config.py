"""
Configuración centralizada usando Pydantic Settings
Lee variables de entorno desde .env o sistema
"""
from typing import List, Literal
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator


class Settings(BaseSettings):
    """Configuración de la aplicación"""

    # Database
    DATABASE_URL: str = Field(
        default="postgresql://user:password@localhost:5432/practi_waitlist",
        description="PostgreSQL connection string"
    )

    # App
    ENVIRONMENT: Literal["development", "production", "staging"] = Field(
        default="development"
    )
    APP_NAME: str = Field(default="PractiMatch Waitlist API")
    VERSION: str = Field(default="1.0.0")

    # JWT Authentication
    SECRET_KEY: str = Field(
        default="your-secret-key-change-this-in-production",
        min_length=32,
        description="Secret key para JWT tokens (mínimo 32 caracteres)"
    )
    JWT_ALGORITHM: str = Field(default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=480, gt=0)

    # Admin User (para create_admin.py)
    ADMIN_EMAIL: str = Field(
        default="admin@practimatch.com",
        description="Email del administrador por defecto"
    )
    ADMIN_PASSWORD: str = Field(
        default="change-this-secure-password-123",
        min_length=8,
        description="Password del administrador por defecto (mínimo 8 caracteres)"
    )

    # CORS
    ALLOWED_ORIGINS: str = Field(
        default="http://localhost:3000,http://localhost:5173",
        description="Comma-separated list of allowed origins"
    )

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = Field(default=10, gt=0, le=100)

    # Logging
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        default="INFO"
    )

    # Configuración de Pydantic v2
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"  # Ignorar variables de entorno no definidas
    )

    @field_validator("SECRET_KEY")
    @classmethod
    def validate_secret_key(cls, v: str, info) -> str:
        """Valida que SECRET_KEY sea lo suficientemente seguro en producción"""
        if v == "your-secret-key-change-this-in-production":
            # Obtener el environment desde los valores ya parseados
            env = info.data.get("ENVIRONMENT", "development")

            if env == "production":
                raise ValueError(
                    "⚠️ CRITICAL: Cannot use default SECRET_KEY in production! "
                    "Set a secure SECRET_KEY in environment variables."
                )
            else:
                # Solo advertir en desarrollo
                import warnings
                warnings.warn(
                    "⚠️  Usando SECRET_KEY por defecto. CAMBIA ESTO EN PRODUCCIÓN!",
                    UserWarning
                )
        return v

    def get_origins_list(self) -> List[str]:
        """Convierte string de origins a lista"""
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]

    def is_production(self) -> bool:
        """Verifica si está en modo producción"""
        return self.ENVIRONMENT == "production"

    def is_development(self) -> bool:
        """Verifica si está en modo desarrollo"""
        return self.ENVIRONMENT == "development"


# Singleton de configuración
settings = Settings()
