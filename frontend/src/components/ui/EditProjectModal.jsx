import { useState, useEffect } from 'react'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import toast from 'react-hot-toast'
import { projectsApi } from '../../api/projects'
import Modal from './Modal'
import Input from './Input'
import Button from './Button'

export default function EditProjectModal({ isOpen, onClose, project }) {
  const [form, setForm] = useState({ name: '', description: '' })
  const queryClient = useQueryClient()

  useEffect(() => {
    if (project) {
      setForm({ name: project.name, description: project.description || '' })
    }
  }, [project])

  const { mutate, isPending } = useMutation({
    mutationFn: () => projectsApi.update(project.id, form),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['projects'] })
      queryClient.invalidateQueries({ queryKey: ['project', project.id] })
      toast.success('Project updated!')
      onClose()
    },
    onError: (err) => {
      toast.error(err.response?.data?.error?.message || 'Failed to update project')
    },
  })

  const handleSubmit = (e) => {
    e.preventDefault()
    mutate()
  }

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Edit Project">
      <form onSubmit={handleSubmit} className="space-y-4">
        <Input
          label="Project Name"
          placeholder="My awesome project"
          value={form.name}
          onChange={(e) => setForm({ ...form, name: e.target.value })}
          required
        />
        <div className="space-y-1">
          <label className="block text-sm font-medium text-gray-700">
            Description (optional)
          </label>
          <textarea
            className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent resize-none"
            rows={3}
            placeholder="What is this project about?"
            value={form.description}
            onChange={(e) => setForm({ ...form, description: e.target.value })}
          />
        </div>
        <div className="flex gap-3 justify-end">
          <Button variant="secondary" type="button" onClick={onClose}>
            Cancel
          </Button>
          <Button type="submit" isLoading={isPending}>
            Save Changes
          </Button>
        </div>
      </form>
    </Modal>
  )
}