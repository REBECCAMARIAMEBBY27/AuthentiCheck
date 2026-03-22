import numpy as np
from app.text_features import extract_all_features
from app.text_classifier import transformer_predict

def normalize_perplexity(p):
    # lower perplexity = more AI-like
    return 1 / (1 + np.exp((p - 50) / 10))

def normalize_burstiness(b):
    # lower burstiness = more AI-like
    return 1 / (1 + np.exp((b - 0.5) / 0.1))

def ensemble_predict(transformer_score, features):
    # use features directly
    final_score = transformer_score  # or your logic
    return final_score

    perplexity = features[0]
    burstiness = features[1]
    entropy_value = features[2]  # this is your coherence replacement
    transformer_score = transformer_predict(text)

    perplexity_score = normalize_perplexity(perplexity)
    burstiness_score = normalize_burstiness(burstiness)

    final_score = (
    0.8 * transformer_score +
    0.1 * perplexity_score +
    0.1 * burstiness_score
)

    return {
        "AI_probability": round(float(final_score), 4),
        "perplexity": float(perplexity),
        "burstiness": float(burstiness),
        "entropy": float(entropy_value)
    }