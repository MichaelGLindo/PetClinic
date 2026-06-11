# PetClinic Automation - Serenity BDD

Proyecto de automatización con Serenity BDD + Cucumber + Selenium

## Requisitos
- Java 11+
- Gradle
- Chrome o Edge instalado
- Backend corriendo en http://localhost:8080
- Frontend corriendo en http://localhost:3000

## Correr las pruebas (un solo comando)

```bash
gradle clean test aggregate
```

## Ver el reporte HTML

Después de correr las pruebas abre:
```
target/site/serenity/index.html
```

## Correr solo con Edge

```bash
gradle clean test aggregate -Dwebdriver.driver=edge
```
