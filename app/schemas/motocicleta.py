from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional

class MotocicletaCreate(BaseModel):
    piloto_id: int
    modelo: str
    año: int
    servicio_ids: list[int] = Field(default_factory=list)
    trabajos_reparacion: list[str] = Field(default_factory=list)

class MotocicletaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    piloto_id: int
    modelo: str
    año: int
    hora_ingreso: datetime

class MotocicletaUpdate(BaseModel):
    modelo: str | None = None
    año: int | None = None
    servicio_ids: list[int] | None = None
    trabajos_reparacion: list[str] | None = None
