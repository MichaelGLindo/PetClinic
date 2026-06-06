from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app import models, database
from app.routers import duenos, mascotas, turnos

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

@app.get("/")
def read_root():
    return {
        "status": "OK",
        "message": "Bienvenido al Backend de PetClinic (FastAPI)",
        "docs_url": "/docs"
    }
