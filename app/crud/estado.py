from sqlalchemy.orm import Session
from app.models.trabajo_servicio import TrabajoServicio
from app.models.motocicleta import Motocicleta
from app.models.piloto import Piloto
from app.models.item import Item


ESTADOS_VALIDOS = {"pendiente", "en proceso", "terminado"}


def create_trabajos_servicio(db: Session, motocicleta_id: int, servicio_ids: list[int]) -> list[TrabajoServicio]:
    if not servicio_ids:
        return []

    servicios_validos = db.query(Item).filter(Item.id.in_(servicio_ids)).all()
    servicios_validos_ids = {servicio.id for servicio in servicios_validos}
    servicio_ids_invalidos = [servicio_id for servicio_id in servicio_ids if servicio_id not in servicios_validos_ids]

    if servicio_ids_invalidos:
        raise ValueError(f"Servicios no válidos: {', '.join(map(str, servicio_ids_invalidos))}")

    trabajos = []
    for servicio_id in servicio_ids:
        trabajo = TrabajoServicio(
            motocicleta_id=motocicleta_id,
            item_id=servicio_id,
            estado="pendiente",
        )
        db.add(trabajo)
        trabajos.append(trabajo)

    return trabajos


def get_all_estados(db: Session) -> list[dict]:
    rows = (
        db.query(TrabajoServicio, Motocicleta, Piloto, Item)
        .join(Motocicleta, TrabajoServicio.motocicleta_id == Motocicleta.id)
        .join(Piloto, Motocicleta.piloto_id == Piloto.id)
        .outerjoin(Item, TrabajoServicio.item_id == Item.id)
        .order_by(TrabajoServicio.fecha_creacion.desc())
        .all()
    )

    estados = []
    for trabajo, motocicleta, piloto, item in rows:
        item_nombre = "Estado general"
        if item is not None:
            item_nombre = item.nombre_item
        elif trabajo.detalle_reparacion:
            item_nombre = trabajo.detalle_reparacion

        estados.append(
            {
                "id": trabajo.id,
                "motocicleta_id": motocicleta.id,
                "motocicleta_modelo": motocicleta.modelo,
                "piloto_nombre": piloto.nombre,
                "item_id": item.id if item else None,
                "item_nombre": item_nombre,
                "estado": trabajo.estado,
                "fecha_creacion": trabajo.fecha_creacion,
                "fecha_actualizacion": trabajo.fecha_actualizacion,
                "tiene_servicio": item is not None,
                "es_estado_general": item is None and not trabajo.detalle_reparacion,
            }
        )
    return estados


def update_estado(db: Session, trabajo_id: int, estado: str) -> TrabajoServicio | None:
    if estado not in ESTADOS_VALIDOS:
        raise ValueError("Estado inválido")

    trabajo = db.query(TrabajoServicio).filter(TrabajoServicio.id == trabajo_id).first()
    if not trabajo:
        return None

    trabajos_motocicleta = (
        db.query(TrabajoServicio)
        .filter(TrabajoServicio.motocicleta_id == trabajo.motocicleta_id)
        .all()
    )

    for registro in trabajos_motocicleta:
        registro.estado = estado

    db.commit()
    db.refresh(trabajo)
    return trabajo


def update_estado_motocicleta(db: Session, motocicleta_id: int, estado: str) -> Motocicleta | None:
    if estado not in ESTADOS_VALIDOS:
        raise ValueError("Estado inválido")

    motocicleta = db.query(Motocicleta).filter(Motocicleta.id == motocicleta_id).first()
    if not motocicleta:
        return None

    trabajos = db.query(TrabajoServicio).filter(TrabajoServicio.motocicleta_id == motocicleta_id).all()
    if not trabajos:
        return None

    for trabajo in trabajos:
        trabajo.estado = estado

    db.commit()
    db.refresh(motocicleta)
    return motocicleta