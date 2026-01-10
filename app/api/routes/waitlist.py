"""
Waitlist endpoints
POST /api/waitlist: registro de usuarios en la waitlist
"""
import logging
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.db.database import get_db
from app.schemas.waitlist import WaitlistCreate, WaitlistResponse
from app.services.waitlist_service import WaitlistService
from app.utils.tracking import DeviceDetector, GeoLocationService, TrafficSourceDetector

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)
logger = logging.getLogger(__name__)


@router.post(
    "/waitlist",
    response_model=WaitlistResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        200: {"description": "Email already registered, counter incremented"},
        201: {"description": "New registration created"}
    },
    tags=["Waitlist"]
)
@limiter.limit("10/minute")  # Máximo 10 registros por minuto por IP
async def register_waitlist(
    request: Request,
    waitlist_data: WaitlistCreate,
    db: Session = Depends(get_db)
):
    """
    Registra un usuario en la waitlist

    **Lógica:**
    - Si el email es nuevo: crea registro con count=1, retorna 201
    - Si el email existe: incrementa count, retorna 200

    **Tracking automático (NO requiere envío desde frontend):**
    - Dispositivo: Detectado desde User-Agent
    - Ciudad/País: Detectado desde IP (geolocalización)
    - Origen: Detectado desde Referer

    **Validaciones:**
    - Email válido (validado por Pydantic)
    - User type debe ser: student | company | university
    - Product of interest requerido
    """
    try:
        # Log del intento de registro
        logger.info(f"Waitlist registration attempt: {waitlist_data.email}")

        # ========================================
        # TRACKING AUTOMÁTICO
        # ========================================

        # 1. Detectar dispositivo desde User-Agent
        user_agent = request.headers.get("User-Agent", "")
        device_type = DeviceDetector.detect(user_agent)

        # 2. Obtener IP real y geolocalizar
        client_ip = GeoLocationService.get_client_ip(request)
        geo_data = await GeoLocationService.get_location(client_ip) if client_ip else {"country": None, "city": None}

        # 3. Detectar origen de tráfico CON LÓGICA DE PRIORIDAD
        # Prioridad: traffic_source_explicit > Referer detectado > "direct"
        referer = request.headers.get("Referer") or request.headers.get("Referrer")
        traffic_source_detected = TrafficSourceDetector.detect(referer, waitlist_data.source)

        # Aplicar lógica de prioridad
        if waitlist_data.traffic_source_explicit:
            # Frontend envió explícitamente la fuente
            traffic_source_final = waitlist_data.traffic_source_explicit.value
            traffic_source_type = "explicit"
            logger.info(f"Using explicit traffic source: {traffic_source_final}")
        else:
            # Usar detección automática
            traffic_source_final = traffic_source_detected
            traffic_source_type = "detected"
            logger.info(f"Using detected traffic source: {traffic_source_final}")

        # Usar país detectado si frontend no envió
        country = waitlist_data.country or geo_data.get("country")
        city = geo_data.get("city")

        logger.info(f"Tracking: device={device_type}, city={city}, country={country}, traffic={traffic_source_final} ({traffic_source_type}), ip={client_ip}")

        # ========================================
        # CREAR O ACTUALIZAR REGISTRO
        # ========================================

        # Crear o incrementar contador con datos de tracking
        waitlist, is_new = WaitlistService.create_or_increment(
            db=db,
            waitlist_data=waitlist_data,
            # Pasar datos de tracking
            device_type=device_type,
            city=city,
            traffic_source=traffic_source_final,
            traffic_source_type=traffic_source_type,
            user_agent=user_agent[:500] if user_agent else None,  # Limitar a 500 chars
            ip_address=client_ip
        )

        # Log del resultado
        if is_new:
            logger.info(f"New registration: {waitlist.email} | count=1 | device={device_type} | city={city}")
        else:
            logger.info(f"Duplicate registration: {waitlist.email} | count={waitlist.registration_count}")

        # Mensaje de respuesta
        message = "Thank you for registering for this product of interest. We will notify you when it is ready."

        # Manejar user_type que puede ser Enum o string desde DB
        user_type_value = waitlist.user_type.value if hasattr(waitlist.user_type, 'value') else str(waitlist.user_type)

        response = WaitlistResponse(
            success=True,
            message=message,
            data={
                "email": waitlist.email,
                "user_type": user_type_value,
                "product_of_interest": waitlist.product_of_interest,
                "registration_count": waitlist.registration_count,
                "is_new_registration": is_new,
                # Tracking data (opcional en respuesta, frontend puede ignorar)
                "device_type": waitlist.device_type,
                "city": waitlist.city,
                "country": waitlist.country,
                "traffic_source": waitlist.traffic_source,
                "created_at": waitlist.created_at.isoformat() if waitlist.created_at else None,
                "updated_at": waitlist.updated_at.isoformat() if waitlist.updated_at else None
            }
        )

        # Retornar 200 para duplicados, 201 para nuevos
        if not is_new:
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=response.model_dump()
            )

        return response

    except ValueError as e:
        # Error de validación de datos
        logger.warning(f"Validation error for {waitlist_data.email}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid data format: {str(e)}"
        )
    except Exception as e:
        # Log del error real
        logger.error(f"Error processing registration for {waitlist_data.email}: {str(e)}", exc_info=True)

        # Mensaje genérico al usuario (no exponer detalles internos)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while processing your registration. Please try again later."
        )

