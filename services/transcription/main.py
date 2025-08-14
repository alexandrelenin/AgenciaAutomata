from fastapi import FastAPI, UploadFile, File
import whisper
import tempfile
import os

app = FastAPI()


@app.post("/transcribe/")
def transcribe_audio(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp:
        tmp.write(file.file.read())
        tmp_path = tmp.name
    model = whisper.load_model("base")
    result = model.transcribe(tmp_path, fp16=False)
    os.remove(tmp_path)
    # Segmentação: cada segmento tem 'text', 'start', 'end'
    segments = []
    for seg in result.get("segments", []):
        segments.append({
            "text": seg["text"],
            "start": seg["start"],
            "end": seg["end"]
        })
    return {
        "transcription": result["text"],
        "segments": segments
    }
