import { useQuery } from '@tanstack/react-query'
import { projectsApi } from '../../api/projects'

const ACTION_ICONS = {
  created: '✅',
  updated: '✏️',
  deleted: '🗑️',
  ai_generated: '🤖',
  uploaded: '📎',
  member_added: '👥',
  member_removed: '👋',
}

const ACTION_COLORS = {
  created: 'text-green-600',
  updated: 'text-blue-600',
  deleted: 'text-red-600',
  ai_generated: 'text-purple-600',
  uploaded: 'text-orange-600',
  member_added: 'text-indigo-600',
  member_removed: 'text-gray-600',
}

const formatTime = (date) => {
  return new Date(date).toLocaleString('en-US', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

const formatStatus = (status) => {
  if (!status) return ''
  return status
    .replace('TaskStatus.', '')
    .replace(/_/g, ' ')
    .toLowerCase()
    .replace(/\b\w/g, c => c.toUpperCase())
}

const formatAction = (activity) => {
  const { entity_type, action, extra_data } = activity
  const name = extra_data?.name || extra_data?.title || extra_data?.filename || ''

  switch (`${entity_type}_${action}`) {
    case 'project_created': return `Created project "${name}"`
    case 'project_updated': return `Updated project`
    case 'project_deleted': return `Deleted project "${name}"`
    case 'task_created': return `Created task "${name}"`
    case 'task_updated':
      if (extra_data?.old_status) {
        return `Moved "${extra_data.title || name}" from ${formatStatus(extra_data.old_status)} to ${formatStatus(extra_data.status)}`
      }
      return `Updated task "${extra_data.title || name}"`
    case 'task_deleted': return `Deleted task "${name}"`
    case 'task_ai_generated': return `AI generated task "${name}"`
    case 'attachment_uploaded': return `Uploaded file "${name}"`
    case 'project_member_member_added': return `Added member to project`
    case 'project_member_member_removed': return `Removed member from project`
    default: return `${action} ${entity_type}`
  }
}

export default function ActivityLog({ projectId }) {
  const { data, isLoading } = useQuery({
    queryKey: ['activities', projectId],
    queryFn: () => projectsApi.getActivities(projectId),
    refetchInterval: 30000, // refresh every 30 detik
  })

  const activities = data?.data || []

  if (isLoading) {
    return (
      <div className="space-y-3">
        {[...Array(5)].map((_, i) => (
          <div key={i} className="animate-pulse flex gap-3">
            <div className="w-8 h-8 bg-gray-200 rounded-full" />
            <div className="flex-1 space-y-2">
              <div className="h-3 bg-gray-200 rounded w-3/4" />
              <div className="h-3 bg-gray-200 rounded w-1/4" />
            </div>
          </div>
        ))}
      </div>
    )
  }

  if (activities.length === 0) {
    return (
      <div className="text-center py-8 text-gray-400 text-sm">
        No activity yet
      </div>
    )
  }

  return (
    <div className="space-y-3">
      {activities.map((activity) => (
        <div key={activity.id} className="flex gap-3 items-start">
          <div className="w-8 h-8 rounded-full bg-gray-100 flex items-center justify-center text-sm flex-shrink-0">
            {ACTION_ICONS[activity.action] || '📌'}
          </div>
          <div className="flex-1 min-w-0">
            <p className={`text-sm font-medium ${ACTION_COLORS[activity.action] || 'text-gray-700'}`}>
              {formatAction(activity)}
            </p>
            <p className="text-xs text-gray-400 mt-0.5">
              {formatTime(activity.created_at)}
            </p>
          </div>
        </div>
      ))}
    </div>
  )
}