package org.petclinic.controller;

import org.petclinic.entity.Mascota;
import org.petclinic.repository.MascotaRepository;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/mascotas")
@CrossOrigin(origins = "http://localhost:3000")
public class MascotaController {

    private final MascotaRepository repository;

    public MascotaController(MascotaRepository repository) {
        this.repository = repository;
    }

    @GetMapping
    public List<Mascota> listar() {
        return repository.findAll();
    }

    @PostMapping
    public Mascota guardar(@RequestBody Mascota mascota) {
        return repository.save(mascota);
    }
}