from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.project import Project


class ProjectRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_by_id(self, project_id: str) -> Project | None:
        result = await self.db.execute(select(Project).where(Project.id == project_id))
        return result.scalar_one_or_none()
    
    async def get_all_by_owner(
        self,
        owner_id: str,
        page: int = 1,
        limit: int = 10,
        search: str | None = None,
        sort: str = "created_at",
        order: str = "desc",
    ) -> tuple[list[Project], int]:
        query = select(Project).where(Project.owner_id == owner_id)
        
        # Search by name
        if search:
            query = query.where(Project.name.ilike(f"%{search}%"))
            
        # Count total
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await self.db.execute(count_query)
        total = total_result.scalar()

        # Sort
        allowed_sort = {"created_at", "updated_at", "name"}
        if sort not in allowed_sort:
            sort = "created_at"
        sort_column = getattr(Project, sort)
        if order == "desc":
            query = query.order_by(sort_column.desc())
        else:
            query = query.order_by(sort_column.asc())
        
        # Paginate
        offset = (page - 1) * limit
        query = query.offset(offset).limit(limit)

        result = await self.db.execute(query)
        return list(result.scalars().all()), total
    
    async def create(self, name: str, description: str | None, owner_id: str) -> Project:
        project = Project(
            name=name,
            description=description,
            owner_id=owner_id,
        )
        self.db.add(project)
        await self.db.flush()
        await self.db.refresh(project)
        return project
    
    async def update(self, project: Project, data: dict) -> Project:
        for key, value in data.items():
            setattr(project, key, value)
        await self.db.flush()
        await self.db.refresh(project)
        return project
    
    async def delete(self, project: Project) -> None:
        await self.db.delete(project)
        await self.db.flush()