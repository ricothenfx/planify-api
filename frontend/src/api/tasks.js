import api from '../lib/axios'

export const tasksApi = {
  getAll: (projectId, params) => api.get(`/projects/${projectId}/tasks`, { params }),
  getById: (projectId, taskId) => api.get(`/projects/${projectId}/tasks/${taskId}`),
  create: (projectId, data) => api.post(`/projects/${projectId}/tasks`, data),
  update: (projectId, taskId, data) => api.patch(`/projects/${projectId}/tasks/${taskId}`, data),
  delete: (projectId, taskId) => api.delete(`/projects/${projectId}/tasks/${taskId}`),

  // AI
  generateTasks: (projectId) => api.post(`/ai/projects/${projectId}/generate-tasks`),

  // Comments
  getComments: (projectId, taskId) => api.get(`/projects/${projectId}/tasks/${taskId}/comments`),
  createComment: (projectId, taskId, content) =>
    api.post(`/projects/${projectId}/tasks/${taskId}/comments`, { content }),
  deleteComment: (projectId, taskId, commentId) =>
    api.delete(`/projects/${projectId}/tasks/${taskId}/comments/${commentId}`),

  // Attachments
  getAttachments: (projectId, taskId) =>
    api.get(`/projects/${projectId}/tasks/${taskId}/attachments`),
  uploadAttachment: (projectId, taskId, formData) =>
    api.post(`/projects/${projectId}/tasks/${taskId}/attachments`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    }),
  deleteAttachment: (projectId, taskId, attachmentId) =>
    api.delete(`/projects/${projectId}/tasks/${taskId}/attachments/${attachmentId}`),
}