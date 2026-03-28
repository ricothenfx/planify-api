import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import toast from 'react-hot-toast'
import { projectsApi } from '../../api/projects'
import Modal from './Modal'
import Button from './Button'
import Input from './Input'

export default function ProjectMembersModal({ isOpen, onClose, projectId }) {
  const [userId, setUserId] = useState('')
  const [role, setRole] = useState('member')
  const queryClient = useQueryClient()

  const { data, isLoading } = useQuery({
    queryKey: ['members', projectId],
    queryFn: () => projectsApi.getMembers(projectId),
    enabled: isOpen,
  })

  const members = data?.data || []

  const addMember = useMutation({
    mutationFn: () => projectsApi.addMember(projectId, {
      user_id: userId,
      role: role,
    }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['members', projectId] })
      setUserId('')
      toast.success('Member added!')
    },
    onError: (err) => {
      toast.error(err.response?.data?.error?.message || 'Failed to add member')
    },
  })

  const removeMember = useMutation({
    mutationFn: (memberId) => projectsApi.removeMember(projectId, memberId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['members', projectId] })
      toast.success('Member removed!')
    },
    onError: (err) => {
      toast.error(err.response?.data?.error?.message || 'Failed to remove member')
    },
  })

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!userId.trim()) return
    addMember.mutate()
  }

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="👥 Project Members">
      <div className="space-y-6">
        {/* Add Member Form */}
        <form onSubmit={handleSubmit} className="space-y-3">
          <Input
            label="User ID"
            placeholder="Paste user ID here"
            value={userId}
            onChange={(e) => setUserId(e.target.value)}
            required
          />
          <div className="space-y-1">
            <label className="block text-sm font-medium text-gray-700">Role</label>
            <select
              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
              value={role}
              onChange={(e) => setRole(e.target.value)}
            >
              <option value="member">Member</option>
              <option value="owner">Owner</option>
            </select>
          </div>
          <Button type="submit" isLoading={addMember.isPending} className="w-full">
            + Add Member
          </Button>
        </form>

        {/* Members List */}
        <div>
          <h4 className="text-sm font-semibold text-gray-900 mb-3">
            Current Members ({members.length})
          </h4>
          {isLoading ? (
            <div className="text-sm text-gray-400">Loading...</div>
          ) : members.length === 0 ? (
            <div className="text-sm text-gray-400 text-center py-4">
              No members yet
            </div>
          ) : (
            <div className="space-y-2">
              {members.map((member) => (
                <div
                  key={member.id}
                  className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
                >
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 rounded-full bg-indigo-100 flex items-center justify-center text-indigo-600 text-sm font-semibold">
                      👤
                    </div>
                    <div>
                      <p className="text-sm font-medium text-gray-900 truncate max-w-32">
                        {member.user_id}
                      </p>
                      <span className={`text-xs px-2 py-0.5 rounded-full ${
                        member.role === 'OWNER'
                          ? 'bg-indigo-100 text-indigo-700'
                          : 'bg-gray-100 text-gray-600'
                      }`}>
                        {member.role}
                      </span>
                    </div>
                  </div>
                  {member.role !== 'OWNER' && (
                    <button
                      onClick={() => removeMember.mutate(member.user_id)}
                      className="text-xs text-red-500 hover:text-red-700 transition-colors"
                    >
                      Remove
                    </button>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </Modal>
  )
}