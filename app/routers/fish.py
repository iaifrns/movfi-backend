from fastapi import APIRouter, Depends, HTTPException, status
from app.schema import FishDataCreateSchema, FishDataSchema
from sqlalchemy.orm import Session
import app.model.model as model
from typing import List
from app.db import get_db

router = APIRouter()

@router.post('/', response_model=FishDataSchema)
def createFish(fish: FishDataCreateSchema, db: Session = Depends(get_db)):
    
    if fish.activity_id:
        activity = db.query(model.Activity).filter(model.Activity.id==fish.activity_id).first()
        print(activity)
        if not activity:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="There is no activity with that id")
    
    try:
        db_fish = model.FishData(
            activity_id = fish.activity_id,
            length = fish.length,
            weight = fish.weight,
            species = fish.species,
            behavior = fish.behavior,
            note = fish.note,
            name = fish.name,
            file = fish.file.model_dump()
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