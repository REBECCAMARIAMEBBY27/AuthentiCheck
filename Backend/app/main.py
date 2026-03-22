from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import os

from app.services.image_service import predict_image
from app.services.audio_service import predict_audio
from app.services.text_service import predict_text

app = FastAPI()

# ✅ CORS (important for frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# temp folder
os.makedirs("temp", exist_ok=True)


@app.post("/analyze")
async def analyze(
    image: UploadFile = File(None),
    audio: UploadFile = File(None),
    text: str = Form(None)
):

    # 🔹 IMAGE
    if image:
        path = f"temp/{image.filename}"
        with open(path, "wb") as f:
            f.write(await image.read())

        label, conf = predict_image(path)

    # 🔹 AUDIO
    elif audio:
        path = f"temp/{audio.filename}"
        with open(path, "wb") as f:
            f.write(await audio.read())

        label, conf = predict_audio(path)

    # 🔹 TEXT
    elif text:
        label, conf = predict_text(text)

    else:
        return {"error": "No input provided"}

    conf = round(conf, 2)

    return {
        "prediction": label,
        "confidence": conf
    }