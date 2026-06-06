import { BrowserRouter, Routes, Route, Link } from "react-router-dom";

import Login from "./pages/Login/Login";
import Dashboard from "./pages/Dashboard/Dashboard";
import Duenos from "./pages/Duenos/Duenos";
import Mascotas from "./pages/Mascotas/Mascotas";
import Turnos from "./pages/Turnos/Turnos";

function App() {
  return (
    <BrowserRouter>

      <nav>
        <Link to="/">Login</Link> |{" "}
        <Link to="/dashboard">Dashboard</Link> |{" "}
        <Link to="/duenos">Dueños</Link> |{" "}
        <Link to="/mascotas">Mascotas</Link> |{" "}
        <Link to="/turnos">Turnos</Link>
      </nav>

      <hr />

      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/duenos" element={<Duenos />} />
        <Route path="/mascotas" element={<Mascotas />} />
        <Route path="/turnos" element={<Turnos />} />
      </Routes>

    </BrowserRouter>
  );
}

export default App;