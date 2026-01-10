# 🚀 PractiMatch Waitlist API

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**Backend API REST para gestión de waitlist pública con dashboard administrativo y tracking avanzado**

[🌐 App en Producción](https://practimatch-api.onrender.com/docs) | [📖 Documentación API](https://practimatch-api.onrender.com/docs) | [🚀 Deployment Guide](./DEPLOYMENT_GUIDE.md)

</div>

---

## 📋 Descripción del Proyecto

**PractiMatch Waitlist API** es un backend completo y profesional construido con FastAPI y PostgreSQL que permite gestionar una lista de espera (waitlist) pública con capacidades administrativas avanzadas.

### ¿Qué hace este proyecto?

Este sistema permite a cualquier usuario registrarse en una waitlist para un producto/servicio, mientras que los administradores pueden:
- Ver todos los registros con filtros avanzados
- Analizar métricas en tiempo real (distribuciones, KPIs, tendencias)
- Detectar automáticamente dispositivos, ubicación y origen de tráfico de cada usuario
- Exportar datos para análisis

**Casos de uso:**
- 🚀 Lanzamiento de productos (capturar early adopters)
- 📱 Apps en desarrollo (validar interés antes de construir)
- 🎓 Plataformas educativas (lista de espera para cursos)
- 💼 SaaS B2B (pipeline de leads cualificados)

---

## 🛠️ Stack Tecnológico

### Backend
- **[FastAPI](https://fastapi.tiangolo.com/)** `0.115.6` - Framework web moderno y rápido
- **[Python](https://www.python.org/)** `3.11+` - Lenguaje de programación
- **[Uvicorn](https://www.uvicorn.org/)** `0.34.0` - Servidor ASGI de alto rendimiento
- **[Pydantic](https://docs.pydantic.dev/)** `2.10.5` - Validación de datos con tipos

### Base de Datos
- **[PostgreSQL](https://www.postgresql.org/)** `15+` - Base de datos relacional
- **[SQLAlchemy](https://www.sqlalchemy.org/)** `2.0.36` - ORM para Python
- **[psycopg2-binary](https://www.psycopg.org/)** `2.9.10` - Adaptador PostgreSQL

### Autenticación y Seguridad
- **[python-jose](https://github.com/mpdavis/python-jose)** `3.3.0` - JWT tokens
- **[passlib](https://passlib.readthedocs.io/)** `1.7.4` + **[bcrypt](https://github.com/pyca/bcrypt)** `4.2.1` - Hashing de contraseñas
- **[slowapi](https://github.com/laurentS/slowapi)** `0.1.9` - Rate limiting

### Tracking y Analytics
- **[httpx](https://www.python-httpx.org/)** `0.28.1` - Cliente HTTP async para geolocalización
- **[user-agents](https://github.com/selwin/python-user-agents)** `2.2.0` - Parser de User-Agent
- **[ipapi.co](https://ipapi.co/)** - API de geolocalización IP (30k requests/mes gratis)

### Infraestructura
- **[Render](https://render.com/)** - Hosting del backend (plan gratuito)
- **PostgreSQL en Render** - Base de datos en la nube (1 GB gratis)

---

## 🎯 Características Principales

### ✅ STEP 1 - Core del Sistema
- 🌐 **Waitlist pública**: Endpoint POST para registro de usuarios sin autenticación
- 🔄 **Manejo de duplicados**: Contador automático de intentos de registro
- 📊 **Tracking avanzado**: Detecta dispositivo, ciudad, país y origen de tráfico **automáticamente**
- ✅ **Validaciones robustas**: Pydantic schemas con protección anti-XSS/SQL injection
- 🏥 **Health check**: Endpoint `/api/health` para monitoreo
- 🛡️ **Rate limiting**: Protección contra abuso (10 requests/min por IP)
- 🌍 **CORS configurado**: Compatible con cualquier frontend

### ✅ STEP 2 - Dashboard Administrativo
- 🔐 **Autenticación JWT**: Login seguro con tokens Bearer
- 🔄 **Sesiones persistentes**: Tokens de larga duración (8 horas)
- 📋 **Lista paginada**: Tabla con filtros múltiples y ordenamiento
- 📈 **Métricas agregadas**: 
  - Total de registros y intentos
  - Distribución por tipo de usuario, país, ciudad, dispositivo
  - Top 10 fuentes de tráfico
  - Emails con más intentos
- 🔍 **Filtros avanzados**: Por email, tipo, fuente, país, ciudad, dispositivo
- ⚡ **Performance optimizado**: 6 índices en BD, paginación obligatoria
- 📚 **Documentación automática**: OpenAPI/Swagger UI interactivo

### 🆕 STEP 3 - Tracking Automático (NUEVO)
- 📱 **Detección de dispositivo**: mobile | desktop | tablet (desde User-Agent)
- 🌍 **Geolocalización**: Ciudad y país detectados desde IP
- 🚦 **Origen de tráfico**: Instagram, Facebook, Google, Direct, etc. (desde Referer)
- 🔒 **Sin cambios en frontend**: Todo el tracking es automático en backend
- ⚡ **Performance**: Timeout de 3 seg, no bloquea requests

---

## 🚀 Cómo Correr el Proyecto Localmente

### 1. Clonar el Repositorio

```bash
git clone https://github.com/RafaCH1906/Dashboard_Practimatch.git
cd Dashboard_Practimatch
```

### 2. Crear Entorno Virtual

**Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar Dependencias

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**✅ Dependencias principales instaladas:**
- FastAPI `0.115.6` - Framework web
- Uvicorn `0.34.0` - Servidor ASGI
- SQLAlchemy `2.0.36` - ORM
- PostgreSQL driver `psycopg2-binary`
- Pydantic `2.10.5` - Validación
- JWT + bcrypt - Autenticación
- httpx + user-agents - Tracking

### 4. Configurar Base de Datos PostgreSQL

**Opción A: PostgreSQL Local**

1. Instalar PostgreSQL 15+
2. Crear base de datos:
   ```sql
   CREATE DATABASE practimatch;
   CREATE USER practimatch_user WITH PASSWORD 'tu_password_seguro';
   GRANT ALL PRIVILEGES ON DATABASE practimatch TO practimatch_user;
   ```

**Opción B: PostgreSQL en Docker**

```bash
docker run --name practimatch-db \
  -e POSTGRES_DB=practimatch \
  -e POSTGRES_USER=practimatch_user \
  -e POSTGRES_PASSWORD=tu_password_seguro \
  -p 5432:5432 \
  -d postgres:15
```

### 5. Configurar Variables de Entorno

Crea un archivo **`.env`** en la raíz del proyecto (copia desde `.env.example`):

```bash
cp .env.example .env
```

Edita `.env` con tus valores **(ver sección Variables de Entorno más abajo)**

### 6. Crear Tablas en la Base de Datos

```bash
python create_tables.py
```

**Esto creará:**
- ✅ Tabla `waitlist` con columnas de tracking
- ✅ Tabla `admin_users`
- ✅ 6 índices para performance
- ✅ Usuario admin por defecto

### 7. Iniciar el Servidor

```bash
uvicorn main:app --reload --port 8000
```

**Servidor corriendo en:**
- 🌐 API: http://localhost:8000
- 📖 Documentación: http://localhost:8000/docs
- 🏥 Health Check: http://localhost:8000/api/health

---

## 🔐 Variables de Entorno Necesarias

Crea un archivo **`.env`** con las siguientes variables:

### 📋 Plantilla Completa

```env
# ============================================
# CONFIGURACIÓN DE BASE DE DATOS
# ============================================
DATABASE_URL=postgresql://practimatch_user:tu_password@localhost/practimatch

# ============================================
# CONFIGURACIÓN DE SEGURIDAD
# ============================================
# Genera un SECRET_KEY único con:
# python -c "import secrets; print(secrets.token_urlsafe(32))"
SECRET_KEY=tu_secret_key_super_seguro_aqui_64_caracteres_minimo
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=480

# ============================================
# USUARIO ADMIN POR DEFECTO
# ============================================
ADMIN_EMAIL=admin@practimatch.com
ADMIN_PASSWORD=Admin123!

# ⚠️ CAMBIAR EN PRODUCCIÓN después del primer deploy

# ============================================
# CONFIGURACIÓN DE ENTORNO
# ============================================
ENVIRONMENT=development
LOG_LEVEL=INFO

# ============================================
# RATE LIMITING
# ============================================
RATE_LIMIT_PER_MINUTE=10

# ============================================
# CORS - Orígenes Permitidos
# ============================================
# Separados por comas, sin espacios
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173,http://localhost:8080
```

### 📝 Descripción de Variables

| Variable | Descripción | Ejemplo | Requerida |
|----------|-------------|---------|-----------|
| **`DATABASE_URL`** | URL de conexión a PostgreSQL | `postgresql://user:pass@host/db` | ✅ Sí |
| **`SECRET_KEY`** | Clave secreta para JWT (32+ caracteres) | `xK9mP2vR8nQ5...` | ✅ Sí |
| **`JWT_ALGORITHM`** | Algoritmo de encriptación JWT | `HS256` | ✅ Sí |
| **`ACCESS_TOKEN_EXPIRE_MINUTES`** | Duración del token (minutos) | `480` (8 horas) | ✅ Sí |
| **`ADMIN_EMAIL`** | Email del usuario admin | `admin@practimatch.com` | ✅ Sí |
| **`ADMIN_PASSWORD`** | Contraseña del admin | `Admin123!` | ✅ Sí |
| **`ENVIRONMENT`** | Entorno de ejecución | `development` o `production` | ⚠️ Recomendada |
| **`LOG_LEVEL`** | Nivel de logging | `DEBUG`, `INFO`, `WARNING`, `ERROR` | ⚠️ Recomendada |
| **`RATE_LIMIT_PER_MINUTE`** | Requests máximos por minuto | `10` | ⚠️ Recomendada |
| **`ALLOWED_ORIGINS`** | Orígenes permitidos para CORS | `http://localhost:3000,...` | ✅ Sí |

### 🔒 Generar SECRET_KEY Seguro

**PowerShell (Windows):**
```powershell
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

**Bash (macOS/Linux):**
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

**Output ejemplo:**
```
xK9mP2vR8nQ5Lm3Nt7PwYq4Rs6Uv1Wx0
```

### ⚠️ Importante para Producción

Cuando despliegues en producción (Render, Railway, etc.):

1. **Cambiar `ADMIN_PASSWORD`** por una contraseña fuerte
2. **Generar nuevo `SECRET_KEY`** único para producción
3. **Actualizar `ALLOWED_ORIGINS`** con tu dominio real:
   ```env
   ALLOWED_ORIGINS=https://tuapp.com,https://www.tuapp.com
   ```
4. **Cambiar `ENVIRONMENT`** a `production`
5. **NO compartir** el archivo `.env` en GitHub (está en `.gitignore`)

---

## 🌐 App en Producción

### 🚀 Enlaces de Producción

| Recurso | URL | Descripción |
|---------|-----|-------------|
| **🏠 API Base** | [https://practimatch-api.onrender.com](https://practimatch-api.onrender.com) | URL base del backend |
| **📖 Documentación** | [https://practimatch-api.onrender.com/docs](https://practimatch-api.onrender.com/docs) | Swagger UI interactivo |
| **🏥 Health Check** | [https://practimatch-api.onrender.com/api/health](https://practimatch-api.onrender.com/api/health) | Estado del servidor |
| **📄 OpenAPI Schema** | [https://practimatch-api.onrender.com/openapi.json](https://practimatch-api.onrender.com/openapi.json) | Schema JSON |

### 🔑 Credenciales de Admin (Demo)

Para probar el dashboard administrativo:

```json
{
  "username": "admin@practimatch.com",
  "password": "Admin123!"
}
```

**⚠️ Nota:** En producción real, estas credenciales deben ser cambiadas inmediatamente.

### 📊 Características en Producción

- ✅ **HTTPS** habilitado (certificado SSL automático)
- ✅ **CORS** configurado para aceptar requests de cualquier origen
- ✅ **Rate Limiting** activo (10 requests/min por IP)
- ✅ **Geolocalización** funcionando (ipapi.co)
- ✅ **Tracking automático** de dispositivo, ciudad y tráfico
- ✅ **Base de datos PostgreSQL** en Render (1 GB)
- ⚠️ **Cold start:** Primera request puede tardar ~30 segundos (plan gratuito)

### 🧪 Probar la API en Producción

**Ejemplo 1: Registrar un usuario en waitlist**

```bash
curl -X POST https://practimatch-api.onrender.com/api/waitlist \
  -H "Content-Type: application/json" \
  -H "User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X)" \
  -H "Referer: https://instagram.com/practimatch" \
  -d '{
    "email": "test@example.com",
    "user_type": "student",
    "product_of_interest": "PractiMatch Platform"
  }'
```

**Ejemplo 2: Login admin**

```bash
curl -X POST https://practimatch-api.onrender.com/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin@practimatch.com",
    "password": "Admin123!"
  }'
```

**Ejemplo 3: Ver métricas (requiere token)**

```bash
curl -X GET https://practimatch-api.onrender.com/api/admin/metrics \
  -H "Authorization: Bearer tu-token-aqui"
```

---
## 📡 API Endpoints

### 🌐 Endpoints Públicos (Sin Autenticación)

#### 1. Health Check
```http
GET /api/health
```

**Response (200 OK):**
```json
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2026-01-09T12:34:56.789Z"
}
```

#### 2. Registrar en Waitlist
```http
POST /api/waitlist
Content-Type: application/json
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "user_type": "student",  // student | company | university
  "product_of_interest": "PractiMatch Platform",
  "source": "Instagram",  // Opcional
  "country": "Mexico"     // Opcional
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "message": "Thank you for registering for this product of interest...",
  "data": {
    "email": "user@example.com",
    "user_type": "student",
    "product_of_interest": "PractiMatch Platform",
    "registration_count": 1,
    "is_new_registration": true,
    "device_type": "mobile",        // Detectado automáticamente
    "city": "Mexico City",          // Detectado automáticamente
    "country": "MX",                // Detectado automáticamente
    "traffic_source": "instagram",  // Detectado automáticamente
    "created_at": "2026-01-09T12:34:56.789Z"
  }
}
```

**Response (200 OK) - Email duplicado:**
```json
{
  "success": true,
  "message": "Thank you for registering...",
  "data": {
    "email": "user@example.com",
    "registration_count": 2,  // Contador incrementado
    "is_new_registration": false
    // ...otros campos
  }
}
```

---

### 🔐 Endpoints Administrativos (Requieren Autenticación)

#### 3. Login Admin
```http
POST /api/auth/login
Content-Type: application/json
```

**Request Body:**
```json
{
  "username": "admin@practimatch.com",
  "password": "Admin123!"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### 4. Lista de Waitlist (Paginada)
```http
GET /api/admin/waitlist
Authorization: Bearer {token}
```

**Query Params (todos opcionales):**
```
?page=1
&limit=20
&user_type=student
&email=user@example.com
&source=Instagram
&country=Mexico
&city=Mexico City           // NUEVO
&device_type=mobile         // NUEVO
&traffic_source=instagram   // NUEVO
&order_by=created_at_desc
```

**Response (200 OK):**
```json
{
  "total": 150,
  "page": 1,
  "limit": 20,
  "pages": 8,
  "items": [
    {
      "id": 1,
      "email": "user@example.com",
      "user_type": "student",
      "product_of_interest": "PractiMatch Platform",
      "registration_count": 2,
      "source": "Instagram",
      "country": "MX",
      "city": "Mexico City",
      "device_type": "mobile",
      "traffic_source": "instagram",
      "user_agent": "Mozilla/5.0...",
      "ip_address": "187.XXX.XXX.XXX",
      "created_at": "2026-01-08T10:00:00Z",
      "updated_at": "2026-01-09T11:00:00Z"
    }
  ]
}
```

#### 5. Métricas Agregadas
```http
GET /api/admin/metrics
Authorization: Bearer {token}
```

**Response (200 OK):**
```json
{
  "total_registrations": 150,
  "total_attempts": 285,
  "by_user_type": [
    {"category": "student", "count": 100},
    {"category": "company", "count": 30},
    {"category": "university", "count": 20}
  ],
  "by_source": [
    {"category": "Instagram", "count": 80},
    {"category": "Facebook", "count": 40},
    {"category": "Direct", "count": 30}
  ],
  "by_country": [
    {"category": "Mexico", "count": 90},
    {"category": "Colombia", "count": 35}
  ],
  "by_city": [
    {"category": "Mexico City", "count": 45},
    {"category": "Guadalajara", "count": 23}
  ],
  "by_device": [
    {"category": "mobile", "count": 95},
    {"category": "desktop", "count": 48},
    {"category": "tablet", "count": 7}
  ],
  "by_traffic_source": [
    {"category": "instagram", "count": 67},
    {"category": "direct", "count": 45},
    {"category": "facebook", "count": 23}
  ],
  "top_emails": [
    {"email": "user@example.com", "registration_count": 5}
  ],
  "latest_by_type": [
    {
      "user_type": "student",
      "email": "recent@example.com",
      "created_at": "2026-01-09T14:30:00Z",
      "registration_count": 1
    }
  ]
}
```

---

## 📸 Screenshots (Opcional)

### Swagger UI - Documentación Interactiva
![Swagger UI](https://via.placeholder.com/800x400/4A90E2/FFFFFF?text=Swagger+UI+%7C+FastAPI+Docs)

*Documentación interactiva en `/docs` con todos los endpoints disponibles*

### Dashboard Admin - Métricas
![Admin Metrics](https://via.placeholder.com/800x400/7B68EE/FFFFFF?text=Admin+Dashboard+%7C+M%C3%A9tricas+en+Tiempo+Real)

*Panel administrativo con métricas agregadas, gráficos y KPIs*

### Waitlist Table - Lista Paginada
![Waitlist Table](https://via.placeholder.com/800x400/50C878/FFFFFF?text=Waitlist+Table+%7C+Lista+Paginada+con+Filtros)

*Tabla de registros con filtros, ordenamiento y paginación*

### Tracking Automático - Device Detection
![Device Tracking](https://via.placeholder.com/800x400/FF6B6B/FFFFFF?text=Tracking+Autom%C3%A1tico+%7C+Dispositivo+%2B+Ciudad+%2B+Tr%C3%A1fico)

*Detección automática de dispositivo, ubicación y origen de tráfico*

---

### Endpoints Públicos (sin autenticación)

#### **Health Check**
```http
GET /api/health
```
Verifica el estado de la API y la conexión a la base de datos.

#### **Registro en Waitlist**
```http
POST /api/waitlist
Content-Type: application/json

{
  "email": "user@example.com",
  "user_type": "student",
  "product_of_interest": "PractiMatch Platform",
  "source": "Instagram",
  "country": "Mexico"
}
```

**Tipos de usuario**: `student` | `company` | `university`

**Respuestas**:
- `201 Created` - Nuevo registro
- `200 OK` - Email duplicado (contador incrementado)
- `422 Unprocessable Entity` - Validación fallida

---

### Endpoints de Autenticación

#### **Login**
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "admin@practimatch.com",
  "password": "TuPasswordSeguro123!"
}
```

**Respuesta exitosa**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### **Información del Usuario Actual**
```http
GET /api/auth/me
Authorization: Bearer <access_token>
```

#### **Renovar Token**
```http
POST /api/auth/refresh
Authorization: Bearer <access_token>
```

---

### Endpoints Administrativos (requieren JWT)

#### **Lista de Waitlist (Paginada)**
```http
GET /api/admin/waitlist?page=1&limit=20&user_type=student
Authorization: Bearer <access_token>
```

**Query Parameters**:
- `page` (int) - Número de página (default: 1)
- `limit` (int) - Registros por página (default: 20, max: 100)
- `user_type` (enum) - Filtrar por tipo: `student` | `company` | `university`
- `product_of_interest` (string) - Búsqueda parcial
- `source` (string) - Filtrar por fuente
- `country` (string) - Filtrar por país
- `email` (string) - Búsqueda parcial
- `order_by` (enum) - `created_at_desc` | `registration_count_desc`

**Respuesta**:
```json
{
  "total": 150,
  "page": 1,
  "limit": 20,
  "pages": 8,
  "items": [
    {
      "id": 1,
      "email": "student@example.com",
      "user_type": "student",
      "product_of_interest": "PractiMatch Platform",
      "registration_count": 2,
      "source": "Instagram",
      "country": "Mexico",
      "created_at": "2026-01-08T10:00:00Z",
      "updated_at": "2026-01-08T11:00:00Z"
    }
  ]
}
```

#### **Métricas Agregadas**
```http
GET /api/admin/metrics
Authorization: Bearer <access_token>
```

**Respuesta**:
```json
{
  "total_registrations": 150,
  "total_attempts": 285,
  "by_user_type": [
    {"category": "student", "count": 100},
    {"category": "company", "count": 30},
    {"category": "university", "count": 20}
  ],
  "by_source": [
    {"category": "Instagram", "count": 80},
    {"category": "Facebook", "count": 40}
  ],
  "by_country": [
    {"category": "Mexico", "count": 90},
    {"category": "Colombia", "count": 35}
  ],
  "top_emails": [
    {"email": "user@example.com", "registration_count": 5}
  ],
  "latest_by_type": [
    {
      "user_type": "student",
      "email": "recent@example.com",
      "created_at": "2026-01-08T14:30:00Z",
      "registration_count": 1
    }
  ]
}
```

---

## 🚀 Deployment en Producción

Este proyecto está deployado en **Render** (plan gratuito). Para deployar tu propia instancia:

### Guía Completa de Deployment

📖 **Lee la guía completa:** [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)

La guía incluye:
- ✅ Deploy en Render (backend + PostgreSQL)
- ✅ Configuración de variables de entorno
- ✅ Ejecución de migraciones SQL
- ✅ Testing en producción
- ✅ Troubleshooting común

### Quick Start (Render)

1. **Fork este repositorio** en tu cuenta de GitHub
2. **Crear cuenta en Render:** https://render.com (gratis, sin tarjeta)
3. **Crear PostgreSQL:**
   - New → PostgreSQL → Plan Free
   - Copiar "Internal Database URL"
4. **Crear Web Service:**
   - New → Web Service → Conectar tu repo
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port 10000`
5. **Configurar variables de entorno** (ver DEPLOYMENT_GUIDE.md)
6. **Ejecutar migración SQL** en PostgreSQL
7. **Verificar:** https://tu-app.onrender.com/api/health

⏱️ **Tiempo total:** ~20 minutos  
💰 **Costo:** $0 (plan gratuito)

---

## 🧪 Testing

### Tests Unitarios

```bash
# Instalar dependencias de testing
pip install pytest pytest-asyncio httpx

# Ejecutar tests
pytest tests/ -v

# Con cobertura
pytest tests/ --cov=app --cov-report=html
```

### Tests de Integración

```bash
# Test del tracking automático
python test_tracking.py
```

**Output esperado:**
```
🧪 PRUEBAS DE TRACKING AUTOMÁTICO
==================================================

🔍 TEST 1: Detección de Dispositivos
✅ iPhone → mobile
✅ iPad → tablet
✅ Windows → desktop

🌍 TEST 2: Geolocalización IP
✅ IP 8.8.8.8 → US, Mountain View

🚦 TEST 3: Detección de Origen de Tráfico
✅ instagram.com → instagram
✅ facebook.com → facebook
✅ (sin referer) → direct

✅ TODAS LAS PRUEBAS COMPLETADAS
```

---

## 📊 Métricas y Monitoring

### Health Check

Verifica el estado del servidor:
```bash
curl https://practimatch-api.onrender.com/api/health
```

### Logs

**Desarrollo:**
```bash
# Los logs aparecen en la consola al correr uvicorn
tail -f logs/app.log
```

**Producción (Render):**
- Ve a tu servicio en Render Dashboard
- Click en "Logs" (pestaña superior)
- Logs en tiempo real

### Métricas Disponibles

El endpoint `/api/admin/metrics` proporciona:
- Total de registros únicos
- Total de intentos de registro
- Distribución por tipo de usuario
- Top 10 países
- Top 10 ciudades
- Top 10 fuentes de tráfico
- Distribución por dispositivo
- Emails con más intentos

---

## 🤝 Contribuir

### Cómo Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

### Estándares de Código

- **Python:** PEP 8
- **Type hints:** Usa tipos en funciones públicas
- **Docstrings:** Documenta clases y métodos públicos
- **Tests:** Escribe tests para nuevas features
- **Commits:** Mensajes descriptivos en inglés

---

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo [LICENSE](LICENSE) para más detalles.

```
MIT License

Copyright (c) 2026 PractiMatch

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 👥 Autores

- **Rafael Chamorro** - [@RafaCH1906](https://github.com/RafaCH1906)

---

## 🙏 Agradecimientos

- **FastAPI** - Framework web moderno y rápido
- **SQLAlchemy** - ORM robusto para Python
- **PostgreSQL** - Base de datos confiable
- **Render** - Hosting gratuito y fácil
- **ipapi.co** - API de geolocalización gratuita
- **Pydantic** - Validación de datos excepcional

---

## 🔗 Links Útiles

| Recurso | URL |
|---------|-----|
| **🌐 App en Producción** | https://practimatch-api.onrender.com |
| **📖 Documentación API** | https://practimatch-api.onrender.com/docs |
| **🐙 Repositorio GitHub** | https://github.com/RafaCH1906/Dashboard_Practimatch |
| **📚 FastAPI Docs** | https://fastapi.tiangolo.com/ |
| **🐘 PostgreSQL Docs** | https://www.postgresql.org/docs/ |
| **🚀 Render** | https://render.com/ |
| **📦 PyPI - FastAPI** | https://pypi.org/project/fastapi/ |

---

## 📞 Contacto y Soporte

- **GitHub Issues:** [Reportar un bug](https://github.com/RafaCH1906/Dashboard_Practimatch/issues)
- **GitHub Discussions:** [Preguntas y discusiones](https://github.com/RafaCH1906/Dashboard_Practimatch/discussions)
- **Email:** contacto@practimatch.com

---

<div align="center">

**⭐ Si este proyecto te fue útil, dale una estrella en GitHub ⭐**

**Hecho con ❤️ por el equipo de PractiMatch**

![Python](https://img.shields.io/badge/Made%20with-Python-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/Built%20with-FastAPI-green?logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/Powered%20by-PostgreSQL-blue?logo=postgresql&logoColor=white)

</div>