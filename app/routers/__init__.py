# app/routers/__init__.py
from app.routers.usuarios import router as usuarios_router
from app.routers.pilotos import router as pilotos_router
from app.routers.motocicletas import router as motocicletas_router
from app.routers.items import router as items_router
from app.routers.estados import router as estados_router

__all__ = ["usuarios_router", "pilotos_router", "motocicletas_router", "items_router", "estados_router"]
