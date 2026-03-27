import { create } from 'zustand'
import toast from 'react-hot-toast'
import api from '../lib/axios'

const useAuthStore = create((set) => ({
  user: null,
  isAuthenticated: false,
  isLoading: false,
  error: null,

  login: async (email, password) => {
    set({ isLoading: true })  // ← hapus error: null di sini
    try {
      const response = await api.post('/auth/login', { email, password })
      const { access_token, refresh_token } = response.data
      localStorage.setItem('access_token', access_token)
      localStorage.setItem('refresh_token', refresh_token)
      const userResponse = await api.get('/users/me')
      set({
        user: userResponse.data,
        isAuthenticated: true,
        isLoading: false,
        error: null,  // ← reset hanya saat sukses
      })
      toast.success('Welcome back!')
      return true
    } catch (error) {
      const message = error.response?.data?.error?.message || 'Login failed'
      set({ error: message, isLoading: false })
      return false
    }
  },

  logout: () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    set({ user: null, isAuthenticated: false })
    toast.success('Signed out successfully')
  },

  fetchUser: async () => {
    const token = localStorage.getItem('access_token')
    if (!token) return

    try {
      const response = await api.get('/users/me')
      set({ user: response.data, isAuthenticated: true })
    } catch {
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
    }
  },
}))

export default useAuthStore