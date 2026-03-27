import { useState, useRef } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import toast from 'react-hot-toast'
import { tasksApi } from '../../api/tasks'

export default function TaskAttachments({ projectId, taskId }) {
  const [isDragging, setIsDragging] = useState(false)
  const fileInputRef = useRef(null)
  const queryClient = useQueryClient()

  const { data, isLoading } = useQuery({
    queryKey: ['attachments', taskId],
    queryFn: () => tasksApi.getAttachments(projectId, taskId),
  })

  const attachments = data?.data || []

  const uploadMutation = useMutation({
    mutationFn: (file) => {
      const formData = new FormData()
      formData.append('file', file)
      return tasksApi.uploadAttachment(projectId, taskId, formData)
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['attachments', taskId] })
      queryClient.invalidateQueries({ queryKey: ['activities', projectId] })
      toast.success('File uploaded!')
    },
    onError: (err) => {
      toast.error(err.response?.data?.error?.message || 'Failed to upload file')
    },
  })

  const deleteMutation = useMutation({
    mutationFn: (attachmentId) =>
      tasksApi.deleteAttachment(projectId, taskId, attachmentId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['attachments', taskId] })
      toast.success('File deleted!')
    },
    onError: () => toast.error('Failed to delete file'),
  })

  const handleFileChange = (e) => {
    const file = e.target.files[0]
    if (file) uploadMutation.mutate(file)
  }

  const handleDrop = (e) => {
    e.preventDefault()
    setIsDragging(false)
    const file = e.dataTransfer.files[0]
    if (file) uploadMutation.mutate(file)
  }

  const formatSize = (bytes) => {
    if (bytes < 1024) return `${bytes} B`
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
  }

  const getFileIcon = (mimeType) => {
    if (mimeType?.startsWith('image/')) return '🖼️'
    if (mimeType === 'application/pdf') return '📄'
    if (mimeType?.includes('word')) return '📝'
    return '📎'
  }

  return (
    <div className="space-y-3">
      {/* Upload Zone */}
      <div
        className={`border-2 border-dashed rounded-lg p-4 text-center cursor-pointer transition-colors ${
          isDragging
            ? 'border-indigo-400 bg-indigo-50'
            : 'border-gray-300 hover:border-indigo-300 hover:bg-gray-50'
        }`}
        onClick={() => fileInputRef.current?.click()}
        onDragOver={(e) => { e.preventDefault(); setIsDragging(true) }}
        onDragLeave={() => setIsDragging(false)}
        onDrop={handleDrop}
      >
        <input
          ref={fileInputRef}
          type="file"
          className="hidden"
          onChange={handleFileChange}
          accept="image/*,.pdf,.doc,.docx,.txt"
        />
        {uploadMutation.isPending ? (
          <p className="text-sm text-indigo-600">Uploading...</p>
        ) : (
          <>
            <p className="text-2xl mb-1">📎</p>
            <p className="text-sm text-gray-500">
              Drop file here or <span className="text-indigo-600">browse</span>
            </p>
            <p className="text-xs text-gray-400 mt-1">
              Images, PDF, Word, Text — max 10MB
            </p>
          </>
        )}
      </div>

      {/* Attachments List */}
      {isLoading ? (
        <div className="text-sm text-gray-400">Loading...</div>
      ) : attachments.length === 0 ? (
        <div className="text-sm text-gray-400 text-center py-2">
          No attachments yet
        </div>
      ) : (
        <div className="space-y-2">
          {attachments.map((attachment) => (
            <div
              key={attachment.id}
              className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
            >
              <span className="text-xl">{getFileIcon(attachment.mime_type)}</span>
              <div className="flex-1 min-w-0">
                
                <a href={attachment.file_url}
                  target="_blank"
                  rel="noreferrer"
                  className="text-sm font-medium text-indigo-600 hover:underline truncate block"
                >
                  {attachment.filename}
                </a>
                <p className="text-xs text-gray-400">
                  {formatSize(attachment.file_size)}
                </p>
              </div>
              <button
                onClick={() => deleteMutation.mutate(attachment.id)}
                className="text-gray-400 hover:text-red-500 transition-colors text-sm"
              >
                🗑️
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}