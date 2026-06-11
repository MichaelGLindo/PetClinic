package org.example.questions;

import net.serenitybdd.screenplay.Question;
import net.serenitybdd.screenplay.Actor;
import net.serenitybdd.screenplay.abilities.BrowseTheWeb;
import org.openqa.selenium.By;

public class ValidarTurno implements Question<Boolean> {

    private final String motivoEsperado;

    public ValidarTurno(String motivoEsperado) {
        this.motivoEsperado = motivoEsperado;
    }

    public static ValidarTurno conMotivo(String motivo) {
        return new ValidarTurno(motivo);
    }

    @Override
    public Boolean answeredBy(Actor actor) {
        try {
            var driver = BrowseTheWeb.as(actor).getDriver();
            var tbody = driver.findElements(By.cssSelector("tbody"));
            if (tbody.isEmpty()) return false;
            return tbody.get(0).getText().contains(motivoEsperado);
        } catch (Exception e) {
            return false;
        }
    }
}
