import { useState, useEffect } from "react";
import { getMascotas, createMascota, getTurnos, getTurnosPorFecha, createTurno, getHistoriales } from "../../services/api";

function ClientPortal() {
  const [activeTab, setActiveTab] = useState("mascotas");
  const [user, setUser] = useState(null);
  
  // Data lists
  const [mascotas, setMascotas] = useState([]);
  const [turnos, setTurnos] = useState([]);
  const [historiales, setHistoriales] = useState([]);
  
  // Loading & Messages
  const [loading, setLoading] = useState(false);
  const [mensaje, setMensaje] = useState("");
  
  // Form States
  const [nuevaMascota, setNuevaMascota] = useState({ nombre: "", especie: "", edad: "" });
  const [nuevoTurno, setNuevoTurno] = useState({ fecha: "", motivo: "", mascotaId: "" });
  const [fechaFiltro, setFechaFiltro] = useState("");

  const cargarTurnos = async (fecha) => {
    try {
      const f = fecha !== undefined ? fecha : fechaFiltro;
      let data;
      if (f) {
        data = await getTurnosPorFecha(f);
      } else {
        data = await getTurnos();
      }
      setTurnos(Array.isArray(data) ? data : []);
    } catch (err) {
      console.error("Error al cargar turnos:", err);
    }
  };

  const cargarDatos = async (fecha) => {
    setLoading(true);
    try {
      const petsData = await getMascotas();
      setMascotas(Array.isArray(petsData) ? petsData : []);

      await cargarTurnos(fecha);

      const historyData = await getHistoriales();
      setHistoriales(Array.isArray(historyData) ? historyData : []);
    } catch (err) {
      console.error("Error al cargar datos:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const userStr = localStorage.getItem("user");
    if (userStr) {
      const u = JSON.parse(userStr);
      setUser(u);
      cargarDatos();
    }
  }, []);

  useEffect(() => {
    cargarTurnos(fechaFiltro);
  }, [fechaFiltro]);

  const handleMascotaChange = (e) => {
    setNuevaMascota({ ...nuevaMascota, [e.target.name]: e.target.value });
  };

  const handleTurnoChange = (e) => {
    setNuevoTurno({ ...nuevoTurno, [e.target.name]: e.target.value });
  };

  const registrarMascota = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMensaje("");
    try {
      // Backend automatically assigns owner's cedula from token
      await createMascota({
        nombre: nuevaMascota.nombre,
        especie: nuevaMascota.especie,
        edad: parseInt(nuevaMascota.edad)
      });
      setMensaje("✅ Mascota registrada correctamente");
      setNuevaMascota({ nombre: "", especie: "", edad: "" });
      cargarDatos();
    } catch (err) {
      setMensaje("❌ Error al registrar mascota: " + err.message);
    } finally {
      setLoading(false);
      setTimeout(() => setMensaje(""), 3000);
    }
  };

  const agendarTurno = async (e) => {
    e.preventDefault();
    if (!nuevoTurno.mascotaId) {
      setMensaje("❌ Debe seleccionar una mascota");
      return;
    }
    setLoading(true);
    setMensaje("");
    try {
      await createTurno({
        fecha: nuevoTurno.fecha,
        motivo: nuevoTurno.motivo,
        mascotaId: parseInt(nuevoTurno.mascotaId)
      });
      setMensaje("✅ Cita agendada correctamente");
      setNuevoTurno({ fecha: "", motivo: "", mascotaId: "" });
      cargarDatos();
    } catch (err) {
      setMensaje("❌ Error al agendar turno: " + err.message);
    } finally {
      setLoading(false);
      setTimeout(() => setMensaje(""), 3000);
    }
  };

  const cambiarFechaTurnos = (e) => {
    setFechaFiltro(e.target.value);
  };

  return (
    <div>
      <div className="page-header" style={{ marginBottom: "2rem" }}>
        <h1 className="page-title">Portal de Propietarios</h1>
        <p className="page-subtitle">Hola, {user ? user.nombre : "Cargando..."}. Aquí puedes gestionar tus mascotas, turnos e historial clínico.</p>
      </div>

      {mensaje && (
        <div className={`alert ${mensaje.startsWith("✅") ? "alert-success" : "alert-error"}`}
          style={{ marginBottom: "1.5rem" }}>
          {mensaje}
        </div>
      )}

      {/* Tabs Menu */}
      <div style={{ display: "flex", gap: "1rem", borderBottom: "2px solid var(--border-color)", marginBottom: "2rem", paddingBottom: "0.5rem" }}>
        <button 
          onClick={() => setActiveTab("mascotas")}
          style={{
            background: "none",
            border: "none",
            fontSize: "1rem",
            fontWeight: 600,
            padding: "0.5rem 1rem",
            color: activeTab === "mascotas" ? "var(--primary-color)" : "var(--text-muted)",
            borderBottom: activeTab === "mascotas" ? "3px solid var(--primary-color)" : "3px solid transparent",
            cursor: "pointer",
            transition: "all 0.2s"
          }}
        >
          🐾 Mis Mascotas
        </button>
        <button 
          onClick={() => setActiveTab("turnos")}
          style={{
            background: "none",
            border: "none",
            fontSize: "1rem",
            fontWeight: 600,
            padding: "0.5rem 1rem",
            color: activeTab === "turnos" ? "var(--primary-color)" : "var(--text-muted)",
            borderBottom: activeTab === "turnos" ? "3px solid var(--primary-color)" : "3px solid transparent",
            cursor: "pointer",
            transition: "all 0.2s"
          }}
        >
          📅 Mis Turnos
        </button>
        <button 
          onClick={() => setActiveTab("historial")}
          style={{
            background: "none",
            border: "none",
            fontSize: "1rem",
            fontWeight: 600,
            padding: "0.5rem 1rem",
            color: activeTab === "historial" ? "var(--primary-color)" : "var(--text-muted)",
            borderBottom: activeTab === "historial" ? "3px solid var(--primary-color)" : "3px solid transparent",
            cursor: "pointer",
            transition: "all 0.2s"
          }}
        >
          🏥 Historial Clínico
        </button>
      </div>

      {/* Tab Contents */}
      {loading && <p style={{ color: "var(--text-muted)", textAlign: "center" }}>Cargando información...</p>}

      {!loading && activeTab === "mascotas" && (
        <div>
          {/* Form to register new pet */}
          <div className="card" style={{ marginBottom: "2rem" }}>
            <h2 style={{ fontSize: "1.1rem", fontWeight: 700, marginBottom: "1rem" }}>🐾 Registrar Nueva Mascota</h2>
            <form onSubmit={registrarMascota} style={{ display: "flex", gap: "1rem", flexWrap: "wrap" }}>
              <input
                className="form-input"
                type="text"
                name="nombre"
                placeholder="Nombre de la mascota"
                value={nuevaMascota.nombre}
                onChange={handleMascotaChange}
                required
                style={{ flex: 2, minWidth: "180px" }}
              />
              <input
                className="form-input"
                type="text"
                name="especie"
                placeholder="Especie (Ej: Perro, Gato)"
                value={nuevaMascota.especie}
                onChange={handleMascotaChange}
                required
                style={{ flex: 1.5, minWidth: "150px" }}
              />
              <input
                className="form-input"
                type="number"
                name="edad"
                placeholder="Edad (años)"
                value={nuevaMascota.edad}
                onChange={handleMascotaChange}
                required
                style={{ flex: 1, minWidth: "100px" }}
              />
              <button className="btn btn-primary" type="submit" disabled={loading}>
                + Registrar
              </button>
            </form>
          </div>

          {/* List of pets */}
          <div className="card">
            <h2 style={{ fontSize: "1.1rem", fontWeight: 700, marginBottom: "1rem" }}>Lista de Mascotas</h2>
            {mascotas.length === 0 ? (
              <p style={{ color: "var(--text-muted)" }}>Aún no tienes mascotas registradas.</p>
            ) : (
              <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(250px, 1fr))", gap: "1.5rem" }}>
                {mascotas.map((m) => (
                  <div key={m.id} className="card" style={{ background: "rgba(255,255,255,0.03)", border: "1px solid var(--border-color)", padding: "1.2rem", position: "relative" }}>
                    <div style={{ fontSize: "2rem", marginBottom: "0.5rem" }}>
                      {m.especie?.toLowerCase().includes("gato") ? "🐱" : 
                       m.especie?.toLowerCase().includes("perro") ? "🐶" : "🐾"}
                    </div>
                    <h3 style={{ fontSize: "1.1rem", fontWeight: 700, margin: 0 }}>{m.nombre}</h3>
                    <p style={{ margin: "0.25rem 0 0 0", color: "var(--text-muted)", fontSize: "0.9rem" }}>
                      <strong>Especie:</strong> {m.especie}
                    </p>
                    <p style={{ margin: "0.25rem 0 0 0", color: "var(--text-muted)", fontSize: "0.9rem" }}>
                      <strong>Edad:</strong> {m.edad} {m.edad === 1 ? "año" : "años"}
                    </p>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}

      {!loading && activeTab === "turnos" && (
        <div>
          {/* Form to schedule new appointment */}
          <div className="card" style={{ marginBottom: "2rem" }}>
            <h2 style={{ fontSize: "1.1rem", fontWeight: 700, marginBottom: "1rem" }}>📅 Agendar Nueva Cita</h2>
            {mascotas.length === 0 ? (
              <p style={{ color: "var(--text-muted)" }}>Debes registrar al menos una mascota antes de agendar un turno.</p>
            ) : (
              <form onSubmit={agendarTurno} style={{ display: "flex", gap: "1rem", flexWrap: "wrap", alignItems: "flex-end" }}>
                <div style={{ flex: 1.5, minWidth: "180px", display: "flex", flexDirection: "column", gap: "0.5rem" }}>
                  <label style={{ fontSize: "0.82rem", fontWeight: 600, color: "var(--text-muted)" }}>Mascota</label>
                  <select
                    className="form-input"
                    name="mascotaId"
                    value={nuevoTurno.mascotaId}
                    onChange={handleTurnoChange}
                    required
                    style={{ width: "100%", height: "2.7rem" }}
                  >
                    <option value="">Selecciona mascota...</option>
                    {mascotas.map((m) => (
                      <option key={m.id} value={m.id}>{m.nombre} ({m.especie})</option>
                    ))}
                  </select>
                </div>
                <div style={{ flex: 1.5, minWidth: "180px", display: "flex", flexDirection: "column", gap: "0.5rem" }}>
                  <label style={{ fontSize: "0.82rem", fontWeight: 600, color: "var(--text-muted)" }}>Fecha y Hora</label>
                  <input
                    className="form-input"
                    type="datetime-local"
                    name="fecha"
                    value={nuevoTurno.fecha}
                    onChange={handleTurnoChange}
                    required
                    style={{ width: "100%", height: "2.7rem" }}
                  />
                </div>
                <div style={{ flex: 3, minWidth: "250px", display: "flex", flexDirection: "column", gap: "0.5rem" }}>
                  <label style={{ fontSize: "0.82rem", fontWeight: 600, color: "var(--text-muted)" }}>Motivo de la Cita</label>
                  <input
                    className="form-input"
                    type="text"
                    name="motivo"
                    placeholder="Consulta de rutina, vacuna, etc."
                    value={nuevoTurno.motivo}
                    onChange={handleTurnoChange}
                    required
                    style={{ width: "100%", height: "2.7rem" }}
                  />
                </div>
                <button className="btn btn-primary" type="submit" style={{ height: "2.7rem" }} disabled={loading}>
                  Agendar Cita
                </button>
              </form>
            )}
          </div>

          {/* List of appointments */}
          <div className="card">
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "1rem" }}>
              <h2 style={{ fontSize: "1.1rem", fontWeight: 700, margin: 0 }}>
                {fechaFiltro ? `Turnos del ${new Date(fechaFiltro + "T12:00:00").toLocaleDateString("es-CO")}` : "Todos tus Turnos"}
              </h2>
              <div style={{ display: "flex", alignItems: "center", gap: "0.5rem" }}>
                <label style={{ fontSize: "0.82rem", fontWeight: 600, color: "var(--text-muted)" }}>Filtrar por fecha:</label>
                <input
                  className="form-input"
                  type="date"
                  value={fechaFiltro}
                  onChange={cambiarFechaTurnos}
                  style={{ padding: "0.4rem 0.75rem", fontSize: "0.85rem", height: "2.2rem" }}
                />
                {fechaFiltro && (
                  <button onClick={() => setFechaFiltro("")}
                    style={{ padding: "0.4rem 0.75rem", borderRadius: "var(--radius-md)", border: "1px solid var(--border-color)", background: "none", cursor: "pointer", fontWeight: 600, fontSize: "0.82rem" }}>
                    Ver todos
                  </button>
                )}
              </div>
            </div>
            {turnos.length === 0 ? (
              <p style={{ color: "var(--text-muted)" }}>No tienes turnos agendados.</p>
            ) : (
              <table style={{ width: "100%", borderCollapse: "collapse", fontSize: "0.9rem" }}>
                <thead>
                  <tr style={{ borderBottom: "2px solid var(--border-color)" }}>
                    <th style={th}>Mascota</th>
                    <th style={th}>Dueño</th>
                    <th style={th}>Fecha y Hora</th>
                    <th style={th}>Motivo</th>
                    <th style={th}>Estado</th>
                  </tr>
                </thead>
                <tbody>
                  {turnos.map((t) => (
                    <tr key={t.id} style={{ borderBottom: "1px solid var(--border-color)" }}>
                      <td style={td}>{t.mascota ? `${t.mascota.id} — ${t.mascota.nombre}` : "Sin mascota"}</td>
                      <td style={td}>{t.mascota?.dueno?.nombre || "-"}</td>
                      <td style={td}>{t.fecha ? new Date(t.fecha).toLocaleString() : "Sin fecha"}</td>
                      <td style={td}>{t.motivo}</td>
                      <td style={td}>
                        <span style={{
                          padding: "0.25rem 0.5rem",
                          borderRadius: "4px",
                          fontSize: "0.75rem",
                          fontWeight: 600,
                          background: new Date(t.fecha) > new Date() ? "rgba(46, 204, 113, 0.15)" : "rgba(149, 165, 166, 0.15)",
                          color: new Date(t.fecha) > new Date() ? "#2ecc71" : "#95a5a6"
                        }}>
                          {new Date(t.fecha) > new Date() ? "Pendiente" : "Completado"}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        </div>
      )}

      {!loading && activeTab === "historial" && (
        <div className="card">
          <h2 style={{ fontSize: "1.1rem", fontWeight: 700, marginBottom: "1rem" }}>Historial Clínico de tus Mascotas</h2>
          {historiales.length === 0 ? (
            <p style={{ color: "var(--text-muted)" }}>No hay registros clínicos asociados a tus mascotas.</p>
          ) : (
            <div style={{ display: "flex", flexDirection: "column", gap: "1.5rem" }}>
              {historiales.map((h) => (
                <div key={h.id} style={{ borderLeft: "4px solid var(--primary-color)", paddingLeft: "1.2rem", paddingBottom: "0.5rem" }}>
                  <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "0.5rem" }}>
                    <h3 style={{ fontSize: "1rem", fontWeight: 700, margin: 0, color: "var(--primary-color)" }}>
                      🐱 {h.mascota ? h.mascota.nombre : "Mascota"} ({h.mascota ? h.mascota.especie : ""})
                    </h3>
                    <span style={{ fontSize: "0.82rem", color: "var(--text-muted)" }}>
                      📅 {h.fecha ? new Date(h.fecha).toLocaleDateString() : "Sin fecha"}
                    </span>
                  </div>
                  <p style={{ margin: "0.25rem 0", fontSize: "0.95rem" }}>
                    <strong>Descripción del caso:</strong> {h.descripcion}
                  </p>
                  <p style={{ margin: "0.25rem 0", fontSize: "0.95rem", color: "#2ecc71" }}>
                    <strong>Diagnóstico / Tratamiento:</strong> {h.diagnostico}
                  </p>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

const th = { textAlign: "left", padding: "0.5rem 0.75rem", color: "var(--text-muted)", fontWeight: 600 };
const td = { padding: "0.5rem 0.75rem" };

export default ClientPortal;
