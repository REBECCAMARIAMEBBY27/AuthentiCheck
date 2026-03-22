import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

MODEL_PATH = "roberta-base-openai-detector" # <-- your saved model folder

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)

model.eval()

def transformer_predict(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)

    with torch.no_grad():
        outputs = model(**inputs)

    probs = torch.softmax(outputs.logits, dim=1)[0]

    return float(probs[1] ** 1.2)