const API_BASE = process.env.REACT_APP_API_URL || 'https://petclinic-dtoc.onrender.com/api';

const getHeaders = () => {
  const token = localStorage.getItem('token');
  return {
    'Content-Type': 'application/json',
    ...(token && { Authorization: `Bearer ${token}` }),
  };
};

const handleResponse = async (response) => {
  if (response.status === 204) return null;
  const data = await response.json().catch(() => null);
  if (!response.ok) {
    throw new Error(data?.message || `Error ${response.status}`);
  }
  return data;
};

// ========================
// Auth
// ========================
export const loginRequest = async (credentials) => {
  const response = await fetch(`${API_BASE}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(credentials),
  });
  return handleResponse(response);
};

// ========================
// Dueños
// ========================
export const getDuenos = async () => {
  const response = await fetch(`${API_BASE}/duenos`, { headers: getHeaders() });
  return handleResponse(response);
};

export const createDueno = async (dueno) => {
  const response = await fetch(`${API_BASE}/duenos`, {
    method: 'POST',
    headers: getHeaders(),
    body: JSON.stringify(dueno),
  });
  return handleResponse(response);
};

export const updateDueno = async (id, dueno) => {
  const response = await fetch(`${API_BASE}/duenos/${id}`, {
    method: 'PUT',
    headers: getHeaders(),
    body: JSON.stringify(dueno),
  });
  return handleResponse(response);
};

export const deleteDueno = async (id) => {
  const response = await fetch(`${API_BASE}/duenos/${id}`, {
    method: 'DELETE',
    headers: getHeaders(),
  });
  return handleResponse(response);
};

// ========================
// Mascotas
// ========================
export const getMascotas = async () => {
  const response = await fetch(`${API_BASE}/mascotas`, { headers: getHeaders() });
  return handleResponse(response);
};

export const createMascota = async (mascota) => {
  const response = await fetch(`${API_BASE}/mascotas`, {
    method: 'POST',
    headers: getHeaders(),
    body: JSON.stringify(mascota),
  });
  return handleResponse(response);
};

export const updateMascota = async (id, mascota) => {
  const response = await fetch(`${API_BASE}/mascotas/${id}`, {
    method: 'PUT',
    headers: getHeaders(),
    body: JSON.stringify(mascota),
  });
  return handleResponse(response);
};

export const deleteMascota = async (id) => {
  const response = await fetch(`${API_BASE}/mascotas/${id}`, {
    method: 'DELETE',
    headers: getHeaders(),
  });
  return handleResponse(response);
};

// ========================
// Turnos
// ========================
export const getTurnos = async () => {
  const response = await fetch(`${API_BASE}/turnos`, { headers: getHeaders() });
  return handleResponse(response);
};

export const createTurno = async (turno) => {
  const response = await fetch(`${API_BASE}/turnos`, {
    method: 'POST',
    headers: getHeaders(),
    body: JSON.stringify(turno),
  });
  return handleResponse(response);
};

export const updateTurno = async (id, turno) => {
  const response = await fetch(`${API_BASE}/turnos/${id}`, {
    method: 'PUT',
    headers: getHeaders(),
    body: JSON.stringify(turno),
  });
  return handleResponse(response);
};

export const deleteTurno = async (id) => {
  const response = await fetch(`${API_BASE}/turnos/${id}`, {
    method: 'DELETE',
    headers: getHeaders(),
  });
  return handleResponse(response);
};