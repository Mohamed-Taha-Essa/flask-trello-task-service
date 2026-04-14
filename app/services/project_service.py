"""
services functions for handling project operations
this file will contain all the business logic for projects
"""


from app.db.database import get_db_session
from app.schemas.project_schemas import ProjectCreate, ProjectResponse, ProjectUpdate
from app.models.project_model import Project
from typing import List ,Optional


def get_projects_by_owner(owner_id: str ,offset:int =0 ,limit:int=50)-> List[ProjectResponse]:
    """
    Get all projects for a specific owner
    """
    with get_db_session() as db:
        projects = db.query(Project).filter(Project.owner_id == owner_id).offset(offset).limit(limit).all()
        return [ProjectResponse.model_validate(project) for project in projects]

def get_project_by_id(project_id:int) -> Optional[ProjectResponse]:
    """
    Get a project by id
    """
    with get_db_session() as db:
        project = db.query(Project).filter(Project.id == project_id).first()
        if project:
            return ProjectResponse.model_validate(project)
        return None


def create_project(project_data: ProjectCreate) -> ProjectResponse:
    """
    Create a new project
    """
    with get_db_session() as db:
        db_project = Project(**project_data.model_dump())
        #add to database
        db.add(db_project)
        #apply changes to database
        db.flush()
        #refresh the project to get the id
        db.refresh(db_project)
        return ProjectResponse.model_validate(db_project)

def update_project(project_id: int, project_data: ProjectUpdate) -> Optional[ProjectResponse]:
    """
    Update a project
    """
    with get_db_session() as db:
        project = db.query(Project).filter(Project.id == project_id).first()
        if project:
            for key, value in project_data.model_dump().items():
                setattr(project, key, value)
            db.flush()
            db.refresh(project)
            return ProjectResponse.model_validate(project)
        return None


def delete_project(project_id: int) -> bool:
    """
    Delete a project
    """
    with get_db_session() as db:
        project = db.query(Project).filter(Project.id == project_id).first()
        if project:
            db.delete(project)
           
            return True
        return False
 