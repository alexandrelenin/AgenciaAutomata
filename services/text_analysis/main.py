from fastapi import FastAPI
from pydantic import BaseModel
import openai
import os

app = FastAPI()
openai.api_key = os.getenv("OPENAI_API_KEY", "")

class TextRequest(BaseModel):
    text: str

@app.post("/analyze/")
def analyze_text(req: TextRequest):
    prompt = f"Resuma o texto, avalie potencial viral e extraia ideias principais:\n{req.text}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return {"analysis": response.choices[0].message["content"]}
