package org.example.models;

public class MascotaData {
    private String nombre;
    private String especie;
    private String edad;
    private String cedulaDueno;

    public MascotaData(String nombre, String especie, String edad, String cedulaDueno) {
        this.nombre      = nombre;
        this.especie     = especie;
        this.edad        = edad;
        this.cedulaDueno = cedulaDueno;
    }

    public String getNombre()      { return nombre; }
    public String getEspecie()     { return especie; }
    public String getEdad()        { return edad; }
    public String getCedulaDueno() { return cedulaDueno; }
}
