""" this file for handeling api for project model"""

from app.services.project_service import get_project_by_id ,get_projects_by_owner ,create_project ,update_project ,delete_project
from app.schemas.project_schemas import ProjectCreate ,ProjectResponse ,ProjectUpdate
from flask import Blueprint ,jsonify ,request
from typing import List ,Optional

projects_bp = Blueprint('projects' ,__name__, prefix="api.v1/projects" ,tags=["projects"] )


@projects_bp.get("/", methods=['GET'])
def read_projects_by_owner() -> List[ProjectResponse]:

    """return all projects by owner id """
    owner_id = request.args.get("owner_id")
    limit = request.args.get('limit',type=int)
    offset = request.args.get('offset',type=int)

    if not owner_id:    
        return jsonify({"error": "Owner ID is required"}), 400

    projects = get_projects_by_owner(owner_id, limit=limit ,offset=offset)
    return jsonify({
        "success": True,
        "data": [p.model_dump() for p in projects]
    }), 200

@projects_bp.get("/<int:project_id>",methods=['GET'])
def read_project(project_id: int) -> Optional[ProjectResponse]:

    """return project detail"""
    project = get_project_by_id(project_id)
    if not project:
        return jsonify({"error": "Project not found"}), 404
    return jsonify(project)  

@projects_bp.post("/", methods=['POST'])
def create_new_project(project_data: ProjectCreate) -> ProjectResponse:
    project = create_project(project_data)
    return jsonify(project)

@projects_bp.put("/{project_id}", response_model=ProjectResponse)
def update_existing_project(project_id: int, project_data: ProjectUpdate) -> Optional[ProjectResponse]:
    project = update_project(project_id, project_data)
    if not project:
        return jsonify( {"error": "project not foune"}), 404
    return project

@projects_bp.delete("/{project_id}", response_model=bool)
def delete_existing_project(project_id: int) -> bool:
    success = delete_project(project_id)
    if not success:
        return jsonify({"detail":"project not found"}), 404
    return jsonify({
        "success": True,
        "message": "Project deleted successfully"
    }), 200