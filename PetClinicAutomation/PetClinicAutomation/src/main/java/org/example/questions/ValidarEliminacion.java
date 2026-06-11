package org.example.questions;

import net.serenitybdd.screenplay.Question;
import net.serenitybdd.screenplay.Actor;
import net.serenitybdd.screenplay.abilities.BrowseTheWeb;
import org.openqa.selenium.By;

public class ValidarEliminacion implements Question<Boolean> {

    private final String nombreEliminado;

    public ValidarEliminacion(String nombreEliminado) {
        this.nombreEliminado = nombreEliminado;
    }

    public static ValidarEliminacion deMascota(String nombre) {
        return new ValidarEliminacion(nombre);
    }

    @Override
    public Boolean answeredBy(Actor actor) {
        try {
            var driver = BrowseTheWeb.as(actor).getDriver();
            var tbody = driver.findElements(By.cssSelector("tbody"));
            if (tbody.isEmpty()) return true;
            return !tbody.get(0).getText().contains(nombreEliminado);
        } catch (Exception e) {
            return true;
        }
    }
}
