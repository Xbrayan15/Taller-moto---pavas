from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.usuario import Usuario
from app.schemas.piloto import PilotoCreate, PilotoResponse, PilotoUpdate
from app.crud.piloto import (
    create_piloto, get_piloto_by_id, get_all_pilotos, update_piloto, delete_piloto
)
from app.auth.jwt import get_current_user

router = APIRouter(prefix="/api/pilotos", tags=["Pilotos"])

@router.post("/", response_model=PilotoResponse)
def create_piloto_endpoint(
    piloto: PilotoCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Crear un nuevo piloto"""
    return create_piloto(db=db, piloto=piloto)

@router.get("/{piloto_id}", response_model=PilotoResponse)
def get_piloto_endpoint(
    piloto_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Obtener un piloto por ID"""
    db_piloto = get_piloto_by_id(db, piloto_id)
    if not db_piloto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Piloto no encontrado"
        )
    return db_piloto

@router.get("/", response_model=list[PilotoResponse])
def get_pilotos(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Obtener todos los pilotos"""
    return get_all_pilotos(db)

@router.put("/{piloto_id}", response_model=PilotoResponse)
def update_piloto_endpoint(
    piloto_id: int,
    piloto_update: PilotoUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Actualizar un piloto"""
    db_piloto = update_piloto(db, piloto_id, piloto_update)
    if not db_piloto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Piloto no encontrado"
        )
    return db_piloto

@router.delete("/{piloto_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_piloto_endpoint(
    piloto_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Eliminar un piloto"""
    if not delete_piloto(db, piloto_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Piloto no encontrado"
        )
