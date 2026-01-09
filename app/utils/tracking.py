"""
Utilidades para tracking de usuarios
- Detección de dispositivo desde User-Agent
- Geolocalización desde IP
- Detección de origen de tráfico
"""
import httpx
import logging
from typing import Optional, Dict
from user_agents import parse

logger = logging.getLogger(__name__)


class DeviceDetector:
    """Detecta el tipo de dispositivo desde User-Agent"""

    @staticmethod
    def detect(user_agent: str) -> str:
        """
        Clasifica el dispositivo como: mobile | desktop | tablet

        Args:
            user_agent: String del User-Agent del request

        Returns:
            str: mobile, desktop, tablet o unknown
        """
        if not user_agent:
            return "unknown"

        try:
            ua = parse(user_agent)

            if ua.is_mobile:
                return "mobile"
            elif ua.is_tablet:
                return "tablet"
            elif ua.is_pc:
                return "desktop"
            else:
                return "unknown"
        except Exception as e:
            logger.warning(f"Error parsing user agent: {e}")
            return "unknown"


class GeoLocationService:
    """
    Servicio de geolocalización basado en IP
    Usa ipapi.co (gratuito, 30k requests/mes)
    """

    BASE_URL = "https://ipapi.co"
    TIMEOUT = 3  # segundos

    @staticmethod
    def get_client_ip(request) -> Optional[str]:
        """
        Obtiene la IP real del cliente
        Compatible con Render y otros proxies (X-Forwarded-For)

        Args:
            request: FastAPI Request object

        Returns:
            str: IP del cliente o None
        """
        # Render y la mayoría de proxies usan X-Forwarded-For
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            # X-Forwarded-For puede tener múltiples IPs: "client, proxy1, proxy2"
            # La primera es la IP real del cliente
            return forwarded_for.split(",")[0].strip()

        # Fallback a X-Real-IP
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip.strip()

        # Fallback a IP directa (desarrollo local)
        if hasattr(request.client, "host"):
            return request.client.host

        return None

    @staticmethod
    async def get_location(ip: str) -> Dict[str, Optional[str]]:
        """
        Obtiene la ubicación geográfica de una IP

        Args:
            ip: Dirección IP

        Returns:
            dict: {"country": "MX", "city": "Mexico City"} o valores None si falla
        """
        # IPs locales no se pueden geolocalizar
        if not ip or ip in ["127.0.0.1", "localhost", "::1"]:
            logger.debug("Skipping geolocation for local IP")
            return {"country": None, "city": None}

        try:
            async with httpx.AsyncClient(timeout=GeoLocationService.TIMEOUT) as client:
                response = await client.get(
                    f"{GeoLocationService.BASE_URL}/{ip}/json/",
                    headers={"User-Agent": "PractiMatch-Waitlist/1.0"}
                )

                if response.status_code == 200:
                    data = response.json()

                    # ipapi.co retorna "error": true si la IP es inválida
                    if data.get("error"):
                        logger.warning(f"IP geolocation error: {data.get('reason')}")
                        return {"country": None, "city": None}

                    country = data.get("country_code")  # ISO code: MX, US, etc.
                    city = data.get("city")

                    logger.info(f"Geolocation success: {ip} -> {city}, {country}")
                    return {"country": country, "city": city}
                else:
                    logger.warning(f"Geolocation API returned {response.status_code}")
                    return {"country": None, "city": None}

        except httpx.TimeoutException:
            logger.warning(f"Geolocation timeout for IP: {ip}")
            return {"country": None, "city": None}
        except Exception as e:
            logger.error(f"Geolocation error: {e}")
            return {"country": None, "city": None}


class TrafficSourceDetector:
    """Detecta el origen del tráfico desde el Referer"""

    @staticmethod
    def detect(referer: Optional[str], source_from_frontend: Optional[str]) -> str:
        """
        Detecta el origen del tráfico

        Prioridad:
        1. source enviado por frontend (retrocompatibilidad)
        2. Referer header (inferido)
        3. "direct" (por defecto)

        Args:
            referer: Header Referer del request
            source_from_frontend: Campo source enviado por frontend

        Returns:
            str: Origen del tráfico (ej: "instagram", "direct", "google")
        """
        # 1. Si frontend envía source explícito, usarlo (retrocompatibilidad)
        if source_from_frontend:
            return source_from_frontend.lower()

        # 2. Si no hay referer = tráfico directo
        if not referer:
            return "direct"

        # 3. Extraer dominio del referer
        referer_lower = referer.lower()

        # Mapeo de dominios conocidos
        if "instagram.com" in referer_lower:
            return "instagram"
        elif "facebook.com" in referer_lower or "fb.com" in referer_lower:
            return "facebook"
        elif "twitter.com" in referer_lower or "t.co" in referer_lower:
            return "twitter"
        elif "linkedin.com" in referer_lower:
            return "linkedin"
        elif "tiktok.com" in referer_lower:
            return "tiktok"
        elif "google." in referer_lower:
            return "google_search"
        elif "youtube.com" in referer_lower:
            return "youtube"
        elif "whatsapp" in referer_lower:
            return "whatsapp"
        else:
            # Extraer dominio base
            try:
                from urllib.parse import urlparse
                parsed = urlparse(referer)
                domain = parsed.netloc or parsed.path
                # Limpiar www.
                domain = domain.replace("www.", "")
                return f"referral_{domain}"
            except:
                return "unknown_referral"

