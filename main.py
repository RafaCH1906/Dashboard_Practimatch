"""
PractiMatch Waitlist API - Entry Point
FastAPI application con endpoints de waitlist y health check
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.config import settings
from app.db.database import init_db
from app.api.routes import health, waitlist, admin, auth

# Configurar rate limiter
limiter = Limiter(key_func=get_remote_address)

# Crear instancia de FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="API para gestión de waitlist con tracking de tráfico y métricas"
)

# Agregar rate limiter a la app
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Configurar CORS (ajustar origins en producción)
allowed_origins = ["*"] if settings.ENVIRONMENT == "development" else settings.get_origins_list()

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
    max_age=3600,  # Cache preflight requests por 1 hora
)


# Event handlers
@app.on_event("startup")
async def startup_event():
    """
    Inicializa la base de datos al arrancar
    Crea todas las tablas si no existen
    """
    init_db()
    print(f"✅ {settings.APP_NAME} iniciado")
    print(f"📊 Base de datos: {settings.DATABASE_URL.split('@')[1] if '@' in settings.DATABASE_URL else 'configured'}")


# Registrar rutas con prefijo /api
app.include_router(health.router, prefix="/api", tags=["Health"])
app.include_router(waitlist.router, prefix="/api", tags=["Waitlist"])
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])


# Root endpoint (opcional, para verificación rápida)
@app.get("/", tags=["Root"])
async def root():
    """Endpoint raíz - redirige a /docs para documentación"""
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "docs": "/docs",
        "health": "/api/health"
    }
