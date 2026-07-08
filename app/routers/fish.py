from fastapi import APIRouter, Depends, HTTPException, status
from app.schema import FishDataCreateSchema, FishDataSchema
from sqlalchemy.orm import Session
import app.model.model as model
from app.db import get_db

router = APIRouter()

@router.post('/', response_model=FishDataSchema)
def createFish(fish: FishDataCreateSchema, db: Session = Depends(get_db)):
    print("it is here ----------------------------")
    db_fish = model.FishData(
        activity_id = fish.activity_id,
        length = fish.length,
        weight = fish.weight,
        species = fish.species,
        behavior = fish.behavior,
        note = fish.note,
        name = fish.name,
    )
    
    try:
        db.add(db_fish)
        db.commit()
        db.refresh(db_fish)
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="an error occured")
    
    return db_fish
    