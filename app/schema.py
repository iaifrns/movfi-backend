from pydantic import BaseModel, Field
from app.model.model import File
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

class ActivityUpdateData(BaseModel):
    name: str = Field(..., description="Name of the activity")
    description: str = Field(None, description="Description of the activity", optional=True)
    
    class Config:
        orm_mode = True
        
class FishDataSchema(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique identifier for the fish data")
    activity_id: str = Field(..., description="ID of the associated activity")
    length: float = Field(None, description="Length of the fish", optional=True)
    weight: float = Field(None, description="Weight of the fish", optional=True)
    species: str = Field(None, description="Species of the fish", optional=True)
    behavior: str = Field(None, description="Behavior of the fish", optional=True)
    note: str = Field(None, description="Additional notes about the fish", optional=True)
    name: str = Field(None, description="Name of the fish", optional=True)
    file: File = Field(None, description="File data information of the fish")

    class Config:
        orm_mode = True
        
class FishDataCreateSchema(BaseModel):
    activity_id: str = Field(..., description="ID of the associated activity")
    length: float = Field(None, description="Length of the fish", optional=True)
    weight: float = Field(None, description="Weight of the fish", optional=True)
    species: str = Field(None, description="Species of the fish", optional=True)
    behavior: str = Field(None, description="Behavior of the fish", optional=True)
    note: str = Field(None, description="Additional notes about the fish", optional=True)
    name: str = Field(None, description="Name of the fish", optional=False)
    file: File = Field(None, description="data file information of the fish")

    class Config:
        orm_mode = True

class FishDataUpdate(BaseModel):
    length: float = Field(None, description="Length of the fish", optional=True)
    weight: float = Field(None, description="Weight of the fish", optional=True)
    species: str = Field(None, description="Species of the fish", optional=True)
    behavior: str = Field(None, description="Behavior of the fish", optional=True)
    note: str = Field(None, description="Additional notes about the fish", optional=True)
    name: str = Field(None, description="Name of the fish", optional=False)
    
    class Config:
        orm_mode = True

""" class SegmentGrowth(str,enum):
    data: np.ndarray
    xs: np.ndarray
    ys: np.ndarray
    num_rows: int
    num_cols: int
    thresh: float """