from sqlalchemy import Column, Integer, String, DateTime, func,JSON
from sqlalchemy.sql import func
from app.db.database import Base
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship

class Board(Base):
    __tablename__ = "boards"

    id = Column(Integer , primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    description = Column(String(500), nullable=True)
    columns = Column(JSON , nullable=False, default=["ToDo", "InProgress", "Done"])

    #relation with project 
    project_id = Column(Integer,ForeignKey("projects.id"), nullable=False , index=True )

    # timestamps
    created_at = Column(DateTime(timezone=True),server_default=func.now())
    updated_at = Column(DateTime(timezone=True),onupdate=func.now())

# relationship backpopulate
    project = relationship("Project", back_populates="boards")
    tasks = relationship("Task" , back_populates= "board")