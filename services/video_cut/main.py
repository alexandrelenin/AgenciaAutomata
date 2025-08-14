from fastapi import FastAPI, UploadFile, File, Form
import ffmpeg
import os
import uuid

app = FastAPI()

@app.post("/cut_video/")
def cut_video(file: UploadFile = File(...), start: float = Form(...), end: float = Form(...)):
    # Salva vídeo temporário
    temp_in = f"/tmp/{uuid.uuid4()}.mp4"
    temp_out = f"/tmp/{uuid.uuid4()}_cut.mp4"
    with open(temp_in, "wb") as f:
        f.write(file.file.read())
    # Executa corte com ffmpeg
    (
        ffmpeg
        .input(temp_in, ss=start, t=end-start)
        .output(temp_out, codec="copy")
        .run(overwrite_output=True)
    )
    # Retorna vídeo cortado
    with open(temp_out, "rb") as f:
        video_bytes = f.read()
    os.remove(temp_in)
    os.remove(temp_out)
    return {"filename": "cut.mp4", "file": video_bytes.hex()}
