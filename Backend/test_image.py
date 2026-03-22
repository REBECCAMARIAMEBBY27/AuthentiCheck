import os
from app.services.image_service import predict_image

image_path = "test.jpg"

print("PATH:", image_path)
print("EXISTS:", os.path.exists(image_path))

label, confidence = predict_image(image_path)

print("Prediction:", label)
print("Confidence:", confidence)