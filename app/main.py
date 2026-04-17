from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from app.database import engine, Base
from app.config import settings
from app.models import Usuario, Piloto, Motocicleta, Item, TrabajoServicio
from app.routers import (
    usuarios_router, pilotos_router, motocicletas_router, items_router, estados_router
)

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)


def _migrate_trabajos_servicios_item_nullable() -> None:
    """Compatibilidad para SQLite: permitir item_id nulo sin perder datos."""
    with engine.begin() as connection:
        columns = connection.execute(text("PRAGMA table_info(trabajos_servicios)")).mappings().all()
        if not columns:
            return

        item_column = next((column for column in columns if column["name"] == "item_id"), None)
        if not item_column or item_column["notnull"] == 0:
            return

        connection.execute(text("PRAGMA foreign_keys=OFF"))
        connection.execute(text("""
            CREATE TABLE trabajos_servicios_new (
                id INTEGER NOT NULL PRIMARY KEY,
                motocicleta_id INTEGER NOT NULL,
                item_id INTEGER,
                detalle_reparacion VARCHAR,
                estado VARCHAR NOT NULL,
                fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
                fecha_actualizacion DATETIME,
                FOREIGN KEY(motocicleta_id) REFERENCES motocicletas (id),
                FOREIGN KEY(item_id) REFERENCES items (id)
            )
        """))
        connection.execute(text("""
            INSERT INTO trabajos_servicios_new (
                id,
                motocicleta_id,
                item_id,
                detalle_reparacion,
                estado,
                fecha_creacion,
                fecha_actualizacion
            )
            SELECT
                id,
                motocicleta_id,
                item_id,
                NULL,
                estado,
                fecha_creacion,
                fecha_actualizacion
            FROM trabajos_servicios
        """))
        connection.execute(text("DROP TABLE trabajos_servicios"))
        connection.execute(text("ALTER TABLE trabajos_servicios_new RENAME TO trabajos_servicios"))
        connection.execute(text("CREATE INDEX IF NOT EXISTS ix_trabajos_servicios_id ON trabajos_servicios (id)"))
        connection.execute(text("PRAGMA foreign_keys=ON"))


_migrate_trabajos_servicios_item_nullable()


def _migrate_trabajos_servicios_add_detalle_reparacion() -> None:
    """Agregar columna detalle_reparacion si aún no existe."""
    with engine.begin() as connection:
        columns = connection.execute(text("PRAGMA table_info(trabajos_servicios)")).mappings().all()
        if not columns:
            return

        has_detalle = any(column["name"] == "detalle_reparacion" for column in columns)
        if not has_detalle:
            connection.execute(text("ALTER TABLE trabajos_servicios ADD COLUMN detalle_reparacion VARCHAR"))


_migrate_trabajos_servicios_add_detalle_reparacion()

# Crear la aplicación FastAPI
app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    description="API para gestionar un taller de motos"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar los orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir los routers
app.include_router(usuarios_router)
app.include_router(pilotos_router)
app.include_router(motocicletas_router)
app.include_router(items_router)
app.include_router(estados_router)

@app.get("/")
def read_root():
    """Endpoint raíz de la API"""
    return {
        "mensaje": "Bienvenido a la API del Taller de Motos",
        "version": settings.api_version,
        "endpoints": {
            "usuarios": "/api/usuarios",
            "pilotos": "/api/pilotos",
            "motocicletas": "/api/motocicletas",
            "items": "/api/items",
            "estados": "/api/estados"
        }
    }

@app.get("/health")
def health_check():
    """Verificar la salud de la API"""
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
