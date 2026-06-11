package org.example.userinterfaces;

import net.serenitybdd.screenplay.targets.Target;
import org.openqa.selenium.By;

public class TurnosPage {
    public static final Target campoFecha    = Target.the("campo fecha").located(By.cssSelector("input[name='fecha']"));
    public static final Target campoMascotaId = Target.the("campo mascota id").located(By.cssSelector("input[name='mascotaId']"));
    public static final Target campoMotivo   = Target.the("campo motivo").located(By.cssSelector("textarea[name='motivo']"));
    public static final Target botonGuardar  = Target.the("botón guardar").located(By.cssSelector("button[type='submit']"));
    public static final Target tablaCuerpo   = Target.the("tabla cuerpo").located(By.cssSelector("tbody"));
}
