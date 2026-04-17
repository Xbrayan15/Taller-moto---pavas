from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Piloto(Base):
    __tablename__ = "pilotos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False, index=True)
    telefono = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<Piloto(id={self.id}, nombre={self.nombre}, email={self.email})>"
