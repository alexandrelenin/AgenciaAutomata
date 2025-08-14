from fastapi import FastAPI, UploadFile, File
import requests
import mimetypes

app = FastAPI()

MICROSERVICES = {
    "audio": "http://transcription-service:5001/transcribe/",
    "video": "http://video-cut-service:5005/cut_video/",
    "text": "http://text-analysis-service:5002/analyze/",
    "image": "http://multimodal-service:5006/analyze_image/"
}

@app.post("/process/")
def process_file(file: UploadFile = File(...)):
    # Detecta tipo de arquivo
    mime_type, _ = mimetypes.guess_type(file.filename)
    if mime_type is None:
        return {"error": "Tipo de arquivo não detectado"}
    if mime_type.startswith("audio"):
        url = MICROSERVICES["audio"]
    elif mime_type.startswith("video"):
        url = MICROSERVICES["video"]
    elif mime_type.startswith("image"):
        url = MICROSERVICES["image"]
    elif mime_type.startswith("text"):
        url = MICROSERVICES["text"]
    else:
        return {"error": f"Tipo não suportado: {mime_type}"}
    # Encaminha para microserviço
    files = {"file": (file.filename, file.file, file.content_type)}
    response = requests.post(url, files=files)
    return response.json()
