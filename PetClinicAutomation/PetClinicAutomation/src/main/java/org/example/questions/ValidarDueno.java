package org.example.questions;

import net.serenitybdd.screenplay.Question;
import net.serenitybdd.screenplay.Actor;
import net.serenitybdd.screenplay.abilities.BrowseTheWeb;
import org.openqa.selenium.By;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.openqa.selenium.support.ui.ExpectedConditions;
import java.time.Duration;

public class ValidarDueno implements Question<Boolean> {

    private final String nombreEsperado;

    public ValidarDueno(String nombreEsperado) { this.nombreEsperado = nombreEsperado; }

    public static ValidarDueno conNombre(String nombre) { return new ValidarDueno(nombre); }

    @Override
    public Boolean answeredBy(Actor actor) {
        try {
            var driver = BrowseTheWeb.as(actor).getDriver();
            // Esperar que la tabla cargue
            new WebDriverWait(driver, Duration.ofSeconds(5))
                    .until(ExpectedConditions.presenceOfElementLocated(By.cssSelector("tbody")));
            String contenido = driver.findElement(By.cssSelector("tbody")).getText();
            return contenido != null && contenido.contains(nombreEsperado);
        } catch (Exception e) {
            return false;
        }
    }
}