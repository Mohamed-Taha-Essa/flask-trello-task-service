""" this file for handeling api for project model"""

from app.services.project_service import get_project_by_id ,get_projects_by_owner ,create_project ,update_project ,delete_project
from app.schemas.project_schemas import ProjectCreate ,ProjectResponse ,ProjectUpdate
from flask import Blueprint ,jsonify ,request
from typing import List ,Optional

projects_bp = Blueprint('projects' ,__name__, prefix="api.v1/projects" ,tags=["projects"] )


@projects_bp.route("/", methods=['GET'])
def read_projects_by_owner():

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

@projects_bp.route("/<int:project_id>",methods=['GET'])
def project_detail(project_id: int):

    """return project detail"""
    project = get_project_by_id(project_id)
    if not project:
        return jsonify({"error": "Project not found"}), 404
    return jsonify(project.model_dump()) ,200  

@projects_bp.route("/", methods=['POST'])
def create_new_project() :
    try :
        data = request.get_json()
        if not data : 
            return jsonify({"error" : "no data provided"}), 404
        
        project_data = ProjectCreate(**data)
        created_project = create_project(project_data)
        return jsonify(created_project.model_dump()) ,201

    except Exception as e : 
        return jsonify({"error ":f"failed to delete board :{e}"}) , 500


    project = create_project(project_data)
    return jsonify(project)

@projects_bp.route("/<int:project_id >", methods=["PUT"])
def update_existing_project(project_id: int, project_data: ProjectUpdate):
    project = update_project(project_id, project_data)
    if not project:
        return jsonify( {"error": "project not foune"}), 404
    return project

@projects_bp.route("/<int:project_id>",methods=["DELETE"])
def delete_existing_project(project_id: int) -> bool:
    success = delete_project(project_id)
    if not success:
        return jsonify({"detail":"project not found"}), 404
    return jsonify({
        "success": True,
        "message": "Project deleted successfully"
    }), 200