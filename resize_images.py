import os
from PIL import Image

folders = ["Backend/dataset/train/real", "Backend/dataset/train/ai"]
SIZE = (224,224)

for folder in folders:
    for f in os.listdir(folder):
        path = os.path.join(folder, f)
        try:
            img = Image.open(path).convert("RGB")
            img = img.resize(SIZE)
            img.save(path)
        except:
            pass

print("Resize complete")