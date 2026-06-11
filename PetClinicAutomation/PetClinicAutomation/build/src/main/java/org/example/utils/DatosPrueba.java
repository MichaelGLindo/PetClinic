package org.example.utils;

import org.example.models.DuenoData;
import org.example.models.MascotaData;
import org.example.models.TurnoData;

public class DatosPrueba {

    public static final String URL_BASE = "http://localhost:3000";

    public static final String USUARIO_ADMIN    = "michael";
    public static final String PASSWORD_ADMIN   = "123456";

    public static DuenoData duenoPrueba() {
        return new DuenoData("10001", "Juan Pérez", "3001234567");
    }

    public static MascotaData mascotaPrueba() {
        return new MascotaData("Firulais", "Perro", "3", "10001");
    }

    public static TurnoData turnoPrueba(String mascotaId) {
        return new TurnoData("12/01/2026 10:00 AM", "Vacunación anual", mascotaId);
    }
}
