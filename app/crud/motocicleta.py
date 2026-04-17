from sqlalchemy.orm import Session
from app.models.motocicleta import Motocicleta
from app.models.item import Item
from app.models.trabajo_servicio import TrabajoServicio
from app.schemas.motocicleta import MotocicletaCreate, MotocicletaUpdate

def create_motocicleta(db: Session, motocicleta: MotocicletaCreate) -> Motocicleta:
    """Crear una nueva motocicleta"""
    data = motocicleta.model_dump()
    servicio_ids = data.pop("servicio_ids", [])
    trabajos_reparacion = [trabajo.strip() for trabajo in data.pop("trabajos_reparacion", []) if trabajo.strip()]

    if servicio_ids:
        servicios_validos = db.query(Item).filter(Item.id.in_(servicio_ids)).all()
        servicios_validos_ids = {servicio.id for servicio in servicios_validos}
        servicios_invalidos = [servicio_id for servicio_id in servicio_ids if servicio_id not in servicios_validos_ids]

        if servicios_invalidos:
            raise ValueError(f"Servicios no válidos: {', '.join(map(str, servicios_invalidos))}")

    db_motocicleta = Motocicleta(**data)
    db.add(db_motocicleta)
    db.flush()

    db.add(
        TrabajoServicio(
            motocicleta_id=db_motocicleta.id,
            item_id=None,
            estado="pendiente",
        )
    )

    if servicio_ids:
        for servicio_id in servicio_ids:
            db.add(
                TrabajoServicio(
                    motocicleta_id=db_motocicleta.id,
                    item_id=servicio_id,
                    estado="pendiente",
                )
            )

    if trabajos_reparacion:
        for trabajo in trabajos_reparacion:
            db.add(
                TrabajoServicio(
                    motocicleta_id=db_motocicleta.id,
                    item_id=None,
                    detalle_reparacion=trabajo,
                    estado="pendiente",
                )
            )

    db.commit()
    db.refresh(db_motocicleta)
    return db_motocicleta

def get_motocicleta_by_id(db: Session, motocicleta_id: int) -> Motocicleta | None:
    """Obtener motocicleta por ID"""
    return db.query(Motocicleta).filter(Motocicleta.id == motocicleta_id).first()

def get_all_motocicletas(db: Session) -> list[Motocicleta]:
    """Obtener todas las motocicletas"""
    return db.query(Motocicleta).all()

def update_motocicleta(db: Session, motocicleta_id: int, motocicleta_update: MotocicletaUpdate) -> Motocicleta | None:
    """Actualizar una motocicleta"""
    db_motocicleta = db.query(Motocicleta).filter(Motocicleta.id == motocicleta_id).first()
    if db_motocicleta:
        update_data = motocicleta_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_motocicleta, key, value)
        db.commit()
        db.refresh(db_motocicleta)
    return db_motocicleta

def delete_motocicleta(db: Session, motocicleta_id: int) -> bool:
    """Eliminar una motocicleta"""
    db_motocicleta = db.query(Motocicleta).filter(Motocicleta.id == motocicleta_id).first()
    if db_motocicleta:
        db.delete(db_motocicleta)
        db.commit()
        return True
    return False
