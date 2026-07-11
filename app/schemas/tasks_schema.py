"""
    Tasks schemas using pydantic
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional , List, Dict
from app.models.tasks import Task 
from app.utils.enums import TaskPriority,TaskStatus

class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200 ,description="task title")
    description: Optional[str] = Field(None, max_length=500, description="task description")
    board_id: int = Field(..., min_length=1, max_length=100, description="task board ID")
    status:TaskStatus = Field(default=TaskStatus.TODO ,description='task status')
    priority:TaskPriority =Field(default=TaskPriority.MEDIUM ,description='task priority')
    due_date:Optional[datetime] = Field(None, description='when the task is due')
    assigned_to:str =Field(...,description='id of user who assigned to the task')
    user_id:str= Field(... , description= " id of user who create the task")


class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200 ,description="task name")
    description: Optional[str] = Field(None, max_length=500, description="task description")
    status:Optional[TaskStatus] = Field(None,description='task status')
    priority:Optional[TaskPriority] =Field(None ,description='task priority')
    due_date:Optional[datetime] = Field(None, description='when the task is due')
    assigned_to:Optional[str] =Field(None,description='id of user who assigned to the task')

class TaskResponse(TaskBase):
    id :int = Field(...,description='task id')
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

class TaskStats(BaseModel):
    total_tasks:int= Field(..., description='Total number of tasks')
    total_by_status: Dict = Field(..., description='Total tasks grouped by status')
    total_by_priority: Dict = Field(..., description='Total tasks grouped by priority')
    total_by_user: Dict = Field(..., description='Total tasks grouped by user')
    