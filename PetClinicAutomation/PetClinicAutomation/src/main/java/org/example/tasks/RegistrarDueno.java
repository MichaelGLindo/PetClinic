package org.example.tasks;

import net.serenitybdd.screenplay.Task;
import net.serenitybdd.screenplay.Actor;
import net.serenitybdd.screenplay.actions.Enter;
import net.serenitybdd.screenplay.actions.Click;
import net.serenitybdd.screenplay.abilities.BrowseTheWeb;
import net.serenitybdd.annotations.Step;
import org.example.models.DuenoData;
import org.example.userinterfaces.DuenosPage;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.By;
import java.time.Duration;

public class RegistrarDueno implements Task {

    private final DuenoData dueno;
    public RegistrarDueno(DuenoData dueno) { this.dueno = dueno; }
    public static RegistrarDueno con(DuenoData dueno) { return new RegistrarDueno(dueno); }

    @Override
    @Step("{0} registra el dueño {dueno.nombre}")
    public <T extends Actor> void performAs(T actor) {
        var driver = BrowseTheWeb.as(actor).getDriver();
        driver.get("http://localhost:3000/duenos");
        new WebDriverWait(driver, Duration.ofSeconds(10))
                .until(ExpectedConditions.presenceOfElementLocated(By.cssSelector("input[name='cedula']")));
        actor.attemptsTo(
                Enter.theValue(dueno.getCedula()).into(DuenosPage.campoCedula),
                Enter.theValue(dueno.getNombre()).into(DuenosPage.campoNombre),
                Enter.theValue(dueno.getTelefono()).into(DuenosPage.campoTelefono),
                Click.on(DuenosPage.botonGuardar)
        );
        try { Thread.sleep(1500); } catch (InterruptedException ignored) {}
    }
}