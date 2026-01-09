"""
Script para crear el primer usuario administrador
Ejecutar: python create_admin.py
"""
from app.db.database import SessionLocal
from app.services.auth_service import AuthService
from app.models.admin_user import AdminUser


def create_first_admin():
    """Crea el primer admin si no existe"""
    db = SessionLocal()

    try:
        # Verificar si ya existe algún admin
        existing_admin = db.query(AdminUser).first()

        if existing_admin:
            print(f"⚠️  Admin ya existe: {existing_admin.email}")
            return

        # Crear admin por defecto
        # TODO: En producción, leer desde variables de entorno
        import os
        email = os.getenv("ADMIN_EMAIL")
        password = os.getenv("ADMIN_PASSWORD")

        if not email or not password:
            print("❌ Error: ADMIN_EMAIL y ADMIN_PASSWORD deben estar configurados")
            return

        admin = AuthService.create_admin_user(
            db=db,
            email=email,
            password=password,
            full_name="Admin Principal"
        )

        print(f"✅ Admin creado exitosamente!")
        print(f"   Email: {email}")
        print(f"   Password: {password}")
        print(f"   ⚠️  CAMBIAR PASSWORD EN PRODUCCIÓN!")

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        db.rollback()

    finally:
        db.close()


if __name__ == "__main__":
    print("🔧 Creando primer usuario administrador...")
    create_first_admin()

