""" this file for handeling api for board model"""
from app.schemas.board_schema import BoardCreate ,BoardUpdate,BoardResponse 
from app.services.board_service import create_board ,update_board,delete_board,get_board_by_id,get_boards_by_project
from app.models.boards import Board
from flask import Blueprint ,jsonify ,request
from typing import List ,Optional

board_bp = Blueprint('board' ,__name__, prefix="api.v1/boards" ,tags=["boards"] )

@board_bp.route("/"  , methods=["POST"] )
def board_create(board_data : BoardCreate):
    try: 
        data = request.get_json()
        if not data : 
            return jsonify({"error" : "no data provided"}), 404
        
        board_data = BoardCreate(**data)
        created_board = create_board(board_data)
        return jsonify(created_board.model_dump()) ,201

    except Exception as e : 
        return jsonify({"error ":f"failed to delete board :{e}"}) , 500

@board_bp.rout("/<int:board_id>",mothods=['GET'])
def get_board(board_id:int):
    try : 
        board = get_board_by_id(board_id)
        if not board:
            return jsonify({"error" : "board not found"}), 404
        return jsonify(board.model_dump()) , 200 
    except Exception as e : 
        return jsonify({"error ":f"failed to fetch board :{e}"}) , 500  

@board_bp.route("/",methods=['GET'])
def boards_list_by_project():
    try: 
        project_id = int(request.args.get("project_id")) 
        limit = request.args.get('limit',type=int)
        offset = request.args.get('offset',type=int)

        if not project_id:
            return jsonify({"error" : "project_id param is required"}) , 400
        
        boards = get_boards_by_project(project_id=project_id ,offset=offset , limit=limit)
        boards_data = [ board.model_dump() for board in boards]

        return jsonify(boards_data) , 200 
    except Exception as e : 
        return jsonify({"error ":f"failed to fetch boards:{e}"}) , 500

@board_bp.route("/<int:board_id>", methods=["PUT"] )
def board_update(board_id: int):
    try : 
        data = request.get_json()
        if not data : 
            return jsonify({"error": "no data provided"}), 400
        board_data = BoardUpdate(**data)
        updated_data = update_board(board_id,board_data)
        return jsonify(updated_data.model_dump())
    
    except Exception as e : 
        return jsonify({"error ":f"failed to update board:{e}"}) , 500

@board_bp.route("/<int:board_id>" ,methods=["DELETE"])
def board_delete(board_id : int):
    try: 
        deleted_board = delete_board(board_id)
        if not deleted_board:
            return jsonify({"error": "board not found"}),404
        return jsonify({"message" : "board deleted successfully"}),200
    except Exception as e : 
        return jsonify({"error ":f"failed to delete board :{e}"}) , 500