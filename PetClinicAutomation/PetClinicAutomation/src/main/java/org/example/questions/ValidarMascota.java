package org.example.questions;

import net.serenitybdd.screenplay.Question;
import net.serenitybdd.screenplay.Actor;
import net.serenitybdd.screenplay.abilities.BrowseTheWeb;
import org.openqa.selenium.By;

public class ValidarMascota implements Question<Boolean> {

    private final String nombreEsperado;

    public ValidarMascota(String nombreEsperado) {
        this.nombreEsperado = nombreEsperado;
    }

    public static ValidarMascota conNombre(String nombre) {
        return new ValidarMascota(nombre);
    }

    @Override
    public Boolean answeredBy(Actor actor) {
        try {
            var driver = BrowseTheWeb.as(actor).getDriver();
            var tbody = driver.findElements(By.cssSelector("tbody"));
            if (tbody.isEmpty()) return false;
            return tbody.get(0).getText().contains(nombreEsperado);
        } catch (Exception e) {
            return false;
        }
    }
}
