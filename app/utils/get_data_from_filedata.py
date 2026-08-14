from sqlalchemy.orm import Session
import app.model.model as models
from app.config.database import sessionLocal

def fetch_data_point(file_id: str, index: int):
    with sessionLocal() as db:  # Connection acquired here
        """Fetch a single element from the JSONB array at the given index"""
        query = db.query(
            models.FileData.data.op('->')(index).label('data_point')
        ).filter(models.FileData.id == file_id)
        
        result = query.first()
        if result:
            return result.data_point
    return None