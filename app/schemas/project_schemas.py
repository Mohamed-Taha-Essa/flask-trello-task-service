"""
    project schemas using pydantic
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class ProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200 ,description="Project name")
    description: Optional[str] = Field(None, max_length=500, description="Project description")
    owner_id: str = Field(..., min_length=1, max_length=100, description="Owner ID")

class ProjectCreate(ProjectBase):
    pass

class ProjectResponse(ProjectBase):
    id: int = Field(..., gt=0, description="Project ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        from_attributes = True


class ProjectUpdate(ProjectBase):
    name: Optional[str] = Field(None, min_length=1, max_length=200 ,description="Project name")
    description: Optional[str] = Field(None, max_length=500, description="Project description")

