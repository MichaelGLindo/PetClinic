package org.example.userinterfaces;

import net.serenitybdd.core.pages.PageObject;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;

public class TurnosPage extends PageObject {

    @FindBy(css = "input[name='fecha']")
    public WebElement campoFecha;

    @FindBy(css = "input[name='mascotaId']")
    public WebElement campoMascotaId;

    @FindBy(css = "textarea[name='motivo']")
    public WebElement campoMotivo;

    @FindBy(css = "button[type='submit']")
    public WebElement botonGuardar;

    @FindBy(css = "tbody")
    public WebElement tablaCuerpo;
}
