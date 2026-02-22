import os
from PIL import Image

folders = ["Backend/dataset/train/real", "Backend/dataset/train/ai"]

for folder in folders:
    removed = 0
    for f in os.listdir(folder):
        path = os.path.join(folder, f)
        try:
            img = Image.open(path)
            img.verify()
        except:
            os.remove(path)
            removed += 1
    print(folder, "removed", removed)