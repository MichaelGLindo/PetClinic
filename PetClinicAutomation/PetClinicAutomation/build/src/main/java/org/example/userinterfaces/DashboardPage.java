package org.example.userinterfaces;

import net.serenitybdd.core.pages.PageObject;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;

public class DashboardPage extends PageObject {

    @FindBy(css = "a[href='/duenos']")
    public WebElement linkDuenos;

    @FindBy(css = "a[href='/mascotas']")
    public WebElement linkMascotas;

    @FindBy(css = "a[href='/turnos']")
    public WebElement linkTurnos;

    @FindBy(css = "a[href='/dashboard']")
    public WebElement linkDashboard;

    @FindBy(css = ".logout-btn")
    public WebElement botonLogout;

    @FindBy(css = ".page-title")
    public WebElement tituloPagina;
}
