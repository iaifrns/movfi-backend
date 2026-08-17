from fastapi import APIRouter, Depends, HTTPException, status
from app.schema import FishDataCreateSchema, FishDataSchema, FishDataUpdate, FileDataCreateSchema, FileDataSchema, FileDataSchemaResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
import app.model.model as model
from typing import List
from app.db import get_db
from concurrent.futures import ThreadPoolExecutor
from app.utils.get_data_from_filedata import fetch_data_point
from app.config.database import sessionLocal

router = APIRouter()

@router.post('/', response_model=FishDataSchema)
def createFish(fish: FishDataCreateSchema, db: Session = Depends(get_db)):
    
    if fish.activity_id:
        activity = db.query(model.Activity).filter(model.Activity.id==fish.activity_id).first()
        print(activity)
        if not activity:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="There is no activity with that id")
    
    try:

        if fish.file is not None:
            file_data = fish.file.model_dump()
        else:
            file_data = None

        db_fish = model.FishData(
            activity_id = fish.activity_id,
            length = fish.length,
            weight = fish.weight,
            species = fish.species,
            behavior = fish.behavior,
            name = fish.name,
            file = file_data,
            
            body_points = fish.body_points,
            fps = fish.fps,
            duration = fish.duration,
            max_amplitude = fish.max_amplitude,
            tail_beat_frequency = fish.tail_beat_frequency,
            wave_length = fish.wave_length
        )

        db.add(db_fish)
        db.commit()
        db.refresh(db_fish)

        return db_fish
    except Exception as e:
        print("there was an error in the code")
        print(e)

        db.rollback()

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error {e}")

@router.post('/set_file_data', response_model=FileDataSchema)
def setFileData(file_data: FileDataCreateSchema, db:Session = Depends(get_db)):
    try:
        fish_id = file_data.file_data_id

        fish = db.query(model.FishData).filter(model.FishData.id == fish_id).first()

        if not fish:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"There is no fish info with the id provided")
        
        file_info = model.FileData(
            file_name = file_data.file_name,
            data= file_data.data,
            fish_id = file_data.fish_id,
        )

        db.add(file_info)
        db.commit()
        db.refresh(file_info)

        return file_info

    except Exception as e:
        db.rollback()

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"something when wrong {e}")

@router.get('/get_file_data_by_fish/{fish_id}', response_model=List[FileDataSchemaResponse])
async def getFillDataByFile(fish_id: str, db:Session = Depends(get_db)):
    try:
        fish = db.query(model.FishData).filter(model.FishData.id == fish_id).first()

        if not fish:
            raise HTTPException(status_code=404, detail="there is no fish with this id")
        
        file_data = db.query(model.FileData).filter(model.FileData.fish_id == fish.id).first()

        data = fetch_data_point(file_data.data, 10)

        return [{
            'id': file_data.id,
            'file_name': file_data.file_name,
            'data': data,
            'fish_id': fish.id,
            'create_at': file_data.create_at,
            'expires_at': file_data.expires_at,
            'last_accessed': file_data.last_accessed,
            'access_count': file_data.access_count,
            'data_length': round(len(file_data.data[0])/2,0)
        }]
        
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occured {e}")

@router.get('/get_all_file_data_by_fish/{fish_id}', response_model=List[FileDataSchemaResponse])
async def getAllFillDataByFile(fish_id: str, db:Session = Depends(get_db)):
    try:
        fish = db.query(model.FishData).filter(model.FishData.id == fish_id).first()

        if not fish:
            raise HTTPException(status_code=404, detail="there is no fish with this id")
        
        file_data = db.query(model.FileData).filter(model.FileData.fish_id == fish.id).first()

        return [{
            'id': file_data.id,
            'file_name': file_data.file_name,
            'data': file_data.data,
            'fish_id': fish.id,
            'create_at': file_data.create_at,
            'expires_at': file_data.expires_at,
            'last_accessed': file_data.last_accessed,
            'access_count': file_data.access_count,
            'data_length': round(len(file_data.data[0])/2,0)
        }]
        
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occured {e}")

@router.get('/get_data/{file_id}/{page}', response_model=List)
def get_data(file_id: str, page: int, db: Session = Depends(get_db)):
    try:
        result = db.query(model.FileData.data).filter(model.FileData.id == file_id).all()

        data = result[0][0]
    
        paginated_data = fetch_data_point(data, 10, page)
    
        return paginated_data
            
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occured {e}")

@router.get("/fishs", response_model=List[FishDataSchema])
def getAllFishs(db:Session = Depends(get_db)):
    fishs = db.query(model.FishData).all()
    
    return fishs

@router.get("/fishs/{activityId}", response_model=List[FishDataSchema])
def getFishsByActivity(activityId:str, db:Session = Depends(get_db)):
    try:
        activId = activityId

        fishs = db.query(model.FishData).filter(model.FishData.activity_id == activId).all()

        return fishs

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error {e}")

@router.put('/modify/{fish_id}', response_model=FishDataSchema)
def modifyFishInfo(fish_id: str, fishInfo: FishDataUpdate, db:Session = Depends(get_db)):
    try:
        fish = db.query(model.FishData).filter(model.FishData.id == fish_id).first()

        if not fish:
            raise HTTPException(status_code=404, detail="User not found")
        
        fish.name = fishInfo.name
        fish.species = fishInfo.species
        fish.weight = fishInfo.weight
        fish.length = fishInfo.length
        fish.behavior = fishInfo.behavior
        fish.note = fishInfo.note

        db.commit()
        db.refresh(fish)

        return fish
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"an error occred {e}")