package org.example.questions;

import net.serenitybdd.screenplay.Question;
import net.serenitybdd.screenplay.Actor;
import net.serenitybdd.screenplay.abilities.BrowseTheWeb;
import org.openqa.selenium.By;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.openqa.selenium.support.ui.ExpectedConditions;
import java.time.Duration;

public class ValidarTurno implements Question<Boolean> {

    private final String motivoEsperado;
    public ValidarTurno(String motivoEsperado) { this.motivoEsperado = motivoEsperado; }
    public static ValidarTurno conMotivo(String motivo) { return new ValidarTurno(motivo); }

    @Override
    public Boolean answeredBy(Actor actor) {
        try {
            var driver = BrowseTheWeb.as(actor).getDriver();
            new WebDriverWait(driver, Duration.ofSeconds(5))
                    .until(ExpectedConditions.presenceOfElementLocated(By.cssSelector("tbody")));
            String contenido = driver.findElement(By.cssSelector("tbody")).getText();
            return contenido != null && contenido.contains(motivoEsperado);
        } catch (Exception e) {
            return false;
        }
    }
}