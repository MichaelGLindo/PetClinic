package org.example.tasks;

import net.serenitybdd.screenplay.Task;
import net.serenitybdd.screenplay.Actor;
import net.serenitybdd.screenplay.actions.Click;
import net.serenitybdd.screenplay.abilities.BrowseTheWeb;
import net.serenitybdd.annotations.Step;
import org.example.models.TurnoData;
import org.example.userinterfaces.TurnosPage;
import org.openqa.selenium.By;
import org.openqa.selenium.Keys;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.openqa.selenium.support.ui.ExpectedConditions;
import java.time.Duration;

public class RegistrarTurno implements Task {

    private final TurnoData turno;
    public RegistrarTurno(TurnoData turno) { this.turno = turno; }
    public static RegistrarTurno con(TurnoData turno) { return new RegistrarTurno(turno); }

    @Override
    @Step("{0} agenda el turno con motivo {turno.motivo}")
    public <T extends Actor> void performAs(T actor) {
        var driver = BrowseTheWeb.as(actor).getDriver();
        driver.get("http://localhost:3000/turnos");
        new WebDriverWait(driver, Duration.ofSeconds(10))
                .until(ExpectedConditions.presenceOfElementLocated(By.cssSelector("input[name='fecha']")));

        // Llenar fecha con JavaScript directo al valor del input
        // Formato requerido por datetime-local: YYYY-MM-DDTHH:mm
        WebElement campoFecha = driver.findElement(By.cssSelector("input[name='fecha']"));
        ((JavascriptExecutor) driver).executeScript(
                "var input = arguments[0];" +
                        "var nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;" +
                        "nativeInputValueSetter.call(input, arguments[1]);" +
                        "input.dispatchEvent(new Event('input', { bubbles: true }));" +
                        "input.dispatchEvent(new Event('change', { bubbles: true }));",
                campoFecha, "2026-12-01T10:00"
        );

        // Llenar mascotaId
        WebElement campoMascota = driver.findElement(By.cssSelector("input[name='mascotaId']"));
        campoMascota.clear();
        campoMascota.sendKeys(turno.getMascotaId());

        // Llenar motivo
        WebElement campoMotivo = driver.findElement(By.cssSelector("textarea[name='motivo']"));
        campoMotivo.clear();
        campoMotivo.sendKeys(turno.getMotivo());

        actor.attemptsTo(Click.on(TurnosPage.botonGuardar));
        try { Thread.sleep(2500); } catch (InterruptedException ignored) {}
    }
}