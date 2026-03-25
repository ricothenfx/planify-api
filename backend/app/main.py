from fastapi import FastAPI
from fastapi .exceptions import RequestValidationError
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
from app.api.v1.api import api_router


setup_logging()


description = """
## 🗂️ Planify API

A **production-ready** Task & Project Management REST API built with FastAPI.

### ✨ Features
* 🔐 **JWT Authentication** — Secure register & login
* 📁 **Project Management** — Full CRUD for projects
* ✅ **Task Management** — Full CRUD with status & priority tracking
* 🤖 **AI Task Generation** — Auto-generate tasks using Gemini AI
* 📡 **Real-time Notifications** — WebSocket-based live updates
* 📋 **Activity Log** — Full audit trail for all actions
* 🛡️ **Rate Limiting** — Protection against brute force attacks

### 🚀 Quick Start
1. **Register** a new account via `/api/v1/users/register`
2. **Login** via `/api/v1/auth/login` to get your JWT token
3. Click the **Authorize** button 🔒 and paste your token
4. Start managing your projects and tasks!

### 📡 WebSocket
Connect to real-time notifications:
```
ws://localhost:8000/api/v1/ws/projects/{project_id}?token=YOUR_JWT_TOKEN
```
"""


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
    return {
        "success": True,
        "data": {
            "status": "ok"
        }
    }