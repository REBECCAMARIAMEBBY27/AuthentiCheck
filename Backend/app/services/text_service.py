from app.text_classifier import transformer_predict
from app.text_features import extract_all_features
from app.ensemble import ensemble_predict

def predict_text(text):
    transformer_score = transformer_predict(text)
    features = extract_all_features(text)

    final_score = ensemble_predict(transformer_score, features)

    confidence = float(final_score) * 100
    confidence = round(confidence, 2)

    label = "AI Generated" if confidence > 50 else "Human Generated"

    return label, confidence