import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import toast from 'react-hot-toast'
import { tasksApi } from '../../api/tasks'
import Modal from './Modal'
import Badge from './Badge'
import Button from './Button'
import TaskAttachments from './TaskAttachments'

export default function TaskDetailModal({ isOpen, onClose, task, projectId }) {
  const [comment, setComment] = useState('')
  const queryClient = useQueryClient()

  const { data: commentsData } = useQuery({
    queryKey: ['comments', task?.id],
    queryFn: () => tasksApi.getComments(projectId, task.id),
    enabled: !!task && isOpen,
  })

  const comments = commentsData?.data || []

  const createComment = useMutation({
    mutationFn: () => tasksApi.createComment(projectId, task.id, comment),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['comments', task.id] })
      queryClient.invalidateQueries({ queryKey: ['activities', projectId] })
      setComment('')
      toast.success('Comment added!')
    },
    onError: () => toast.error('Failed to add comment'),
  })

  const deleteComment = useMutation({
    mutationFn: (commentId) =>
      tasksApi.deleteComment(projectId, task.id, commentId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['comments', task.id] })
      toast.success('Comment deleted!')
    },
  })

  if (!task) return null

  return (
    <Modal isOpen={isOpen} onClose={onClose} title={task.title}>
      <div className="space-y-6 max-h-[70vh] overflow-y-auto">
        {/* Task Info */}
        <div className="flex gap-2 flex-wrap">
          <Badge variant={task.status}>{task.status.replace('_', ' ')}</Badge>
          <Badge variant={task.priority}>{task.priority}</Badge>
          {task.due_date && (
            <span className="text-xs text-gray-500 flex items-center gap-1">
              📅 {new Date(task.due_date).toLocaleDateString('en-US', {
                month: 'short', day: 'numeric', year: 'numeric'
              })}
            </span>
          )}
        </div>

        {task.description && (
          <p className="text-sm text-gray-600">{task.description}</p>
        )}

        {/* Attachments */}
        <div>
          <h4 className="text-sm font-semibold text-gray-900 mb-3">
            📎 Attachments
          </h4>
          <TaskAttachments projectId={projectId} taskId={task.id} />
        </div>

        {/* Comments */}
        <div>
          <h4 className="text-sm font-semibold text-gray-900 mb-3">
            💬 Comments ({comments.length})
          </h4>

          <div className="space-y-3 mb-4">
            {comments.length === 0 ? (
              <p className="text-sm text-gray-400 text-center py-2">
                No comments yet
              </p>
            ) : (
              comments.map((c) => (
                <div key={c.id} className="flex gap-3 group">
                  <div className="w-7 h-7 rounded-full bg-indigo-100 flex items-center justify-center text-xs text-indigo-600 font-semibold flex-shrink-0">
                    U
                  </div>
                  <div className="flex-1 bg-gray-50 rounded-lg p-3">
                    <p className="text-sm text-gray-700">{c.content}</p>
                    <div className="flex items-center justify-between mt-1">
                      <p className="text-xs text-gray-400">
                        {new Date(c.created_at).toLocaleString('en-US', {
                          month: 'short', day: 'numeric',
                          hour: '2-digit', minute: '2-digit'
                        })}
                      </p>
                      <button
                        onClick={() => deleteComment.mutate(c.id)}
                        className="text-xs text-gray-400 hover:text-red-500 opacity-0 group-hover:opacity-100 transition-all"
                      >
                        Delete
                      </button>
                    </div>
                  </div>
                </div>
              ))
            )}
          </div>

          {/* Add Comment */}
          <div className="flex gap-2">
            <input
              type="text"
              placeholder="Add a comment..."
              value={comment}
              onChange={(e) => setComment(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && comment.trim()) {
                  createComment.mutate()
                }
              }}
              className="flex-1 px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
            <Button
              onClick={() => createComment.mutate()}
              disabled={!comment.trim()}
              isLoading={createComment.isPending}
              size="sm"
            >
              Send
            </Button>
          </div>
        </div>
      </div>
    </Modal>
  )
}