import axios from 'axios'

const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: BASE_URL,
  timeout: 600000, // 5 minutes — pipeline takes time
})

export const planTrip = async (tripData) => {
  const token = sessionStorage.getItem('token')
  const response = await api.post('/plan', tripData, {
    headers: token ? { Authorization: `Bearer ${token}` } : {}
  })
  return response.data
}

export const healthCheck = async () => {
  const response = await api.get('/health')
  return response.data
}

export default api