from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.repositories.project_repository import ProjectRepository
from app.schemas.project import ProjectCreate, ProjectResponse, ProjectUpdate


class ProjectService:
    def __init__(self, db: AsyncSession):
        self.repo = ProjectRepository(db)
    
    async def create(self, data: ProjectCreate, owner_id: str) -> ProjectResponse:
        project = await self.repo.create(
            name=data.name,
            description=data.description,
            owner_id=owner_id,
        )
        return ProjectResponse.model_validate(project)
    
    async def get_all(self, owner_id: str) -> list[ProjectResponse]:
        projects = await self.repo.get_all_by_owner(owner_id)
        return [ProjectResponse.model_validate(p) for p in projects]
    
    async def get_by_id(self, project_id: str, owner_id: str) -> ProjectResponse:
        project = await self._get_and_verify_owner(project_id, owner_id)
        return ProjectResponse.model_validate(project)
    
    async def update(self, project_id: str, data: ProjectUpdate, owner_id: str) -> ProjectResponse:
        project = await self._get_and_verify_owner(project_id, owner_id)
        update_data = data.model_dump(exclude_none=True)
        project = await self.repo.update(project, update_data)
        return ProjectResponse.model_validate(project)
    
    async def delete(self, project_id: str, owner_id: str) -> None:
        project = await self._get_and_verify_owner(project_id, owner_id)
        await self.repo.delete(project)

    async def _get_and_verify_owner(self, project_id: str, owner_id: str):
        project = await self.repo.get_by_id(project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found",
            )
        if project.owner_id != owner_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to access this project",
            )
        return project