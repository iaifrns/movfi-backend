from fastapi import APIRouter, Depends, status, HTTPException
from app.schema import QuickStartCreate, QuickStartResponse, QuickStartCreateSimulator
from sqlalchemy.orm import Session
from app.db import get_db
import app.model.model as model
from app.utils.travel_wave_equation import travel_wave_equation

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

            if data.fish.file is not None:
                file_data = data.fish.file.model_dump()
            else:
                file_data = None

            fish = model.FishData(
                activity_id = activity.id,
                length = data.fish.length,
                weight = data.fish.weight,
                species = data.fish.species,
                behavior = data.fish.behavior,
                name = data.fish.name,
                file = file_data,

                body_points = data.fish.body_points,
                fps = data.fish.fps,
                duration = data.fish.duration,
                max_amplitude = data.fish.max_amplitude,
                tail_beat_frequency = data.fish.tail_beat_frequency,
                wave_length = data.fish.wave_length
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

@router.post(path='/simulated_data', response_model= QuickStartResponse)
def quickStartSimulat(data: QuickStartCreateSimulator, db: Session = Depends(get_db)):
    try:
        activity = model.Activity(
            name = data.activity.name,
            description = data.activity.description,
            user_id = data.activity.user_id
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
                name = data.fish.name,
                            
                body_points = data.fish.body_points,
                fps = data.fish.fps,
                duration = data.fish.duration,
                max_amplitude = data.fish.max_amplitude,
                tail_beat_frequency = data.fish.tail_beat_frequency,
                wave_length = data.fish.wave_length
            )

            db.add(fish)
            db.flush()

            try:
                file_data = model.FileData(
                    file_name = "None",
                    data= travel_wave_equation(
                        num_points = fish.body_points,
                        max_ampl = fish.max_amplitude, 
                        wave_length = fish.wave_length, 
                        tail_beat_freq = fish.tail_beat_frequency, 
                        duration = fish.duration, 
                        fsp = fish.fps
                    ),
                    fish_id = fish.id
                )

                db.add(file_data)
                db.commit()
                db.flush()
                db.refresh(activity)

                return {'activity':activity, 'fish':fish, 'file_data': file_data}
            except Exception as e:
                db.rollback()
                raise HTTPException(status_code=500, detail=f"Error occured 3 {e}")

        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Error occured 2 {e}")
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error occured 1 {e}")