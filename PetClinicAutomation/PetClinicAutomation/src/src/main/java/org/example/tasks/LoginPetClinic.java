package org.example.tasks;

import net.serenitybdd.screenplay.Task;
import net.serenitybdd.screenplay.Actor;
import net.serenitybdd.screenplay.actions.Click;
import net.serenitybdd.screenplay.actions.Enter;
import net.serenitybdd.annotations.Step;
import org.example.userinterfaces.LoginPage;

public class LoginPetClinic implements Task {

    private final String username;
    private final String password;

    public LoginPetClinic(String username, String password) {
        this.username = username;
        this.password = password;
    }

    public static LoginPetClinic conCredenciales(String username, String password) {
        return new LoginPetClinic(username, password);
    }

    @Override
    @Step("{0} inicia sesión con usuario {username}")
    public <T extends Actor> void performAs(T actor) {
        LoginPage loginPage = new LoginPage();
        actor.attemptsTo(
            Enter.theValue(username).into(loginPage.campoUsuario),
            Enter.theValue(password).into(loginPage.campoPassword),
            Click.on(loginPage.botonIngresar)
        );
    }
}
