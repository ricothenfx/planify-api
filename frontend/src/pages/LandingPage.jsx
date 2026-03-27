import { Link } from 'react-router-dom'

const features = [
  {
    icon: '🔐',
    title: 'Secure Authentication',
    description: 'JWT + Refresh Token, account lockout, password reset via email',
  },
  {
    icon: '🤖',
    title: 'AI-Powered',
    description: 'Auto-generate tasks from project description using Gemini AI',
  },
  {
    icon: '📡',
    title: 'Real-time Notifications',
    description: 'WebSocket-based live updates when tasks are created or updated',
  },
  {
    icon: '📋',
    title: 'Activity Log',
    description: 'Full audit trail — track every action across your projects',
  },
  {
    icon: '👥',
    title: 'Team Collaboration',
    description: 'Invite members, assign tasks, manage roles within projects',
  },
  {
    icon: '📎',
    title: 'File Attachments',
    description: 'Upload and attach files to tasks via Cloudinary storage',
  },
]

const techStack = [
  { name: 'FastAPI', color: 'bg-green-100 text-green-700' },
  { name: 'PostgreSQL', color: 'bg-blue-100 text-blue-700' },
  { name: 'Redis', color: 'bg-red-100 text-red-700' },
  { name: 'Docker', color: 'bg-sky-100 text-sky-700' },
  { name: 'React', color: 'bg-cyan-100 text-cyan-700' },
  { name: 'WebSocket', color: 'bg-purple-100 text-purple-700' },
  { name: 'Gemini AI', color: 'bg-orange-100 text-orange-700' },
  { name: 'JWT Auth', color: 'bg-indigo-100 text-indigo-700' },
  { name: 'Cloudinary', color: 'bg-yellow-100 text-yellow-700' },
  { name: 'SQLAlchemy', color: 'bg-pink-100 text-pink-700' },
  { name: 'Alembic', color: 'bg-teal-100 text-teal-700' },
  { name: 'Pydantic', color: 'bg-lime-100 text-lime-700' },
]

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-white">
      {/* Navbar */}
      <nav className="border-b border-gray-100 px-6 py-4">
        <div className="max-w-6xl mx-auto flex items-center justify-between">
          <h1 className="text-xl font-bold text-indigo-600">🗂️ Planify</h1>
          <div className="flex items-center gap-4">
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
          🤖 AI-Powered Project Management
        </div>
        <h1 className="text-5xl font-bold text-gray-900 mb-6 leading-tight">
          Manage projects smarter
          <br />
          <span className="text-indigo-600">with AI assistance</span>
        </h1>
        <p className="text-xl text-gray-500 mb-10 max-w-2xl mx-auto">
          A production-ready project management API and app — built with FastAPI, PostgreSQL, Redis, WebSocket, and Gemini AI.
        </p>
        <div className="flex items-center justify-center gap-4">
          <Link
            to="/register"
            className="bg-indigo-600 text-white px-8 py-3 rounded-xl font-medium hover:bg-indigo-700 transition-colors shadow-lg shadow-indigo-200"
          >
            Get Started
          </Link>
          
          <a href="http://localhost:8000/docs"
            target="_blank"
            rel="noreferrer"
            className="text-gray-600 px-8 py-3 rounded-xl font-medium border border-gray-200 hover:border-gray-300 transition-colors"
          >
            API Docs
          </a>
        </div>
      </section>

      {/* Features */}
      <section className="bg-gray-50 py-24">
        <div className="max-w-6xl mx-auto px-6">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              Everything you need
            </h2>
            <p className="text-gray-500 max-w-xl mx-auto">
              Built with production-grade features that real companies use
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
      <section className="py-24">
        <div className="max-w-6xl mx-auto px-6">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              Tech Stack
            </h2>
            <p className="text-gray-500">
              Built with modern, production-ready technologies
            </p>
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

      {/* CTA */}
      <section className="bg-indigo-600 py-24">
        <div className="max-w-6xl mx-auto px-6 text-center">
          <h2 className="text-3xl font-bold text-white mb-4">
            Ready to get started?
          </h2>
          <p className="text-indigo-200 mb-8 max-w-xl mx-auto">
            Create your account and start managing projects with AI assistance
          </p>
          <Link
            to="/register"
            className="bg-white text-indigo-600 px-8 py-3 rounded-xl font-medium hover:bg-indigo-50 transition-colors"
          >
            Create free account
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-gray-100 py-8">
        <div className="max-w-6xl mx-auto px-6 flex items-center justify-between">
          <p className="text-sm text-gray-500">
            🗂️ Planify — Built with FastAPI + React
          </p>
          
          <a href="http://localhost:8000/docs"
            target="_blank"
            rel="noreferrer"
            className="text-sm text-indigo-600 hover:underline"
          >
            API Documentation
          </a>
        </div>
      </footer>
    </div>
  )
}