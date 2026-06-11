package org.example.userinterfaces;

import net.serenitybdd.core.pages.PageObject;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;

public class MascotasPage extends PageObject {

    @FindBy(css = "input[name='nombre']")
    public WebElement campoNombre;

    @FindBy(css = "input[name='especie']")
    public WebElement campoEspecie;

    @FindBy(css = "input[name='edad']")
    public WebElement campoEdad;

    @FindBy(css = "input[name='cedulaDueno']")
    public WebElement campoCedulaDueno;

    @FindBy(css = "button[type='submit']")
    public WebElement botonGuardar;

    @FindBy(css = "tbody")
    public WebElement tablaCuerpo;
}
