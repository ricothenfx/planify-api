from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.task import Task, TaskStatus, TaskPriority


class TaskRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_by_id(self, task_id: str) -> Taks | None:
        result = await self.db.execute(select(Task).where(Task.id == task_id))
        return result.scalar_one_or_none()
    
    async def get_all_by_project(
        self,
        project_id: str,
        page: int = 1,
        limit: int = 10,
        status: TaskStatus | None = None,
        priority: TaskPriority | None = None,
        assignee_id: str | None = None,
        sort: str = "created_at",
        order: str = "desc",
    ) -> tuple[list[Task], int]:
        query = select(Task).where(Task.project_id == project_id)

        # Filter
        if status:
            query = query.where(Task.status == status)
        if priority:
            query = query.where(Task.priority == priority)
        if assignee_id:
            query = query.where(Task.assignee_id == assignee_id)
        
        # Count total
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await self.db.execute(count_query)
        total = total_result.scalar()

        # Sort
        allowed_sort = {"created_at", "updated_at", "title", "priority", "due_date"}
        if sort not in allowed_sort:
            sort = "created_at"
        sort_column = getattr(Task, sort)
        if order == "desc":
            query = query.order_by(sort_column.desc())
        else:
            query = query.order_by(sort_column.asc())
        
        # Paginate
        offset = (page - 1) * limit
        query = query.offset(offset).limit(limit)

        result = await self.db.execute(query)
        return list(result.scalars().all()), total
    
    async def create(self, project_id: str, data: dict) -> Task:
        task = Task(project_id=project_id, **data)
        self.db.add(task)
        await self.db.flush()
        await self.db.refresh(task)
        return task
    
    async def update(self, task: Task, data: dict) -> Task:
        for key, value in data.items():
            setattr(task, key, value)
        await self.db.flush()
        await self.db.refresh(task)
        return task
    
    async def delete(self, task: Task) -> None:
        await self.db.delete(task)
        await self.db.flush()