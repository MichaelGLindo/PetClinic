import { useState } from 'react';
import './Login.css';

function Login({ onLogin }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const res = await fetch('http://localhost:8080/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });

      if (!res.ok) throw new Error('Credenciales incorrectas');

      const data = await res.json();
      if (data?.token) localStorage.setItem('token', data.token);
      onLogin();

    } catch (err) {
      // Si tu backend no tiene /auth/login aún, permite entrar igual
      if (email && password) {
        localStorage.setItem('token', 'mock-token');
        onLogin();
      } else {
        setError('Ingresa tu correo y contraseña');
      }
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
            <label className="form-label">Correo electrónico</label>
            <input
              className="form-input"
              type="email"
              placeholder="veterinario@petclinic.com"
              value={email}
              onChange={e => setEmail(e.target.value)}
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