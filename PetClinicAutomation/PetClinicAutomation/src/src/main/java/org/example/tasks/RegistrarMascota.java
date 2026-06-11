package org.example.tasks;

import net.serenitybdd.screenplay.Task;
import net.serenitybdd.screenplay.Actor;
import net.serenitybdd.screenplay.actions.Click;
import net.serenitybdd.screenplay.actions.Enter;
import net.serenitybdd.annotations.Step;
import org.example.models.MascotaData;
import org.example.userinterfaces.DashboardPage;
import org.example.userinterfaces.MascotasPage;

public class RegistrarMascota implements Task {

    private final MascotaData mascota;

    public RegistrarMascota(MascotaData mascota) {
        this.mascota = mascota;
    }

    public static RegistrarMascota con(MascotaData mascota) {
        return new RegistrarMascota(mascota);
    }

    @Override
    @Step("{0} registra la mascota {mascota.nombre}")
    public <T extends Actor> void performAs(T actor) {
        MascotasPage mascotasPage = new MascotasPage();
        actor.attemptsTo(
            Click.on(new DashboardPage().linkMascotas),
            Enter.theValue(mascota.getNombre()).into(mascotasPage.campoNombre),
            Enter.theValue(mascota.getEspecie()).into(mascotasPage.campoEspecie),
            Enter.theValue(mascota.getEdad()).into(mascotasPage.campoEdad),
            Enter.theValue(mascota.getCedulaDueno()).into(mascotasPage.campoCedulaDueno),
            Click.on(mascotasPage.botonGuardar)
        );
    }
}
