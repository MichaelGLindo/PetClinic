from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Usuario, Dueno
from app.schemas import UsuarioCreate, UsuarioLogin, ClientRegister

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
        "rol": user.rol,
        "dueno_cedula": user.dueno_cedula
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }

@router.post("/register-client")
def register_client(
    client: ClientRegister,
    db: Session = Depends(get_db)
):
    # Check if user already exists
    existe_usuario = db.query(Usuario).filter(Usuario.username == client.username).first()
    if existe_usuario:
        raise HTTPException(status_code=400, detail="El nombre de usuario ya está registrado")
    
    # Check if dueno already exists
    existe_dueno = db.query(Dueno).filter(Dueno.cedula == client.cedula).first()
    if existe_dueno:
        raise HTTPException(status_code=400, detail="Ya existe un dueño registrado con esa cédula")
    
    # Create Dueno
    nuevo_dueno = Dueno(
        cedula=client.cedula,
        nombre=client.nombre,
        telefono=client.telefono
    )
    db.add(nuevo_dueno)
    
    # Create Usuario
    nuevo_usuario = Usuario(
        username=client.username,
        password=hash_password(client.password),
        rol="USER",
        dueno_cedula=client.cedula
    )
    db.add(nuevo_usuario)
    db.commit()
    
    return {"mensaje": "Dueño y usuario registrados correctamente"}