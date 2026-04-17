from sqlalchemy.orm import Session
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate
from app.auth.jwt import hash_password

def create_usuario(db: Session, usuario: UsuarioCreate) -> Usuario:
    """Crear un nuevo usuario"""
    db_usuario = Usuario(
        email=usuario.email,
        rol=usuario.rol,
        contraseña=hash_password(usuario.contraseña)
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def get_usuario_by_email(db: Session, email: str) -> Usuario | None:
    """Obtener usuario por email"""
    return db.query(Usuario).filter(Usuario.email == email).first()

def get_usuario_by_id(db: Session, user_id: int) -> Usuario | None:
    """Obtener usuario por ID"""
    return db.query(Usuario).filter(Usuario.id == user_id).first()

def get_all_usuarios(db: Session) -> list[Usuario]:
    """Obtener todos los usuarios"""
    return db.query(Usuario).all()

def delete_usuario(db: Session, user_id: int) -> bool:
    """Eliminar un usuario"""
    db_usuario = db.query(Usuario).filter(Usuario.id == user_id).first()
    if db_usuario:
        db.delete(db_usuario)
        db.commit()
        return True
    return False
