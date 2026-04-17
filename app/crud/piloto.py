from sqlalchemy.orm import Session
from app.models.piloto import Piloto
from app.schemas.piloto import PilotoCreate, PilotoUpdate

def create_piloto(db: Session, piloto: PilotoCreate) -> Piloto:
    """Crear un nuevo piloto"""
    db_piloto = Piloto(**piloto.model_dump())
    db.add(db_piloto)
    db.commit()
    db.refresh(db_piloto)
    return db_piloto

def get_piloto_by_id(db: Session, piloto_id: int) -> Piloto | None:
    """Obtener piloto por ID"""
    return db.query(Piloto).filter(Piloto.id == piloto_id).first()

def get_all_pilotos(db: Session) -> list[Piloto]:
    """Obtener todos los pilotos"""
    return db.query(Piloto).all()

def update_piloto(db: Session, piloto_id: int, piloto_update: PilotoUpdate) -> Piloto | None:
    """Actualizar un piloto"""
    db_piloto = db.query(Piloto).filter(Piloto.id == piloto_id).first()
    if db_piloto:
        update_data = piloto_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_piloto, key, value)
        db.commit()
        db.refresh(db_piloto)
    return db_piloto

def delete_piloto(db: Session, piloto_id: int) -> bool:
    """Eliminar un piloto"""
    db_piloto = db.query(Piloto).filter(Piloto.id == piloto_id).first()
    if db_piloto:
        db.delete(db_piloto)
        db.commit()
        return True
    return False
