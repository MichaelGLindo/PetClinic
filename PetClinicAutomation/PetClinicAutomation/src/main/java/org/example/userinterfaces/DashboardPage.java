package org.example.userinterfaces;

import net.serenitybdd.screenplay.targets.Target;
import org.openqa.selenium.By;

public class DashboardPage {
    public static final Target linkDuenos    = Target.the("link dueños").located(By.cssSelector("a[href='/duenos']"));
    public static final Target linkMascotas  = Target.the("link mascotas").located(By.cssSelector("a[href='/mascotas']"));
    public static final Target linkTurnos    = Target.the("link turnos").located(By.cssSelector("a[href='/turnos']"));
    public static final Target linkDashboard = Target.the("link dashboard").located(By.cssSelector("a[href='/dashboard']"));
    public static final Target botonLogout   = Target.the("botón logout").located(By.cssSelector(".logout-btn"));
    public static final Target tituloPagina  = Target.the("título página").located(By.cssSelector(".page-title"));
}
