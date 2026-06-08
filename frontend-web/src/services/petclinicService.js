const API_URL = 'http://localhost:8080';

export async function getDuenos() {
  const response = await fetch(`${API_URL}/duenos`);
  return response.json();
}

export async function getMascotas() {
  const response = await fetch(`${API_URL}/mascotas`);
  return response.json();
}

export async function getTurnos() {
  const response = await fetch(`${API_URL}/turnos`);
  return response.json();
}