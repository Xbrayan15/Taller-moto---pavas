from sqlalchemy.orm import Session
from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate

def create_item(db: Session, item: ItemCreate) -> Item:
    """Crear un nuevo item"""
    db_item = Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_item_by_id(db: Session, item_id: int) -> Item | None:
    """Obtener item por ID"""
    return db.query(Item).filter(Item.id == item_id).first()

def get_all_items(db: Session) -> list[Item]:
    """Obtener todos los items"""
    return db.query(Item).all()

def update_item(db: Session, item_id: int, item_update: ItemUpdate) -> Item | None:
    """Actualizar un item"""
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item:
        update_data = item_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_item, key, value)
        db.commit()
        db.refresh(db_item)
    return db_item

def delete_item(db: Session, item_id: int) -> bool:
    """Eliminar un item"""
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
        return True
    return False
