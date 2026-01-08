"""
Configuración centralizada usando Pydantic Settings
Lee variables de entorno desde .env o sistema
"""
from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Configuración de la aplicación"""

    # Database
    DATABASE_URL: str = Field(
        default="postgresql://user:password@localhost:5432/practi_waitlist",
        description="PostgreSQL connection string"
    )

    # App
    ENVIRONMENT: str = Field(default="development")
    APP_NAME: str = Field(default="PractiMatch Waitlist API")
    VERSION: str = Field(default="1.0.0")

    # CORS
    ALLOWED_ORIGINS: str = Field(
        default="http://localhost:3000,http://localhost:5173",
        description="Comma-separated list of allowed origins"
    )

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = Field(default=10)

    # Logging
    LOG_LEVEL: str = Field(default="INFO")

    def get_origins_list(self) -> List[str]:
        """Convierte string de origins a lista"""
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]

    class Config:
        env_file = ".env"
        case_sensitive = True


# Singleton de configuración
settings = Settings()

