from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.usuario import Usuario
from app.schemas.estado import EstadoServicioResponse, EstadoUpdate, EstadoMotocicletaResponse
from app.crud.estado import get_all_estados, update_estado, update_estado_motocicleta
from app.auth.jwt import get_current_user


router = APIRouter(prefix="/api/estados", tags=["Estados"])


@router.get("/", response_model=list[EstadoServicioResponse])
def listar_estados(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    return get_all_estados(db)


@router.patch("/{trabajo_id}", response_model=EstadoServicioResponse)
def cambiar_estado(
    trabajo_id: int,
    estado_update: EstadoUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    trabajo = update_estado(db, trabajo_id, estado_update.estado)
    if not trabajo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registro de estado no encontrado"
        )

    return {
        "id": trabajo.id,
        "motocicleta_id": trabajo.motocicleta_id,
        "motocicleta_modelo": trabajo.motocicleta.modelo,
        "piloto_nombre": trabajo.motocicleta.piloto.nombre,
        "item_id": trabajo.item_id,
        "item_nombre": (
            trabajo.item.nombre_item
            if trabajo.item
            else (trabajo.detalle_reparacion or "Estado general")
        ),
        "estado": trabajo.estado,
        "fecha_creacion": trabajo.fecha_creacion,
        "fecha_actualizacion": trabajo.fecha_actualizacion,
        "tiene_servicio": trabajo.item is not None,
        "es_estado_general": trabajo.item is None and not trabajo.detalle_reparacion,
    }


@router.patch("/motocicleta/{motocicleta_id}", response_model=EstadoMotocicletaResponse)
def cambiar_estado_motocicleta(
    motocicleta_id: int,
    estado_update: EstadoUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    motocicleta = update_estado_motocicleta(db, motocicleta_id, estado_update.estado)
    if not motocicleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Motocicleta o estado no encontrado"
        )

    return {
        "motocicleta_id": motocicleta.id,
        "motocicleta_modelo": motocicleta.modelo,
        "piloto_nombre": motocicleta.piloto.nombre,
        "estado": estado_update.estado,
    }