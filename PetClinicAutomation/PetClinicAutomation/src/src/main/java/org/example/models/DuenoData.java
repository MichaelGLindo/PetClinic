package org.example.models;

public class DuenoData {
    private String cedula;
    private String nombre;
    private String telefono;

    public DuenoData(String cedula, String nombre, String telefono) {
        this.cedula   = cedula;
        this.nombre   = nombre;
        this.telefono = telefono;
    }

    public String getCedula()   { return cedula; }
    public String getNombre()   { return nombre; }
    public String getTelefono() { return telefono; }
}
