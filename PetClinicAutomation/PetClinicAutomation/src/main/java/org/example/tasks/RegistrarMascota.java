package org.example.tasks;

import net.serenitybdd.screenplay.Task;
import net.serenitybdd.screenplay.Actor;
import net.serenitybdd.screenplay.actions.Enter;
import net.serenitybdd.screenplay.actions.Click;
import net.serenitybdd.screenplay.abilities.BrowseTheWeb;
import net.serenitybdd.annotations.Step;
import org.example.models.MascotaData;
import org.example.userinterfaces.MascotasPage;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.By;
import java.time.Duration;

public class RegistrarMascota implements Task {

    private final MascotaData mascota;
    public RegistrarMascota(MascotaData mascota) { this.mascota = mascota; }
    public static RegistrarMascota con(MascotaData mascota) { return new RegistrarMascota(mascota); }

    @Override
    @Step("{0} registra la mascota {mascota.nombre}")
    public <T extends Actor> void performAs(T actor) {
        var driver = BrowseTheWeb.as(actor).getDriver();
        driver.get("http://localhost:3000/mascotas");
        new WebDriverWait(driver, Duration.ofSeconds(10))
                .until(ExpectedConditions.presenceOfElementLocated(By.cssSelector("input[name='nombre']")));
        actor.attemptsTo(
                Enter.theValue(mascota.getNombre()).into(MascotasPage.campoNombre),
                Enter.theValue(mascota.getEspecie()).into(MascotasPage.campoEspecie),
                Enter.theValue(mascota.getEdad()).into(MascotasPage.campoEdad),
                Enter.theValue(mascota.getCedulaDueno()).into(MascotasPage.campoCedulaDueno),
                Click.on(MascotasPage.botonGuardar)
        );
        try { Thread.sleep(1500); } catch (InterruptedException ignored) {}
    }
}