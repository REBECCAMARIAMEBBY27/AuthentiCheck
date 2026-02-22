from fastapi import FastAPI
from app.routers.image_router import router as image_router

app = FastAPI()

app.include_router(image_router)