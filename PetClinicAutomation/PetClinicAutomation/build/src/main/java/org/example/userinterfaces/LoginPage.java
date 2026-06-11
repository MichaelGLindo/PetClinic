package org.example.userinterfaces;

import net.serenitybdd.core.pages.PageObject;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;

public class LoginPage extends PageObject {

    @FindBy(css = "input[name='username'], input[type='text']")
    public WebElement campoUsuario;

    @FindBy(css = "input[type='password']")
    public WebElement campoPassword;

    @FindBy(css = "button[type='submit']")
    public WebElement botonIngresar;
}
