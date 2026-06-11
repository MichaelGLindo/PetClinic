import { useState, useEffect } from "react";
import { getMascotas, createMascota, updateMascota, deleteMascota } from "../../services/api";

const empty = { nombre: "", especie: "", edad: "", cedulaDueno: "" };

function Mascotas() {
  const [mascota, setMascota] = useState(empty);
  const [lista, setLista] = useState([]);
  const [loading, setLoading] = useState(false);
  const [mensaje, setMensaje] = useState("");
  const [editandoId, setEditandoId] = useState(null);

  useEffect(() => {
    cargarMascotas();
  }, []);

  const cargarMascotas = async () => {
    try {
      const data = await getMascotas();
      setLista(Array.isArray(data) ? data : []);
    } catch (err) {
      console.error(err);
    }
  };

  const manejarCambio = (e) => {
    setMascota({ ...mascota, [e.target.name]: e.target.value });
  };

  const guardarMascota = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      if (editandoId) {
        await updateMascota(editandoId, mascota);
        setMensaje("✅ Mascota actualizada correctamente");
        setEditandoId(null);
      } else {
        await createMascota(mascota);
        setMensaje("✅ Mascota registrada correctamente");
      }
      setMascota(empty);
      cargarMascotas();
    } catch (err) {
      setMensaje("❌ Error al guardar: " + err.message);
    } finally {
      setLoading(false);
      setTimeout(() => setMensaje(""), 3000);
    }
  };

  const editarMascota = (m) => {
    setEditandoId(m.id);
    setMascota({
      nombre: m.nombre,
      especie: m.especie,
      edad: m.edad,
      cedulaDueno: m.dueno?.cedula || "",
    });
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const cancelarEdicion = () => {
    setEditandoId(null);
    setMascota(empty);
  };

  const eliminarMascota = async (id) => {
    if (!window.confirm("¿Eliminar esta mascota?")) return;
    try {
      await deleteMascota(id);
      cargarMascotas();
    } catch (err) {
      alert("Error al eliminar: " + err.message);
    }
  };

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">Mascotas</h1>
        <p className="page-subtitle">Registro de mascotas</p>
      </div>

      {mensaje && (
        <div className={`alert ${mensaje.startsWith("✅") ? "alert-success" : "alert-error"}`}
          style={{ marginBottom: "1rem" }}>
          {mensaje}
        </div>
      )}

      <div className="card" style={{ marginBottom: "2rem" }}>
        <h2 style={{ fontSize: "1rem", fontWeight: 700, marginBottom: "1rem" }}>
          {editandoId ? "✏️ Editando Mascota" : "Nueva Mascota"}
        </h2>
        <form onSubmit={guardarMascota} style={{ display: "flex", gap: "1rem", flexWrap: "wrap" }}>
          <input
            className="form-input"
            type="text"
            name="nombre"
            placeholder="Nombre"
            value={mascota.nombre}
            onChange={manejarCambio}
            required
            style={{ flex: 1, minWidth: "140px" }}
          />
          <input
            className="form-input"
            type="text"
            name="especie"
            placeholder="Especie (ej: Perro, Gato)"
            value={mascota.especie}
            onChange={manejarCambio}
            required
            style={{ flex: 1, minWidth: "140px" }}
          />
          <input
            className="form-input"
            type="number"
            name="edad"
            placeholder="Edad"
            value={mascota.edad}
            onChange={manejarCambio}
            required
            min="0"
            style={{ flex: 1, minWidth: "100px" }}
          />
          <input
            className="form-input"
            type="text"
            name="cedulaDueno"
            placeholder="Cédula del Dueño"
            value={mascota.cedulaDueno}
            onChange={manejarCambio}
            required
            style={{ flex: 1, minWidth: "140px" }}
          />
          <button className="btn btn-primary" type="submit" disabled={loading}>
            {loading ? "Guardando..." : editandoId ? "💾 Actualizar" : "➕ Guardar"}
          </button>
          {editandoId && (
            <button type="button" onClick={cancelarEdicion}
              style={{ padding: "0.65rem 1rem", borderRadius: "var(--radius-md)", border: "1px solid var(--border-color)", background: "none", cursor: "pointer", fontWeight: 600 }}>
              Cancelar
            </button>
          )}
        </form>
      </div>

      <div className="card">
        <h2 style={{ fontSize: "1rem", fontWeight: 700, marginBottom: "1rem" }}>
          Lista de Mascotas ({lista.length})
        </h2>
        {lista.length === 0 ? (
          <p style={{ color: "var(--text-muted)" }}>No hay mascotas registradas.</p>
        ) : (
          <table style={{ width: "100%", borderCollapse: "collapse", fontSize: "0.9rem" }}>
            <thead>
              <tr style={{ borderBottom: "2px solid var(--border-color)" }}>
                <th style={th}>Nombre</th>
                <th style={th}>Especie</th>
                <th style={th}>Edad</th>
                <th style={th}>Dueño</th>
                <th style={th}>Acciones</th>
              </tr>
            </thead>
            <tbody>
              {lista.map((m) => (
                <tr key={m.id} style={{ borderBottom: "1px solid var(--border-color)" }}>
                  <td style={td}>{m.nombre}</td>
                  <td style={td}>{m.especie}</td>
                  <td style={td}>{m.edad}</td>
                  <td style={td}>{m.dueno?.cedula} — {m.dueno?.nombre}</td>
                  <td style={td}>
                    <button onClick={() => editarMascota(m)}
                      style={{ background: "none", border: "none", cursor: "pointer", fontSize: "1.1rem", marginRight: "0.5rem" }}>
                      ✏️
                    </button>
                    <button onClick={() => eliminarMascota(m.id)}
                      style={{ background: "none", border: "none", cursor: "pointer", color: "#e74c3c", fontSize: "1.1rem" }}>
                      🗑️
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}

const th = { textAlign: "left", padding: "0.5rem 0.75rem", color: "var(--text-muted)", fontWeight: 600 };
const td = { padding: "0.5rem 0.75rem" };

export default Mascotas;