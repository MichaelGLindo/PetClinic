import { useState } from 'react';
import './Login.css';

function Login({ onLogin }) {
  const [isRegister, setIsRegister] = useState(false);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [cedula, setCedula] = useState('');
  const [nombre, setNombre] = useState('');
  const [telefono, setTelefono] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess('');

    try {
      if (isRegister) {
        const res = await fetch('http://localhost:8080/auth/register-client', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ username, password, cedula, nombre, telefono }),
        });

        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || 'Error al registrarse');

        setSuccess('✅ Registro exitoso. ¡Ya puedes iniciar sesión!');
        setIsRegister(false);
        setPassword('');
      } else {
        const res = await fetch('http://localhost:8080/auth/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ username, password }),
        });

        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || 'Credenciales incorrectas');

        const token = data.access_token;
        localStorage.setItem('token', token);

        const payload = JSON.parse(atob(token.split('.')[1]));
        localStorage.setItem('user', JSON.stringify({
          nombre: payload.sub,
          rol: payload.rol,
          cedula: payload.dueno_cedula,
        }));

        onLogin();
      }
    } catch (err) {
      setError(err.message || 'Ocurrió un error');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-bg">
      <div className="login-card" style={{ maxWidth: isRegister ? '480px' : '380px' }}>
        <div className="login-header">
          <div className="login-logo">🏥</div>
          <h1 className="login-title">PetClinic</h1>
          <p className="login-subtitle">
            {isRegister ? 'Registro de Propietario' : 'Sistema Veterinario'}
          </p>
        </div>

        {error && <div className="alert alert-error" style={{ marginBottom: '1rem' }}>{error}</div>}
        {success && <div className="alert alert-success" style={{ marginBottom: '1rem' }}>{success}</div>}

        <form onSubmit={handleSubmit} className="login-form">
          {isRegister && (
            <>
              <div className="form-group">
                <label className="form-label">Cédula</label>
                <input
                  className="form-input"
                  type="text"
                  placeholder="C.I. o DNI"
                  value={cedula}
                  onChange={e => setCedula(e.target.value)}
                  required
                />
              </div>

              <div className="form-group">
                <label className="form-label">Nombre Completo</label>
                <input
                  className="form-input"
                  type="text"
                  placeholder="Juan Pérez"
                  value={nombre}
                  onChange={e => setNombre(e.target.value)}
                  required
                />
              </div>

              <div className="form-group">
                <label className="form-label">Teléfono</label>
                <input
                  className="form-input"
                  type="text"
                  placeholder="099123456"
                  value={telefono}
                  onChange={e => setTelefono(e.target.value)}
                  required
                />
              </div>
            </>
          )}

          <div className="form-group">
            <label className="form-label">Usuario</label>
            <input
              className="form-input"
              type="text"
              placeholder="juanperez"
              value={username}
              onChange={e => setUsername(e.target.value)}
              required
            />
          </div>

          <div className="form-group">
            <label className="form-label">Contraseña</label>
            <input
              className="form-input"
              type="password"
              placeholder="••••••••"
              value={password}
              onChange={e => setPassword(e.target.value)}
              required
            />
          </div>

          <button className="btn btn-primary login-btn" type="submit" disabled={loading}>
            {loading ? 'Procesando...' : isRegister ? 'Registrarse ✓' : 'Ingresar →'}
          </button>
        </form>

        <div style={{ textAlign: 'center', marginTop: '1.5rem', fontSize: '0.9rem' }}>
          {isRegister ? (
            <span style={{ color: 'var(--text-muted)' }}>
              ¿Ya tienes cuenta?{' '}
              <button
                type="button"
                onClick={() => { setIsRegister(false); setError(''); }}
                style={{ background: 'none', border: 'none', color: 'var(--primary-color)', fontWeight: 600, cursor: 'pointer', padding: 0 }}
              >
                Inicia sesión aquí
              </button>
            </span>
          ) : (
            <span style={{ color: 'var(--text-muted)' }}>
              ¿Eres nuevo?{' '}
              <button
                type="button"
                onClick={() => { setIsRegister(true); setError(''); }}
                style={{ background: 'none', border: 'none', color: 'var(--primary-color)', fontWeight: 600, cursor: 'pointer', padding: 0 }}
              >
                Regístrate como Dueño
              </button>
            </span>
          )}
        </div>
      </div>
    </div>
  );
}

export default Login;