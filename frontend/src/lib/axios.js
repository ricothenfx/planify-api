import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor — tambah token otomatis
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const original = error.config

    // Jangan retry kalau ini auth endpoint
    const isAuthEndpoint = original.url?.includes('/auth/')
    
    if (error.response?.status === 401 && !original._retry && !isAuthEndpoint) {
      original._retry = true

      try {
        const refreshToken = localStorage.getItem('refresh_token')
        if (!refreshToken) throw new Error('No refresh token')
        
        const response = await axios.post(
          'http://localhost:8000/api/v1/auth/refresh',
          { refresh_token: refreshToken }
        )

        const { access_token, refresh_token } = response.data
        localStorage.setItem('access_token', access_token)
        localStorage.setItem('refresh_token', refresh_token)

        original.headers.Authorization = `Bearer ${access_token}`
        return api(original)
      } catch {
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        window.location.href = '/login'
      }
    }

    return Promise.reject(error)
  }
)

export default api