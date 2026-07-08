from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schema import ActivityOutputSchema, ActivityCreateSchema
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