from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ItemCreate(BaseModel):
    nombre_item: str
    descripcion: str | None = None
    precio: str | None = None

class ItemResponse(BaseModel):
    id: int
    nombre_item: str
    descripcion: Optional[str]
    precio: Optional[str]
    fecha_creacion: datetime

    class Config:
        from_attributes = True

class ItemUpdate(BaseModel):
    nombre_item: str | None = None
    descripcion: str | None = None
    precio: str | None = None
