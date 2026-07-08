from fastapi import FastAPI

import app.model.model as model
from app.config.database import engine
from app.routers import activity

model.base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(activity.router, prefix="/api/activity", tags=["Activity"])
        