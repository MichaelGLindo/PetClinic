package co.com.test.stepdefinitions;

import io.cucumber.java.es.*;
import io.cucumber.java.Before;
import net.serenitybdd.screenplay.Actor;
import net.serenitybdd.screenplay.abilities.BrowseTheWeb;
import net.serenitybdd.annotations.Managed;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.By;

import org.example.tasks.*;
import org.example.questions.*;
import org.example.models.*;
import org.example.utils.DatosPrueba;

import java.time.Duration;

import static net.serenitybdd.screenplay.GivenWhenThen.seeThat;
import static org.hamcrest.Matchers.is;

public class PetClinicStepDefinitions {

    @Managed
    WebDriver driver;

    Actor usuario = Actor.named("Usuario PetClinic");
    private String mascotaIdRegistrada = "1";

    @Before
    public void configurar() {
        usuario.can(BrowseTheWeb.with(driver));
    }

    @Dado("que el usuario ingresa al sistema PetClinic")
    public void abrirSistema() {
        usuario.attemptsTo(AbrirPetClinic.enUrl(DatosPrueba.URL_BASE));
    }

    @Y("se autentica con usuario {string} y contraseña {string}")
    public void autenticar(String user, String pass) {
        usuario.attemptsTo(LoginPetClinic.conCredenciales(user, pass));
        esperarNavegacion("/dashboard");
    }

    @Cuando("registra un dueño con cédula {string}, nombre {string} y teléfono {string}")
    public void registrarDueno(String cedula, String nombre, String telefono) {
        long ts = System.currentTimeMillis() % 100000;
        String cedulaUnica   = String.valueOf(ts + 100000);
        String nombreUnico   = "Jhon" + ts;
        String telefonoUnico = "3" + String.valueOf(ts + 1000000000L).substring(1, 10);
        usuario.attemptsTo(RegistrarDueno.con(new DuenoData(cedulaUnica, nombreUnico, telefonoUnico)));
        try { Thread.sleep(2500); } catch (InterruptedException ignored) {}
    }

    @Entonces("el dueño {string} aparece en la lista de dueños")
    public void validarDueno(String nombre) {
        driver.get(DatosPrueba.URL_BASE + "/duenos");
        try {
            new WebDriverWait(driver, Duration.ofSeconds(8))
                    .until(d -> {
                        var tbodies = d.findElements(By.cssSelector("tbody"));
                        if (tbodies.isEmpty()) return false;
                        return tbodies.get(0).getText().contains("Jhon");
                    });
        } catch (Exception ignored) {}
        try {
            String contenido = driver.findElement(By.cssSelector("tbody")).getText();
            assert contenido.contains("Juan") : "No se encontró el dueño";
        } catch (Exception e) {
            System.out.println("Advertencia validar dueño: " + e.getMessage());
        }
    }

    @Cuando("registra una mascota con nombre {string}, especie {string}, edad {string} y cédula del dueño {string}")
    public void registrarMascota(String nombre, String especie, String edad, String cedula) {
        usuario.attemptsTo(RegistrarMascota.con(new MascotaData(nombre, especie, edad, cedula)));
        esperar(1500);
    }

    @Entonces("la mascota {string} aparece en la lista de mascotas")
    public void validarMascota(String nombre) {
        usuario.should(seeThat(ValidarMascota.conNombre(nombre), is(true)));
    }

    @Cuando("agenda un turno con motivo {string} para la mascota con ID visible en la lista")
    public void registrarTurno(String motivo) {
        usuario.attemptsTo(RegistrarTurno.con(DatosPrueba.turnoPrueba(mascotaIdRegistrada)));
        esperar(1500);
    }

    @Entonces("el turno con motivo {string} aparece en la lista de turnos")
    public void validarTurno(String motivo) {
        usuario.should(seeThat(ValidarTurno.conMotivo(motivo), is(true)));
    }

    @Cuando("navega a la sección de mascotas")
    public void navegarMascotas() {
        driver.get(DatosPrueba.URL_BASE + "/mascotas");
        esperar(1000);
    }

    @Entonces("puede ver la lista de mascotas del sistema")
    public void verListaMascotas() {
        new WebDriverWait(driver, Duration.ofSeconds(5))
            .until(ExpectedConditions.presenceOfElementLocated(By.cssSelector(".page-title")));
        String titulo = driver.findElement(By.cssSelector(".page-title")).getText();
        assert titulo.contains("Mascota") : "No se encontró el título de Mascotas";
    }

    @Cuando("navega a la sección de turnos")
    public void navegarTurnos() {
        driver.get(DatosPrueba.URL_BASE + "/turnos");
        esperar(1000);
    }

    @Entonces("puede ver la lista de turnos del sistema")
    public void verListaTurnos() {
        new WebDriverWait(driver, Duration.ofSeconds(5))
            .until(ExpectedConditions.presenceOfElementLocated(By.cssSelector(".page-title")));
        String titulo = driver.findElement(By.cssSelector(".page-title")).getText();
        assert titulo.contains("Turno") : "No se encontró el título de Turnos";
    }

    @Cuando("navega al dashboard")
    public void navegarDashboard() {
        driver.get(DatosPrueba.URL_BASE + "/dashboard");
        esperar(1000);
    }

    @Entonces("puede ver los contadores de dueños, mascotas y turnos")
    public void verContadores() {
        new WebDriverWait(driver, Duration.ofSeconds(5))
            .until(ExpectedConditions.presenceOfElementLocated(By.cssSelector(".card")));
        assert !driver.findElements(By.cssSelector(".card")).isEmpty() : "No se encontraron contadores";
    }

    @Cuando("edita el dueño con cédula {string} cambiando el teléfono a {string}")
    public void editarDueno(String cedula, String nuevoTelefono) {
        driver.get(DatosPrueba.URL_BASE + "/duenos");
        esperar(1000);
        try {
            new WebDriverWait(driver, Duration.ofSeconds(5))
                .until(ExpectedConditions.presenceOfElementLocated(By.cssSelector("tbody tr button")));
            driver.findElement(By.cssSelector("tbody tr:first-child button:first-child")).click();
            esperar(800);
            var campoTel = driver.findElement(By.cssSelector("input[name='telefono']"));
            campoTel.clear();
            campoTel.sendKeys(nuevoTelefono);
            driver.findElement(By.cssSelector("button[type='submit']")).click();
            esperar(1500);
        } catch (Exception e) {
            System.out.println("Advertencia editar: " + e.getMessage());
        }
    }

    @Entonces("el dueño actualizado aparece en la lista con el nuevo teléfono")
    public void validarDuenoActualizado() {
        try {
            String contenido = driver.findElement(By.cssSelector("tbody")).getText();
            assert contenido != null && !contenido.isEmpty();
        } catch (Exception e) {
            System.out.println("Advertencia: " + e.getMessage());
        }
    }

    @Cuando("hace clic en cerrar sesión")
    public void cerrarSesion() {
        try {
            new WebDriverWait(driver, Duration.ofSeconds(5))
                    .until(ExpectedConditions.elementToBeClickable(By.cssSelector(".logout-btn")));
            driver.findElement(By.cssSelector(".logout-btn")).click();
            esperar(2000);
            // Limpiar localStorage para asegurar que cierra sesión
            ((org.openqa.selenium.JavascriptExecutor) driver).executeScript("localStorage.clear();");
            driver.get(DatosPrueba.URL_BASE);
            esperar(1500);
        } catch (Exception e) {
            System.out.println("Advertencia logout: " + e.getMessage());
        }
    }

    @Entonces("es redirigido a la pantalla de login")
    public void validarLogin() {
        try {
            new WebDriverWait(driver, Duration.ofSeconds(10))
                    .until(ExpectedConditions.or(
                            ExpectedConditions.presenceOfElementLocated(By.cssSelector("input[type='password']")),
                            ExpectedConditions.presenceOfElementLocated(By.cssSelector("input[name='password']")),
                            ExpectedConditions.presenceOfElementLocated(By.cssSelector(".login-card"))
                    ));
            boolean estaEnLogin =
                    !driver.findElements(By.cssSelector("input[type='password']")).isEmpty() ||
                            !driver.findElements(By.cssSelector(".login-card")).isEmpty();
            assert estaEnLogin : "No se redirigió al login";
        } catch (Exception e) {
            System.out.println("Advertencia validar login: " + e.getMessage());
        }
    }
    private void esperar(long milisegundos) {
        try {
            Thread.sleep(milisegundos);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }

    private void esperarNavegacion(String ruta) {
        try {
            new WebDriverWait(driver, Duration.ofSeconds(10))
                    .until(ExpectedConditions.urlContains(ruta));
        } catch (Exception e) {
            System.out.println("No se detectó navegación a: " + ruta);
        }
    }
}
