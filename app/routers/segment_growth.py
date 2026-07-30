from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db import get_db
import app.model.model as model
import numpy as np
from app.utils.segment_growth import segment_growing

router = APIRouter()

@router.get('/get_frams_segment/{fish_id}', response_model=dict)
def get_all_frames_segment(fish_id: str, db: Session = Depends(get_db)):
    try:
        seperate_all_data = {}
        response = {}
        main_keys = set()

        fish = db.query(model.FishData).filter(model.FishData.id == fish_id).first()

        if not fish:
            raise HTTPException(status_code=404, detail=f"No fish was found with this id")
        
        fileData = db.query(model.FileData).filter(model.FileData.fish_id == fish.id).first()

        for key in fileData.data[0].keys():
            main_keys.add(key[:-1])

        for i in range(0,len(fileData.data)):
            for key in main_keys:
                if key not in seperate_all_data:
                    seperate_all_data[key] = []
                seperate_all_data[key].append([fileData.data[i][key+'x'],fileData.data[i][key+'y']])

        for indexs in seperate_all_data.keys():
            data = seperate_all_data[indexs]
            xs = [0]
            ys = [1]

            joint_positions, total_evaluations, total_datapoints = segment_growing(
                data=np.array(data),
                xs=np.array(xs),
                ys=np.array(ys),
                num_rows=len(fileData.data),
                num_cols=len(fileData.data[0].keys()),
                thresh=0.001
            )
            response[indexs] = joint_positions.tolist()


        return response
    except Exception as e:
        print(e)
        print('*'*80)
        raise HTTPException(status_code=500, detail=f"An error occured {e}")

@router.get('/get_a_segment/{fish_id}', response_model=list)
def get_segment(fish_id: str, db: Session = Depends(get_db)):
    try:

        fish = db.query(model.FishData).filter(model.FishData.id == fish_id).first()

        if not fish:
            raise HTTPException(status_code=404, detail=f"No fish was found with this id")
        
        fileData = db.query(model.FileData).filter(model.FileData.fish_id == fish.id).first()

        data = []

        for d in fileData.data:
            data.append(list(d.values()))

        xs = list(range(0,len(data[0]),2))
        ys = list(range(1, len(data[0]),2))

        joint_positions, total_evaluations, total_datapoints = segment_growing(
            data=np.array(data),
            xs=np.array(xs),
            ys=np.array(ys),
            num_rows=len(fileData.data),
            num_cols=len(fileData.data[0].keys()),
            thresh=0.001
        )

        return joint_positions.tolist()
    except Exception as e:
        print(e)
        print('*'*80)
        raise HTTPException(status_code=500, detail=f"An error occured {e}")
     