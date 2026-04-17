from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class Motocicleta(Base):
    __tablename__ = "motocicletas"

    id = Column(Integer, primary_key=True, index=True)
    piloto_id = Column(Integer, ForeignKey("pilotos.id"), nullable=False)
    modelo = Column(String, nullable=False)
    año = Column(Integer, nullable=False)
    hora_ingreso = Column(DateTime(timezone=True), server_default=func.now())
    
    piloto = relationship("Piloto", backref="motocicletas")
    trabajos_servicio = relationship(
        "TrabajoServicio",
        back_populates="motocicleta",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Motocicleta(id={self.id}, modelo={self.modelo}, piloto_id={self.piloto_id})>"
