# 🏥 PetClinic — Sistema de Gestión Veterinaria

Hackathon Académico · Tecnólogo en Desarrollo de Software

---

## 📋 Descripción

Sistema web para gestión de una clínica veterinaria. Permite registrar dueños, mascotas y turnos, con autenticación JWT y control de roles (ADMIN / RECEPCIONISTA).

---

## 🗂️ Estructura del proyecto

```
petclinic/
├── backend/
│   └── app/
│       ├── routers/
│       │   ├── auth.py
│       │   ├── duenos.py
│       │   ├── mascotas.py
│       │   └── turnos.py
│       ├── crud.py
│       ├── database.py
│       ├── main.py
│       ├── models.py
│       ├── schemas.py
│       └── security.py
├── frontend-web/
│   └── src/
│       ├── pages/
│       │   ├── Login/
│       │   ├── Dashboard/
│       │   ├── Duenos/
│       │   ├── Mascotas/
│       │   └── Turnos/
│       └── services/
│           └── api.js
└── tests/
    └── test_petclinic.py
```

---

## ⚙️ Requisitos previos

- Python 3.10+
- Node.js 18+
- MySQL 8+
- pip

---

## 🚀 Cómo correr el proyecto

### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd petclinic
```

### 2. Configurar la base de datos

Crear la base de datos en MySQL:

```sql
CREATE DATABASE petclinic;
```

### 3. Configurar el backend

```bash
cd backend
pip install -r requirements.txt
```

Crear el archivo `.env` en la carpeta `backend/` con:

```
DATABASE_URL=mysql+pymysql://root:tu_password@localhost:3306/petclinic
SECRET_KEY=tu_clave_secreta
```

Iniciar el servidor:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

El backend queda disponible en: `http://localhost:8080`  
Documentación Swagger: `http://localhost:8080/docs`

### 4. Configurar el frontend

```bash
cd frontend-web
npm install
npm start
```

El frontend queda disponible en: `http://localhost:3000`

---

## 👤 Usuarios de prueba

Crear usuarios desde Swagger `POST /auth/register`:

```json
{ "username": "admin",    "password": "admin123",  "rol": "ADMIN" }
{ "username": "recepcion","password": "recep123",  "rol": "RECEPCIONISTA" }
```

---

## ✅ Correr los tests

```bash
cd backend
pip install pytest httpx
pytest tests/test_petclinic.py -v
```

---

## 🧩 Entidades del sistema

| Entidad  | Campos principales                          |
|----------|---------------------------------------------|
| Dueño    | cedula, nombre, telefono                    |
| Mascota  | id, nombre, especie, edad, cedula del dueño |
| Turno    | id, fecha, motivo, id de mascota            |
| Usuario  | username, password, rol                     |

---

## 🔐 Roles y permisos

| Acción         | ADMIN | RECEPCIONISTA |
|----------------|-------|---------------|
| Ver registros  | ✅    | ✅            |
| Crear          | ✅    | ✅            |
| Editar         | ✅    | ✅            |
| Eliminar       | ✅    | ❌            |

---

## 📌 Decisiones técnicas

- **FastAPI** para el backend por su velocidad y documentación automática con Swagger
- **JWT** para autenticación stateless con roles embebidos en el token
- **React** para el frontend con estado local y llamadas REST directas
- **MySQL** como base de datos relacional para mantener integridad referencial entre dueños, mascotas y turnos

---

## 👥 Equipo

- Michael Galindo
