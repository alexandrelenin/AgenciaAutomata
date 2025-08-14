from fastapi import FastAPI, UploadFile, File, Form
from pydantic import BaseModel
from typing import List
from PIL import Image, ImageDraw, ImageFont
import openai
import io
import os

app = FastAPI()

# Roteiro via LLM
class CarouselRequest(BaseModel):
    topic: str
    n_slides: int = 5

class CarouselResponse(BaseModel):
    slides: List[str]
    images: List[str]  # base64 encoded

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
openai.api_key = OPENAI_API_KEY

@app.post("/generate_carousel", response_model=CarouselResponse)
def generate_carousel(req: CarouselRequest):
    # 1. Gerar roteiro dos slides via LLM
    prompt = f"Crie um roteiro para um carrossel de Instagram sobre '{req.topic}' com {req.n_slides} slides. Cada slide deve ser uma frase curta e impactante."
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    roteiro = response.choices[0].message['content'].split('\n')
    slides = [s for s in roteiro if s.strip()][:req.n_slides]

    # 2. Gerar imagens simples (mock) com Pillow
    images = []
    for idx, text in enumerate(slides):
        img = Image.new('RGB', (800, 800), color=(255, 255, 255))
        d = ImageDraw.Draw(img)
        font = ImageFont.load_default()
        d.text((50, 350), text, fill=(0, 0, 0), font=font)
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        images.append(buf.getvalue().hex())  # hex para simplificar

    return CarouselResponse(slides=slides, images=images)

@app.post("/montar_carrossel/")
def montar_carrossel(files: List[UploadFile] = File(...)):
    # Recebe imagens e monta carrossel (zip)
    from zipfile import ZipFile
    buf = io.BytesIO()
    with ZipFile(buf, 'w') as zipf:
        for idx, file in enumerate(files):
            content = file.file.read()
            zipf.writestr(f"slide_{idx+1}.png", content)
    buf.seek(0)
    return {
        "filename": "carousel.zip",
        "file": buf.getvalue().hex()
    }
