import { useState } from "react";

function Turnos() {

  const [turno, setTurno] = useState({
    fecha: "",
    motivo: "",
    mascotaId: ""
  });

  const manejarCambio = (e) => {
    setTurno({
      ...turno,
      [e.target.name]: e.target.value
    });
  };

  const guardarTurno = (e) => {
    e.preventDefault();

    console.log("Turno agendado:", turno);

    alert("Turno agendado correctamente");
  };

  return (
    <div>
      <h1>Agendar Turno</h1>

      <form onSubmit={guardarTurno}>

        <div>
          <label>Fecha:</label>
          <br />
          <input
            type="datetime-local"
            name="fecha"
            value={turno.fecha}
            onChange={manejarCambio}
          />
        </div>

        <br />

        <div>
          <label>Motivo de la consulta:</label>
          <br />
          <textarea
            name="motivo"
            rows="4"
            cols="40"
            value={turno.motivo}
            onChange={manejarCambio}
          />
        </div>

        <br />

        <div>
          <label>ID de la Mascota:</label>
          <br />
          <input
            type="number"
            name="mascotaId"
            value={turno.mascotaId}
            onChange={manejarCambio}
          />
        </div>

        <br />

        <button type="submit">
          Agendar Turno
        </button>

      </form>
    </div>
  );
}

export default Turnos;