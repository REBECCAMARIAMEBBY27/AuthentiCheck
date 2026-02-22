import cv2
import numpy as np
import os

# ✅ CORRECT PATHS
INPUT_PATH = "dataset/train"
OUTPUT_PATH = "fft_dataset"

def save_fft(img_path, save_path):
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        return
    
    img = cv2.resize(img, (224,224))

    f = np.fft.fft2(img)
    fshift = np.fft.fftshift(f)
    magnitude = np.log(np.abs(fshift) + 1)

    magnitude = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX)
    magnitude = magnitude.astype(np.uint8)

    cv2.imwrite(save_path, magnitude)

# Create output folders
for cls in ["real", "ai"]:
    os.makedirs(f"{OUTPUT_PATH}/{cls}", exist_ok=True)

# Convert images
for cls in ["real", "ai"]:
    files = os.listdir(f"{INPUT_PATH}/{cls}")
    print(f"Processing {len(files)} {cls} images")

    for file in files:
        src = f"{INPUT_PATH}/{cls}/{file}"
        dst = f"{OUTPUT_PATH}/{cls}/{file}"
        save_fft(src, dst)

print("✅ FFT images generated successfully!")