from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    rol = Column(String, nullable=False)  # "admin" o "mecanico"
    contraseña = Column(String, nullable=False)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<Usuario(id={self.id}, email={self.email}, rol={self.rol})>"
