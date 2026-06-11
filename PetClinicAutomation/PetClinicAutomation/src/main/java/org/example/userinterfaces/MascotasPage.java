package org.example.userinterfaces;

import net.serenitybdd.screenplay.targets.Target;
import org.openqa.selenium.By;

public class MascotasPage {
    public static final Target campoNombre      = Target.the("campo nombre").located(By.cssSelector("input[name='nombre']"));
    public static final Target campoEspecie     = Target.the("campo especie").located(By.cssSelector("input[name='especie']"));
    public static final Target campoEdad        = Target.the("campo edad").located(By.cssSelector("input[name='edad']"));
    public static final Target campoCedulaDueno = Target.the("campo cédula dueño").located(By.cssSelector("input[name='cedulaDueno']"));
    public static final Target botonGuardar     = Target.the("botón guardar").located(By.cssSelector("button[type='submit']"));
    public static final Target tablaCuerpo      = Target.the("tabla cuerpo").located(By.cssSelector("tbody"));
}
