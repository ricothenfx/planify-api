from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.repositories.project_repository import ProjectRepository
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse
from app.schemas.pagination import PaginatedResponse
from app.services.activity_service import ActivityService
from app.core.cache import CacheService
#import logging


#logger = logging.getLogger(__name__)


class ProjectService:
    def __init__(self, db: AsyncSession):
        self.repo = ProjectRepository(db)
        self.activity = ActivityService(db)
        self.cache = CacheService(prefix="projects")
    
    async def create(self, data: ProjectCreate, owner_id: str) -> ProjectResponse:
        project = await self.repo.create(
            name=data.name,
            description=data.description,
            owner_id=owner_id,
        )
        await self.activity.log(
            user_id=owner_id,
            project_id=project.id,
            entity_type="project",
            entity_id=project.id,
            action="created",
            extra_data={"name": project.name},
        )
        # Invalidate list cache
        await self.cache.delete_pattern(f"list:{owner_id}:*")
        return ProjectResponse.model_validate(project)
    
    async def get_all(
        self,
        owner_id: str,
        page: int = 1,
        limit: int = 10,
        search: str | None = None,
        sort: str = "created_at",
        order: str = "desc",
    ):
        # Cache key unique per parameter combination
        cache_key = f"list:{owner_id}:{page}:{limit}:{search}:{sort}:{order}"
        #logger.info(f"Checking cache key: {cache_key}")  # temporary
        cached = await self.cache.get(cache_key)
        if cached:
            #logger.info("Returning from cache") # temporary
            return cached

        projects, total = await self.repo.get_all_by_owner(
            owner_id=owner_id,
            page=page,
            limit=limit,
            search=search,
            sort=sort,
            order=order,
        )
        result = PaginatedResponse.create(
            items=[ProjectResponse.model_validate(p) for p in projects],
            total=total,
            page=page,
            limit=limit,
        )
        # Save to cache
        await self.cache.set(cache_key, result.model_dump())
        return result
    
    async def get_by_id(self, project_id: str, owner_id: str) -> ProjectResponse:
        cache_key = f"detail:{project_id}"
        cached = await self.cache.get(cache_key)
        if cached:
            return ProjectResponse(**cached)

        project = await self._get_and_verify_owner(project_id, owner_id)
        result = ProjectResponse.model_validate(project)
        await self.cache.set(cache_key, result.model_dump())
        return result
    
    async def update(self, project_id: str, data: ProjectUpdate, owner_id: str) -> ProjectResponse:
        project = await self._get_and_verify_owner(project_id, owner_id)
        update_data = data.model_dump(exclude_none=True)
        project = await self.repo.update(project, update_data)
        await self.activity.log(
            user_id=owner_id,
            project_id=project.id,
            entity_type="project",
            entity_id=project.id,
            action="updated",
            extra_data=update_data,
        )
        # Invalidate cache
        await self.cache.delete(f"detail:{project_id}")
        await self.cache.delete_pattern(f"list:{owner_id}:*")
        return ProjectResponse.model_validate(project)
    
    async def delete(self, project_id: str, owner_id: str) -> None:
        project = await self._get_and_verify_owner(project_id, owner_id)
        await self.activity.log(
            user_id=owner_id,
            project_id=project.id,
            entity_type="project",
            entity_id=project.id,
            action="deleted",
            extra_data={"name": project.name},
        )
        # Invalidate cache
        await self.cache.delete(f"detail:{project_id}")
        await self.cache.delete_pattern(f"list:{owner_id}:*")
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