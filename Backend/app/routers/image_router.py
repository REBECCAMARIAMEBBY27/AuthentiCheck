from fastapi import APIRouter, UploadFile, File
import shutil
import os
from app.services.image_service import predict_image

router = APIRouter()

UPLOAD_DIR = "app/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/predict-image")
async def predict(file: UploadFile = File(...)):
    file_path = f"{UPLOAD_DIR}/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    label, confidence = predict_image(file_path)

    return {
        "prediction": label,
        "confidence": confidence
    }