# PractiMatch Waitlist API

Backend para gestión de waitlist con FastAPI + PostgreSQL.

## 🎯 Características

- ✅ Registro de usuarios en waitlist (email, tipo, producto de interés)
- ✅ Detección de emails duplicados con contador de intentos
- ✅ Tracking de tráfico (source, country)
- ✅ Validación con Pydantic
- ✅ Respuestas tipadas
- ✅ Health check endpoint
- ✅ CORS configurado

## 📁 Estructura del Proyecto

```
PractiMatch_Back/
├── app/
│   ├── __init__.py
│   ├── config.py              # Configuración con Pydantic Settings
│   ├── db/
│   │   ├── __init__.py
│   │   └── database.py        # SQLAlchemy setup
│   ├── models/
│   │   ├── __init__.py
│   │   └── waitlist.py        # Modelo Waitlist ORM
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── waitlist.py        # Schemas Pydantic
│   ├── services/
│   │   ├── __init__.py
│   │   └── waitlist_service.py # Lógica de negocio
│   └── api/
│       ├── __init__.py
│       └── routes/
│           ├── __init__.py
│           ├── health.py      # GET /api/health
│           └── waitlist.py    # POST /api/waitlist
├── main.py                    # Entry point FastAPI
├── requirements.txt
├── .env.example
├── .env
└── test_main.http            # Tests HTTP
```

## 🚀 Setup

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Configurar PostgreSQL

Crear la base de datos:

```sql
CREATE DATABASE practi_waitlist;
```

### 3. Configurar variables de entorno

Editar el archivo `.env` con tus credenciales de PostgreSQL:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/practi_waitlist
ENVIRONMENT=development
```

### 4. Ejecutar la aplicación

```bash
uvicorn main:app --reload
```

La API estará disponible en: `http://127.0.0.1:8000`

## 📚 Documentación API

FastAPI genera documentación interactiva automáticamente:

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

## 🔗 Endpoints

### GET `/api/health`

Health check - verifica que la API y la base de datos estén funcionando.

**Response:**
```json
{
  "status": "healthy",
  "app_name": "PractiMatch Waitlist API",
  "version": "1.0.0",
  "database": "connected"
}
```

### POST `/api/waitlist`

Registra un usuario en la waitlist.

**Request Body:**
```json
{
  "email": "user@example.com",
  "user_type": "student",  // student | company | university
  "product_of_interest": "PractiMatch Platform",
  "source": "Instagram",   // opcional
  "country": "Mexico"      // opcional
}
```

**Response (nuevo registro):**
```json
{
  "success": true,
  "message": "Thank you for registering for this product of interest. We will notify you when it is ready.",
  "data": {
    "email": "user@example.com",
    "user_type": "student",
    "product_of_interest": "PractiMatch Platform",
    "registration_count": 1,
    "is_new_registration": true
  }
}
```

**Response (email duplicado):**
```json
{
  "success": true,
  "message": "Thank you for registering for this product of interest. We will notify you when it is ready.",
  "data": {
    "email": "user@example.com",
    "user_type": "student",
    "product_of_interest": "PractiMatch Platform",
    "registration_count": 2,
    "is_new_registration": false
  }
}
```

## 🗄️ Modelo de Datos

### Tabla: `waitlist`

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | Integer | Primary key |
| `email` | String(255) | Email único (indexed) |
| `user_type` | Enum | student \| company \| university |
| `product_of_interest` | String(255) | Producto de interés |
| `registration_count` | Integer | Contador de intentos de registro |
| `source` | String(100) | Origen del tráfico (opcional) |
| `country` | String(100) | País del usuario (opcional) |
| `created_at` | DateTime | Timestamp de creación |
| `updated_at` | DateTime | Timestamp de última actualización |

## 🧪 Testing

Usar el archivo `test_main.http` con la extensión REST Client de VS Code o IntelliJ HTTP Client.

## 🔧 Decisiones Técnicas

### ✅ Por qué esta estructura?

1. **Separación de responsabilidades**: 
   - `models/`: definición de tablas
   - `schemas/`: validación de entrada/salida
   - `services/`: lógica de negocio
   - `api/routes/`: endpoints HTTP

2. **SQLAlchemy ORM**: 
   - Abstracción de base de datos
   - Type safety
   - Migraciones futuras con Alembic

3. **Pydantic**: 
   - Validación automática
   - Documentación OpenAPI
   - Type hints

4. **Dependency Injection**: 
   - `get_db()` como dependency
   - Cierre automático de sesiones

5. **Base.metadata.create_all()**: 
   - Simple para desarrollo
   - Sin Alembic en STEP 1
   - Fácil de migrar después

### 🔐 Seguridad

- **Rate Limiting**: 10 requests/minuto por IP (slowapi)
- **Input Sanitization**: Regex patterns para prevenir XSS/SQL injection
- **Error Handling**: Mensajes genéricos, no expone internals
- **CORS**: Configurable por environment
- **Logging**: Estructurado con niveles INFO/WARNING/ERROR

### 🔄 Lógica de Duplicados

- Email duplicado → incrementa `registration_count`
- Actualiza `source` y `country` si se proveen
- Mismo mensaje de éxito (UX consistente)
- Campo `is_new_registration` indica si es nuevo

## 📝 TODO (STEP 2+)

- [ ] Admin dashboard con autenticación JWT
- [ ] Paginación en endpoints
- [ ] Métricas agregadas (count by user_type, source, country)
- [ ] Alembic para migraciones
- [ ] Tests unitarios (pytest)
- [ ] Rate limiting
- [ ] Logging estructurado

## 📦 Stack

- **FastAPI** 0.109.0
- **SQLAlchemy** 2.0.25
- **PostgreSQL** (psycopg2-binary)
- **Pydantic Settings** 2.1.0
- **Uvicorn** 0.27.0

---

**Autor**: PractiMatch Team  
**Version**: 1.0.0 (STEP 1)

