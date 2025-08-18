
from fastapi import FastAPI, UploadFile, File
import requests
import mimetypes
import os
import uuid
import hashlib
from datetime import datetime
from dotenv import load_dotenv
import chromadb

load_dotenv()

app = FastAPI()

# Configuração ChromaDB
CHROMA_HOST = os.getenv("CHROMA_HOST", "chromadb")
CHROMA_PORT = int(os.getenv("CHROMA_PORT", "8000"))
chroma_client = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)
collection = chroma_client.get_or_create_collection(name="media_content")

MICROSERVICES = {
    # Use nomes dos serviços no Docker network por padrão
    "audio": os.getenv("TRANSCRIPTION_URL", "http://transcription-service:5001/transcribe/"),
    "video": os.getenv("VIDEO_CUT_URL", "http://video-cut-service:5005/cut_video/"),
    "text": os.getenv("TEXT_ANALYSIS_URL", "http://text-analysis-service:5002/analyze/"),
    "image": os.getenv("MULTIMODAL_URL", "http://multimodal-service:5006/analyze_image/")
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

        # Gera embedding via microserviço
        embedding_url = os.getenv("EMBEDDING_URL", "http://embedding-service:5003/embed/")
        embedding_payload = {"text": result.get("transcription", "")}
        embedding_response = requests.post(embedding_url, json=embedding_payload)
        embedding_result = embedding_response.json()

        # Armazena no ChromaDB
        transcription_text = result.get("transcription", "")
        embedding_vector = embedding_result.get("embedding", [])

        # Gera ID único baseado no conteúdo
        content_hash = hashlib.md5(transcription_text.encode()).hexdigest()
        doc_id = f"{file.filename}_{content_hash}_{int(datetime.now().timestamp())}"

        # Metadados completos
        metadata = {
            "source_file": file.filename,
            "file_type": "audio",
            "timestamp": datetime.now().isoformat(),
            "analysis": str(llm_result.get("analysis", "")),
            "provider": llm_result.get("provider", "unknown"),
            "segments_count": len(result.get("segments", []))
        }

        # Salva no ChromaDB
        try:
            collection.add(
                documents=[transcription_text],
                embeddings=[embedding_vector],
                metadatas=[metadata],
                ids=[doc_id]
            )
        except Exception as e:
            print(f"Erro ao salvar no ChromaDB: {e}")

        return {
            "transcription": result.get("transcription", ""),
            "segments": result.get("segments", []),
            "llm_analysis": llm_result,
            "embedding": embedding_result.get("embedding", []),
            "doc_id": doc_id,
            "stored_in_chromadb": True
        }

    if mime_type.startswith("video"):
        url = MICROSERVICES["video"]
        files = {"file": (file.filename, file.file, file.content_type)}
        response = requests.post(url, files=files)
        return response.json()

    if mime_type.startswith("image"):
        url = MICROSERVICES["image"]
        files = {"file": (file.filename, file.file, file.content_type)}
        response = requests.post(url, files=files)
        return response.json()

    if mime_type.startswith("text"):
        url = MICROSERVICES["text"]
        files = {"file": (file.filename, file.file, file.content_type)}
        response = requests.post(url, files=files)
        return response.json()

    return {"error": f"Tipo não suportado: {mime_type}"}
