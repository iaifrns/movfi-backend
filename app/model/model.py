from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from app.config.database import base
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from datetime import datetime, timedelta
from pydantic import BaseModel
import uuid

Base = declarative_base()

class File(BaseModel):
    id: str
    fullPath: str
    path: str

class Activity(base):
    __tablename__ = "activity"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    user_id = Column(Integer, nullable=False, default=1)  # Assuming a default user_id for demonstration
    
    fish_data = relationship("FishData", back_populates="activity", cascade="all, delete-orphan")


class FishData(base):
    __tablename__ = "fish_data"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    activity_id = Column(String, ForeignKey('activity.id', ondelete='CASCADE'), nullable=False)
    length = Column(Float, nullable=True)
    weight = Column(Float, nullable=True)
    species = Column(String, nullable=True)
    behavior = Column(String, nullable=True)
    note = Column(String, nullable=True)
    name = Column(String, nullable=True)
    file = Column(JSONB, nullable=True)
    
    activity = relationship('Activity', back_populates="fish_data")
    fish_data = relationship("FileData", back_populates="fish_data", cascade="all, delete-orphan")

    def set_file(self, profile: File):
        """Set file from Pydantic model"""
        self.file = profile.model_dump()
    
    def get_file(self) -> File:
        """Get file as Pydantic model"""
        return File(**self.file) if self.file else None
        

class FileData(base):
    __tablename__ = "file_data"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    file_name = Column(String, nullable=False)
    data= Column(JSONB, nullable=False)
    fish_id = Column(String, ForeignKey("fish_data.id", ondelete="CASCADE"), nullable=False)
    create_at = Column(DateTime, server_default=func.now())
    expires_at = Column(DateTime, default=lambda: datetime.utcnow() + timedelta(days=7))
    last_accessed = Column(DateTime, nullable=True, default= lambda: datetime.utcnow())
    access_count = Column(Integer, default=0)

    fish_data = relationship("FishData", back_populates='fish_data')