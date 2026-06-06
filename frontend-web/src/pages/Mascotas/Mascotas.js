import { useState } from "react";

function Mascotas() {

  const [mascota, setMascota] = useState({
    nombre: "",
    especie: "",
    edad: "",
    cedulaDueno: ""
  });

  const manejarCambio = (e) => {
    setMascota({
      ...mascota,
      [e.target.name]: e.target.value
    });
  };

  const guardarMascota = (e) => {
    e.preventDefault();

    console.log("Mascota registrada:", mascota);

    alert("Mascota registrada correctamente");
  };

  return (
    <div>
      <h1>Registrar Mascota</h1>

      <form onSubmit={guardarMascota}>

        <div>
          <label>Nombre:</label>
          <br />
          <input
            type="text"
            name="nombre"
            value={mascota.nombre}
            onChange={manejarCambio}
          />
        </div>

        <br />

        <div>
          <label>Especie:</label>
          <br />
          <input
            type="text"
            name="especie"
            value={mascota.especie}
            onChange={manejarCambio}
          />
        </div>

        <br />

        <div>
          <label>Edad:</label>
          <br />
          <input
            type="number"
            name="edad"
            value={mascota.edad}
            onChange={manejarCambio}
          />
        </div>

        <br />

        <div>
          <label>Cédula del Dueño:</label>
          <br />
          <input
            type="text"
            name="cedulaDueno"
            value={mascota.cedulaDueno}
            onChange={manejarCambio}
          />
        </div>

        <br />

        <button type="submit">
          Guardar Mascota
        </button>

      </form>
    </div>
  );
}

export default Mascotas;