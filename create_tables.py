"""
Script para crear las tablas en PostgreSQL
Ejecutar: python create_tables.py
"""
from app.db.database import engine, Base
from app.models import waitlist, admin_user  # Importar ambos modelos


def create_tables():
    """Crea todas las tablas definidas en los modelos"""
    print("🔧 Creando tablas en PostgreSQL...")

    try:
        # Crear todas las tablas
        Base.metadata.create_all(bind=engine)
        print("✅ Tablas creadas exitosamente!")

        # Mostrar tablas creadas
        print("\n📋 Tablas en la base de datos:")
        for table_name in Base.metadata.tables.keys():
            print(f"  - {table_name}")

    except Exception as e:
        print(f"❌ Error al crear tablas: {e}")
        raise


if __name__ == "__main__":
    create_tables()

