# 🚀 PractiMatch Waitlist API

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**Backend API para gestión de waitlist pública con dashboard administrativo**

[Características](#-características) • [Instalación](#-instalación) • [Uso](#-uso) • [🚀 Deployment](#-deployment) • [Documentación](#-documentación) • [API](#-api-endpoints)

</div>

---

## 📋 Descripción

**PractiMatch Waitlist API** es un backend completo construido con FastAPI y PostgreSQL que permite:

- ✅ **Registro público en waitlist** con detección de duplicados
- ✅ **Dashboard administrativo** con autenticación JWT
- ✅ **Métricas en tiempo real** (agregaciones, filtros, gráficos)
- ✅ **Tracking de tráfico** (fuente, país, intentos de registro)
- ✅ **API REST documentada** con OpenAPI/Swagger
- ✅ **Seguridad robusta** (bcrypt, JWT, rate limiting, CORS)

---

## 🎯 Características

### STEP 1 - Core del Sistema
- 🌐 **Waitlist pública**: Endpoint POST para registro de usuarios
- 🔄 **Manejo de duplicados**: Contador automático de intentos
- 📊 **Tracking**: Origen del tráfico (Instagram, Facebook, Direct, etc.)
- ✅ **Validaciones**: Pydantic schemas con protección anti-XSS
- 🏥 **Health check**: Endpoint de monitoreo
- 🛡️ **Rate limiting**: Protección contra abuso (SlowAPI)
- 🌍 **CORS**: Configurado para desarrollo y producción

### STEP 2 - Dashboard Administrativo
- 🔐 **Autenticación JWT**: Login seguro con bcrypt
- 🔄 **Refresh token**: Renovación automática de sesiones
- 📋 **Lista paginada**: Tabla con filtros múltiples
- 📈 **Métricas agregadas**: KPIs, distribuciones, top usuarios
- 🔍 **Búsqueda y filtros**: Por email, tipo, fuente, país
- ⚡ **Performance optimizado**: Índices en BD, queries eficientes
- 📚 **OpenAPI/Swagger**: Documentación interactiva

---

## 📦 Requisitos

### Software Necesario

| Software | Versión Mínima | Recomendada |
|----------|----------------|-------------|
| **Python** | 3.11+ | 3.12 |
| **PostgreSQL** | 14+ | 15+ |
| **pip** | 23+ | Latest |
| **Git** | 2.30+ | Latest |

### Sistema Operativo
- ✅ Windows 10/11
- ✅ macOS 12+
- ✅ Linux (Ubuntu 20.04+, Debian 11+)

---

## 🚀 Instalación

### 1. Clonar el Repositorio

```bash
git clone https://github.com/tu-usuario/practimatch-waitlist-api.git
cd practimatch-waitlist-api
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

**Dependencias principales:**
- `fastapi==0.109.0` - Framework web
- `uvicorn[standard]==0.27.0` - Servidor ASGI
- `sqlalchemy==2.0.25` - ORM
- `psycopg2-binary==2.9.9` - Driver PostgreSQL
- `pydantic==2.5.3` - Validación de datos
- `python-jose[cryptography]==3.3.0` - JWT
- `passlib[bcrypt]==1.7.4` - Hashing de passwords
- `slowapi==0.1.9` - Rate limiting

---

## ⚙️ Configuración

### 1. Configurar PostgreSQL

**Crear base de datos:**

```sql
-- Conectar a PostgreSQL
psql -U postgres

-- Crear base de datos
CREATE DATABASE practi_waitlist;

-- Crear usuario (opcional)
CREATE USER practi_user WITH PASSWORD 'tu_password_seguro';
GRANT ALL PRIVILEGES ON DATABASE practi_waitlist TO practi_user;
```

### 2. Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto:

```bash
# Copiar el ejemplo
cp .env.example .env

# Editar con tus valores
notepad .env  # Windows
nano .env     # Linux/macOS
```

**Archivo `.env` requerido:**

```env
# ==========================================
# DATABASE CONFIGURATION
# ==========================================
DATABASE_URL=postgresql://postgres:tu_password@localhost:5432/practi_waitlist

# ==========================================
# APPLICATION SETTINGS
# ==========================================
ENVIRONMENT=development
APP_NAME=PractiMatch Waitlist API
VERSION=2.0.0

# ==========================================
# JWT AUTHENTICATION (⚠️ CAMBIAR EN PRODUCCIÓN)
# ==========================================
SECRET_KEY=tu-secret-key-super-seguro-minimo-32-caracteres-aqui
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=480

# ==========================================
# ADMIN USER (para create_admin.py script)
# ==========================================
ADMIN_EMAIL=admin@practimatch.com
ADMIN_PASSWORD=TuPasswordSeguro123!

# ==========================================
# RATE LIMITING
# ==========================================
RATE_LIMIT_PER_MINUTE=10

# ==========================================
# CORS ORIGINS (comma-separated)
# ==========================================
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173,http://localhost:5174

# ==========================================
# LOGGING
# ==========================================
LOG_LEVEL=INFO
```

### 3. Inicializar Base de Datos

```bash
# Crear tablas
python create_tables.py

# Crear primer usuario administrador
python create_admin.py
```

**Output esperado:**
```
🔧 Creando tablas en PostgreSQL...
✅ Tablas creadas exitosamente!

📋 Tablas en la base de datos:
  - waitlist
  - admin_users

🔧 Creando primer usuario administrador...
✅ Admin creado exitosamente!
   Email: admin@practimatch.com
   Password: TuPasswordSeguro123!
```

---

## 🏃 Cómo Correr Localmente

### Desarrollo (con auto-reload)

```bash
# Activar entorno virtual (si no está activo)
.venv\Scripts\Activate.ps1  # Windows
source .venv/bin/activate    # macOS/Linux

# Iniciar servidor
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using WatchFiles
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
✅ PractiMatch Waitlist API iniciado
📊 Base de datos: configured
INFO:     Application startup complete.
```

### Producción

```bash
# Sin auto-reload, optimizado
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Acceder a la Aplicación

| Servicio | URL | Descripción |
|----------|-----|-------------|
| **API Root** | http://127.0.0.1:8000 | Endpoint raíz |
| **Health Check** | http://127.0.0.1:8000/api/health | Status de la API |
| **Swagger UI** | http://127.0.0.1:8000/docs | Documentación interactiva |
| **ReDoc** | http://127.0.0.1:8000/redoc | Documentación alternativa |
| **OpenAPI JSON** | http://127.0.0.1:8000/openapi.json | Schema OpenAPI |

---

## 📡 API Endpoints

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

## 🧪 Testing

### Probar con archivo HTTP

Usa el archivo `test_main.http` con la extensión REST Client de VS Code:

```bash
# Instalar extensión REST Client en VS Code
code --install-extension humao.rest-client

# Abrir archivo de tests
code test_main.http
```

### Probar con curl

**Health check:**
```bash
curl http://127.0.0.1:8000/api/health
```

**Registro en waitlist:**
```bash
curl -X POST http://127.0.0.1:8000/api/waitlist \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "user_type": "student",
    "product_of_interest": "PractiMatch Platform"
  }'
```

**Login:**
```bash
curl -X POST http://127.0.0.1:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@practimatch.com",
    "password": "TuPasswordSeguro123!"
  }'
```

---

## 📁 Estructura del Proyecto

```
Dashboard_Practimatch/
├── app/
│   ├── api/
│   │   └── routes/
│   │       ├── admin.py          # Rutas administrativas
│   │       ├── auth.py           # Autenticación JWT
│   │       ├── health.py         # Health check
│   │       └── waitlist.py       # Waitlist pública
│   ├── db/
│   │   └── database.py           # SQLAlchemy config
│   ├── middleware/
│   │   └── auth.py               # JWT middleware
│   ├── models/
│   │   ├── __init__.py
│   │   ├── admin_user.py         # Modelo Admin
│   │   └── waitlist.py           # Modelo Waitlist
│   ├── schemas/
│   │   ├── admin.py              # Schemas admin
│   │   ├── auth.py               # Schemas auth
│   │   └── waitlist.py           # Schemas waitlist
│   ├── services/
│   │   ├── admin_service.py      # Lógica admin
│   │   ├── auth_service.py       # Lógica auth
│   │   └── waitlist_service.py   # Lógica waitlist
│   ├── utils/
│   │   └── logger.py             # Configuración logging
│   └── config.py                 # Settings Pydantic
├── create_admin.py               # Script crear admin
├── create_tables.py              # Script crear tablas
├── main.py                       # Entry point FastAPI
├── requirements.txt              # Dependencias Python
├── .env.example                  # Ejemplo de variables
├── .env                          # Variables locales (no versionar)
└── README.md                     # Este archivo
```

---

## 🔒 Seguridad

### Implementado

✅ **Autenticación JWT** - HS256, expiración 8 horas  
✅ **Passwords hasheados** - bcrypt con salt automático  
✅ **Rate limiting** - 10 req/min público, 60 req/min admin  
✅ **CORS configurado** - Origins específicos por environment  
✅ **Validación de input** - Pydantic + regex anti-XSS  
✅ **SQL Injection prevention** - SQLAlchemy ORM  
✅ **Error handling** - Mensajes genéricos, sin internals  

### Recomendaciones para Producción

⚠️ **Cambiar SECRET_KEY**: Usar un valor seguro de 32+ caracteres  
⚠️ **HTTPS**: Usar certificado SSL/TLS  
⚠️ **CORS**: Configurar origins específicos  
⚠️ **Firewall**: Limitar acceso a PostgreSQL  
⚠️ **Backups**: Configurar backups automáticos de BD  
⚠️ **Monitoring**: Implementar logging centralizado  

---

## 📚 Documentación

### Archivos de Documentación

- **`BACKEND_AUDIT_REPORT.md`** - Auditoría técnica completa
- **`FRONTEND_GUIDE.md`** - Guía para desarrollo frontend
- **`AUDIT_SUMMARY.md`** - Resumen ejecutivo
- **`CHECKLIST.md`** - Checklist de features
- **`STEP2_ADMIN.md`** - Guía de implementación STEP 2
- **`test_main.http`** - Ejemplos de requests HTTP

### Swagger UI

Accede a la documentación interactiva en:
```
http://127.0.0.1:8000/docs
```

### Generar Tipos TypeScript (para frontend)

```bash
npm install -D openapi-typescript
npx openapi-typescript http://127.0.0.1:8000/openapi.json --output types/api.ts
```

---

## 🛠️ Scripts Útiles

### Crear Admin Adicional

```python
# create_another_admin.py
from app.db.database import SessionLocal
from app.services.auth_service import AuthService

db = SessionLocal()
admin = AuthService.create_admin_user(
    db=db,
    email="otro@admin.com",
    password="PasswordSeguro456!",
    full_name="Otro Admin"
)
print(f"✅ Admin creado: {admin.email}")
db.close()
```

### Exportar Waitlist a CSV

```python
# export_waitlist.py
import csv
from app.db.database import SessionLocal
from app.models.waitlist import Waitlist

db = SessionLocal()
waitlist = db.query(Waitlist).all()

with open('waitlist_export.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['ID', 'Email', 'User Type', 'Product', 'Count', 'Source', 'Country', 'Created'])
    
    for item in waitlist:
        writer.writerow([
            item.id,
            item.email,
            item.user_type,
            item.product_of_interest,
            item.registration_count,
            item.source or 'N/A',
            item.country or 'N/A',
            item.created_at
        ])

print(f"✅ Exportados {len(waitlist)} registros a waitlist_export.csv")
db.close()
```

---

## 🐛 Troubleshooting

### Error: "ModuleNotFoundError: No module named 'pydantic_settings'"

```bash
pip install pydantic-settings==2.1.0
```

### Error: "connection refused" al conectar a PostgreSQL

1. Verificar que PostgreSQL está corriendo:
```bash
# Windows
Get-Service postgresql*

# macOS
brew services list

# Linux
sudo systemctl status postgresql
```

2. Verificar `DATABASE_URL` en `.env`
3. Verificar que el puerto 5432 no está bloqueado

### Error: "Access denied for user"

1. Crear usuario con privilegios:
```sql
CREATE USER practi_user WITH PASSWORD 'tu_password';
GRANT ALL PRIVILEGES ON DATABASE practi_waitlist TO practi_user;
```

2. Actualizar `DATABASE_URL` en `.env`

### Error: "Secret key must be at least 32 characters"

Generar una clave segura:
```python
import secrets
print(secrets.token_urlsafe(32))
```

Copiar el resultado a `SECRET_KEY` en `.env`

---

