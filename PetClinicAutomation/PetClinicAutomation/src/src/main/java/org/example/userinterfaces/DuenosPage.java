package org.example.userinterfaces;

import net.serenitybdd.core.pages.PageObject;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;

public class DuenosPage extends PageObject {

    @FindBy(css = "input[name='cedula']")
    public WebElement campoCedula;

    @FindBy(css = "input[name='nombre']")
    public WebElement campoNombre;

    @FindBy(css = "input[name='telefono']")
    public WebElement campoTelefono;

    @FindBy(css = "button[type='submit']")
    public WebElement botonGuardar;

    @FindBy(css = "tbody")
    public WebElement tablaCuerpo;
}
