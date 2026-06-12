# 🐾 PetClinic - Sistema de Gestión Veterinaria

![React](https://img.shields.io/badge/Frontend-React-61DAFB)
![Python](https://img.shields.io/badge/Backend-Python-3776AB)
![FastAPI](https://img.shields.io/badge/API-FastAPI-009688)
![JWT](https://img.shields.io/badge/Auth-JWT-orange)
![MySQL](https://img.shields.io/badge/Database-MySQL-blue)

## 📋 Descripción

PetClinic es una aplicación web desarrollada para la administración de clínicas veterinarias.

El sistema permite gestionar propietarios, mascotas y turnos médicos desde una interfaz moderna e intuitiva, incorporando autenticación mediante JWT y control de acceso por roles.

---

## 🚀 Funcionalidades

### 🔐 Autenticación y Seguridad

* Inicio de sesión mediante JWT.
* Persistencia de sesión.
* Control de acceso por roles.
* Protección de rutas privadas.
* Restricción de acciones según permisos.

### 👤 Gestión de Propietarios

* Crear propietarios.
* Consultar propietarios.
* Editar información.
* Eliminar propietarios (solo administradores).

### 🐾 Gestión de Mascotas

* Registrar mascotas.
* Asociar mascotas a propietarios.
* Consultar historial de mascotas.
* Editar registros.
* Eliminar mascotas (solo administradores).

### 📅 Gestión de Turnos

* Agendar citas veterinarias.
* Consultar turnos.
* Modificar turnos.
* Eliminar turnos (solo administradores).

### 📊 Dashboard

* Resumen general del sistema.
* Total de propietarios registrados.
* Total de mascotas registradas.
* Total de turnos programados.
* Accesos rápidos para creación de registros.

---


## 🏗️ Arquitectura

```text
Frontend (React)
       │
       ▼
 REST API (FastAPI)
       │
       ▼
     MySQL
```

---

## 🛠️ Tecnologías Utilizadas

### Frontend

* React
* JavaScript
* HTML5
* CSS3

### Backend

* Python
* FastAPI
* JWT Authentication
* SQLAlchemy

### Base de Datos

* MySQL

### Herramientas

* Git
* GitHub
* VS Code
* Postman

---

## 👥 Roles del Sistema

### ADMIN

Puede:

* Crear propietarios.
* Editar propietarios.
* Eliminar propietarios.
* Crear mascotas.
* Editar mascotas.
* Eliminar mascotas.
* Gestionar turnos.

### USER

Puede:

* Consultar información.
* Registrar información permitida.
* No puede eliminar registros.

---

## 📂 Estructura del Proyecto

```text
PETCLINIC
│
├── backend
│   ├── app
│   │   ├── routers
│   │   ├── auth.py
│   │   ├── crud.py
│   │   ├── database.py
│   │   ├── models.py
│   │   └── main.py
│
├── frontend-web
│   ├── src
│   │   ├── pages
│   │   ├── components
│   │   ├── services
│   │   └── App.js
│
└── README.md
```

---

## ⚙️ Instalación

### Backend

```bash
cd backend

python -m venv .venv

.venv\Scripts\activate

pip install -r requirements.txt

uvicorn app.main:app --reload
```

Servidor:

```text
http://localhost:8000
```

---

### Frontend

```bash
cd frontend-web

npm install

npm start
```

Aplicación:

```text
http://localhost:3000
```

---

## 🔗 API REST

### Autenticación

```http
POST /auth/login
```

### Dueños

```http
GET    /api/duenos
POST   /api/duenos
PUT    /api/duenos/{id}
DELETE /api/duenos/{id}
```

### Mascotas

```http
GET    /api/mascotas
POST   /api/mascotas
PUT    /api/mascotas/{id}
DELETE /api/mascotas/{id}
```

### Turnos

```http
GET    /api/turnos
POST   /api/turnos
PUT    /api/turnos/{id}
DELETE /api/turnos/{id}
```

---

## 🎯 Estado del Proyecto

| Módulo           | Estado |
| ---------------- | ------ |
| Login JWT        | ✅      |
| Dashboard        | ✅      |
| Dueños           | ✅      |
| Mascotas         | ✅      |
| Turnos           | ✅      |
| Control de Roles | ✅      |
| API REST         | ✅      |
| Despliegue       | ✅      |

---

## 👨‍💻 Autor

**Michael Galindo**

Proyecto desarrollado como práctica académica y demostración de habilidades Full Stack.
