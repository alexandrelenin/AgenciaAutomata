from fastapi import FastAPI, UploadFile, File
from transformers import pipeline
from PIL import Image
import torch
import io

app = FastAPI()

# Carrega pipeline multimodal (exemplo: CLIP)
try:
    clip_pipe = pipeline("zero-shot-image-classification", model="openai/clip-vit-base-patch16")
except Exception:
    clip_pipe = None

@app.post("/analyze_image/")
def analyze_image(file: UploadFile = File(...), labels: str = "imagem, gráfico, texto"):
    # Recebe imagem e analisa via CLIP
    image_bytes = file.file.read()
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    candidate_labels = [l.strip() for l in labels.split(",")]
    if clip_pipe:
        result = clip_pipe(image, candidate_labels)
    else:
        result = {"error": "Modelo CLIP não carregado"}
    return {"labels": candidate_labels, "result": result}
