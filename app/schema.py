import enum
from pydantic import BaseModel, Field
import numpy as np
import uuid
    
class ActivitySchema(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique identifier for the activity")
    name: str = Field(..., description="Name of the activity")
    description: str = Field(None, description="Description of the activity", optional=True)
    user_id: int = Field(1, description="ID of the user associated with the activity")  # Assuming a default user_id for demonstration

    class Config:
        orm_mode = True
        
class ActivityCreateSchema(BaseModel):
    name: str = Field(..., description="Name of the activity")
    description: str = Field(None, description="Description of the activity", optional=True)
    user_id: int = Field(1, description="ID of the user associated with the activity")  # Assuming a default user_id for demonstration

    class Config:
        orm_mode = True
        
class ActivityOutputSchema(BaseModel):
    id: str = Field(..., description="Unique identifier for the activity")
    name: str = Field(..., description="Name of the activity")
    description: str = Field(None, description="Description of the activity", optional=True)
    user_id: int = Field(..., description="ID of the user associated with the activity")  # Assuming a default user_id for demonstration

    class Config:
        orm_mode = True
        

""" class SegmentGrowth(str,enum):
    data: np.ndarray
    xs: np.ndarray
    ys: np.ndarray
    num_rows: int
    num_cols: int
    thresh: float """