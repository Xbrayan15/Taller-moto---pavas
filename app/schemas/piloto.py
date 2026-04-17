from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime

class PilotoCreate(BaseModel):
    nombre: str
    telefono: str
    email: EmailStr

class PilotoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    nombre: str
    telefono: str
    email: str
    fecha_creacion: datetime

class PilotoUpdate(BaseModel):
    nombre: str | None = None
    telefono: str | None = None
    email: EmailStr | None = None
