"""
    project data model using sqlalchemy 
"""
from sqlalchemy import Column, Integer, String, DateTime, func  
from sqlalchemy.sql import func
from app.db.database import Base

class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200),nullable=False, index=True)
    description = Column(String(500),nullable=True)

    #project owner 
    owner_id = Column(String(100),nullable=False, index=True)

    # timestamps
    created_at = Column(DateTime(timezone=True),server_default=func.now())
    updated_at = Column(DateTime(timezone=True),onupdate=func.now())

