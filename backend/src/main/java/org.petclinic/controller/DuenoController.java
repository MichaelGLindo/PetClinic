package org.petclinic.controller;

import org.petclinic.entity.Dueno;
import org.petclinic.repository.DuenoRepository;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/duenos")
@CrossOrigin(origins = "http://localhost:3000")
public class DuenoController {

    private final DuenoRepository repository;

    public DuenoController(DuenoRepository repository) {
        this.repository = repository;
    }

    @GetMapping
    public List<Dueno> listar() {
        return repository.findAll();
    }

    @PostMapping
    public Dueno guardar(@RequestBody Dueno dueno) {
        return repository.save(dueno);
    }
}