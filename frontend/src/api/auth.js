import api from '../lib/axios'

export const authApi = {
  register: (data) => api.post('/users/register', data),
  login: (data) => api.post('/auth/login', data),
  me: () => api.get('/users/me'),
  changePassword: (data) => api.post('/auth/change-password', data),
  forgotPassword: (email) => api.post('/auth/forgot-password', { email }),
  resetPassword: (data) => api.post('/auth/reset-password', data),
}