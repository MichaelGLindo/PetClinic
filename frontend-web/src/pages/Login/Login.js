import { useState } from 'react';
import './Login.css';

function Login({ onLogin }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const res = await fetch('https://petclinic-dtoc.onrender.com/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password }),
      });

      if (!res.ok) throw new Error('Credenciales incorrectas');

      const data = await res.json();

      // Tu backend devuelve "access_token"
      const token = data.access_token;
      localStorage.setItem('token', token);

      // Decodificar el JWT para sacar nombre y rol
      const payload = JSON.parse(atob(token.split('.')[1]));
      localStorage.setItem('user', JSON.stringify({
        nombre: payload.sub,
        rol: payload.rol,
      }));

      onLogin();

    } catch (err) {
      setError(err.message || 'Error al iniciar sesión');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-bg">
      <div className="login-card">

        <div className="login-header">
          <div className="login-logo">🏥</div>
          <h1 className="login-title">PetClinic</h1>
          <p className="login-subtitle">Sistema Veterinario</p>
        </div>

        {error && <div className="alert alert-error">{error}</div>}

        <form onSubmit={handleSubmit} className="login-form">
          <div className="form-group">
            <label className="form-label">Usuario</label>
            <input
              className="form-input"
              type="text"
              placeholder="michael"
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
            {loading ? 'Ingresando...' : 'Ingresar →'}
          </button>
        </form>

      </div>
    </div>
  );
}

export default Login;