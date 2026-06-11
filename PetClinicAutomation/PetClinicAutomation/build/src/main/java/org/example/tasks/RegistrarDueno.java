package org.example.tasks;

import net.serenitybdd.screenplay.Task;
import net.serenitybdd.screenplay.Actor;
import net.serenitybdd.screenplay.actions.Click;
import net.serenitybdd.screenplay.actions.Enter;
import net.serenitybdd.annotations.Step;
import org.example.models.DuenoData;
import org.example.userinterfaces.DashboardPage;
import org.example.userinterfaces.DuenosPage;

public class RegistrarDueno implements Task {

    private final DuenoData dueno;

    public RegistrarDueno(DuenoData dueno) {
        this.dueno = dueno;
    }

    public static RegistrarDueno con(DuenoData dueno) {
        return new RegistrarDueno(dueno);
    }

    @Override
    @Step("{0} registra el dueño {dueno.nombre}")
    public <T extends Actor> void performAs(T actor) {
        DuenosPage duenosPage = new DuenosPage();
        actor.attemptsTo(
            Click.on(new DashboardPage().linkDuenos),
            Enter.theValue(dueno.getCedula()).into(duenosPage.campoCedula),
            Enter.theValue(dueno.getNombre()).into(duenosPage.campoNombre),
            Enter.theValue(dueno.getTelefono()).into(duenosPage.campoTelefono),
            Click.on(duenosPage.botonGuardar)
        );
    }
}
