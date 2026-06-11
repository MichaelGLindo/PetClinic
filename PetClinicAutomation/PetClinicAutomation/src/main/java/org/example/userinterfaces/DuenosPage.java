package org.example.userinterfaces;

import net.serenitybdd.screenplay.targets.Target;
import org.openqa.selenium.By;

public class DuenosPage {
    public static final Target campoCedula   = Target.the("campo cédula").located(By.cssSelector("input[name='cedula']"));
    public static final Target campoNombre   = Target.the("campo nombre").located(By.cssSelector("input[name='nombre']"));
    public static final Target campoTelefono = Target.the("campo teléfono").located(By.cssSelector("input[name='telefono']"));
    public static final Target botonGuardar  = Target.the("botón guardar").located(By.cssSelector("button[type='submit']"));
    public static final Target tablaCuerpo   = Target.the("tabla cuerpo").located(By.cssSelector("tbody"));
}
