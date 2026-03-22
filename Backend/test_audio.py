import os
from app.services.audio_service import predict_audio

# 🔍 check if file exists
print("EXISTS:", os.path.exists("test.wav"))

audio_path = "test.wav"

label, conf = predict_audio(audio_path)

print("Audio:", label, conf)