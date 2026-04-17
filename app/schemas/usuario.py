from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional

class UsuarioCreate(BaseModel):
    email: EmailStr
    rol: str  # "admin" o "mecanico"
    contraseña: str

class UsuarioResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    email: str
    rol: str
    fecha_creacion: datetime

class UsuarioLogin(BaseModel):
    email: EmailStr
    contraseña: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None


class UsuarioChangePassword(BaseModel):
    contraseña_actual: str
    contraseña_nueva: str
