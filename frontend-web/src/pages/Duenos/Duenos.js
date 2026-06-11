import { useState, useEffect } from "react";
import { getDuenos, createDueno, updateDueno, deleteDueno } from "../../services/api";

const empty = { cedula: "", nombre: "", telefono: "" };

function Duenos() {
  const [dueno, setDueno] = useState(empty);
  const [lista, setLista] = useState([]);
  const [loading, setLoading] = useState(false);
  const [mensaje, setMensaje] = useState("");
  const [editandoId, setEditandoId] = useState(null);

  useEffect(() => {
    cargarDuenos();
  }, []);

  const cargarDuenos = async () => {
    try {
      const data = await getDuenos();
      setLista(Array.isArray(data) ? data : []);
    } catch (err) {
      console.error(err);
    }
  };

  const manejarCambio = (e) => {
    setDueno({ ...dueno, [e.target.name]: e.target.value });
  };

  const guardarDueno = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      if (editandoId) {
        await updateDueno(editandoId, dueno);
        setMensaje("✅ Dueño actualizado correctamente");
        setEditandoId(null);
      } else {
        await createDueno(dueno);
        setMensaje("✅ Dueño registrado correctamente");
      }
      setDueno(empty);
      cargarDuenos();
    } catch (err) {
      setMensaje("❌ Error al guardar: " + err.message);
    } finally {
      setLoading(false);
      setTimeout(() => setMensaje(""), 3000);
    }
  };

  const editarDueno = (d) => {
    setEditandoId(d.cedula);
    setDueno({ cedula: d.cedula, nombre: d.nombre, telefono: d.telefono });
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const cancelarEdicion = () => {
    setEditandoId(null);
    setDueno(empty);
  };

  const eliminarDueno = async (id) => {
    if (!window.confirm("¿Eliminar este dueño?")) return;
    try {
      await deleteDueno(id);
      cargarDuenos();
    } catch (err) {
      alert("Error al eliminar: " + err.message);
    }
  };

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">Dueños</h1>
        <p className="page-subtitle">Registro de propietarios de mascotas</p>
      </div>

      {mensaje && (
        <div className={`alert ${mensaje.startsWith("✅") ? "alert-success" : "alert-error"}`}
          style={{ marginBottom: "1rem" }}>
          {mensaje}
        </div>
      )}

      <div className="card" style={{ marginBottom: "2rem" }}>
        <h2 style={{ fontSize: "1rem", fontWeight: 700, marginBottom: "1rem" }}>
          {editandoId ? "✏️ Editando Dueño" : "Nuevo Dueño"}
        </h2>
        <form onSubmit={guardarDueno} style={{ display: "flex", gap: "1rem", flexWrap: "wrap" }}>
          <input
            className="form-input"
            type="text"
            name="cedula"
            placeholder="Cédula"
            value={dueno.cedula}
            onChange={manejarCambio}
            required
            disabled={!!editandoId}
            style={{ flex: 1, minWidth: "140px", opacity: editandoId ? 0.6 : 1 }}
          />
          <input
            className="form-input"
            type="text"
            name="nombre"
            placeholder="Nombre completo"
            value={dueno.nombre}
            onChange={manejarCambio}
            required
            style={{ flex: 2, minWidth: "180px" }}
          />
          <input
            className="form-input"
            type="text"
            name="telefono"
            placeholder="Teléfono"
            value={dueno.telefono}
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
          Lista de Dueños ({lista.length})
        </h2>
        {lista.length === 0 ? (
          <p style={{ color: "var(--text-muted)" }}>No hay dueños registrados.</p>
        ) : (
          <table style={{ width: "100%", borderCollapse: "collapse", fontSize: "0.9rem" }}>
            <thead>
              <tr style={{ borderBottom: "2px solid var(--border-color)" }}>
                <th style={th}>Cédula</th>
                <th style={th}>Nombre</th>
                <th style={th}>Teléfono</th>
                <th style={th}>Acciones</th>
              </tr>
            </thead>
            <tbody>
              {lista.map((d) => (
                <tr key={d.cedula} style={{ borderBottom: "1px solid var(--border-color)" }}>
                  <td style={td}>{d.cedula}</td>
                  <td style={td}>{d.nombre}</td>
                  <td style={td}>{d.telefono}</td>
                  <td style={td}>
                    <button onClick={() => editarDueno(d)}
                      style={{ background: "none", border: "none", cursor: "pointer", fontSize: "1.1rem", marginRight: "0.5rem" }}>
                      ✏️
                    </button>
                    <button onClick={() => eliminarDueno(d.cedula)}
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

export default Duenos;