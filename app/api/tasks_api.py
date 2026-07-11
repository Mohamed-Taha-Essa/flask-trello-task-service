"""this file for handling api for task model"""

from app.services.tasks_service import (
    get_task_by_id,
    get_tasks_by_board,
    create_task,
    update_task,
    delete_task,
    get_task_stats,
)
from app.schemas.tasks_schema import TaskCreate, TaskResponse, TaskUpdate, TaskStats
from flask import Blueprint, jsonify, request

task_bp = Blueprint('tasks', __name__, prefix="api.v1/tasks", tags=["tasks"])


@task_bp.route("/", methods=['GET'])
def tasks_list_by_board():
    try:
        board_id = request.args.get("board_id", type=int)
        limit = request.args.get('limit', default=50, type=int)
        offset = request.args.get('offset', default=0, type=int)

        if not board_id:
            return jsonify({"error": "board_id param is required"}), 400

        tasks = get_tasks_by_board(board_id=board_id, offset=offset, limit=limit)
        tasks_data = [task.model_dump() for task in tasks]
        return jsonify(tasks_data), 200

    except Exception as e:
        return jsonify({"error": f"failed to fetch tasks: {e}"}), 500


@task_bp.route("/<int:task_id>", methods=['GET'])
def task_detail(task_id: int):
    try:
        task = get_task_by_id(task_id)
        if not task:
            return jsonify({"error": "task not found"}), 404
        return jsonify(task.model_dump()), 200

    except Exception as e:
        return jsonify({"error": f"failed to fetch task: {e}"}), 500


@task_bp.route("/", methods=['POST'])
def create_new_task():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "no data provided"}), 400

        task_data = TaskCreate(**data)
        created_task = create_task(task_data)
        return jsonify(created_task.model_dump()), 201

    except Exception as e:
        return jsonify({"error": f"failed to create task: {e}"}), 500


@task_bp.route("/<int:task_id>", methods=["PUT"])
def update_existing_task(task_id: int):
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "no data provided"}), 400

        task_data = TaskUpdate(**data)
        updated_task = update_task(task_id, task_data)
        if not updated_task:
            return jsonify({"error": "task not found"}), 404

        return jsonify(updated_task.model_dump()), 200

    except Exception as e:
        return jsonify({"error": f"failed to update task: {e}"}), 500


@task_bp.route("/<int:task_id>", methods=["DELETE"])
def delete_existing_task(task_id: int):
    try:
        deleted = delete_task(task_id)
        if not deleted:
            return jsonify({"error": "task not found"}), 404
        return jsonify({"message": "task deleted successfully"}), 200

    except Exception as e:
        return jsonify({"error": f"failed to delete task: {e}"}), 500


@task_bp.route("/stats", methods=["GET"])
def task_statistics():
    try:
        board_id = request.args.get("board_id", type=int)
        if not board_id:
            return jsonify({"error": "board_id param is required"}), 400

        stats = get_task_stats(board_id)
        return jsonify(stats.model_dump()), 200

    except Exception as e:
        return jsonify({"error": f"failed to get task stats: {e}"}), 500
