from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from app.database import get_db
from app.models.usuario import Usuario
from app.schemas.usuario import (
    UsuarioCreate,
    UsuarioResponse,
    UsuarioLogin,
    Token,
    UsuarioChangePassword,
)
from app.crud.usuario import (
    create_usuario, get_usuario_by_email, get_all_usuarios, delete_usuario
)
from app.auth.jwt import (
    create_access_token, verify_password, hash_password, get_current_user, verify_admin
)
from app.config import settings

router = APIRouter(prefix="/api/usuarios", tags=["Usuarios"])

@router.post("/registro", response_model=UsuarioResponse)
def registro(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    """Registrar un nuevo usuario"""
    # Verificar si el usuario ya existe
    db_usuario = get_usuario_by_email(db, email=usuario.email)
    if db_usuario:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )
    
    return create_usuario(db=db, usuario=usuario)

@router.post("/login", response_model=Token)
def login(usuario_login: UsuarioLogin, db: Session = Depends(get_db)):
    """Iniciar sesión y obtener token"""
    db_usuario = get_usuario_by_email(db, email=usuario_login.email)
    
    if not db_usuario or not verify_password(usuario_login.contraseña, db_usuario.contraseña):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": db_usuario.email},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UsuarioResponse)
def get_me(current_user: Usuario = Depends(get_current_user)):
    """Obtener información del usuario actual"""
    return current_user

@router.get("/", response_model=list[UsuarioResponse])
def get_usuarios(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(verify_admin)
):
    """Obtener todos los usuarios (solo admin)"""
    return get_all_usuarios(db)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_usuario_endpoint(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(verify_admin)
):
    """Eliminar un usuario (solo admin)"""
    if not delete_usuario(db, user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )


@router.patch("/cambiar-password", status_code=status.HTTP_200_OK)
def cambiar_password(
    payload: UsuarioChangePassword,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Permite al usuario actual cambiar su contraseña."""
    if not verify_password(payload.contraseña_actual, current_user.contraseña):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La contraseña actual no es correcta"
        )

    if payload.contraseña_actual == payload.contraseña_nueva:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La nueva contraseña debe ser diferente"
        )

    current_user.contraseña = hash_password(payload.contraseña_nueva)
    db.commit()

    return {"mensaje": "Contraseña actualizada correctamente"}
