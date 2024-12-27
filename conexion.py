import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
from dotenv import load_dotenv

# Cargar las variables de entorno desde un archivo .env
load_dotenv()

# Configuración de la base de datos
TURSO_DATABASE_URL = os.getenv("TURSO_DATABASE_URL")
TURSO_AUTH_TOKEN = os.getenv("TURSO_AUTH_TOKEN")

# Construir la URL especial de SQLAlchemy para Turso
SQLALCHEMY_DATABASE_URL = f"sqlite+{TURSO_DATABASE_URL}/?authToken={TURSO_AUTH_TOKEN}&secure=true"

# Crear el motor de la base de datos
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    poolclass=QueuePool,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800,
    connect_args={"check_same_thread": False},
    echo=True
)

# Crear una sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Función para probar la conexión
def probar_conexion():
    try:
        # Crear una sesión
        session = SessionLocal()
        # Ejecutar una consulta simple
        result = session.execute("SELECT 1;")
        print("Conexión exitosa:", result.fetchone())
    except Exception as e:
        print("Error al conectar a la base de datos:", e)
    finally:
        # Cerrar la sesión
        session.close()

# Probar la conexión
probar_conexion()
