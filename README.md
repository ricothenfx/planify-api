# 🗂️ Planify API

> A **production-ready** Task & Project Management REST API + Web App — built as a portfolio project demonstrating real-world backend engineering practices.

![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green?style=flat-square&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue?style=flat-square&logo=postgresql)
![Redis](https://img.shields.io/badge/Redis-7-red?style=flat-square&logo=redis)
![Docker](https://img.shields.io/badge/Docker-ready-blue?style=flat-square&logo=docker)
![React](https://img.shields.io/badge/React-18-cyan?style=flat-square&logo=react)

---

## 🌐 Live Demo

| | URL |
|--|--|
| 🖥️ **Web App** | `http://localhost:5173` |
| 📚 **API Docs (Swagger)** | `http://localhost:8000/docs` |
| 📖 **API Docs (ReDoc)** | `http://localhost:8000/redoc` |
| ❤️ **Health Check** | `http://localhost:8000/health` |

---

## ✨ Features

### 🔐 Auth & Security
- JWT Authentication with **Access + Refresh Token** rotation
- **Account Lockout** — auto-lock after 5 failed attempts (30 min)
- **Password Reset** via email (Resend)
- **Change Password** for authenticated users
- bcrypt password hashing, UUID-based user IDs

### 📁 Project & Task Management
- Full **CRUD** for Projects and Tasks
- **Kanban-style** task status: `todo` → `in_progress` → `done`
- Task **priority levels**: `low`, `medium`, `high`
- **Due dates**, assignees, descriptions
- **Pagination + Filter + Sort** on all list endpoints

### 🤖 AI Features (Google Gemini 2.5 Flash)
- **AI Task Generation** — describe your project, get 5-8 actionable tasks instantly
- **AI Smart Suggestions** — move a task status, get contextual next-action suggestions

### 📡 Real-time
- **WebSocket notifications** for all project events
- Events: `task_created`, `task_updated`, `task_deleted`, `comment_created`, `ai_tasks_generated`

### 👥 Collaboration
- **Project Members** — invite users, manage roles (Owner/Member)
- **Task Comments** — threaded comments with real-time updates
- **File Attachments** — upload images, PDFs, documents (Cloudinary CDN)
- **Activity Log** — full audit trail for every action

### ⚡ Performance & Infrastructure
- **Redis caching** with smart cache invalidation
- **Rate limiting** per IP via Redis
- **PostgreSQL** with async SQLAlchemy 2.0
- **Alembic** database migrations
- **Docker + docker-compose** — one command setup

---

## 🏗️ Architecture
```
HTTP Request
    ↓
Routes (FastAPI)        ← Input validation (Pydantic v2)
    ↓
Services                ← Business logic
    ↓
Repositories            ← Database operations (async)
    ↓
Models (SQLAlchemy)     ← PostgreSQL via asyncpg
    
Side effects:
Services → Cache (Redis)
Services → Activity Log
Services → WebSocket broadcast
Services → AI (Gemini API)
```

**Design principles:**
- Layered architecture — each layer has one responsibility
- Repository pattern — all DB operations isolated
- Dependency injection via FastAPI `Depends()`
- Async throughout — non-blocking I/O

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Framework** | FastAPI |
| **Database** | PostgreSQL 16 + SQLAlchemy 2.0 async |
| **Cache** | Redis 7 |
| **Auth** | JWT (python-jose) + bcrypt |
| **AI** | Google Gemini 2.5 Flash |
| **Storage** | Cloudinary |
| **Email** | Resend |
| **Migration** | Alembic |
| **Container** | Docker + docker-compose |
| **Validation** | Pydantic v2 |
| **Package Manager** | uv |
| **Frontend** | React 18 + Vite + Tailwind CSS |

---

## 🚀 Quick Start

### Prerequisites
- Docker + Docker Compose
- Git

### 1. Clone the repo
```bash
git clone https://github.com/ricothenfx/planify-api.git
cd planify-api
```

### 2. Setup environment variables
```bash
cp .env.example .env
```

Edit `.env` with your credentials:
```env
SECRET_KEY=your-secret-key-here
GEMINI_API_KEY=your-gemini-api-key
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-cloudinary-api-key
CLOUDINARY_API_SECRET=your-cloudinary-api-secret
RESEND_API_KEY=your-resend-api-key
RESEND_FROM_EMAIL=onboarding@resend.dev
FRONTEND_URL=http://localhost:5173
```

### 3. Run with Docker
```bash
docker-compose up --build
```

### 4. Run database migrations
```bash
docker exec planify-backend uv run alembic upgrade head
```

### 5. Open the app
- Web App: http://localhost:5173
- API Docs: http://localhost:8000/docs

---

## 📁 Project Structure
```
planify-api/
├── backend/
│   ├── app/
│   │   ├── api/v1/
│   │   │   └── routes/          # HTTP endpoints
│   │   ├── core/
│   │   │   ├── config.py        # Settings (pydantic-settings)
│   │   │   ├── database.py      # Async DB connection
│   │   │   ├── security.py      # JWT + bcrypt
│   │   │   ├── cache.py         # Redis cache service
│   │   │   ├── dependencies.py  # FastAPI dependencies
│   │   │   ├── middleware.py    # Request logging
│   │   │   └── exceptions.py   # Custom error handlers
│   │   ├── models/              # SQLAlchemy models
│   │   ├── schemas/             # Pydantic schemas
│   │   ├── services/            # Business logic
│   │   └── repositories/        # Database operations
│   ├── alembic/                 # DB migrations
│   ├── Dockerfile
│   └── pyproject.toml
├── frontend/
│   ├── src/
│   │   ├── api/                 # API client functions
│   │   ├── components/          # React components
│   │   ├── pages/               # Page components
│   │   ├── stores/              # Zustand state
│   │   └── lib/                 # Axios config
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## 📡 API Overview

### Auth
```
POST   /api/v1/auth/login           # Login → access + refresh token
POST   /api/v1/auth/refresh         # Rotate tokens
POST   /api/v1/auth/forgot-password # Send reset email
POST   /api/v1/auth/reset-password  # Reset with token
POST   /api/v1/auth/change-password # Change password (auth required)
```

### Projects
```
GET    /api/v1/projects             # List with pagination + search
POST   /api/v1/projects             # Create project
GET    /api/v1/projects/:id         # Get project detail
PATCH  /api/v1/projects/:id         # Update project
DELETE /api/v1/projects/:id         # Delete project
```

### Tasks
```
GET    /api/v1/projects/:id/tasks              # List with filters
POST   /api/v1/projects/:id/tasks              # Create task
PATCH  /api/v1/projects/:id/tasks/:id          # Update task → AI suggestions
DELETE /api/v1/projects/:id/tasks/:id          # Delete task
```

### AI
```
POST   /api/v1/ai/projects/:id/generate-tasks  # AI task generation
```

### WebSocket
```
WS     /api/v1/ws/projects/:id?token=JWT       # Real-time events
```

> Full API documentation available at `/docs` (Swagger UI) or `/redoc`

---

## 🔑 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `SECRET_KEY` | JWT signing key (min 32 chars) | ✅ |
| `DATABASE_URL` | PostgreSQL connection string | ✅ |
| `REDIS_URL` | Redis connection string | ✅ |
| `GEMINI_API_KEY` | Google AI Studio API key | ✅ |
| `CLOUDINARY_CLOUD_NAME` | Cloudinary cloud name | ✅ |
| `CLOUDINARY_API_KEY` | Cloudinary API key | ✅ |
| `CLOUDINARY_API_SECRET` | Cloudinary API secret | ✅ |
| `RESEND_API_KEY` | Resend email API key | ✅ |
| `FRONTEND_URL` | Frontend URL for email links | ✅ |

---

## 👤 Author

Built by Rico — Backend Developer

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?style=flat-square&logo=linkedin)](https://linkedin.com/in/rico-then)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black?style=flat-square&logo=github)](https://github.com/ricothenfx)

---

## 📄 License

MIT