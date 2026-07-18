from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.schema import ActivityOutputSchema, ActivityCreateSchema, ActivityUpdateData
import app.model.model as model
from app.db import get_db

router = APIRouter()

@router.get("/activities", response_model=List[ActivityOutputSchema])
def get_activities(db: Session = Depends(get_db)):
    activities = db.query(model.Activity).all()
    return activities

@router.post("/", response_model=ActivityOutputSchema)
def create_activity(activity: ActivityCreateSchema, db: Session = Depends(get_db)):
    db_activity = model.Activity(
        name=activity.name,
        description=activity.description,
        user_id=activity.user_id
    )
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    return db_activity

@router.get(path='/get_one',response_model=ActivityOutputSchema)
def get_one_activity(db:Session = Depends(get_db)):
    activity = db.query(model.Activity).one()

    return activity

@router.get(path='/get_activity_by_id/{activityId}')
def get_one_activity_id(activityId: str, db:Session = Depends(get_db)):
    try:
        activity = db.query(model.Activity).filter(model.Activity.id == activityId).one()

        return activity
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"System error {e}")
    
@router.put(path='/modify/{activity_id}', response_model=ActivityOutputSchema)
def updateActivity(activity_id:str, activityData: ActivityUpdateData, db:Session = Depends(get_db)):
    try:
        activity = db.query(model.Activity).filter(model.Activity.id == activity_id).first()

        if not activity:
            raise HTTPException(status_code=404, detail="No Activity found")
        
        activity.name = activityData.name
        activity.description = activityData.description

        db.commit()
        db.refresh(activity)

        return activity
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"an error occured {e}")