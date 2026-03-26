import { useNavigate } from 'react-router-dom'
import Badge from './Badge'

export default function ProjectCard({ project }) {
  const navigate = useNavigate()

  const formatDate = (date) => {
    return new Date(date).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
    })
  }

  return (
    <div
      onClick={() => navigate(`/projects/${project.id}`)}
      className="bg-white rounded-xl border border-gray-200 p-5 hover:border-indigo-300 hover:shadow-md transition-all cursor-pointer group"
    >
      <div className="flex items-start justify-between mb-3">
        <div className="w-10 h-10 rounded-lg bg-indigo-100 flex items-center justify-center text-xl">
          📁
        </div>
        <Badge variant="default">Active</Badge>
      </div>

      <h3 className="font-semibold text-gray-900 group-hover:text-indigo-600 transition-colors mb-1">
        {project.name}
      </h3>

      {project.description && (
        <p className="text-sm text-gray-500 line-clamp-2 mb-3">
          {project.description}
        </p>
      )}

      <p className="text-xs text-gray-400">
        Created {formatDate(project.created_at)}
      </p>
    </div>
  )
}