import axios from 'axios'

const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: BASE_URL,
  timeout: 600000, // 5 minutes — pipeline takes time
})

// Add a response interceptor to handle 401 errors
api.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      // Token expired or invalid — sign out
      sessionStorage.removeItem('token')
      sessionStorage.removeItem('username')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

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
