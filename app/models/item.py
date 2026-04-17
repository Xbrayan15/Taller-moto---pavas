from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    nombre_item = Column(String, nullable=False, index=True)
    descripcion = Column(String)
    precio = Column(String)  # Puede ser modificado según necesidad
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<Item(id={self.id}, nombre_item={self.nombre_item})>"
