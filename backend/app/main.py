from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import IntegrityError
from app import models, database
from app.routers import duenos, mascotas, turnos, dashboard, historiales

# Create DB tables (similar to spring.jpa.hibernate.ddl-auto=update)
try:
    models.Base.metadata.create_all(bind=database.engine)
except Exception as e:
    print(f"Warning: Could not create tables on startup. Make sure your MySQL database server is running and configured correctly: {e}")

app = FastAPI(
    title="PetClinic API",
    description="Python FastAPI backend for PetClinic",
    version="1.0.0"
)

@app.exception_handler(IntegrityError)
def integrity_exception_handler(request: Request, exc: IntegrityError):
    error_msg = str(exc.orig)
    if "Duplicate entry" in error_msg:
        return JSONResponse(
            status_code=400,
            content={"detail": "Ya existe un registro con esa cédula o clave identificadora."}
        )
    elif "Cannot delete or update a parent row" in error_msg:
        return JSONResponse(
            status_code=400,
            content={"detail": "No se puede eliminar el registro porque tiene datos relacionados asociados."}
        )
    elif "a foreign key constraint fails" in error_msg:
        return JSONResponse(
            status_code=400,
            content={"detail": "El registro relacionado especificado no existe."}
        )
    return JSONResponse(
        status_code=400,
        content={"detail": f"Error de integridad en la base de datos: {error_msg}"}
    )

# CORS configurations matching @CrossOrigin(origins = "http://localhost:3000")
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",  # Vite default port
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(duenos.router)
app.include_router(mascotas.router)
app.include_router(turnos.router)
app.include_router(dashboard.router)
app.include_router(historiales.router)

@app.get("/")
def read_root():
    return {
        "status": "OK",
        "message": "Bienvenido al Backend de PetClinic (FastAPI)",
        "docs_url": "/docs"
    }
