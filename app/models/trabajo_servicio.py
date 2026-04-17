from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class TrabajoServicio(Base):
    __tablename__ = "trabajos_servicios"

    id = Column(Integer, primary_key=True, index=True)
    motocicleta_id = Column(Integer, ForeignKey("motocicletas.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=True)
    detalle_reparacion = Column(String, nullable=True)
    estado = Column(String, nullable=False, default="pendiente")
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_actualizacion = Column(DateTime(timezone=True), onupdate=func.now())

    motocicleta = relationship("Motocicleta", back_populates="trabajos_servicio")
    item = relationship("Item")

    def __repr__(self):
        return (
            f"<TrabajoServicio(id={self.id}, motocicleta_id={self.motocicleta_id}, "
            f"item_id={self.item_id}, detalle_reparacion={self.detalle_reparacion}, estado={self.estado})>"
        )