from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.config.database import base
from sqlalchemy.orm import relationship
import uuid

class Activity(base):
    __tablename__ = "activity"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    user_id = Column(Integer, nullable=False, default=1)  # Assuming a default user_id for demonstration
    
    fish_data = relationship("FishData", back_populates="activity")

class FishData(base):
    __tablename__ = "fish_data"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    activity_id = Column(String, ForeignKey('activity.id'), nullable=False)
    length = Column(Float, nullable=True)
    weight = Column(Float, nullable=True)
    species = Column(String, nullable=True)
    behavior = Column(String, nullable=True)
    note = Column(String, nullable=True)
    name = Column(String, nullable=True)
    
    activity = relationship('Activity', back_populates="fish_data")
        