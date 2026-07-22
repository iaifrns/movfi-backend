from fastapi import APIRouter, Depends, status, HTTPException
from app.schema import QuickStartCreate, QuickStartResponse
from sqlalchemy.orm import Session
from app.db import get_db
import app.model.model as model

router = APIRouter()

@router.post(path='/', response_model=QuickStartResponse)
def quickStart(data: QuickStartCreate, db:Session = Depends(get_db)):
    try:
        activity = model.Activity(
        name=data.activity.name,
        description=data.activity.description,
        user_id=data.activity.user_id
        )

        db.add(activity)
        db.flush()

        try:
            fish = model.FishData(
                activity_id = activity.id,
                length = data.fish.length,
                weight = data.fish.weight,
                species = data.fish.species,
                behavior = data.fish.behavior,
                note = data.fish.note,
                name = data.fish.name,
                file = data.fish.file.model_dump()
            )

            db.add(fish)
            db.flush()


            try:

                file_info = model.FileData(
                    file_name = data.file_data.file_name,
                    data= data.file_data.data,
                    fish_id = fish.id
                )

                db.add(file_info)
                db.commit()
                db.flush()
                db.refresh(activity)
                
                return {'activity':activity, 'fish':fish, 'file_data':file_info}

            except Exception as e:
                db.rollback()

                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"an Error occured 3 {e}")


        except Exception as e:
            db.rollback()

            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"an Error occured 2 {e}")

    except Exception as e:
        db.rollback()

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"an Error occured 1 {e}")