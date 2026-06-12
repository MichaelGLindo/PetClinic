package org.example.tasks;

import net.serenitybdd.screenplay.Task;
import net.serenitybdd.screenplay.Actor;
import net.serenitybdd.screenplay.actions.Click;
import net.serenitybdd.screenplay.targets.Target;
import net.serenitybdd.screenplay.abilities.BrowseTheWeb;
import net.serenitybdd.annotations.Step;
import org.openqa.selenium.By;
import org.openqa.selenium.Alert;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.openqa.selenium.support.ui.ExpectedConditions;
import java.time.Duration;

public class EliminarDueno implements Task {

    private final String cedula;

    public EliminarDueno(String cedula) {
        this.cedula = cedula;
    }

    public static EliminarDueno conCedula(String cedula) {
        return new EliminarDueno(cedula);
    }

    @Override
    @Step("{0} elimina el dueño con cédula {cedula}")
    public <T extends Actor> void performAs(T actor) {
        var driver = BrowseTheWeb.as(actor).getDriver();
        driver.get("http://localhost:3000/duenos");

        Target botonEliminar = Target.the("botón eliminar dueño con cédula " + cedula)
                .located(By.xpath("//tr[td[1][text()='" + cedula + "']]//button[contains(., '🗑️')]"));

        actor.attemptsTo(
                Click.on(botonEliminar)
        );

        // Aceptar la alerta de confirmación
        try {
            new WebDriverWait(driver, Duration.ofSeconds(5))
                    .until(ExpectedConditions.alertIsPresent());
            Alert alert = driver.switchTo().alert();
            alert.accept();
        } catch (Exception e) {
            System.out.println("Advertencia al aceptar la alerta: " + e.getMessage());
        }
    }
}
