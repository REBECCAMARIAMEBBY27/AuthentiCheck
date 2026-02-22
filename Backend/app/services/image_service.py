import cv2
import numpy as np
from tensorflow.keras.models import load_model
import os

IMG_SIZE=224

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

image_model = load_model(os.path.join(BASE_DIR, "saved_models", "image_model.h5"))
fft_model = load_model(os.path.join(BASE_DIR, "saved_models", "fft_model.h5"))

def preprocess_image(path):
    img = cv2.imread(path)
    img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
    img = img / 255.0
    img = np.expand_dims(img, axis=0)
    return img

def preprocess_fft(path):
    gray = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    gray = cv2.resize(gray, (IMG_SIZE, IMG_SIZE))

    f = np.fft.fft2(gray)
    fshift = np.fft.fftshift(f)
    mag = np.log(np.abs(fshift) + 1)

    mag = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)
    mag = mag.astype(np.uint8)
    mag = cv2.cvtColor(mag, cv2.COLOR_GRAY2BGR)
    mag = mag / 255.0
    mag = np.expand_dims(mag, axis=0)

    return mag

def predict_image(path):
    img_input = preprocess_image(path)
    fft_input = preprocess_fft(path)

    p1 = image_model.predict(img_input)[0][0]
    p2 = fft_model.predict(fft_input)[0][0]

    final_score = (p1 + p2) / 2

    label = "AI Generated" if final_score > 0.5 else "Human Generated"
    confidence = round(float(final_score * 100), 2)

    return label, confidence