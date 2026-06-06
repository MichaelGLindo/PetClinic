package org.petclinic.repository;

import org.petclinic.entity.Dueno;
import org.springframework.data.jpa.repository.JpaRepository;

public interface DuenoRepository extends JpaRepository<Dueno, String> {
}