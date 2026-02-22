from tensorflow.keras.applications import ResNet50
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os

# 🔹 CORRECT DATASET PATH
DATASET_PATH = "Backend/dataset/train"

# 🔹 Create save folder if not exists
if not os.path.exists("saved_models"):
    os.mkdir("saved_models")

# 🔹 Data augmentation
datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2,
    rotation_range=15,
    zoom_range=0.1,
    horizontal_flip=True
)

train_data = datagen.flow_from_directory(
    DATASET_PATH,
    target_size=(224,224),
    batch_size=32,
    class_mode="binary",
    subset="training"
)

val_data = datagen.flow_from_directory(
    DATASET_PATH,
    target_size=(224,224),
    batch_size=32,
    class_mode="binary",
    subset="validation"
)

# 🔹 Load ResNet50
base_model = ResNet50(
    weights="imagenet",
    include_top=False,
    input_shape=(224,224,3)
)

# 🔹 Freeze base layers
for layer in base_model.layers:
    layer.trainable = False

# 🔹 Build model
model = Sequential([
    base_model,
    Flatten(),
    Dense(256, activation="relu"),
    Dropout(0.5),
    Dense(1, activation="sigmoid")
])

model.compile(
    optimizer="adam",
    loss="binary_crossentropy",
    metrics=["accuracy"]
)

print("🚀 Training started...")

model.fit(
    train_data,
    validation_data=val_data,
    epochs=20
)

model.save("saved_models/image_model.h5")

print("✅ Model saved as saved_models/image_model.h5")