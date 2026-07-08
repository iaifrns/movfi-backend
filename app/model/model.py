from sqlalchemy import Column, Integer, String, Float
from app.config.database import base
import uuid

class Activity(base):
    __tablename__ = "activity"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    user_id = Column(Integer, nullable=False, default=1)  # Assuming a default user_id for demonstration