from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import IntegrityError
from app import models, database
from app.routers import duenos, mascotas, turnos, dashboard, historiales, auth

# Create DB tables (similar to spring.jpa.hibernate.ddl-auto=update)
try:
    models.Base.metadata.create_all(bind=database.engine)
    # Check if dueno_cedula column exists in usuarios table and add it if missing
    from sqlalchemy import inspect, text
    inspector = inspect(database.engine)
    if "usuarios" in inspector.get_table_names():
        columns = [c["name"] for c in inspector.get_columns("usuarios")]
        if "dueno_cedula" not in columns:
            with database.engine.connect() as conn:
                conn.execute(text("ALTER TABLE usuarios ADD COLUMN dueno_cedula VARCHAR(255) NULL"))
                try:
                    conn.execute(text("ALTER TABLE usuarios ADD CONSTRAINT fk_usuarios_duenos FOREIGN KEY (dueno_cedula) REFERENCES duenos(cedula) ON DELETE SET NULL"))
                except Exception as fk_err:
                    print(f"FK constraint warning: {fk_err}")
                conn.commit()
                print("Successfully added dueno_cedula column to usuarios table.")
except Exception as e:
    print(f"Warning: Could not create/migrate tables on startup. Make sure your MySQL database server is running: {e}")

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
    "https://pet-clinic-oywb.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth.router)
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
