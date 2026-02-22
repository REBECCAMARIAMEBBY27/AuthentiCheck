from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.optimizers import Adam
import os

# ============================
# CONFIG
# ============================

DATASET_PATH = "fft_dataset"
IMG_SIZE = (224,224)
BATCH_SIZE = 16
EPOCHS = 10

# ============================
# DATA LOADER
# ============================

datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2
)

train_data = datagen.flow_from_directory(
    DATASET_PATH,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="binary",
    subset="training"
)

val_data = datagen.flow_from_directory(
    DATASET_PATH,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="binary",
    subset="validation"
)

# ============================
# BUILD FFT CNN
# ============================

model = Sequential([
    Conv2D(32,(3,3),activation="relu",input_shape=(224,224,3)),
    MaxPooling2D(),

    Conv2D(64,(3,3),activation="relu"),
    MaxPooling2D(),

    Conv2D(128,(3,3),activation="relu"),
    MaxPooling2D(),

    Flatten(),
    Dense(256,activation="relu"),
    Dropout(0.5),
    Dense(1,activation="sigmoid")
])

model.compile(
    optimizer=Adam(learning_rate=0.0001),
    loss="binary_crossentropy",
    metrics=["accuracy"]
)

print("🚀 Training FFT model...")

model.fit(
    train_data,
    validation_data=val_data,
    epochs=EPOCHS
)

model.save("saved_models/fft_model.h5")

print("✅ FFT model saved at saved_models/fft_model.h5")