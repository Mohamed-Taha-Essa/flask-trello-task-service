
from app.db.database import get_db_session
from app.models import boards
from app.schemas.project_schemas import ProjectCreate, ProjectResponse, ProjectUpdate
from app.models.projects import Project
from typing import List ,Optional

from app.models.boards import Board
from app.schemas.board_schema import BoardCreate, BoardResponse, BoardUpdate


def get_boards_by_project(project_id: int ,offset:int =0 ,limit:int=50)-> List[BoardResponse]:
    """

    """
    with get_db_session() as db :
        db_boards = db.query(Board).filter(Board.project_id == project_id).offset(offset).limit(limit).all()
        return [BoardResponse(board) for board in db_boards]

def get_board_by_id(board_id:int) -> Optional[BoardResponse]:
    """
    Get a board by its ID.
    :param board_id: The ID of the board to retrieve.
    :return: The board if found, None otherwise.    
    """
    with get_db_session() as db:
        db_board = db.query(Board).filter(Board.id == board_id).first()
        if db_board:
            return BoardResponse.model_validate(db_board)
        return None

def create_board(board_data: BoardCreate) -> BoardResponse:
    """
    Create a new board.
    :param board_data: The data for the new board.
    :return: The created board.
    """
    with get_db_session() as db:
        #db_board = Board(**board_data.model_dump())
        db_board = Board(
            name=board_data.name,
            description=board_data.description,
            project_id=board_data.project_id,
            columns=board_data.columns
        )
        db.add(db_board)
        db.flush()
        db.refresh(db_board)
        return BoardResponse.model_validate(db_board)

def update_board(board_id: int, board_data: BoardUpdate) -> Optional[BoardResponse]:
    """
    Update a board by its ID.
    :param board_id: The ID of the board to update.
    :param board_data: The updated board data.
    """
    with get_db_session() as db:
        db_board = db.query(Board).filter(Board.id == board_id).first()
        if not db_board:
            return None
        
        if board_data.name is not None:
            db_board.name = board_data.name
        if board_data.description is not None:
            db_board.description = board_data.description
        if board_data.columns is not None:
            db_board.columns = board_data.columns
        db.flush()
        db.refresh(db_board)
        return BoardResponse.model_validate(db_board)

def delete_board(board_id: int) -> bool:
    """
    Delete a board by its ID.
    :param board_id: The ID of the board to delete.
    :return: True if the board was deleted, False otherwise.
    """
    with get_db_session() as db:
        db_board = db.query(Board).filter(Board.id == board_id).first()
        if db_board:
            db.delete(db_board)
            db.flush()
            return True
        return False    