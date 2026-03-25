from fastapi import APIRouter
from app.api.v1.routes.users import router as users_router
from app.api.v1.routes.auth import router as auth_router
from app.api.v1.routes.projects import router as projects_router
from app.api.v1.routes.tasks import router as tasks_router
from app.api.v1.routes.activities import router as activities_router
from app.api.v1.routes.ai import router as ai_router
from app.api.v1.routes.websocket import router as ws_router
from app.api.v1.routes.project_members import router as project_members_router


api_router = APIRouter(prefix="/api/v1")
api_router.include_router(users_router)
api_router.include_router(auth_router)
api_router.include_router(projects_router)
api_router.include_router(tasks_router)
api_router.include_router(activities_router)
api_router.include_router(ai_router)
api_router.include_router(ws_router)
api_router.include_router(project_members_router)