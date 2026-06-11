# language: es
Característica: Gestión del sistema PetClinic
  Como usuario del sistema veterinario
  Quiero gestionar dueños, mascotas y turnos
  Para llevar el control de la clínica

  Antecedentes:
    Dado que el usuario ingresa al sistema PetClinic
    Y se autentica con usuario "michael" y contraseña "123456"

  Escenario: 1 - Registrar un dueño exitosamente
    Cuando registra un dueño con cédula "10001", nombre "Juan Pérez" y teléfono "3001234567"
    Entonces el dueño "Juan Pérez" aparece en la lista de dueños

  Escenario: 2 - Registrar una mascota con dueño existente
    Cuando registra una mascota con nombre "Firulais", especie "Perro", edad "3" y cédula del dueño "10001"
    Entonces la mascota "Firulais" aparece en la lista de mascotas

  Escenario: 3 - Registrar un turno con mascota existente
    Cuando agenda un turno con motivo "Vacunación anual" para la mascota con ID visible en la lista
    Entonces el turno con motivo "Vacunación anual" aparece en la lista de turnos

  Escenario: 4 - Consultar mascotas registradas
    Cuando navega a la sección de mascotas
    Entonces puede ver la lista de mascotas del sistema

  Escenario: 5 - Consultar turnos registrados
    Cuando navega a la sección de turnos
    Entonces puede ver la lista de turnos del sistema

  Escenario: 6 - El dashboard muestra los contadores
    Cuando navega al dashboard
    Entonces puede ver los contadores de dueños, mascotas y turnos

  Escenario: 7 - Editar un dueño existente
    Cuando edita el dueño con cédula "10001" cambiando el teléfono a "3109999999"
    Entonces el dueño actualizado aparece en la lista con el nuevo teléfono

  Escenario: 8 - Cerrar sesión del sistema
    Cuando hace clic en cerrar sesión
    Entonces es redirigido a la pantalla de login
