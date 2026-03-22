# AuthentiCheck — AI Media Authenticity Checker

A small full-stack demo that scores whether **text**, **images**, or **audio** look more **human-generated** or **AI-generated**. The backend is a FastAPI service; the UI is a static page with tabs for each modality.

## What it does

| Modality | Approach (high level) |
|----------|-------------------------|
| **Text** | Hugging Face `roberta-base-openai-detector` (PyTorch) for a transformer score; optional stylometric features (GPT‑2 perplexity, burstiness, entropy, etc.) are computed in `text_features.py`. The ensemble currently uses the transformer score (see `ensemble.py`). |
| **Image** | Two Keras models: one on the RGB image and one on an FFT magnitude view, averaged. Labels **AI Generated** vs **Human Generated** using a 0.5 threshold on the combined score. |
| **Audio** | The API’s `audio_service` returns a **fixed placeholder** result. A separate script `Backend/predict_audio.py` can load `audio_classifier.keras` / `audio_classifier.h5` for offline prediction (not wired into the live API yet). |

## Setup

1. **Create and activate a virtual environment** (from this folder):

   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Image models** — `Backend/app/services/image_service.py` expects:

   - `Backend/saved_models/image_model.h5`
   - `Backend/saved_models/fft_model.h5`

   These paths are gitignored. Train them with `train_image.py` / `Backend/train_fft_model.py` and your datasets, or place compatible `.h5` files there.

4. **First run (text)** — The RoBERTa detector and GPT‑2 (for perplexity in `text_features.py`) download from Hugging Face on first use. Ensure outbound network access.

## Run the backend

From the **Backend** directory (so imports like `app.main:app` resolve):

```bash
cd Backend
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

API docs: `http://127.0.0.1:8000/docs` (FastAPI automatic OpenAPI UI).

## Run the frontend

The UI is plain static files. Either open `frontend/index.html` in a browser (some browsers restrict `fetch` to file URLs) or serve the folder:

```bash
cd frontend
python -m http.server 5500
```

Then visit `http://127.0.0.1:5500`. The script calls **`http://127.0.0.1:8000/analyze`** — keep the API on port 8000 or update `script.js`.

## API

**`POST /analyze`** — `multipart/form-data` with **one** of:

- `text` — string (form field)
- `image` — file upload
- `audio` — file upload