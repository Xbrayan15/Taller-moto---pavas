from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.usuario import Usuario
from app.schemas.motocicleta import MotocicletaCreate, MotocicletaResponse, MotocicletaUpdate
from app.crud.motocicleta import (
    create_motocicleta, get_motocicleta_by_id, get_all_motocicletas, update_motocicleta, delete_motocicleta
)
from app.auth.jwt import get_current_user

router = APIRouter(prefix="/api/motocicletas", tags=["Motocicletas"])

@router.post("/", response_model=MotocicletaResponse)
def create_motocicleta_endpoint(
    motocicleta: MotocicletaCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Crear una nueva motocicleta"""
    try:
        return create_motocicleta(db=db, motocicleta=motocicleta)
    except ValueError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )

@router.get("/{motocicleta_id}", response_model=MotocicletaResponse)
def get_motocicleta_endpoint(
    motocicleta_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Obtener una motocicleta por ID"""
    db_motocicleta = get_motocicleta_by_id(db, motocicleta_id)
    if not db_motocicleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Motocicleta no encontrada"
        )
    return db_motocicleta

@router.get("/", response_model=list[MotocicletaResponse])
def get_motocicletas(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Obtener todas las motocicletas"""
    return get_all_motocicletas(db)

@router.put("/{motocicleta_id}", response_model=MotocicletaResponse)
def update_motocicleta_endpoint(
    motocicleta_id: int,
    motocicleta_update: MotocicletaUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Actualizar una motocicleta"""
    db_motocicleta = update_motocicleta(db, motocicleta_id, motocicleta_update)
    if not db_motocicleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Motocicleta no encontrada"
        )
    return db_motocicleta

@router.delete("/{motocicleta_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_motocicleta_endpoint(
    motocicleta_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Eliminar una motocicleta"""
    if not delete_motocicleta(db, motocicleta_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Motocicleta no encontrada"
        )
