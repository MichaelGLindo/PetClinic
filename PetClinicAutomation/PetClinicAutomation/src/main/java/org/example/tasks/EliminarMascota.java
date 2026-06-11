package org.example.tasks;

import net.serenitybdd.screenplay.Task;
import net.serenitybdd.screenplay.Actor;
import net.serenitybdd.screenplay.actions.Click;
import net.serenitybdd.screenplay.targets.Target;
import net.serenitybdd.annotations.Step;
import org.example.userinterfaces.DashboardPage;
import org.openqa.selenium.By;

public class EliminarMascota implements Task {

    private final int fila;

    public EliminarMascota(int fila) {
        this.fila = fila;
    }

    public static EliminarMascota enFila(int fila) {
        return new EliminarMascota(fila);
    }

    @Override
    @Step("{0} elimina la mascota en fila {fila}")
    public <T extends Actor> void performAs(T actor) {
        Target botonEliminar = Target.the("botón eliminar fila " + fila)
            .located(By.cssSelector("tbody tr:nth-child(" + fila + ") button:last-child"));
        actor.attemptsTo(
            Click.on(DashboardPage.linkMascotas),
            Click.on(botonEliminar)
        );
    }
}
