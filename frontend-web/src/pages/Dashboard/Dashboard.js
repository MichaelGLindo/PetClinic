import { useEffect, useState } from 'react';
import { getDuenos, getMascotas, getTurnos } from '../../services/api';

const statCards = [
  { key: 'duenos',   label: 'Dueños',   icon: '👤', color: 'var(--color-primary)' },
  { key: 'mascotas', label: 'Mascotas', icon: '🐾', color: 'var(--color-info)' },
  { key: 'turnos',   label: 'Turnos',   icon: '📅', color: 'var(--color-warning)' },
];

export default function Dashboard() {
  const [stats, setStats] = useState({ duenos: 0, mascotas: 0, turnos: 0 });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    Promise.all([getDuenos(), getMascotas(), getTurnos()])
      .then(([d, m, t]) => setStats({
        duenos:   Array.isArray(d) ? d.length : 0,
        mascotas: Array.isArray(m) ? m.length : 0,
        turnos:   Array.isArray(t) ? t.length : 0,
      }))
      .catch(() => setError('Error al cargar estadísticas. Verifica tu sesión.'))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">Dashboard</h1>
        <p className="page-subtitle">Resumen general del sistema</p>
      </div>

      {error && (
        <div className="alert alert-error" style={{ marginBottom: '1rem' }}>{error}</div>
      )}

      {loading ? (
        <p style={{ color: 'var(--text-muted)' }}>Cargando estadísticas...</p>
      ) : (
        <div style={grid}>
          {statCards.map(c => (
            <div key={c.key} className="card" style={cardStyle}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                <div>
                  <p style={{ color: 'var(--text-muted)', fontSize: '0.8rem', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.06em' }}>
                    {c.label}
                  </p>
                  <p style={{ fontSize: '2.5rem', fontWeight: 800, color: c.color, lineHeight: 1.1, marginTop: 4 }}>
                    {stats[c.key]}
                  </p>
                </div>
                <span style={{ fontSize: '2rem', opacity: 0.8 }}>{c.icon}</span>
              </div>
            </div>
          ))}
        </div>
      )}

      <div className="card" style={{ marginTop: '2rem' }}>
        <h2 style={{ fontSize: '1rem', fontWeight: 700, color: 'var(--text-primary)', marginBottom: '1rem' }}>
          Accesos rápidos
        </h2>
        <div style={{ display: 'flex', gap: '0.75rem', flexWrap: 'wrap' }}>
          {[
            { href: '/duenos',   label: '➕ Nuevo dueño',   bg: 'var(--color-primary)' },
            { href: '/mascotas', label: '➕ Nueva mascota',  bg: 'var(--color-info)' },
            { href: '/turnos',   label: '📅 Agendar turno', bg: 'var(--color-warning)' },
          ].map(b => (
            <a key={b.href} href={b.href} style={{
              padding: '0.65rem 1.2rem',
              background: b.bg,
              color: '#0f1117',
              borderRadius: 'var(--radius-md)',
              fontWeight: 600,
              fontSize: '0.9rem',
              textDecoration: 'none',
            }}>
              {b.label}
            </a>
          ))}
        </div>
      </div>
    </div>
  );
}

const grid = {
  display: 'grid',
  gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
  gap: '1.25rem',
};

const cardStyle = {
  transition: 'border-color 0.18s',
};