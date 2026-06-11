package org.example.userinterfaces;

import net.serenitybdd.screenplay.targets.Target;
import org.openqa.selenium.By;

public class LoginPage {
    public static final Target campoUsuario  = Target.the("campo usuario").located(By.cssSelector("input[name='username'], input[type='text']"));
    public static final Target campoPassword = Target.the("campo password").located(By.cssSelector("input[type='password']"));
    public static final Target botonIngresar = Target.the("botón ingresar").located(By.cssSelector("button[type='submit']"));
}
