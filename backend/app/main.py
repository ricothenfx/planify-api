from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.core.config import settings
from app.core.rate_limit import limiter
from app.core.logging import setup_logging
from app.core.middleware import RequestLoggingMiddleware
from app.core.exceptions import (
    http_exception_handler,
    validation_exception_handler,
    generic_exception_handler,
)
from app.core.database import AsyncSessionLocal
from app.api.v1.api import api_router
from sqlalchemy import text
import time


setup_logging()


description = """
## 🗂️ Planify API

A **production-ready** Task & Project Management REST API built with modern Python backend stack.

> 💼 Built as a portfolio project demonstrating real-world backend engineering skills

---

### 🏗️ Architecture
```
HTTP Request → Routes → Services → Repositories → Database
                  ↓          ↓
              Schemas    Cache (Redis)
```

**Layered Architecture** with clear separation of concerns:
- **Routes** — HTTP request handling, input validation
- **Services** — Business logic, orchestration
- **Repositories** — Database operations (SQLAlchemy 2.0 async)
- **Schemas** — Request/response validation (Pydantic v2)

---

### ✨ Features

| Feature | Description |
|---------|-------------|
| 🔐 **JWT Auth** | Access + Refresh token, auto-rotation |
| 🔒 **Account Lockout** | Auto-lock after 5 failed attempts |
| 📧 **Password Reset** | Secure email-based reset via Resend |
| 🤖 **AI Task Generation** | Generate tasks from project description (Gemini AI) |
| 💡 **AI Smart Suggestions** | Contextual next-action suggestions on status change |
| 📡 **WebSocket** | Real-time notifications for all project events |
| 📋 **Activity Log** | Full audit trail for every action |
| 👥 **Project Members** | Role-based member management (Owner/Member) |
| 📎 **File Attachments** | Upload files to tasks via Cloudinary |
| 💬 **Task Comments** | Threaded comments on tasks |
| 🔍 **Pagination** | Cursor-based pagination with filter & sort |
| ⚡ **Redis Cache** | Response caching with smart invalidation |
| 🛡️ **Rate Limiting** | Per-IP rate limiting with Redis backend |
| 🐳 **Docker** | Full containerization with docker-compose |

---

### 🚀 Quick Start

**1. Register**
```
POST /api/v1/users/register
```

**2. Login & get token**
```
POST /api/v1/auth/login
```

**3. Authorize** — Click 🔒 button above, paste your `access_token`

**4. Start managing projects & tasks!**

---

### 📡 WebSocket Connection

Connect to real-time notifications:
```
ws://localhost:8000/api/v1/ws/projects/{project_id}?token=YOUR_JWT_TOKEN
```

Events: `task_created`, `task_updated`, `task_deleted`, `comment_created`, `ai_tasks_generated`

---

### 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Framework | FastAPI 0.100+ |
| Database | PostgreSQL 16 + SQLAlchemy 2.0 async |
| Cache | Redis 7 |
| Auth | JWT (python-jose) + bcrypt |
| AI | Google Gemini 2.5 Flash |
| Storage | Cloudinary |
| Email | Resend |
| Migration | Alembic |
| Container | Docker + docker-compose |
| Validation | Pydantic v2 |
"""

tags_metadata = [
    {
        "name": "Auth",
        "description": """
**Authentication & Authorization endpoints**

- `POST /register` — Create new account
- `POST /login` — Get access + refresh token  
- `POST /refresh` — Rotate tokens (access + refresh)
- `POST /forgot-password` — Send reset link via email
- `POST /reset-password` — Reset with token from email
- `POST /change-password` — Change password (authenticated)

> 🔒 Login is rate-limited to **5 requests/minute** per IP
> 🔒 Account locks for **30 minutes** after 5 failed attempts
        """,
    },
    {
        "name": "Users",
        "description": """
**User profile management**

- `POST /register` — Register new user (UUID-based ID, bcrypt password)
- `GET /me` — Get current authenticated user profile

> 🔑 All endpoints except register require Bearer token
        """,
    },
    {
        "name": "Projects",
        "description": """
**Project management with full CRUD**

- Supports **pagination**, **search**, and **sort**
- Responses are **cached in Redis** for performance
- Cache automatically invalidated on create/update/delete

Query params: `page`, `limit`, `search`, `sort`, `order`
        """,
    },
    {
        "name": "Tasks",
        "description": """
**Task management within projects**

- Kanban-style status: `todo` → `in_progress` → `done`
- Priority levels: `low`, `medium`, `high`
- Supports due dates, assignees, pagination, filter & sort
- Status updates trigger **AI Smart Suggestions**
- All changes broadcast via **WebSocket**

Query params: `page`, `limit`, `status`, `priority`, `sort`, `order`
        """,
    },
    {
        "name": "Project Members",
        "description": """
**Team collaboration — manage project members**

- Roles: `owner` (full access) | `member` (read + task management)
- Only owners can add/remove members
- Activity logged for all member changes
        """,
    },
    {
        "name": "Task Comments",
        "description": """
**Threaded comments on tasks**

- Only comment author can edit/delete their own comments
- New comments broadcast via WebSocket in real-time
        """,
    },
    {
        "name": "Task Attachments",
        "description": """
**File attachments on tasks via Cloudinary**

- Supported: Images (jpg, png, gif, webp), PDF, Word, Text
- Max file size: **10MB**
- Files stored on Cloudinary CDN — globally accessible URLs
        """,
    },
    {
        "name": "AI",
        "description": """
**🤖 AI-powered features using Google Gemini 2.5 Flash**

- `POST /ai/projects/{id}/generate-tasks` — Auto-generate 5-8 relevant tasks from project name & description
- Tasks are created with realistic priority distribution (not all high!)
- Status updates on tasks return **Smart Suggestions** for next actions
        """,
    },
    {
        "name": "Activities",
        "description": """
**📋 Full audit trail for all project actions**

Tracks: project created/updated/deleted, task created/updated/deleted, 
task status changes, file uploads, member added/removed, AI task generation, comments

Ordered by most recent first.
        """,
    },
    {
        "name": "WebSocket",
        "description": """
**📡 Real-time notifications via WebSocket**

Connect with JWT token as query parameter:
```
ws://localhost:8000/api/v1/ws/projects/{project_id}?token=JWT_TOKEN
```

**Events emitted:**
- `task_created` — New task added
- `task_updated` — Task modified  
- `task_deleted` — Task removed
- `comment_created` — New comment
- `ai_tasks_generated` — AI batch task creation

**Authentication:** Token validated on connect. Invalid token closes with code `4001`.
        """,
    },
    {
        "name": "Health",
        "description": """
**System health monitoring**

- `GET /health` — Detailed health check: database latency, AI service, storage
- Returns `503` if any critical component is unhealthy
- Used by load balancers and monitoring tools
        """,
    },
]


tags_metadata = [
    {
        "name": "Auth",
        "description": "Register, login to get JWT access token, password reset, and token refresh",
    },
    {
        "name": "Users",
        "description": "User profile management",
    },
    {
        "name": "Projects",
        "description": "Create and manage your projects",
    },
    {
        "name": "Tasks",
        "description": "Manage tasks within projects — supports status and priority tracking",
    },
    {
        "name": "Project Members",
        "description": "Manage project members and roles"
    },
    {
        "name": "Task Comments",
        "description": "Comment on tasks"
    },
    {
        "name": "Task Attachments",
        "description": "Upload files to tasks"
    },
    {
        "name": "AI",
        "description": "🤖 AI-powered features — auto-generate tasks using Gemini AI",
    },
    {
        "name": "Activities",
        "description": "📋 Audit log — track all actions within a project",
    },
    {
        "name": "WebSocket",
        "description": "📡 Real-time notifications via WebSocket",
    },
    {
        "name": "Health",
        "description": "Health check endpoints"
    },
]


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    description=description,
    openapi_tags=tags_metadata,
    contact={
        "name": "Planify API",
        "url": "https://github.com/ricothenfx/planify-api",
    },
    license_info={
        "name": "MIT"
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(RequestLoggingMiddleware)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)


app.include_router(api_router)


@app.get("/", tags=["Health"])
async def root():
    return {
        "success": True,
        "data": {
            "app": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "status": "running",
        },
    }


@app.get("/health", tags=["Health"])
async def health_check():
    start = time.time()
    health = {
        "status": "healthy",
        "version": settings.APP_VERSION,
        "checks": {},
    }

    # Check database
    try:
        async with AsyncSessionLocal() as session:
            await session.execute(text("SELECT 1"))
        health["checks"]["database"] = {
            "status": "healthy",
            "latency_ms": round((time.time() - start) * 1000, 2),
        }
    except Exception as e:
        health["checks"]["database"] = {
            "status": "unhealthy",
            "error": str(e),
        }
        health["status"] = "unhealthy"

    # Check AI service
    try:
        from app.core.config import settings as s
        ai_status = "healthy" if s.GEMINI_API_KEY else "not configured"
        health["checks"]["ai_service"] = {"status": ai_status}
    except Exception:
        health["checks"]["ai_service"] = {"status": "unhealthy"}

    # Check storage service
    try:
        from app.core.config import settings as s
        storage_status = "healthy" if s.CLOUDINARY_API_KEY else "not configured"
        health["checks"]["storage"] = {"status": storage_status}
    except Exception:
        health["checks"]["storage"] = {"status": "unhealthy"}

    status_code = 200 if health["status"] == "healthy" else 503
    return health