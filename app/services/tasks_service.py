"""
services functions for handling task operations
this file will contain all the business logic for tasks
"""

from app.db.database import get_db_session
from app.schemas.tasks_schema import TaskCreate, TaskResponse, TaskUpdate, TaskStats
from app.models.tasks import Task
from typing import List, Optional


def get_tasks_list(board_id: int, user_id: Optional[int] = None, assigned_to: Optional[int] = None, offset: int = 0, limit: int = 50, status: Optional[str] = None, priority: Optional[str] = None) -> List[TaskResponse]:
    """
    Get all tasks for a specific board
    """
    with get_db_session() as db:
        query = db.query(Task).filter(Task.board_id == board_id)
        
        if status:
            query = query.filter(Task.status == status)
        
        if priority:
            query = query.filter(Task.priority == priority)
        
        tasks = query.offset(offset).limit(limit).all()
        return [TaskResponse.model_validate(task) for task in tasks]


def get_tasks_by_user(user_id: int ,status: Optional[str] = None) -> List[TaskResponse]:
    """
    Get all tasks for a specific user
    """
    with get_db_session() as db:
        query = db.query(Task).filter(Task.user_id == user_id).order_by(Task.created_at.desc()).all()
        if status:
            query = query.filter(Task.status == status).all()
        return [TaskResponse.model_validate(task) for task in query]

def get_task_by_id(task_id: int) -> Optional[TaskResponse]:
    """
    Get a task by id
    """
    with get_db_session() as db:
        task = db.query(Task).filter(Task.id == task_id).first()
        if task:
            return TaskResponse.model_validate(task)
        return None


def create_task(task_data: TaskCreate) -> TaskResponse:
    """
    Create a new task
    """
    with get_db_session() as db:
        db_task = Task(**task_data.model_dump())
        db.add(db_task)
        db.flush()
        db.refresh(db_task)
        return TaskResponse.model_validate(db_task)


def update_task(task_id: int, task_data: TaskUpdate) -> Optional[TaskResponse]:
    """
    Update a task
    """
    with get_db_session() as db:
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            return None

        update_data = task_data.model_dump(exclude_unset=True)
        if 'name' in update_data:
            update_data['title'] = update_data.pop('name')

        for key, value in update_data.items():
            setattr(task, key, value)

        db.flush()
        db.refresh(task)
        return TaskResponse.model_validate(task)


def delete_task(task_id: int) -> bool:
    """
    Delete a task
    """
    with get_db_session() as db:
        task = db.query(Task).filter(Task.id == task_id).first()
        if task:
            db.delete(task)
            return True
        return False


def get_task_stats(board_id: int) -> TaskStats:
    """
    Get task statistics for a board
    """
    with get_db_session() as db:
        rows = db.query(Task.status,Task.priority,Task.user_id).all()

        #initialize counter 
        status_count = {s.value:0 for s in TaskStatus}
        priority_count = {p.value:0 for p in TaskPriority}
        user_count = {}
        
        for status, priority, user_id in rows:
            status_count[status.value] += 1
            priority_count[priority.value] += 1
            user_count[user_id] = user_count.get(user_id, 0) + 1
        
        return TaskStats(
            total_tasks=len(rows),
            status_counts=status_count,
            priority_counts=priority_count,
            user_counts=user_count
        )