import { useState } from 'react'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import toast from 'react-hot-toast'
import { projectsApi } from '../../api/projects'
import Modal from './Modal'
import Input from './Input'
import Button from './Button'

export default function CreateProjectModal({ isOpen, onClose }) {
  const [form, setForm] = useState({ name: '', description: '' })
  const queryClient = useQueryClient()

  const { mutate, isPending, error } = useMutation({
    mutationFn: () => projectsApi.create(form),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['projects'] })
      setForm({ name: '', description: '' })
      toast.success('Project created!')
      onClose()
    },
    onError: (err) => {
      toast.error(err.response?.data?.error?.message || 'Failed to create project')
    },
  })

  const handleSubmit = (e) => {
    e.preventDefault()
    mutate()
  }

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Create New Project">
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
            Create Project
          </Button>
        </div>
      </form>
    </Modal>
  )
}