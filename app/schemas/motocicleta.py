from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from pydantic import Field

class MotocicletaCreate(BaseModel):
    piloto_id: int
    modelo: str
    año: int
    servicio_ids: list[int] = Field(default_factory=list)
    trabajos_reparacion: list[str] = Field(default_factory=list)

class MotocicletaResponse(BaseModel):
    id: int
    piloto_id: int
    modelo: str
    año: int
    hora_ingreso: datetime

    class Config:
        orm_mode = True

class MotocicletaUpdate(BaseModel):
    modelo: str | None = None
    año: int | None = None
