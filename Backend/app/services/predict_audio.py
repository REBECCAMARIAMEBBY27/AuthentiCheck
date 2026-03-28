import os
import sys
import warnings
import logging
import tempfile
import subprocess

# Must be set BEFORE tensorflow imports
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

warnings.filterwarnings('ignore')
logging.getLogger('tensorflow').setLevel(logging.ERROR)
logging.getLogger('absl').setLevel(logging.ERROR)

import numpy as np
import librosa
import tensorflow as tf
import imageio_ffmpeg

SAMPLE_RATE = 22050
DURATION = 3
N_MFCC = 40

# Load model
if os.path.exists("audio_classifier.keras"):
    model = tf.keras.models.load_model("audio_classifier.keras")
else:
    model = tf.keras.models.load_model("audio_classifier.h5")


def predict_audio(file_path):
    # Convert any format to wav
    file_ext = os.path.splitext(file_path)[1].lower()

    if file_ext != '.wav':
        ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
        tmp = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
        tmp.close()

        subprocess.run(
            [ffmpeg, '-y', '-i', file_path,
             '-ar', '22050', '-ac', '1', tmp.name],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        audio, sr = librosa.load(tmp.name, sr=SAMPLE_RATE, duration=DURATION)
        os.remove(tmp.name)

    else:
        audio, sr = librosa.load(file_path, sr=SAMPLE_RATE, duration=DURATION)

    # Pad / trim
    target_len = SAMPLE_RATE * DURATION
    if len(audio) < target_len:
        audio = np.pad(audio, (0, target_len - len(audio)))
    else:
        audio = audio[:target_len]

    # Feature extraction
    mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=N_MFCC)

    mel = librosa.power_to_db(
        librosa.feature.melspectrogram(y=audio, sr=sr, n_mels=40),
        ref=np.max
    )

    zcr = librosa.feature.zero_crossing_rate(audio)

    features = np.vstack([mfcc, mel, zcr])
    features = features[np.newaxis, ..., np.newaxis]

    # Normalize
    mean = features.mean(axis=(1, 2, 3), keepdims=True)
    std = features.std(axis=(1, 2, 3), keepdims=True) + 1e-6
    features = (features - mean) / std

    # Predict
    prob = model.predict(features, verbose=0)[0][0]
    print("PROB:", prob)

    ai_prob = round((1 - prob) * 100, 2)
    hum_prob = round(prob * 100, 2)

    # ✅ FIXED INDENTATION
    if hum_prob >= ai_prob:
        return "Human Generated", float(hum_prob / 100)
    else:
        return "AI Generated", float(ai_prob / 100)


# Optional CLI test
if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else None
    if path:
        label, conf = predict_audio(path)
        print("\n--- RESULT ---")
        print(f"Label      : {label}")
        print(f"Confidence : {conf * 100:.2f}%")
        print("--------------\n")
    else:
        print("Usage: python predict_audio.py path/to/audio.wav")