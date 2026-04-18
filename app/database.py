from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import settings

# Crear la URL de la base de datos
SQLALCHEMY_DATABASE_URL = settings.database_url

# Crear el motor de la base de datos
engine_kwargs = {}
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    engine_kwargs["connect_args"] = {"check_same_thread": False}

engine = create_engine(SQLALCHEMY_DATABASE_URL, **engine_kwargs)

# Crear la sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos
Base = declarative_base()

# Función para obtener la sesión de la BD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
