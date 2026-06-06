import { useState } from "react";

function Duenos() {

  const [dueno, setDueno] = useState({
    cedula: "",
    nombre: "",
    telefono: ""
  });

  const manejarCambio = (e) => {
    setDueno({
      ...dueno,
      [e.target.name]: e.target.value
    });
  };

  const guardarDueno = (e) => {
    e.preventDefault();

    console.log("Dueño registrado:", dueno);

    alert("Dueño registrado correctamente");
  };

  return (
    <div>
      <h1>Registrar Dueño</h1>

      <form onSubmit={guardarDueno}>

        <div>
          <label>Cédula:</label>
          <br />
          <input
            type="text"
            name="cedula"
            value={dueno.cedula}
            onChange={manejarCambio}
          />
        </div>

        <br />

        <div>
          <label>Nombre:</label>
          <br />
          <input
            type="text"
            name="nombre"
            value={dueno.nombre}
            onChange={manejarCambio}
          />
        </div>

        <br />

        <div>
          <label>Teléfono:</label>
          <br />
          <input
            type="text"
            name="telefono"
            value={dueno.telefono}
            onChange={manejarCambio}
          />
        </div>

        <br />

        <button type="submit">
          Guardar Dueño
        </button>

      </form>
    </div>
  );
}

export default Duenos;