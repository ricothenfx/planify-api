import { Link } from 'react-router-dom'

const API_BASE = import.meta.env.VITE_API_URL?.replace('/api/v1', '') || 'http://localhost:8000'

const features = [
  {
    icon: '🔐',
    title: 'JWT Auth + Account Lockout',
    description: 'Access & refresh tokens, auto-rotation, account locks after 5 failed attempts, password reset via email.',
  },
  {
    icon: '🤖',
    title: 'AI Task Generation',
    description: 'Describe your project — Gemini AI auto-generates 5-8 actionable tasks with realistic priority distribution.',
  },
  {
    icon: '💡',
    title: 'AI Smart Suggestions',
    description: 'Move a task to "In Progress"? AI suggests contextual next actions based on task context.',
  },
  {
    icon: '📡',
    title: 'Real-time WebSocket',
    description: 'All task and comment events broadcast instantly to connected clients — no polling needed.',
  },
  {
    icon: '📋',
    title: 'Full Audit Trail',
    description: 'Every action logged — who created what, when status changed, files uploaded, members added.',
  },
  {
    icon: '👥',
    title: 'Team Collaboration',
    description: 'Invite members, assign roles (Owner/Member), manage access per project.',
  },
  {
    icon: '📎',
    title: 'File Attachments',
    description: 'Upload images, PDFs, and documents to tasks. Stored on Cloudinary CDN — globally accessible.',
  },
  {
    icon: '⚡',
    title: 'Redis Caching',
    description: 'Project responses cached in Redis with smart invalidation. Cached requests respond in ~2ms.',
  },
  {
    icon: '🛡️',
    title: 'Rate Limiting + Security',
    description: 'Per-IP rate limiting via Redis, UUID-based IDs, bcrypt passwords, CORS protection.',
  },
]

const techStack = [
  { name: 'FastAPI', color: 'bg-green-100 text-green-700' },
  { name: 'PostgreSQL 16', color: 'bg-blue-100 text-blue-700' },
  { name: 'Redis 7', color: 'bg-red-100 text-red-700' },
  { name: 'Docker', color: 'bg-sky-100 text-sky-700' },
  { name: 'React + Vite', color: 'bg-cyan-100 text-cyan-700' },
  { name: 'WebSocket', color: 'bg-purple-100 text-purple-700' },
  { name: 'Gemini AI', color: 'bg-orange-100 text-orange-700' },
  { name: 'JWT Auth', color: 'bg-indigo-100 text-indigo-700' },
  { name: 'Cloudinary', color: 'bg-yellow-100 text-yellow-700' },
  { name: 'SQLAlchemy 2.0', color: 'bg-pink-100 text-pink-700' },
  { name: 'Alembic', color: 'bg-teal-100 text-teal-700' },
  { name: 'Pydantic v2', color: 'bg-lime-100 text-lime-700' },
  { name: 'Resend Email', color: 'bg-violet-100 text-violet-700' },
  { name: 'Tailwind CSS', color: 'bg-rose-100 text-rose-700' },
]

const stats = [
  { value: '15+', label: 'API Endpoints' },
  { value: '4', label: 'AI Features' },
  { value: '100%', label: 'Async' },
  { value: '0', label: 'Compromises' },
]

const architecture = [
  { layer: 'Routes', desc: 'HTTP handling + input validation', color: 'bg-indigo-50 border-indigo-200' },
  { layer: 'Services', desc: 'Business logic + orchestration', color: 'bg-purple-50 border-purple-200' },
  { layer: 'Repositories', desc: 'Database operations (async)', color: 'bg-blue-50 border-blue-200' },
  { layer: 'Models', desc: 'SQLAlchemy 2.0 + UUID PKs', color: 'bg-green-50 border-green-200' },
]

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-white">
      {/* Navbar */}
      <nav className="border-b border-gray-100 px-6 py-4 sticky top-0 bg-white/80 backdrop-blur-sm z-10">
        <div className="max-w-6xl mx-auto flex items-center justify-between">
          <h1 className="text-xl font-bold text-indigo-600">🗂️ Planify</h1>
          <div className="flex items-center gap-4">
            
            <a href={`${API_BASE}/docs`}
              target="_blank"
              rel="noreferrer"
              className="text-sm text-gray-600 hover:text-gray-900 transition-colors"
            >
              API Docs
            </a>
            <Link
              to="/login"
              className="text-sm text-gray-600 hover:text-gray-900 transition-colors"
            >
              Sign in
            </Link>
            <Link
              to="/register"
              className="text-sm bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 transition-colors"
            >
              Get started
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero */}
      <section className="max-w-6xl mx-auto px-6 py-24 text-center">
        <div className="inline-flex items-center gap-2 bg-indigo-50 text-indigo-600 text-sm font-medium px-4 py-2 rounded-full mb-6">
          🤖 AI-Powered • 📡 Real-time • 🐳 Dockerized
        </div>
        <h1 className="text-5xl font-bold text-gray-900 mb-6 leading-tight">
          Production-ready
          <br />
          <span className="text-indigo-600">Project Management API</span>
        </h1>
        <p className="text-xl text-gray-500 mb-10 max-w-2xl mx-auto">
          A full-stack portfolio project built with FastAPI, PostgreSQL, Redis, WebSocket,
          and Gemini AI — demonstrating real-world backend engineering practices.
        </p>
        <div className="flex items-center justify-center gap-4 flex-wrap">
          <Link
            to="/register"
            className="bg-indigo-600 text-white px-8 py-3 rounded-xl font-medium hover:bg-indigo-700 transition-colors shadow-lg shadow-indigo-200"
          >
            Try the app
          </Link>
          
          <a href={`${API_BASE}/docs`}
            target="_blank"
            rel="noreferrer"
            className="text-gray-600 px-8 py-3 rounded-xl font-medium border border-gray-200 hover:border-indigo-300 transition-colors"
          >
            View API Docs
          </a>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-4 gap-6 mt-16 max-w-2xl mx-auto">
          {stats.map((stat) => (
            <div key={stat.label} className="text-center">
              <p className="text-3xl font-bold text-indigo-600">{stat.value}</p>
              <p className="text-sm text-gray-500 mt-1">{stat.label}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Architecture */}
      <section className="bg-gray-50 py-16">
        <div className="max-w-6xl mx-auto px-6">
          <div className="text-center mb-10">
            <h2 className="text-2xl font-bold text-gray-900 mb-2">
              Clean Layered Architecture
            </h2>
            <p className="text-gray-500">
              Separation of concerns — every layer has one responsibility
            </p>
          </div>
          <div className="flex flex-col md:flex-row items-center justify-center gap-2 max-w-3xl mx-auto">
            {architecture.map((item, index) => (
              <div key={item.layer} className="flex items-center gap-2 flex-1 w-full">
                <div className={`flex-1 border rounded-xl p-4 text-center ${item.color}`}>
                  <p className="font-semibold text-gray-800 text-sm">{item.layer}</p>
                  <p className="text-xs text-gray-500 mt-1">{item.desc}</p>
                </div>
                {index < architecture.length - 1 && (
                  <span className="text-gray-400 text-lg hidden md:block">→</span>
                )}
              </div>
            ))}
          </div>
          <p className="text-center text-sm text-gray-400 mt-4">
            HTTP Request → Routes → Services → Repositories → PostgreSQL
          </p>
        </div>
      </section>

      {/* Features */}
      <section className="py-24">
        <div className="max-w-6xl mx-auto px-6">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              Built for production, not just tutorials
            </h2>
            <p className="text-gray-500 max-w-xl mx-auto">
              Every feature reflects real-world engineering decisions
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {features.map((feature) => (
              <div
                key={feature.title}
                className="bg-white rounded-2xl p-6 border border-gray-100 hover:border-indigo-200 hover:shadow-md transition-all"
              >
                <div className="text-3xl mb-4">{feature.icon}</div>
                <h3 className="font-semibold text-gray-900 mb-2">{feature.title}</h3>
                <p className="text-sm text-gray-500">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Tech Stack */}
      <section className="bg-gray-50 py-16">
        <div className="max-w-6xl mx-auto px-6">
          <div className="text-center mb-10">
            <h2 className="text-2xl font-bold text-gray-900 mb-2">Tech Stack</h2>
            <p className="text-gray-500">Modern, production-ready technologies</p>
          </div>
          <div className="flex flex-wrap justify-center gap-3">
            {techStack.map((tech) => (
              <span
                key={tech.name}
                className={`px-4 py-2 rounded-full text-sm font-medium ${tech.color}`}
              >
                {tech.name}
              </span>
            ))}
          </div>
        </div>
      </section>

      {/* API Preview */}
      <section className="py-24">
        <div className="max-w-6xl mx-auto px-6">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              Clean, consistent API design
            </h2>
            <p className="text-gray-500">RESTful endpoints with proper HTTP status codes</p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-4xl mx-auto">
            <div className="bg-gray-900 rounded-2xl p-6 text-sm font-mono">
              <p className="text-green-400 mb-3">// Register</p>
              <p className="text-blue-400">POST <span className="text-white">/api/v1/users/register</span></p>
              <p className="text-gray-400 mt-2">→ 201 Created + UUID user ID</p>
              <br />
              <p className="text-green-400 mb-3">// Login</p>
              <p className="text-blue-400">POST <span className="text-white">/api/v1/auth/login</span></p>
              <p className="text-gray-400 mt-2">→ access_token + refresh_token</p>
              <br />
              <p className="text-green-400 mb-3">// AI Generate Tasks</p>
              <p className="text-blue-400">POST <span className="text-white">/api/v1/ai/projects/:id/generate-tasks</span></p>
              <p className="text-gray-400 mt-2">→ 5-8 AI-generated tasks</p>
            </div>
            <div className="bg-gray-900 rounded-2xl p-6 text-sm font-mono">
              <p className="text-green-400 mb-3">// Get tasks with filters</p>
              <p className="text-blue-400">GET <span className="text-white">/api/v1/projects/:id/tasks</span></p>
              <p className="text-gray-400 mt-1">?status=todo&priority=high</p>
              <p className="text-gray-400">&sort=due_date&order=asc</p>
              <p className="text-gray-400">&page=1&limit=10</p>
              <br />
              <p className="text-green-400 mb-3">// WebSocket</p>
              <p className="text-blue-400">WS <span className="text-white">/api/v1/ws/projects/:id</span></p>
              <p className="text-gray-400 mt-1">?token=JWT_TOKEN</p>
              <p className="text-gray-400 mt-2">→ Real-time events</p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="bg-indigo-600 py-24">
        <div className="max-w-6xl mx-auto px-6 text-center">
          <h2 className="text-3xl font-bold text-white mb-4">
            Ready to explore?
          </h2>
          <p className="text-indigo-200 mb-8 max-w-xl mx-auto">
            Try the live app or dive into the API documentation
          </p>
          <div className="flex items-center justify-center gap-4 flex-wrap">
            <Link
              to="/register"
              className="bg-white text-indigo-600 px-8 py-3 rounded-xl font-medium hover:bg-indigo-50 transition-colors"
            >
              Try the app
            </Link>
            
            <a href={`${API_BASE}/docs`}
              target="_blank"
              rel="noreferrer"
              className="border border-indigo-400 text-white px-8 py-3 rounded-xl font-medium hover:bg-indigo-700 transition-colors"
            >
              API Documentation
            </a>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-gray-100 py-8">
        <div className="max-w-6xl mx-auto px-6 flex items-center justify-between flex-wrap gap-4">
          <div>
            <p className="font-semibold text-gray-900">🗂️ Planify API</p>
            <p className="text-sm text-gray-500 mt-1">
              Built with FastAPI + PostgreSQL + Redis + React
            </p>
          </div>
          <div className="flex gap-6">
            
            <a href={`${API_BASE}/docs`}
              target="_blank"
              rel="noreferrer"
              className="text-sm text-indigo-600 hover:underline"
            >
              Swagger UI
            </a>
            
            <a href={`${API_BASE}/redoc`}
              target="_blank"
              rel="noreferrer"
              className="text-sm text-indigo-600 hover:underline"
            >
              ReDoc
            </a>
            
            <a href={`${API_BASE}/health`}
              target="_blank"
              rel="noreferrer"
              className="text-sm text-indigo-600 hover:underline"
            >
              Health Check
            </a>
          </div>
        </div>
      </footer>
    </div>
  )
}