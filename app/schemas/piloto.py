from pydantic import BaseModel, EmailStr
from datetime import datetime

class PilotoCreate(BaseModel):
    nombre: str
    telefono: str
    email: EmailStr

class PilotoResponse(BaseModel):
    id: int
    nombre: str
    telefono: str
    email: str
    fecha_creacion: datetime

    class Config:
        orm_mode = True

class PilotoUpdate(BaseModel):
    nombre: str | None = None
    telefono: str | None = None
    email: EmailStr | None = None
