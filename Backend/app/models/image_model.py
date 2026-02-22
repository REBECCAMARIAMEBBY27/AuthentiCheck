from tensorflow.keras.models import load_model

MODEL_PATH = "saved_models/image_model.h5"

def load_image_model():
    return load_model(MODEL_PATH)

def predict_image_prob(model, img):
    pred = model.predict(img)
    return pred[0][0]
