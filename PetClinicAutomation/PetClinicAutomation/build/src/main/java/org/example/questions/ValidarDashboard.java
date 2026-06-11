package org.example.questions;

import net.serenitybdd.screenplay.Question;
import net.serenitybdd.screenplay.Actor;
import net.serenitybdd.screenplay.abilities.BrowseTheWeb;
import org.openqa.selenium.By;

public class ValidarDashboard implements Question<Boolean> {

    public static ValidarDashboard estaVisible() {
        return new ValidarDashboard();
    }

    @Override
    public Boolean answeredBy(Actor actor) {
        try {
            var driver = BrowseTheWeb.as(actor).getDriver();
            var elementos = driver.findElements(By.cssSelector(".page-title"));
            return !elementos.isEmpty() && !elementos.get(0).getText().isEmpty();
        } catch (Exception e) {
            return false;
        }
    }
}
