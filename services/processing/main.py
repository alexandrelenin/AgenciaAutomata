
from fastapi import FastAPI, UploadFile, File
import requests
import mimetypes
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

MICROSERVICES = {
    "audio": os.getenv("TRANSCRIPTION_URL", "http://localhost:5001/transcribe/"),
    "video": os.getenv("VIDEO_CUT_URL", "http://localhost:5005/cut_video/"),
    "text": os.getenv("TEXT_ANALYSIS_URL", "http://localhost:5002/analyze/"),
    "image": os.getenv("MULTIMODAL_URL", "http://localhost:5006/analyze_image/")
}

@app.post("/process/")
def process_file(file: UploadFile = File(...)):
    # Detecta tipo de arquivo
    mime_type, _ = mimetypes.guess_type(file.filename)
    if mime_type is None:
        return {"error": "Tipo de arquivo não detectado"}
    if mime_type.startswith("audio"):
        # Transcrição
        url = MICROSERVICES["audio"]
        files = {"file": (file.filename, file.file, file.content_type)}
        response = requests.post(url, files=files)
        result = response.json()
        # Encaminha texto para análise LLM
        text_url = MICROSERVICES["text"]
        text_payload = {"text": result.get("transcription", "")}
        llm_response = requests.post(text_url, json=text_payload)
        llm_result = llm_response.json()
        return {
            "transcription": result.get("transcription", ""),
            "segments": result.get("segments", []),
            "llm_analysis": llm_result
        }
    elif mime_type.startswith("video"):
        url = MICROSERVICES["video"]
        files = {"file": (file.filename, file.file, file.content_type)}
        response = requests.post(url, files=files)
        return response.json()
    elif mime_type.startswith("image"):
        url = MICROSERVICES["image"]
        files = {"file": (file.filename, file.file, file.content_type)}
        response = requests.post(url, files=files)
        return response.json()
    elif mime_type.startswith("text"):
        url = MICROSERVICES["text"]
        files = {"file": (file.filename, file.file, file.content_type)}
        response = requests.post(url, files=files)
        return response.json()
    else:
        return {"error": f"Tipo não suportado: {mime_type}"}
