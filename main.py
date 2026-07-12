from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import app.model.model as model
from app.config.database import engine
from app.routers import activity, fish

model.base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,      # Allows requests from these origins
    allow_credentials=True,      # Allows cookies and authorization headers to be included
    allow_methods=["*"],         # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],         # Allows all headers
)

app.include_router(activity.router, prefix="/api/activity", tags=["Activity"])
app.include_router(fish.router, prefix="/api/fish", tags=['Fish'] )
        