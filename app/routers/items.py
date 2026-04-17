from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.usuario import Usuario
from app.schemas.item import ItemCreate, ItemResponse, ItemUpdate
from app.crud.item import (
    create_item, get_item_by_id, get_all_items, update_item, delete_item
)
from app.auth.jwt import get_current_user

router = APIRouter(prefix="/api/items", tags=["Items"])

@router.post("/", response_model=ItemResponse)
def create_item_endpoint(
    item: ItemCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Crear un nuevo item (servicio)"""
    return create_item(db=db, item=item)

@router.get("/{item_id}", response_model=ItemResponse)
def get_item_endpoint(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Obtener un item por ID"""
    db_item = get_item_by_id(db, item_id)
    if not db_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item no encontrado"
        )
    return db_item

@router.get("/", response_model=list[ItemResponse])
def get_items(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Obtener todos los items (servicios)"""
    return get_all_items(db)

@router.put("/{item_id}", response_model=ItemResponse)
def update_item_endpoint(
    item_id: int,
    item_update: ItemUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Actualizar un item"""
    db_item = update_item(db, item_id, item_update)
    if not db_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item no encontrado"
        )
    return db_item

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item_endpoint(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Eliminar un item"""
    if not delete_item(db, item_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item no encontrado"
        )
