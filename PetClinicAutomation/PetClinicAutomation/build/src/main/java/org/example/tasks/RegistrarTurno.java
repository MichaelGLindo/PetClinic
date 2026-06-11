package org.example.tasks;

import net.serenitybdd.screenplay.Task;
import net.serenitybdd.screenplay.Actor;
import net.serenitybdd.screenplay.actions.Click;
import net.serenitybdd.screenplay.actions.Enter;
import net.serenitybdd.annotations.Step;
import org.example.models.TurnoData;
import org.example.userinterfaces.DashboardPage;
import org.example.userinterfaces.TurnosPage;

public class RegistrarTurno implements Task {

    private final TurnoData turno;

    public RegistrarTurno(TurnoData turno) {
        this.turno = turno;
    }

    public static RegistrarTurno con(TurnoData turno) {
        return new RegistrarTurno(turno);
    }

    @Override
    @Step("{0} agenda el turno con motivo {turno.motivo}")
    public <T extends Actor> void performAs(T actor) {
        TurnosPage turnosPage = new TurnosPage();
        actor.attemptsTo(
            Click.on(new DashboardPage().linkTurnos),
            Enter.theValue(turno.getFecha()).into(turnosPage.campoFecha),
            Enter.theValue(turno.getMascotaId()).into(turnosPage.campoMascotaId),
            Enter.theValue(turno.getMotivo()).into(turnosPage.campoMotivo),
            Click.on(turnosPage.botonGuardar)
        );
    }
}
