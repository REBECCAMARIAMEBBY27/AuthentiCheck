import torch
import numpy as np
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import nltk
from scipy.stats import entropy
import textstat

nltk.download('punkt')

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load GPT2 for perplexity
gpt2_model = GPT2LMHeadModel.from_pretrained("gpt2").to(device)
gpt2_tokenizer = GPT2Tokenizer.from_pretrained("gpt2")


# 1️⃣ Perplexity
def calculate_perplexity(text):
    encodings = gpt2_tokenizer(text, return_tensors="pt").to(device)
    with torch.no_grad():
        outputs = gpt2_model(**encodings, labels=encodings["input_ids"])
    loss = outputs.loss
    return torch.exp(loss).item()


# 2️⃣ Burstiness
def calculate_burstiness(text):
    sentences = nltk.sent_tokenize(text)
    lengths = [len(s.split()) for s in sentences]
    if len(lengths) < 2:
        return 0
    return np.std(lengths) / np.mean(lengths)


# 3️⃣ Sentence Entropy
def calculate_entropy(text):
    tokens = text.split()
    probs = np.unique(tokens, return_counts=True)[1] / len(tokens)
    return entropy(probs)


# 4️⃣ Stylometric Features
def stylometric_features(text):
    return {
        "avg_word_length": np.mean([len(w) for w in text.split()]),
        "flesch_reading": textstat.flesch_reading_ease(text),
        "lexical_diversity": len(set(text.split())) / len(text.split())
    }


# 5️⃣ Repetition Score
def repetition_score(text):
    tokens = text.split()
    unique_ratio = len(set(tokens)) / len(tokens)
    return 1 - unique_ratio


# 6️⃣ Token Distribution Smoothness
def token_distribution(text):
    tokens = text.split()
    freq = np.unique(tokens, return_counts=True)[1]
    return np.var(freq)


def extract_all_features(text):
    stylometry = stylometric_features(text)

    features = [
        calculate_perplexity(text),
        calculate_burstiness(text),
        calculate_entropy(text),
        stylometry["avg_word_length"],
        stylometry["flesch_reading"],
        stylometry["lexical_diversity"],
        repetition_score(text),
        token_distribution(text)
    ]

    return np.array(features)