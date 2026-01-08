"""
Configuración de logging para la aplicación
"""
import logging
import sys
from datetime import datetime


def setup_logging(log_level: str = "INFO"):
    """
    Configura el sistema de logging

    Args:
        log_level: Nivel de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    # Formato estructurado
    log_format = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    # Configurar root logger
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format=log_format,
        datefmt=date_format,
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )

    # Configurar loggers específicos
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("fastapi").setLevel(logging.INFO)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)  # Menos verbose en SQL

    return logging.getLogger(__name__)


# Logger global
logger = logging.getLogger(__name__)

