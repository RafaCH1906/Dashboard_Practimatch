"""
Configuración de SQLAlchemy
- Engine: conexión a PostgreSQL
- SessionLocal: factory para sesiones
- Base: clase base para modelos ORM
- get_db: dependency para FastAPI
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import settings

# Motor de base de datos
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,  # Verifica conexiones antes de usarlas
    echo=settings.ENVIRONMENT == "development"  # Log SQL en dev
)

# Factory de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Clase base para modelos
Base = declarative_base()


def get_db():
    """
    Dependency para obtener sesión de DB en endpoints
    Se cierra automáticamente al finalizar la request
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Inicializa la base de datos creando todas las tablas
    Solo para desarrollo - en producción usar Alembic
    """
    from app.models import waitlist  # Import para registrar modelos
    Base.metadata.create_all(bind=engine)

