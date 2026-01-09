# 🎯 STEP 2 - Admin Dashboard Backend

## ✅ **IMPLEMENTACIÓN COMPLETADA**

### **Resumen**
Backend completo para dashboard administrativo con autenticación JWT, endpoints protegidos, métricas agregadas y paginación.

---

## 📦 **INSTALACIÓN Y SETUP**

### **1. Instalar nuevas dependencias**

```bash
pip install python-jose[cryptography]==3.3.0
pip install passlib[bcrypt]==1.7.4
pip install python-multipart==0.0.6
```

O simplemente:
```bash
pip install -r requirements.txt
```

### **2. Crear tablas (incluye admin_users)**

```bash
python create_tables.py
```

**Output esperado:**
```
🔧 Creando tablas en PostgreSQL...
✅ Tablas creadas exitosamente!

📋 Tablas en la base de datos:
  - waitlist
  - admin_users
```

### **3. Crear primer usuario administrador**

```bash
python create_admin.py
```

**Output esperado:**
```
🔧 Creando primer usuario administrador...
✅ Admin creado exitosamente!
   Email: admin@practimatch.com
   Password: admin123
   ⚠️  CAMBIAR PASSWORD EN PRODUCCIÓN!
```

### **4. Iniciar servidor**

```bash
uvicorn main:app --reload
```

### **5. Abrir Swagger UI**

http://localhost:8000/docs

---

## 🔐 **AUTENTICACIÓN**

### **Login**

```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "admin@practimatch.com",
  "password": "admin123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### **Usar el token en requests**

```http
GET /api/admin/waitlist
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### **Verificar autenticación**

```http
GET /api/auth/me
Authorization: Bearer <token>
```

**Response:**
```json
{
  "id": 1,
  "email": "admin@practimatch.com",
  "full_name": "Admin Principal",
  "is_active": true,
  "created_at": "2026-01-08T10:00:00Z",
  "last_login": "2026-01-08T14:30:00Z"
}
```

---

## 📊 **ENDPOINTS ADMINISTRATIVOS**

### **1. GET /api/admin/waitlist - Lista paginada**

**Parámetros de Query:**
- `page` (int, default=1): Número de página
- `limit` (int, default=20, max=100): Registros por página
- `user_type` (enum): student | company | university
- `product_of_interest` (string): Búsqueda parcial
- `source` (string): Filtro por fuente
- `country` (string): Filtro por país
- `email` (string): Búsqueda parcial por email
- `order_by` (string): created_at_desc | registration_count_desc

**Ejemplo:**
```http
GET /api/admin/waitlist?page=1&limit=20&user_type=student&source=Instagram
Authorization: Bearer <token>
```

**Response:**
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

### **2. GET /api/admin/metrics - Métricas agregadas**

**Ejemplo:**
```http
GET /api/admin/metrics
Authorization: Bearer <token>
```

**Response:**
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
    {"category": "Colombia", "count": 35},
    {"category": "Unknown", "count": 25}
  ],
  "top_emails": [
    {"email": "user@example.com", "registration_count": 5},
    {"email": "another@example.com", "registration_count": 4}
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

## 🏗️ **ARQUITECTURA**

### **Nuevos archivos creados:**

```
app/
├── models/
│   └── admin_user.py          ✅ Modelo ORM para admins
├── schemas/
│   ├── auth.py                ✅ Schemas de autenticación
│   └── admin.py               ✅ Schemas admin (paginación, métricas)
├── services/
│   ├── auth_service.py        ✅ JWT y password hashing
│   └── admin_service.py       ✅ Queries y métricas
├── middleware/
│   └── auth.py                ✅ Dependency para proteger rutas
└── api/
    └── routes/
        ├── auth.py            ✅ Login y /me
        └── admin.py           ✅ Waitlist y metrics

Scripts:
create_admin.py                ✅ Crear primer admin
create_tables.py               ✅ Crear tablas (actualizado)
```

### **Tabla admin_users:**

```sql
CREATE TABLE admin_users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_login TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_admin_users_email ON admin_users(email);
```

---

## 🔒 **SEGURIDAD**

### **Implementado:**
- ✅ **JWT tokens** con expiración (8 horas)
- ✅ **Password hashing** con bcrypt
- ✅ **Bearer token** authentication
- ✅ **Middleware** para proteger rutas
- ✅ **Validación** de admin activo
- ✅ **Logging** de intentos de login

### **TODO (Mejoras futuras):**
- ⚠️ Mover SECRET_KEY a .env
- ⚠️ Refresh tokens
- ⚠️ Rate limiting en /login
- ⚠️ Password reset flow
- ⚠️ Roles y permisos (super_admin, admin_read, admin_write)
- ⚠️ Audit log (quién hizo qué cuándo)

---

## 📈 **MÉTRICAS INCLUIDAS**

1. **Total de registros únicos** (count de emails)
2. **Total de intentos** (suma de registration_count)
3. **Por tipo de usuario** (student/company/university)
4. **Por fuente** (Instagram, Facebook, TikTok, etc.)
5. **Por país** (Top 10 países)
6. **Top emails** (emails con más intentos)
7. **Último registro por tipo** (más reciente de cada tipo)

---

## 🧪 **TESTING**

### **Usar el archivo `test_main.http`**

1. Login y copiar token
2. Reemplazar `<COPIAR_TOKEN_AQUI>` con el token real
3. Probar endpoints protegidos

### **Tests manuales:**

```bash
# 1. Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@practimatch.com","password":"your-secure-password"}'

# 2. Guardar token
TOKEN="<pegar_token_aqui>"

# 3. Get waitlist
curl -X GET "http://localhost:8000/api/admin/waitlist?page=1&limit=10" \
  -H "Authorization: Bearer $TOKEN"

# 4. Get metrics
curl -X GET http://localhost:8000/api/admin/metrics \
  -H "Authorization: Bearer $TOKEN"
```

---

## 🎯 **DECISIONES TÉCNICAS**

### **1. JWT en lugar de Sessions**
- ✅ Stateless (escala horizontalmente)
- ✅ No requiere almacenamiento server-side
- ✅ Estándar de la industria
- ✅ Compatible con SPA/Mobile

### **2. Paginación obligatoria**
- ✅ Límite máximo de 100 registros por request
- ✅ Previene cargas masivas
- ✅ Mejor performance con datasets grandes

### **3. Métricas en tiempo real**
- ✅ Sin cache (para datasets pequeños-medianos)
- ✅ Siempre actualizadas
- ⚠️ Considerar Redis si >100k registros

### **4. Filtros combinables**
- ✅ Múltiples filtros simultáneos
- ✅ Búsqueda parcial con ILIKE
- ✅ Queries eficientes con índices

### **5. Read-only por ahora**
- ✅ Solo GET endpoints
- ⚠️ POST/PUT/DELETE en futuras iteraciones

---

## 🚀 **PRÓXIMOS PASOS (FUTURO)**

### **Prioridad Alta:**
1. ✅ Mover SECRET_KEY a environment variables
2. ✅ Agregar tests (pytest)
3. ✅ Rate limiting en /login

### **Prioridad Media:**
4. ⚠️ Refresh tokens
5. ⚠️ Export CSV endpoint
6. ⚠️ Soft delete (en lugar de DELETE físico)
7. ⚠️ Alembic migrations

### **Prioridad Baja:**
8. ⚠️ Roles y permisos
9. ⚠️ Audit log
10. ⚠️ WebSockets para updates en tiempo real

---

## ❗ **IMPORTANTE PARA PRODUCCIÓN**

### **Cambiar antes de deploy:**

1. **SECRET_KEY** en `auth_service.py`:
   ```python
   # ❌ Cambiar esto:
   SECRET_KEY = "your-secret-key-change-in-production-min-32-chars-practimatch-2026"
   
   # ✅ Por esto (leer de .env):
   SECRET_KEY = os.getenv("SECRET_KEY")
   ```

2. **Password del admin**:
   ```bash
   # Crear admin con password seguro
   python create_admin.py
   # Luego cambiar manualmente en DB o crear script
   ```

3. **CORS origins**:
   ```python
   # Configurar en .env
   ALLOWED_ORIGINS=https://tudominio.com,https://admin.tudominio.com
   ```

4. **Database URL**:
   ```env
   # Usar credenciales seguras
   DATABASE_URL=postgresql://user:secure_pass@host:5432/db
   ```

---

## ✅ **CHECKLIST DE IMPLEMENTACIÓN**

- [x] Instalar dependencias JWT
- [x] Crear modelo AdminUser
- [x] Crear schemas auth
- [x] Crear schemas admin
- [x] Crear auth_service
- [x] Crear admin_service
- [x] Crear middleware auth
- [x] Crear rutas auth
- [x] Crear rutas admin
- [x] Actualizar main.py
- [x] Crear create_admin.py
- [x] Actualizar create_tables.py
- [x] Actualizar test_main.http
- [x] Actualizar .env.example
- [x] Documentar en README

---

## 🎉 **RESULTADO FINAL**

### **Endpoints públicos (STEP 1):**
- ✅ GET /api/health
- ✅ POST /api/waitlist

### **Endpoints auth (STEP 2):**
- ✅ POST /api/auth/login
- ✅ GET /api/auth/me

### **Endpoints admin (STEP 2):**
- ✅ GET /api/admin/waitlist (paginado, filtros, búsqueda)
- ✅ GET /api/admin/metrics (agregados en tiempo real)

### **Características:**
- ✅ JWT Authentication
- ✅ Password hashing (bcrypt)
- ✅ Paginación (max 100 por página)
- ✅ Filtros múltiples
- ✅ Búsqueda parcial
- ✅ Métricas agregadas
- ✅ Logging completo
- ✅ Swagger UI documentado
- ✅ Code modular y escalable

---

**El proyecto está LISTO para conectar un frontend React/Vue/Angular** 🚀

**Documentación completa en:** http://localhost:8000/docs

