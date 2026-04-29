""" this file for handeling api for project model"""

from app.services.project_service import get_project_by_id ,get_projects_by_owner ,create_project ,update_project ,delete_project
from app.schemas.project_schemas import ProjectCreate ,ProjectResponse ,ProjectUpdate
from fastapi import APIRouter ,HTTPException ,Depends
from typing import List ,Optional

router = APIRouter( prefix="/projects" ,tags=["projects"] )


@router.get("/owner/{owner_id}", response_model=List[ProjectResponse])
def read_projects_by_owner(owner_id: str, offset: int = 0, limit: int = 50) -> List[ProjectResponse]:

    projects = get_projects_by_owner(owner_id, offset, limit)
    return projects

@router.get("/{project_id}", response_model=ProjectResponse)
def read_project(project_id: int) -> Optional[ProjectResponse]:
    project = get_project_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project  

@router.post("/", response_model=ProjectResponse)
def create_new_project(project_data: ProjectCreate) -> ProjectResponse:
    project = create_project(project_data)
    return project

@router.put("/{project_id}", response_model=ProjectResponse)
def update_existing_project(project_id: int, project_data: ProjectUpdate) -> Optional[ProjectResponse]:
    project = update_project(project_id, project_data)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.delete("/{project_id}", response_model=bool)
def delete_existing_project(project_id: int) -> bool:
    success = delete_project(project_id)
    if not success:
        raise HTTPException(status_code=404, detail="Project not found")
    return success