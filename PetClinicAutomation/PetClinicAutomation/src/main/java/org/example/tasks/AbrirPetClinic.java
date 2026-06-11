package org.example.tasks;

import net.serenitybdd.screenplay.Task;
import net.serenitybdd.screenplay.Actor;
import net.serenitybdd.screenplay.actions.Open;
import net.serenitybdd.annotations.Step;

public class AbrirPetClinic implements Task {

    private final String url;

    public AbrirPetClinic(String url) {
        this.url = url;
    }

    public static AbrirPetClinic enUrl(String url) {
        return new AbrirPetClinic(url);
    }

    @Override
    @Step("{0} abre PetClinic en {url}")
    public <T extends Actor> void performAs(T actor) {
        actor.attemptsTo(Open.url(url));
    }
}
