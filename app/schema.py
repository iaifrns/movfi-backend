from pydantic import BaseModel, Field
from app.model.model import File
import uuid
from datetime import datetime
from typing import List, Any, Dict, Union, Optional
    
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
    name: str = Field(None, description="Name of the fish", optional=True)
    file: Optional[File] = Field(None, description="File data information of the fish")

    body_points: int = Field(None, description="Number of body points", optional=True)
    fps: float = Field(None, description="Frames per second", optional=True)
    duration: float = Field(None, description="Duration of the recording", optional=True)
    max_amplitude: float = Field(None, description="Maximum amplitude", optional=True)
    tail_beat_frequency: float = Field(None, description="Tail beat frequency", optional=True)
    wave_length: float = Field(None, description="Wave length", optional=True)

    class Config:
        orm_mode = True
        
class FishDataCreateSchema(BaseModel):
    activity_id: str = Field(..., description="ID of the associated activity")
    length: float = Field(None, description="Length of the fish", optional=True)
    weight: float = Field(None, description="Weight of the fish", optional=True)
    species: str = Field(None, description="Species of the fish", optional=True)
    behavior: str = Field(None, description="Behavior of the fish", optional=True)
    name: str = Field(None, description="Name of the fish", optional=False)
    file: Optional[File] = Field(None, description="data file information of the fish", optional=True)

    body_points: int = Field(None, description="Number of body points", optional=True, value=None)
    fps: float = Field(None, description="Frames per second", optional=True, value=None)
    duration: float = Field(None, description="Duration of the recording", optional=True, value=None)
    max_amplitude: float = Field(None, description="Maximum amplitude", optional=True, value=None)
    tail_beat_frequency: float = Field(None, description="Tail beat frequency", optional=True, value=None)
    wave_length: float = Field(None, description="Wave length", optional=True, value=None)

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

class FileDataSchema(BaseModel):
    id: str
    file_name: str = Field(None)
    data: List[Dict[str, Any]]
    fish_id: str
    create_at: datetime
    expires_at: datetime
    last_accessed: datetime
    access_count: int

class FileDataSchemaResponse(BaseModel):
    id: str
    file_name: str = Field(None)
    data: List[Dict[str, Any]]
    fish_id: str
    create_at: datetime
    expires_at: datetime
    last_accessed: datetime
    access_count: int
    data_length: int

class FileDataCreateSchema(BaseModel):
    file_name: str = Field(None)
    data: List[Dict[str, float]]  # If all values are numbers
    # OR
    data: List[Dict[str, Union[float, int, str]]]  # If mixed types
    # OR most flexible
    data: List[Dict[str, Any]]  # Accept anything
    fish_id: str

class QuickStartCreate(BaseModel):
    fish: FishDataCreateSchema
    activity: ActivityCreateSchema
    file_data: FileDataCreateSchema

class QuickStartCreateSimulator(BaseModel):
    fish: FishDataCreateSchema
    activity: ActivityCreateSchema

class QuickStartResponse(BaseModel):
    fish: FishDataSchema
    activity: ActivitySchema
    file_data: FileDataSchema

class CustomResponse(BaseModel):
    joints: list
    segementation_length: float
    tail_amplitude: float

""" class SegmentGrowth(str,enum):
    data: np.ndarray
    xs: np.ndarray
    ys: np.ndarray
    num_rows: int
    num_cols: int
    thresh: float """