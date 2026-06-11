import { useState, useEffect } from "react";
import { getTurnos, createTurno, updateTurno, deleteTurno } from "../../services/api";

const empty = { fecha: "", motivo: "", mascotaId: "" };

function Turnos() {
  const [turno, setTurno] = useState(empty);
  const [lista, setLista] = useState([]);
  const [loading, setLoading] = useState(false);
  const [mensaje, setMensaje] = useState("");
  const [editandoId, setEditandoId] = useState(null);

  useEffect(() => {
    cargarTurnos();
  }, []);

  const cargarTurnos = async () => {
    try {
      const data = await getTurnos();
      setLista(Array.isArray(data) ? data : []);
    } catch (err) {
      console.error(err);
    }
  };

  const manejarCambio = (e) => {
    setTurno({ ...turno, [e.target.name]: e.target.value });
  };

  const guardarTurno = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      if (editandoId) {
        await updateTurno(editandoId, turno);
        setMensaje("✅ Turno actualizado correctamente");
        setEditandoId(null);
      } else {
        await createTurno(turno);
        setMensaje("✅ Turno agendado correctamente");
      }
      setTurno(empty);
      cargarTurnos();
    } catch (err) {
      setMensaje("❌ Error al guardar: " + err.message);
    } finally {
      setLoading(false);
      setTimeout(() => setMensaje(""), 3000);
    }
  };

  const editarTurno = (t) => {
    setEditandoId(t.id);
    setTurno({
      fecha: t.fecha ? t.fecha.slice(0, 16) : "",
      motivo: t.motivo || "",
      mascotaId: t.mascota?.id || "",
    });
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const cancelarEdicion = () => {
    setEditandoId(null);
    setTurno(empty);
  };

  const eliminarTurno = async (id) => {
    if (!window.confirm("¿Eliminar este turno?")) return;
    try {
      await deleteTurno(id);
      cargarTurnos();
    } catch (err) {
      alert("Error al eliminar: " + err.message);
    }
  };

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">Turnos</h1>
        <p className="page-subtitle">Agenda de consultas veterinarias</p>
      </div>

      {mensaje && (
        <div className={`alert ${mensaje.startsWith("✅") ? "alert-success" : "alert-error"}`}
          style={{ marginBottom: "1rem" }}>
          {mensaje}
        </div>
      )}

      <div className="card" style={{ marginBottom: "2rem" }}>
        <h2 style={{ fontSize: "1rem", fontWeight: 700, marginBottom: "1rem" }}>
          {editandoId ? "✏️ Editando Turno" : "Nuevo Turno"}
        </h2>
        <form onSubmit={guardarTurno} style={{ display: "flex", gap: "1rem", flexWrap: "wrap" }}>
          <input
            className="form-input"
            type="datetime-local"
            name="fecha"
            value={turno.fecha}
            onChange={manejarCambio}
            required
            style={{ flex: 1, minWidth: "180px" }}
          />
          <input
            className="form-input"
            type="number"
            name="mascotaId"
            placeholder="ID de la Mascota"
            value={turno.mascotaId}
            onChange={manejarCambio}
            required
            min="1"
            style={{ flex: 1, minWidth: "140px" }}
          />
          <textarea
            className="form-input"
            name="motivo"
            placeholder="Motivo de la consulta"
            value={turno.motivo}
            onChange={manejarCambio}
            required
            rows="1"
            style={{ flex: 2, minWidth: "200px", resize: "none" }}
          />
          <button className="btn btn-primary" type="submit" disabled={loading}>
            {loading ? "Guardando..." : editandoId ? "💾 Actualizar" : "📅 Agendar"}
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
          Lista de Turnos ({lista.length})
        </h2>
        {lista.length === 0 ? (
          <p style={{ color: "var(--text-muted)" }}>No hay turnos agendados.</p>
        ) : (
          <table style={{ width: "100%", borderCollapse: "collapse", fontSize: "0.9rem" }}>
            <thead>
              <tr style={{ borderBottom: "2px solid var(--border-color)" }}>
                <th style={th}>Fecha</th>
                <th style={th}>Motivo</th>
                <th style={th}>Mascota</th>
                <th style={th}>Acciones</th>
              </tr>
            </thead>
            <tbody>
              {lista.map((t) => (
                <tr key={t.id} style={{ borderBottom: "1px solid var(--border-color)" }}>
                  <td style={td}>{t.fecha ? new Date(t.fecha).toLocaleString("es-CO") : "-"}</td>
                  <td style={td}>{t.motivo}</td>
                  <td style={td}>{t.mascota?.id} — {t.mascota?.nombre}</td>
                  <td style={td}>
                    <button onClick={() => editarTurno(t)}
                      style={{ background: "none", border: "none", cursor: "pointer", fontSize: "1.1rem", marginRight: "0.5rem" }}>
                      ✏️
                    </button>
                    <button onClick={() => eliminarTurno(t.id)}
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

export default Turnos;