from datetime import datetime
from typing import Literal, Optional
from pydantic import BaseModel


EstadoValor = Literal["pendiente", "en proceso", "terminado"]


class EstadoServicioResponse(BaseModel):
    id: int
    motocicleta_id: int
    motocicleta_modelo: str
    piloto_nombre: str
    item_id: Optional[int] = None
    item_nombre: Optional[str] = None
    estado: EstadoValor
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime] = None
    tiene_servicio: bool = True
    es_estado_general: bool = False

    class Config:
        from_attributes = True


class EstadoUpdate(BaseModel):
    estado: EstadoValor


class EstadoMotocicletaResponse(BaseModel):
    motocicleta_id: int
    motocicleta_modelo: str
    piloto_nombre: str
    estado: EstadoValor