import { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route, Link, Navigate, useLocation } from 'react-router-dom';
import './App.css';

import Login from './pages/Login/Login';
import Dashboard from './pages/Dashboard/Dashboard';
import Duenos from './pages/Duenos/Duenos';
import Mascotas from './pages/Mascotas/Mascotas';
import Turnos from './pages/Turnos/Turnos';
import ClientPortal from './pages/ClientPortal/ClientPortal';

function Sidebar({ onLogout, user }) {
  const location = useLocation();
  const isAdmin = user?.rol === 'ADMIN';
  const navItems = isAdmin 
    ? [
        { path: '/dashboard', label: 'Dashboard', icon: '📊' },
        { path: '/duenos',    label: 'Dueños',    icon: '👤' },
        { path: '/mascotas',  label: 'Mascotas',  icon: '🐾' },
        { path: '/turnos',    label: 'Turnos',    icon: '📅' },
      ]
    : [
        { path: '/portal',    label: 'Mi Portal', icon: '🏥' },
      ];

  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <div className="sidebar-logo">🏥</div>
        <h2 className="sidebar-title">PetClinic</h2>
        <p className="sidebar-subtitle">Sistema Veterinario</p>
      </div>

      <nav className="sidebar-nav">
        {navItems.map((item) => (
          <Link
            key={item.path}
            to={item.path}
            className={`sidebar-link ${location.pathname === item.path ? 'active' : ''}`}
          >
            <span className="sidebar-link-icon">{item.icon}</span>
            <span>{item.label}</span>
          </Link>
        ))}
      </nav>

      <div className="sidebar-footer">
        {user && (
          <div style={{
            marginBottom: '0.75rem',
            padding: '0.6rem 0.75rem',
            background: 'rgba(255,255,255,0.06)',
            borderRadius: '8px',
            fontSize: '0.82rem',
            lineHeight: 1.5,
          }}>
            <div style={{ fontWeight: 600 }}>👤 {user.nombre}</div>
            <div style={{ opacity: 0.7 }}>🔑 {user.rol === 'ADMIN' ? 'Administrador' : 'Propietario'}</div>
          </div>
        )}
        <button className="logout-btn" onClick={onLogout}>
          🚪 Cerrar Sesión
        </button>
      </div>
    </aside>
  );
}

function AppLayout({ onLogout, user }) {
  const isAdmin = user?.rol === 'ADMIN';

  return (
    <div className="app-layout">
      <Sidebar onLogout={onLogout} user={user} />
      <main className="main-content">
        <Routes>
          {isAdmin ? (
            <>
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/duenos"    element={<Duenos />} />
              <Route path="/mascotas"  element={<Mascotas />} />
              <Route path="/turnos"    element={<Turnos />} />
              <Route path="*"          element={<Navigate to="/dashboard" replace />} />
            </>
          ) : (
            <>
              <Route path="/portal"    element={<ClientPortal />} />
              <Route path="*"          element={<Navigate to="/portal" replace />} />
            </>
          )}
        </Routes>
      </main>
    </div>
  );
}

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [user, setUser] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem('token');
    const storedUser = localStorage.getItem('user');
    if (token) {
      setIsLoggedIn(true);
      if (storedUser) setUser(JSON.parse(storedUser));
    }
  }, []);

  const handleLogin = () => {
    const storedUser = localStorage.getItem('user');
    setIsLoggedIn(true);
    if (storedUser) setUser(JSON.parse(storedUser));
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setIsLoggedIn(false);
    setUser(null);
  };

  return (
    <BrowserRouter>
      {isLoggedIn ? (
        <AppLayout onLogout={handleLogout} user={user} />
      ) : (
        <Routes>
          <Route path="*" element={<Login onLogin={handleLogin} />} />
        </Routes>
      )}
    </BrowserRouter>
  );
}

export default App;