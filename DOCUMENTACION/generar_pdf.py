from fpdf import FPDF

class PetClinicPDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 15)
        self.set_text_color(20, 184, 166)
        self.cell(0, 10, 'PetClinic - Sistema de Gestion Veterinaria', new_x="LMARGIN", new_y="NEXT", align='C')
        self.set_font('Helvetica', '', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 5, 'Documentacion Completa del Proyecto', new_x="LMARGIN", new_y="NEXT", align='C')
        self.line(10, self.get_y()+2, 200, self.get_y()+2)
        self.ln(8)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, f'Pagina {self.page_no()}/{{nb}}', align='C')

    def chapter_title(self, num, title):
        self.set_font('Helvetica', 'B', 14)
        self.set_text_color(20, 184, 166)
        self.cell(0, 10, f'{num}. {title}', new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(20, 184, 166)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(4)

    def section_title(self, title):
        self.set_font('Helvetica', 'B', 11)
        self.set_text_color(139, 92, 246)
        self.cell(0, 8, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def body_text(self, text):
        self.set_font('Helvetica', '', 10)
        self.set_text_color(50, 50, 50)
        self.multi_cell(0, 5.5, text)
        self.ln(2)

    def bullet(self, text):
        self.set_font('Helvetica', '', 10)
        self.set_text_color(50, 50, 50)
        self.set_x(10)
        self.multi_cell(0, 5.5, f'  -  {text}')

    def table_row(self, cells, widths, header=False):
        if header:
            self.set_font('Helvetica', 'B', 9)
            self.set_fill_color(20, 184, 166)
            self.set_text_color(255, 255, 255)
        else:
            self.set_font('Helvetica', '', 9)
            self.set_text_color(50, 50, 50)
            self.set_fill_color(245, 245, 245)

        h = 7
        for i, cell in enumerate(cells):
            self.cell(widths[i], h, cell, border=1, fill=header, align='C' if header else 'L')
        self.ln(h)

pdf = PetClinicPDF()
pdf.alias_nb_pages()
pdf.set_auto_page_break(auto=True, margin=20)

# ===================== PORTADA =====================
pdf.add_page()
pdf.ln(40)
pdf.set_font('Helvetica', 'B', 28)
pdf.set_text_color(20, 184, 166)
pdf.cell(0, 15, 'PetClinic', new_x="LMARGIN", new_y="NEXT", align='C')
pdf.set_font('Helvetica', '', 16)
pdf.set_text_color(80, 80, 80)
pdf.cell(0, 10, 'Sistema de Gestion Veterinaria', new_x="LMARGIN", new_y="NEXT", align='C')
pdf.ln(10)
pdf.set_font('Helvetica', '', 12)
pdf.cell(0, 8, 'Integrante: Michael Galindo', new_x="LMARGIN", new_y="NEXT", align='C')
pdf.cell(0, 8, 'Documento de Arquitectura y Base de Datos', new_x="LMARGIN", new_y="NEXT", align='C')
pdf.ln(20)
pdf.set_font('Helvetica', 'I', 10)
pdf.set_text_color(128)
pdf.cell(0, 8, 'Junio 2026', new_x="LMARGIN", new_y="NEXT", align='C')

# ===================== 1. ARQUITECTURA GENERAL =====================
pdf.add_page()
pdf.chapter_title('1', 'ARQUITECTURA GENERAL DEL SISTEMA')

pdf.section_title('1.1 Que es PetClinic?')
pdf.body_text('PetClinic es un sistema completo de gestion para veterinarias que permite administrar dueos, mascotas, turnos (citas) e historial clinico. El sistema esta compuesto por un backend API, un frontend web y un modulo de automatizacion de pruebas.')

pdf.section_title('1.2 Estructura del Proyecto')
pdf.body_text('El repositorio contiene las siguientes carpetas principales:')

structure = [
    ('backend/', 'API REST con Python FastAPI'),
    ('frontend-web/', 'Aplicacion web construida con React 19'),
    ('app-movil/', 'Carpeta vacia - aplicacion movil pendiente de implementar'),
    ('PetClinicAutomation/', 'Suite de automatizacion con Serenity BDD + Cucumber'),
    ('DOCUMENTACION/', 'Diagramas y documentacion del proyecto'),
]
for name, desc in structure:
    pdf.bullet(f'{name} -> {desc}')

pdf.ln(4)
pdf.section_title('1.3 Stack Tecnologico')
widths = [45, 45, 50, 50]
pdf.table_row(['Componente', 'Tecnologia', 'Version', 'Estado'], widths, header=True)
pdf.table_row(['Backend', 'Python FastAPI', '>0.110.0', 'Activo'], widths)
pdf.table_row(['Frontend', 'React', '19.2.7', 'Activo'], widths)
pdf.table_row(['Base Datos', 'MySQL', '-', 'Activo'], widths)
pdf.table_row(['ORM Python', 'SQLAlchemy', '>2.0.0', 'Activo'], widths)
pdf.table_row(['Automatizacion', 'Serenity BDD', '5.3.9', 'Activo'], widths)
pdf.table_row(['App Movil', '-', '-', 'Pendiente'], widths)

# ===================== 2. MODELO DE DOMINIO =====================
pdf.add_page()
pdf.chapter_title('2', 'MODELO DE DOMINIO (BASE DE DATOS)')

pdf.section_title('2.1 Entidades del Sistema')
pdf.body_text('El sistema maneja 5 entidades principales que representan las tablas de la base de datos MySQL:')

widths_ent = [30, 35, 125]
pdf.table_row(['Entidad', 'Tabla BD', 'Campos Principales'], widths_ent, header=True)
pdf.table_row(['Dueno', 'duenos', 'cedula (PK), nombre, telefono'], widths_ent)
pdf.table_row(['Mascota', 'mascotas', 'id (PK), nombre, especie, edad, dueno_cedula (FK)'], widths_ent)
pdf.table_row(['Turno', 'turnos', 'id (PK), fecha, motivo, mascota_id (FK)'], widths_ent)
pdf.table_row(['Historial', 'historial_clinico', 'id (PK), fecha, descripcion, diagnostico, mascota_id (FK)'], widths_ent)
pdf.table_row(['Usuario', 'usuarios', 'id (PK), username, password_hash, rol, dueno_cedula (FK)'], widths_ent)

pdf.ln(4)
pdf.section_title('2.2 Relaciones entre Entidades')
pdf.body_text('Las relaciones entre entidades son las siguientes:')
pdf.bullet('Dueno (1) ---- (*) Mascota: Un dueo puede tener muchas mascotas')
pdf.bullet('Mascota (1) ---- (*) Turno: Una mascota puede tener muchos turnos/citas')
pdf.bullet('Mascota (1) ---- (*) HistorialClinico: Una mascota puede tener muchos registros clinicos')
pdf.bullet('Dueno (1) ---- (1) Usuario: Un dueo tiene un usuario asociado para login')

pdf.ln(4)
pdf.section_title('2.3 Diagrama de Relaciones (Mermaid)')
pdf.body_text('Dueno (1) --- (*) ---> Mascota (1) --- (*) ---> Turno')
pdf.body_text('                      Mascota (1) --- (*) ---> HistorialClinico')
pdf.body_text('Dueno (1) --- (1) ---> Usuario')

# ===================== 3. BACKEND FASTAPI =====================
pdf.add_page()
pdf.chapter_title('3', 'BACKEND - PYTHON FASTAPI')

pdf.section_title('3.1 Arquitectura en Capas')
pdf.body_text('El backend principal sigue un patron de arquitectura en capas:')
pdf.bullet('Router Layer (endpoints): Maneja las peticiones HTTP y retorna respuestas JSON')
pdf.bullet('CRUD Layer (datos): Contiene todas las operaciones de base de datos')
pdf.bullet('Model Layer (entidades): Define las tablas con SQLAlchemy ORM')
pdf.bullet('Schema Layer (validacion): Define los DTOs con Pydantic para validacion')

pdf.section_title('3.2 Archivos Principales')
widths_files = [40, 150]
pdf.table_row(['Archivo', 'Funcion'], widths_files, header=True)
pdf.table_row(['main.py', 'Punto de entrada, configura CORS, incluye routers, crea tablas'], widths_files)
pdf.table_row(['database.py', 'Conexion a MySQL, crea engine y sesion, get_db()'], widths_files)
pdf.table_row(['models.py', 'Modelos SQLAlchemy: Dueno, Mascota, Turno, Historial, Usuario'], widths_files)
pdf.table_row(['schemas.py', 'Schemas Pydantic para validacion de request/response'], widths_files)
pdf.table_row(['crud.py', 'Todas las operaciones CRUD de cada entidad'], widths_files)
pdf.table_row(['security.py', 'Hash bcrypt, creacion y verificacion JWT'], widths_files)
pdf.table_row(['auth_dependencies.py', 'Dependencia para extraer usuario del token'], widths_files)
pdf.table_row(['roles.py', 'Dependencia require_role() para autorizacion por rol'], widths_files)

pdf.ln(4)
pdf.section_title('3.3 Endpoints de la API')
widths_ep = [30, 55, 105]
pdf.table_row(['Metodo', 'Ruta', 'Descripcion'], widths_ep, header=True)
pdf.table_row(['POST', '/auth/login', 'Iniciar sesion, retorna token JWT'], widths_ep)
pdf.table_row(['POST', '/auth/register', 'Registrar nuevo usuario'], widths_ep)
pdf.table_row(['POST', '/auth/register-client', 'Registrar cliente + dueo'], widths_ep)
pdf.table_row(['GET', '/api/duenos', 'Listar dueos (admin: todos, user: propio)'], widths_ep)
pdf.table_row(['POST', '/api/duenos', 'Crear nuevo dueo'], widths_ep)
pdf.table_row(['PUT', '/api/duenos/{cedula}', 'Actualizar dueo'], widths_ep)
pdf.table_row(['DELETE', '/api/duenos/{cedula}', 'Eliminar dueo (solo admin)'], widths_ep)
pdf.table_row(['GET', '/api/mascotas', 'Listar mascotas'], widths_ep)
pdf.table_row(['POST', '/api/mascotas', 'Crear mascota'], widths_ep)
pdf.table_row(['PUT', '/api/mascotas/{id}', 'Actualizar mascota'], widths_ep)
pdf.table_row(['DELETE', '/api/mascotas/{id}', 'Eliminar mascota (solo admin)'], widths_ep)
pdf.table_row(['GET', '/api/turnos', 'Listar turnos'], widths_ep)
pdf.table_row(['POST', '/api/turnos', 'Crear turno'], widths_ep)
pdf.table_row(['PUT', '/api/turnos/{id}', 'Actualizar turno'], widths_ep)
pdf.table_row(['DELETE', '/api/turnos/{id}', 'Eliminar turno (solo admin)'], widths_ep)
pdf.table_row(['GET', '/api/historiales', 'Listar historial clinico'], widths_ep)
pdf.table_row(['POST', '/api/historiales', 'Crear registro clinico (solo admin)'], widths_ep)
pdf.table_row(['PUT', '/api/historiales/{id}', 'Actualizar registro (solo admin)'], widths_ep)
pdf.table_row(['DELETE', '/api/historiales/{id}', 'Eliminar registro (solo admin)'], widths_ep)
pdf.table_row(['GET', '/api/dashboard/stats', 'Estadisticas del dashboard'], widths_ep)

pdf.add_page()
pdf.section_title('3.4 Dependencias Python (requirements.txt)')
widths_dep = [50, 35, 105]
pdf.table_row(['Libreria', 'Version', 'Proposito'], widths_dep, header=True)
pdf.table_row(['fastapi', '>=0.110.0', 'Framework web async para APIs REST'], widths_dep)
pdf.table_row(['uvicorn[standard]', '>=0.28.0', 'Servidor ASGI para ejecutar FastAPI'], widths_dep)
pdf.table_row(['sqlalchemy', '>=2.0.0', 'ORM para mapear objetos a tablas MySQL'], widths_dep)
pdf.table_row(['pymysql', '>=1.1.0', 'Driver para conectarse a MySQL'], widths_dep)
pdf.table_row(['cryptography', '>=42.0.0', 'Requerido por pymysql para auth MySQL'], widths_dep)
pdf.table_row(['pydantic', '>=2.6.0', 'Validacion de datos y serializacion JSON'], widths_dep)
pdf.table_row(['python-jose[cryptography]', '-', 'Creacion y verificacion de tokens JWT'], widths_dep)
pdf.table_row(['passlib[bcrypt]', '-', 'Hasheo de contraseñas con algoritmo bcrypt'], widths_dep)

# ===================== 4. FRONTEND REACT =====================
pdf.add_page()
pdf.chapter_title('4', 'FRONTEND - REACT 19')

pdf.section_title('4.1 Estructura del Proyecto')
pdf.body_text('El frontend es una SPA (Single Page Application) construida con React 19 usando Create React App. Utiliza React Router v7 para navegacion y manejo de rutas basado en roles.')

pdf.section_title('4.2 Archivos Principales')
widths_fe = [45, 145]
pdf.table_row(['Archivo', 'Funcion'], widths_fe, header=True)
pdf.table_row(['App.js', 'Componente raiz: router, layout con sidebar, estado de auth'], widths_fe)
pdf.table_row(['index.css', 'Sistema de diseno global: tokens CSS, reset, tipografia, botones'], widths_fe)
pdf.table_row(['services/api.js', 'Capa HTTP centralizada con fetch, headers JWT, manejo respuestas'], widths_fe)
pdf.table_row(['pages/Login/Login.js', 'Formulario dual login/registro, decodifica JWT'], widths_fe)
pdf.table_row(['pages/Dashboard/Dashboard.js', 'Panel admin con tarjetas de estadisticas'], widths_fe)
pdf.table_row(['pages/Duenos/Duenos.js', 'CRUD completo de dueños con tabla y formulario inline'], widths_fe)
pdf.table_row(['pages/Mascotas/Mascotas.js', 'CRUD completo de mascotas'], widths_fe)
pdf.table_row(['pages/Turnos/Turnos.js', 'CRUD completo de turnos con picker de fecha'], widths_fe)
pdf.table_row(['pages/ClientPortal/ClientPortal.js', 'Portal del cliente con tabs: mascotas, turnos, historial'], widths_fe)

pdf.ln(4)
pdf.section_title('4.3 Rutas por Rol')
widths_r = [35, 70, 85]
pdf.table_row(['Rol', 'Rutas Disponibles', 'Redirect por Defecto'], widths_r, header=True)
pdf.table_row(['Sin login', 'Todas renderizan Login', '-'], widths_r)
pdf.table_row(['ADMIN', '/dashboard, /duenos, /mascotas, /turnos', '/dashboard'], widths_r)
pdf.table_row(['USER', '/portal', '/portal'], widths_r)

pdf.section_title('4.4 Manejo de Estado')
pdf.body_text('No se usa libreria externa de estado (Redux, Zustand). Todo se maneja con:')
pdf.bullet('useState: Estado local en cada componente (listas, formularios, loading)')
pdf.bullet('useEffect: Carga de datos al montar componentes, llamadas a la API')
pdf.bullet('localStorage: Persistencia de token JWT y datos del usuario')
pdf.bullet('App.js: Estado raiz con isLoggedIn y user (nombre, rol, cedula)')

pdf.section_title('4.5 Sistema de Diseno')
pdf.body_text('Tema oscuro personalizado con CSS Custom Properties:')
pdf.bullet('Color primario: Teal (#14b8a6)')
pdf.bullet('Color secundario: Violet (#8b5cf6)')
pdf.bullet('Fondo: #0a0f1e, #111827, #1a2035')
pdf.bullet('Fuente: Inter (Google Fonts)')
pdf.bullet('Responsive: Media query en 768px para movil')

# ===================== 5. AUTENTICACION =====================
pdf.add_page()
pdf.chapter_title('5', 'SISTEMA DE AUTENTICACION Y SEGURIDAD')

pdf.section_title('5.1 Flujo de Login')
pdf.body_text('1. El usuario ingresa username y password en el formulario Login')
pdf.body_text('2. Se envia POST a /auth/login con las credenciales')
pdf.body_text('3. El backend verifica el password con bcrypt (hash)')
pdf.body_text('4. Si es correcto, genera un token JWT con payload: sub(username), rol, dueno_cedula')
pdf.body_text('5. El frontend guarda el token en localStorage')
pdf.body_text('6. Se decodifica el JWT para extraer rol y cedula del usuario')
pdf.body_text('7. Todas las peticiones HTTP incluyen el header: Authorization: Bearer [token]')

pdf.section_title('5.2 JWT (JSON Web Token)')
pdf.bullet('Algoritmo: HS256 (HMAC-SHA256)')
pdf.bullet('Expiracion: 60 minutos')
pdf.bullet('Payload contiene: sub (usuario), rol (ADMIN/USER), dueno_cedula')
pdf.bullet('Secret key: petclinic-secret-key (hardcoded)')

pdf.section_title('5.3 Roles y Permisos')
widths_perm = [55, 65, 70]
pdf.table_row(['Operacion', 'ADMIN', 'USER'], widths_perm, header=True)
pdf.table_row(['Crear Dueño', 'Permitido', 'Permitido'], widths_perm)
pdf.table_row(['Crear Mascota', 'Permitido', 'Permitido'], widths_perm)
pdf.table_row(['Crear Turno', 'Permitido', 'Permitido'], widths_perm)
pdf.table_row(['Ver Dashboard', 'Permitido', 'Permitido'], widths_perm)
pdf.table_row(['Ver Sus Propios Datos', 'Permitido', 'Permitido'], widths_perm)
pdf.table_row(['Eliminar Dueño', 'Permitido', 'No permitido'], widths_perm)
pdf.table_row(['Eliminar Mascota', 'Permitido', 'No permitido'], widths_perm)
pdf.table_row(['Eliminar Turno', 'Permitido', 'No permitido'], widths_perm)
pdf.table_row(['Crear Historial', 'Permitido', 'No permitido'], widths_perm)
pdf.table_row(['Eliminar Historial', 'Permitido', 'No permitido'], widths_perm)

pdf.section_title('5.4 CORS (Cross-Origin Resource Sharing)')
pdf.body_text('Configurado para permitir peticiones desde:')
pdf.bullet('http://localhost:3000 (desarrollo frontend)')
pdf.bullet('http://localhost:5173 (Vite dev server)')
pdf.bullet('http://127.0.0.1:3000 y :5173')
pdf.bullet('https://pet-clinic-oywb.vercel.app (produccion Vercel)')

# ===================== 6. AUTOMATIZACION =====================
pdf.add_page()
pdf.chapter_title('6', 'AUTOMATIZACION DE PRUEBAS - SERENITY BDD')

pdf.section_title('6.1 Stack de Testing')
pdf.bullet('Framework BDD: Serenity BDD 5.3.9 + Cucumber 7.15.0')
pdf.bullet('Browser Automation: Selenium WebDriver (via Serenity Screenplay)')
pdf.bullet('Driver Management: WebDriverManager 5.6.3')
pdf.bullet('Test Runner: JUnit 4.13.2')
pdf.bullet('Navegador: Chrome (default), Edge (opcional)')

pdf.section_title('6.2 Patron Screenplay')
pdf.body_text('El proyecto usa el patron Screenplay que separa:')
pdf.bullet('Models (DuenoData, MascotaData, TurnoData): DTOs para datos de prueba')
pdf.bullet('Tasks (7 acciones): AbrirPetClinic, LoginPetClinic, RegistrarDueno, RegistrarMascota, RegistrarTurno, EliminarMascota, EliminarDueno')
pdf.bullet('Questions (5 validaciones): ValidarDueno, ValidarMascota, ValidarTurno, ValidarEliminacion, ValidarDashboard')
pdf.bullet('User Interfaces (5 page objects): LoginPage, DashboardPage, DuenosPage, MascotasPage, TurnosPage')
pdf.bullet('Utils: DatosPrueba (factory con datos aleatorios para evitar duplicados)')

pdf.section_title('6.3 Escenarios de Prueba (8 total)')
widths_sc = [10, 80, 100]
pdf.table_row(['#', 'Escenario', 'Que Prueba'], widths_sc, header=True)
pdf.table_row(['1', 'Registrar un dueno exitosamente', 'CRUD de dueo con cedula unica'], widths_sc)
pdf.table_row(['2', 'Registrar mascota con dueo existente', 'Mascota Firulais ligada a cedula 10001'], widths_sc)
pdf.table_row(['3', 'Registrar turno con mascota existente', 'Cita con motivo "Vacunacion anual"'], widths_sc)
pdf.table_row(['4', 'Consultar mascotas registradas', 'Navegar a /mascotas, verificar titulo'], widths_sc)
pdf.table_row(['5', 'Consultar turnos registrados', 'Navegar a /turnos, verificar titulo'], widths_sc)
pdf.table_row(['6', 'Dashboard muestra contadores', 'Verificar tarjetas de estadisticas'], widths_sc)
pdf.table_row(['7', 'Editar dueo existente', 'Cambiar telefono de cedula 10001'], widths_sc)
pdf.table_row(['8', 'Cerrar sesion del sistema', 'Logout y verificar redirect a login'], widths_sc)

pdf.section_title('6.4 Como Ejecutar')
pdf.body_text('Comando: gradle clean test aggregate')
pdf.body_text('Reporte: target/site/serenity/index.html (reporte HTML unico)')

# ===================== 7. BASE DE DATOS MySQL =====================
pdf.add_page()
pdf.chapter_title('7', 'BASE DE DATOS - MYSQL')

pdf.section_title('7.1 Configuracion')
pdf.bullet('Motor: MySQL')
pdf.bullet('Nombre de base de datos: veterinaria')
pdf.bullet('Host: localhost:3306')
pdf.bullet('Usuario: root')
pdf.bullet('Password: Admin123*')
pdf.bullet('DDL Mode: update (Hibernate crea/actualiza tablas automaticamente)')

pdf.section_title('7.2 Script de Creacion de Tablas')
pdf.body_text('Las tablas se crean automaticamente via SQLAlchemy. Schema de la base de datos:')

pdf.set_font('Courier', '', 8)
pdf.set_text_color(50, 50, 50)
sql = """CREATE TABLE duenos (
  cedula VARCHAR(20) PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  telefono VARCHAR(20)
);

CREATE TABLE mascotas (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  especie VARCHAR(50),
  edad INT,
  dueno_cedula VARCHAR(20),
  FOREIGN KEY (dueno_cedula) REFERENCES duenos(cedula)
);

CREATE TABLE turnos (
  id INT AUTO_INCREMENT PRIMARY KEY,
  fecha DATETIME NOT NULL,
  motivo TEXT,
  mascota_id INT,
  FOREIGN KEY (mascota_id) REFERENCES mascotas(id)
);

CREATE TABLE historial_clinico (
  id INT AUTO_INCREMENT PRIMARY KEY,
  fecha DATETIME NOT NULL,
  descripcion TEXT,
  diagnostico TEXT,
  mascota_id INT,
  FOREIGN KEY (mascota_id) REFERENCES mascotas(id)
);

CREATE TABLE usuarios (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(50) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  rol VARCHAR(20) DEFAULT 'USER',
  dueno_cedula VARCHAR(20),
  FOREIGN KEY (dueno_cedula) REFERENCES duenos(cedula)
);"""
pdf.multi_cell(0, 3.5, sql)

pdf.set_font('Helvetica', '', 10)
pdf.ln(4)
pdf.section_title('7.3 Indices y Restricciones')
pdf.bullet('PRIMARY KEY: cedula (duenos), id (mascotas, turnos, historial, usuarios)')
pdf.bullet('FOREIGN KEY: mascotas -> duenos, turnos -> mascotas, historial -> mascotas, usuarios -> duenos')
pdf.bullet('UNIQUE: username en usuarios')
pdf.bullet('NOT NULL: nombre, fecha, username, password_hash')
pdf.bullet('DEFAULT: rol = USER en usuarios')

# ===================== 8. HERRAMIENTAS =====================
pdf.add_page()
pdf.chapter_title('8', 'HERRAMIENTAS Y CONFIGURACION')

pdf.section_title('8.1 Control de Versiones')
pdf.bullet('Git: Sistema de control de versiones local')
pdf.bullet('GitHub: Repositorio remoto para colaboracion')

pdf.section_title('8.2 Herramientas de Desarrollo')
pdf.bullet('VS Code / IntelliJ IDEA: Editores de codigo')
pdf.bullet('Postman: Testing manual de endpoints API')
pdf.bullet('draw.io: Creacion de diagramas UML (clases)')
pdf.bullet('MySQL Workbench: Administracion de base de datos')

pdf.section_title('8.3 Despliegue')
pdf.bullet('Frontend: Vercel (deploy automatico desde GitHub)')
pdf.bullet('Backend: Servidor local en http://localhost:8080')
pdf.bullet('Script de inicio: run_backend.bat (ejecuta uvicorn)')

pdf.section_title('8.4 Archivos de Configuracion Importantes')
widths_conf = [55, 135]
pdf.table_row(['Archivo', 'Funcion'], widths_conf, header=True)
pdf.table_row(['backend/requirements.txt', 'Dependencias Python del backend'], widths_conf)
pdf.table_row(['frontend-web/package.json', 'Dependencias y scripts npm (React)'], widths_conf)
pdf.table_row(['frontend-web/vercel.json', 'Reglas de reescritura SPA para Vercel'], widths_conf)
pdf.table_row(['serenity.conf', 'Configuracion de navegador y reports'], widths_conf)

# ===================== 9. RESUMEN EJECUTIVO =====================
pdf.add_page()
pdf.chapter_title('9', 'RESUMEN EJECUTIVO')

pdf.body_text('PetClinic es un sistema de gestion veterinaria que implementa las siguientes funcionalidades:')

pdf.ln(2)
pdf.section_title('Funcionalidades Implementadas')
pdf.bullet('Registro y gestion de duenos de mascotas')
pdf.bullet('Registro y gestion de mascotas (especie, edad, dueo)')
pdf.bullet('Gestion de turnos/citas veterinarias')
pdf.bullet('Historial clinico de cada mascota')
pdf.bullet('Autenticacion con JWT y roles (ADMIN/USER)')
pdf.bullet('Dashboard con estadisticas (total duenos, mascotas, turnos)')
pdf.bullet('Portal del cliente para ver sus datos')
pdf.bullet('8 escenarios de prueba automatizados (E2E)')

pdf.ln(4)
pdf.section_title('Tecnologias Clave')
pdf.bullet('Backend: Python FastAPI + SQLAlchemy + JWT + MySQL')
pdf.bullet('Frontend: React 19 + React Router v7 + CSS Custom Properties')
pdf.bullet('Testing: Serenity BDD + Cucumber + Selenium (Screenplay Pattern)')
pdf.bullet('Base de Datos: MySQL con 5 tablas y relaciones 1:N')

pdf.ln(4)
pdf.section_title('Estado del Proyecto')
widths_est = [60, 130]
pdf.table_row(['Componente', 'Estado'], widths_est, header=True)
pdf.table_row(['Backend FastAPI', 'COMPLETO - CRUD, Auth, Dashboard'], widths_est)
pdf.table_row(['Frontend React', 'COMPLETO - Login, CRUD, Portal, Dashboard'], widths_est)
pdf.table_row(['Base de Datos MySQL', 'COMPLETO - 5 tablas, relaciones OK'], widths_est)
pdf.table_row(['Automatizacion E2E', 'COMPLETO - 8 escenarios, reportes HTML'], widths_est)
pdf.table_row(['App Movil', 'PENDIENTE - Carpeta vacia'], widths_est)
pdf.table_row(['Documentacion', 'PARCIAL - Diagrama de clases UML'], widths_est)

pdf.ln(6)
pdf.set_font('Helvetica', 'I', 10)
pdf.set_text_color(128)
pdf.cell(0, 8, 'Documento generado automaticamente - PetClinic 2026', new_x="LMARGIN", new_y="NEXT", align='C')

output_path = r'C:\Users\Michael\Documents\PetClinic\DOCUMENTACION\PetClinic_Documentacion.pdf'
pdf.output(output_path)
print(f'PDF generado en: {output_path}')
