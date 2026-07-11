from app.db.database import Base
from sqlalchemy import Column, Integer, String, DateTime, func,Enum
from sqlalchemy.sql import func

from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship
from app.utils.enums import TaskStatus,TaskPriority

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer , primary_key=True, index=True)
    title = Column(String(200), nullable=False, index=True)
    description = Column(String(500), nullable=True)

#project owner 
    user_id = Column(String(200), nullable=False , index=True)

    assigned_to =Column(String(200), nullable=False , index=True)

    status = Column(Enum(TaskStatus) , default=TaskStatus.IN_PROGRESS)
    priority =Column(Enum(TaskPriority) , default= TaskPriority.MEDIUM)
    due_date = Column(DateTime(timezone=True) , nullable=False)

    #relation with board 
    board_id = Column(Integer,ForeignKey("boards.id"), nullable=False , index=True )

    # timestamps
    created_at = Column(DateTime(timezone=True),server_default=func.now())
    updated_at = Column(DateTime(timezone=True),onupdate=func.now())

# relationship backpopulate
    board = relationship("Board", back_populates="tasks")