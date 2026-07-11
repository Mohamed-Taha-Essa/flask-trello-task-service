"""
    project schemas using pydantic
"""
from app.schemas.projects_schemas import ProjectBase
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional , List
from app.models.projects import Project
from app.api.boards_api import Board

class BoardBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200 ,description="Board name")
    description: Optional[str] = Field(None, max_length=500, description="Board description")
    project_id: str = Field(..., min_length=1, max_length=100, description="Project ID")
# it's prefer to using list instead of List because of the default value and pydantic validation   
    columns: List[str] = Field(default=["ToDo", "InProgress", "Done"], description="List of column names")

class BoardCreate(BoardBase):
    pass

class BoardResponse(BoardBase):
    id: int = Field(..., gt=0, description="Board ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        from_attributes = True


class BoardUpdate(BoardBase):
    name: Optional[str] = Field(None, min_length=1, max_length=200 ,description="Board name")
    description: Optional[str] = Field(None, max_length=500, description="Board description")
    columns: Optional[List[str]] = Field(None, description="List of column names")
