# Arquitectura del Sistema PetClinic

## Diagrama de Arquitectura General

```mermaid
graph TB
    subgraph "Capa de Presentación"
        FW[Frontend Web<br/>React 19 + React Router]
        AM[App Móvil<br/>Carpeta vacía - Pendiente]
    end

    subgraph "Capa de Backend"
        subgraph "API REST (Activa)"
            FA[FastAPI<br/>Python]
            subgraph "Seguridad"
                JWT[JWT Auth]
                RBAC[Role-Based Access<br/>ADMIN / USER]
            end
            subgraph "Endpoints"
                AUTH[/auth/*<br/>login, register]
                DUENOS[/api/duenos<br/>CRUD]
                MASCOTAS[/api/mascotas<br/>CRUD]
                TURNOS[/api/turnos<br/>CRUD]
                HIST[/api/historiales<br/>CRUD]
                DASH[/api/dashboard<br/>stats]
            end
        end
        subgraph "API Secundaria (Incompleta)"
            SB[Spring Boot<br/>Java 17]
            SVC[Service Layer<br/>Vacío]
        end
    end

    subgraph "Capa de Datos"
        MySQL[(MySQL<br/>veterinaria)]
    end

    subgraph "Testing"
        JUNIT[JUnit 5<br/>Backend Tests]
        AUTOM[Serenity BDD + Cucumber<br/>E2E Tests]
    end

    FW --> FA
    FA --> MySQL
    SB -.-> MySQL
    AUTOM --> FW
    JUNIT --> SB
```

## Modelo de Dominio (Diagrama de Clases)

```mermaid
classDiagram
    class Dueno {
        +String cedula
        +String nombre
        +String telefono
    }
    
    class Mascota {
        +Long id
        +String nombre
        +String especie
        +Int edad
        +String dueno_cedula
    }
    
    class Turno {
        +Long id
        +DateTime fecha
        +String motivo
        +Long mascota_id
    }
    
    class HistorialClinico {
        +Long id
        +DateTime fecha
        +String descripcion
        +String diagnostico
        +Long mascota_id
    }
    
    class Usuario {
        +Long id
        +String username
        +String password_hash
        +String rol
        +String dueno_cedula
    }
    
    Dueno "1" --> "*" Mascota : posee
    Mascota "1" --> "*" Turno : tiene
    Mascota "1" --> "*" HistorialClinico : registra
    Dueno "1" --> "1" Usuario : vinculado_a
```

## Flujo de Autenticación

```mermaid
sequenceDiagram
    participant U as Usuario
    participant FW as Frontend React
    participant API as FastAPI Backend
    participant DB as MySQL

    U->>FW: Ingresa credenciales
    FW->>API: POST /auth/login
    API->>DB: SELECT usuario
    DB-->>API: Usuario encontrado
    API->>API: Verificar password (bcrypt)
    API->>API: Generar JWT (HS256, 60min)
    API-->>FW: {access_token, user}
    FW->>FW: Guardar en localStorage
    FW->>FW: Decodificar JWT (rol, cedula)
    
    Note over FW: Peticiones autenticadas
    
    FW->>API: GET /api/duenos
    API->>API: Extraer JWT del header
    API->>API: Verificar token + rol
    API->>DB: SELECT duenos
    DB-->>FW: Datos filtrados por rol
```

## Arquitectura del Frontend React

```mermaid
graph LR
    subgraph "Estructura de Directorios"
        APP[App.js<br/>Router + Layout]
        
        subgraph "Páginas"
            LOGIN[Login<br/>Autenticación]
            DASH[Dashboard<br/>Estadísticas]
            DUENOS[Duenos<br/>CRUD Admin]
            MASC[Mascotas<br/>CRUD Admin]
            TURN[Turnos<br/>CRUD Admin]
            PORTAL[ClientPortal<br/>Vista Cliente]
        end
        
        subgraph "Servicios"
            API[api.js<br/>Capa HTTP]
        end
    end
    
    APP --> LOGIN
    APP --> DASH
    APP --> DUENOS
    APP --> MASC
    APP --> TURN
    APP --> PORTAL
    
    DASH --> API
    DUENOS --> API
    MASC --> API
    TURN --> API
    PORTAL --> API
```

## Arquitectura de Automatización (Serenity BDD)

```mermaid
graph TB
    subgraph "Capa de Presentación (Page Objects)"
        LP[LoginPage]
        DP[DashboardPage]
        DUP[DuenosPage]
        MP[MascotasPage]
        TP[TurnosPage]
    end
    
    subgraph "Capa de Acciones (Tasks)"
        ABR[AbrirPetClinic]
        LOG[LoginPetClinic]
        RD[RegistrarDueno]
        RM[RegistrarMascota]
        RT[RegistrarTurno]
        EM[EliminarMascota]
        ED[EliminarDueno]
    end
    
    subgraph "Capa de Verificación (Questions)"
        VD[ValidarDueno]
        VM[ValidarMascota]
        VT[ValidarTurno]
        VE[ValidarEliminacion]
        VDB[ValidarDashboard]
    end
    
    subgraph "Modelos de Datos"
        DD[DuenoData]
        MD[MascotaData]
        TD[TurnoData]
    end
    
    ABR --> LP
    LOG --> LP
    RD --> DUP
    RM --> MP
    RT --> TP
    EM --> MP
    ED --> DUP
    
    VD --> DUP
    VM --> MP
    VT --> TP
    VE --> DUP
    VDB --> DP
```

## Capas de Seguridad

```mermaid
graph TB
    subgraph "Roles"
        ADMIN[ADMIN]
        USER[USER]
    end
    
    subgraph "Operaciones Permitidas"
        O1[Crear Dueño]
        O2[Crear Mascota]
        O3[Crear Turno]
        O4[Crear Historial]
        O5[Eliminar Dueño]
        O6[Eliminar Mascota]
        O7[Eliminar Turno]
        O8[Eliminar Historial]
        O9[Ver Dashboard]
    end
    
    ADMIN --> O1
    ADMIN --> O2
    ADMIN --> O3
    ADMIN --> O4
    ADMIN --> O5
    ADMIN --> O6
    ADMIN --> O7
    ADMIN --> O8
    ADMIN --> O9
    
    USER --> O1
    USER --> O2
    USER --> O3
    USER --> O9
    
    USER -.->|No permitido| O5
    USER -.->|No permitido| O6
    USER -.->|No permitido| O7
    USER -.->|No permitido| O8
```

## Resumen de Tecnologías

| Componente | Tecnología | Estado |
|------------|------------|--------|
| **Backend Principal** | Python FastAPI | ✅ Activo |
| **Backend Secundario** | Java Spring Boot | ⚠️ Incompleto |
| **Frontend Web** | React 19 | ✅ Activo |
| **Base de Datos** | MySQL | ✅ Activo |
| **Automatización** | Serenity BDD + Cucumber | ✅ Activo |
| **Autenticación** | JWT (HS256) | ✅ Implementado |
| **Testing Backend** | JUnit 5 | ✅ Configurado |
| **App Móvil** | - | ❌ Pendiente |
