"""
Waitlist endpoints
POST /api/waitlist: registro de usuarios en la waitlist
"""
import logging
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.db.database import get_db
from app.schemas.waitlist import WaitlistCreate, WaitlistResponse
from app.services.waitlist_service import WaitlistService

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)
logger = logging.getLogger(__name__)


@router.post(
    "/waitlist",
    response_model=WaitlistResponse,
    status_code=status.HTTP_201_CREATED,
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

    **Validaciones:**
    - Email válido (validado por Pydantic)
    - User type debe ser: student | company | university
    - Product of interest requerido
    """
    try:
        # Log del intento de registro
        logger.info(f"Waitlist registration attempt: {waitlist_data.email}")

        # Crear o incrementar contador
        waitlist, is_new = WaitlistService.create_or_increment(db, waitlist_data)

        # Log del resultado
        if is_new:
            logger.info(f"New registration: {waitlist.email} | count=1")
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
                "is_new_registration": is_new
            }
        )

        # Cambiar status code si es registro duplicado
        if not is_new:
            # Retornar 200 en lugar de 201 para duplicados
            return response

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

