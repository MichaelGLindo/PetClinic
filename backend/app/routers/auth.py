from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Usuario
from app.schemas import UsuarioCreate
from app.schemas import UsuarioLogin

from app.security import (
    hash_password,
    verify_password,
    create_access_token
)

router = APIRouter(
    prefix="/auth",
    tags=["Autenticacion"]
)


@router.post("/register")
def register(
        usuario: UsuarioCreate,
        db: Session = Depends(get_db)
):

    existe = db.query(Usuario).filter(
        Usuario.username == usuario.username
    ).first()

    if existe:
        raise HTTPException(
            status_code=400,
            detail="Usuario ya existe"
        )

    nuevo = Usuario(
        username=usuario.username,
        password=hash_password(
            usuario.password),
            rol=usuario.rol
        
    )

    db.add(nuevo)
    db.commit()

    return {
        "mensaje": "Usuario creado"
    }

@router.post("/login")
def login(
        usuario: UsuarioLogin,
        db: Session = Depends(get_db)
):

    user = db.query(Usuario).filter(
        Usuario.username == usuario.username
    ).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Credenciales invalidas"
        )

    if not verify_password(
            usuario.password,
            user.password):

        raise HTTPException(
            status_code=401,
            detail="Credenciales invalidas"
        )

    token = create_access_token({
        "sub": user.username,
        "rol": user.rol   
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }