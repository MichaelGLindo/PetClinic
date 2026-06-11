package org.example.models;

public class TurnoData {
    private String fecha;
    private String motivo;
    private String mascotaId;

    public TurnoData(String fecha, String motivo, String mascotaId) {
        this.fecha     = fecha;
        this.motivo    = motivo;
        this.mascotaId = mascotaId;
    }

    public String getFecha()     { return fecha; }
    public String getMotivo()    { return motivo; }
    public String getMascotaId() { return mascotaId; }
}
