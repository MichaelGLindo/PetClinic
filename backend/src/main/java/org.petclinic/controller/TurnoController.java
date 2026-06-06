package org.petclinic.controller;

import org.petclinic.entity.Turno;
import org.petclinic.repository.TurnoRepository;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/turnos")
@CrossOrigin(origins = "http://localhost:3000")
public class TurnoController {

    private final TurnoRepository repository;

    public TurnoController(TurnoRepository repository) {
        this.repository = repository;
    }

    @GetMapping
    public List<Turno> listar() {
        return repository.findAll();
    }

    @PostMapping
    public Turno guardar(@RequestBody Turno turno) {
        return repository.save(turno);
    }
}