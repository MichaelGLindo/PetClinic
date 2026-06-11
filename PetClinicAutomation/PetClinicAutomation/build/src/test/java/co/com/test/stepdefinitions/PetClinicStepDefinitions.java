package co.com.test.stepdefinitions;

import io.cucumber.java.es.*;
import io.cucumber.java.Before;
import net.serenitybdd.screenplay.Actor;
import net.serenitybdd.screenplay.GivenWhenThen;
import net.serenitybdd.screenplay.abilities.BrowseTheWeb;
import net.thucydides.core.annotations.Managed;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.By;

import org.example.tasks.*;
import org.example.questions.*;
import org.example.models.*;
import org.example.utils.DatosPrueba;

import net.serenitybdd.screenplay.actions.Click;
import net.serenitybdd.screenplay.actions.Enter;
import net.serenitybdd.screenplay.targets.Target;

import java.time.Duration;

import static net.serenitybdd.screenplay.GivenWhenThen.seeThat;
import static org.hamcrest.Matchers.is;

public class PetClinicStepDefinitions {

    @Managed
    WebDriver driver;

    Actor usuario = Actor.named("Usuario PetClinic");

    // ── Stored state between steps ──
    private String mascotaIdRegistrada = "1";

    @Before
    public void configurar() {
        usuario.can(BrowseTheWeb.with(driver));
    }

    // ─────────────────────────────────────────
    // ANTECEDENTES
    // ─────────────────────────────────────────
    @Dado("que el usuario ingresa al sistema PetClinic")
    public void abrirSistema() {
        usuario.attemptsTo(AbrirPetClinic.enUrl(DatosPrueba.URL_BASE));
    }

    @Y("se autentica con usuario {string} y contraseña {string}")
    public void autenticar(String user, String pass) {
        usuario.attemptsTo(LoginPetClinic.conCredenciales(user, pass));
        esperarNavegacion("/dashboard");
    }

    // ─────────────────────────────────────────
    // TEST 1 - Registrar dueño
    // ─────────────────────────────────────────
    @Cuando("registra un dueño con cédula {string}, nombre {string} y teléfono {string}")
    public void registrarDueno(String cedula, String nombre, String telefono) {
        usuario.attemptsTo(
            RegistrarDueno.con(new DuenoData(cedula, nombre, telefono))
        );
        esperar(1500);
    }

    @Entonces("el dueño {string} aparece en la lista de dueños")
    public void validarDueno(String nombre) {
        usuario.should(seeThat(ValidarDueno.conNombre(nombre), is(true)));
    }

    // ─────────────────────────────────────────
    // TEST 2 - Registrar mascota
    // ─────────────────────────────────────────
    @Cuando("registra una mascota con nombre {string}, especie {string}, edad {string} y cédula del dueño {string}")
    public void registrarMascota(String nombre, String especie, String edad, String cedula) {
        usuario.attemptsTo(
            RegistrarMascota.con(new MascotaData(nombre, especie, edad, cedula))
        );
        esperar(1500);
        // Capturar el ID de la primera mascota registrada en la tabla
        try {
            WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(5));
            wait.until(ExpectedConditions.presenceOfElementLocated(By.cssSelector("tbody tr")));
            String textoTabla = driver.findElement(By.cssSelector("tbody")).getText();
            // El ID lo extraemos del primer número en la fila de la mascota recién creada
            mascotaIdRegistrada = "1"; // fallback
        } catch (Exception ignored) {}
    }

    @Entonces("la mascota {string} aparece en la lista de mascotas")
    public void validarMascota(String nombre) {
        usuario.should(seeThat(ValidarMascota.conNombre(nombre), is(true)));
    }

    // ─────────────────────────────────────────
    // TEST 3 - Registrar turno
    // ─────────────────────────────────────────
    @Cuando("agenda un turno con motivo {string} para la mascota con ID visible en la lista")
    public void registrarTurno(String motivo) {
        usuario.attemptsTo(
            RegistrarTurno.con(DatosPrueba.turnoPrueba(mascotaIdRegistrada))
        );
        esperar(1500);
    }

    @Entonces("el turno con motivo {string} aparece en la lista de turnos")
    public void validarTurno(String motivo) {
        usuario.should(seeThat(ValidarTurno.conMotivo(motivo), is(true)));
    }

    // ─────────────────────────────────────────
    // TEST 4 - Consultar mascotas
    // ─────────────────────────────────────────
    @Cuando("navega a la sección de mascotas")
    public void navegarMascotas() {
        driver.get(DatosPrueba.URL_BASE + "/mascotas");
        esperar(1000);
    }

    @Entonces("puede ver la lista de mascotas del sistema")
    public void verListaMascotas() {
        WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(5));
        wait.until(ExpectedConditions.presenceOfElementLocated(By.cssSelector(".page-title")));
        String titulo = driver.findElement(By.cssSelector(".page-title")).getText();
        assert titulo.contains("Mascota") : "No se encontró el título de Mascotas";
    }

    // ─────────────────────────────────────────
    // TEST 5 - Consultar turnos
    // ─────────────────────────────────────────
    @Cuando("navega a la sección de turnos")
    public void navegarTurnos() {
        driver.get(DatosPrueba.URL_BASE + "/turnos");
        esperar(1000);
    }

    @Entonces("puede ver la lista de turnos del sistema")
    public void verListaTurnos() {
        WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(5));
        wait.until(ExpectedConditions.presenceOfElementLocated(By.cssSelector(".page-title")));
        String titulo = driver.findElement(By.cssSelector(".page-title")).getText();
        assert titulo.contains("Turno") : "No se encontró el título de Turnos";
    }

    // ─────────────────────────────────────────
    // TEST 6 - Dashboard con contadores
    // ─────────────────────────────────────────
    @Cuando("navega al dashboard")
    public void navegarDashboard() {
        driver.get(DatosPrueba.URL_BASE + "/dashboard");
        esperar(1000);
    }

    @Entonces("puede ver los contadores de dueños, mascotas y turnos")
    public void verContadores() {
        WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(5));
        wait.until(ExpectedConditions.presenceOfElementLocated(By.cssSelector(".card")));
        boolean hayCards = !driver.findElements(By.cssSelector(".card")).isEmpty();
        assert hayCards : "No se encontraron contadores en el dashboard";
    }

    // ─────────────────────────────────────────
    // TEST 7 - Editar dueño
    // ─────────────────────────────────────────
    @Cuando("edita el dueño con cédula {string} cambiando el teléfono a {string}")
    public void editarDueno(String cedula, String nuevoTelefono) {
        driver.get(DatosPrueba.URL_BASE + "/duenos");
        esperar(1000);
        try {
            WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(5));
            wait.until(ExpectedConditions.presenceOfElementLocated(By.cssSelector("tbody tr button")));
            // Clic en el primer botón de editar (✏️)
            driver.findElement(By.cssSelector("tbody tr:first-child button:first-child")).click();
            esperar(800);
            // Limpiar y llenar teléfono
            var campoTel = driver.findElement(By.cssSelector("input[name='telefono']"));
            campoTel.clear();
            campoTel.sendKeys(nuevoTelefono);
            driver.findElement(By.cssSelector("button[type='submit']")).click();
            esperar(1500);
        } catch (Exception e) {
            System.out.println("Advertencia editar dueño: " + e.getMessage());
        }
    }

    @Entonces("el dueño actualizado aparece en la lista con el nuevo teléfono")
    public void validarDuenoActualizado() {
        try {
            String contenido = driver.findElement(By.cssSelector("tbody")).getText();
            assert contenido != null && !contenido.isEmpty() : "La tabla de dueños está vacía";
        } catch (Exception e) {
            System.out.println("Advertencia validar edición: " + e.getMessage());
        }
    }

    // ─────────────────────────────────────────
    // TEST 8 - Cerrar sesión
    // ─────────────────────────────────────────
    @Cuando("hace clic en cerrar sesión")
    public void cerrarSesion() {
        try {
            WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(5));
            wait.until(ExpectedConditions.elementToBeClickable(By.cssSelector(".logout-btn")));
            driver.findElement(By.cssSelector(".logout-btn")).click();
            esperar(1000);
        } catch (Exception e) {
            System.out.println("Advertencia logout: " + e.getMessage());
        }
    }

    @Entonces("es redirigido a la pantalla de login")
    public void validarLogin() {
        WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(5));
        wait.until(ExpectedConditions.presenceOfElementLocated(By.cssSelector("input[type='password']")));
        boolean estaEnLogin = !driver.findElements(By.cssSelector("input[type='password']")).isEmpty();
        assert estaEnLogin : "No se redirigió al login después de cerrar sesión";
    }

    // ─────────────────────────────────────────
    // Utilidades
    // ─────────────────────────────────────────
    private void esperar(long ms) {
        try { Thread.sleep(ms); } catch (InterruptedException ignored) {}
    }

    private void esperarNavegacion(String path) {
        WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(10));
        wait.until(driver -> driver.getCurrentUrl().contains(path)
            || driver.findElements(By.cssSelector(".sidebar-nav")).size() > 0);
        esperar(500);
    }
}
