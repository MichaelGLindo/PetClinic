package org.example.utils;

import org.example.models.DuenoData;
import org.example.models.MascotaData;
import org.example.models.TurnoData;

public class DatosPrueba {

    public static final String URL_BASE = "http://localhost:3000";
    public static final String USUARIO_ADMIN  = "admin2";
    public static final String PASSWORD_ADMIN = "Michael123456";

    public static DuenoData duenoPrueba() {
        // Cédula aleatoria para evitar duplicados en cada ejecución
        String cedula = "9" + (System.currentTimeMillis() % 100000);
        return new DuenoData(cedula, "Juan Pérez", "3001234567");
    }

    public static MascotaData mascotaPrueba() {
        return new MascotaData("Firulais", "Perro", "3", "10001");
    }

    public static TurnoData turnoPrueba(String mascotaId) {
        return new TurnoData("2026-12-01T10:00", "Vacunación anual", mascotaId);
    }
}