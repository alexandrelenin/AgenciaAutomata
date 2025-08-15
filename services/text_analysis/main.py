
from fastapi import FastAPI
from pydantic import BaseModel
import os
import openai
import requests
from dotenv import load_dotenv


# Carrega variáveis do .env.keys
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../../.env.keys'))

app = FastAPI()

class TextRequest(BaseModel):
    text: str
    provider: str = os.getenv("TEXT_ANALYSIS_PROVIDER", "openai")

# Adapter para OpenAI
def openai_adapter(text):
    openai.api_key = os.getenv("OPENAI_API_KEY", "")
    prompt = f"Resuma o texto, avalie potencial viral e extraia ideias principais:\n{text}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message["content"]

# Adapter para Hugging Face (exemplo usando modelo de resumo)
def huggingface_adapter(text):
    hf_token = os.getenv("HF_API_TOKEN", "")
    api_url = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
    headers = {"Authorization": f"Bearer {hf_token}"}
    payload = {"inputs": text}
    response = requests.post(api_url, headers=headers, json=payload)
    if response.status_code == 200:
        result = response.json()
        if isinstance(result, list) and "summary_text" in result[0]:
            return result[0]["summary_text"]
        return str(result)
    return f"Erro HuggingFace: {response.text}"


# Adapter para Google Cloud Natural Language
def google_adapter(text):
    try:
        from google.cloud import language_v1
        client = language_v1.LanguageServiceClient()
        document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
        response = client.analyze_sentiment(request={'document': document})
        sentiment = response.document_sentiment
        return f"Score: {sentiment.score}, Magnitude: {sentiment.magnitude}"
    except Exception as e:
        return f"Erro Google: {str(e)}"

# Adapter para IBM Watson NLU
def ibm_adapter(text):
    try:
        from ibm_watson import NaturalLanguageUnderstandingV1
        from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
        ibm_apikey = os.getenv("IBM_API_KEY", "")
        ibm_url = os.getenv("IBM_URL", "")
        authenticator = IAMAuthenticator(ibm_apikey)
        nlu = NaturalLanguageUnderstandingV1(version='2022-04-07', authenticator=authenticator)
        nlu.set_service_url(ibm_url)
        response = nlu.analyze(text=text, features={"sentiment": {}, "keywords": {}}).get_result()
        return str(response)
    except Exception as e:
        return f"Erro IBM: {str(e)}"

# Adapter para Cohere
def cohere_adapter(text):
    try:
        import cohere
        cohere_api_key = os.getenv("COHERE_API_KEY", "")
        co = cohere.Client(cohere_api_key)
        response = co.summarize(text=text)
        return response.summary if hasattr(response, 'summary') else str(response)
    except Exception as e:
        return f"Erro Cohere: {str(e)}"

# Adapter para outros provedores (stub)
def stub_adapter(text):
    return "Provedor não implementado."

def analyze_text_adapter(text, provider):
    if provider == "openai":
        return openai_adapter(text)
    elif provider == "huggingface":
        return huggingface_adapter(text)
    elif provider == "google":
        return google_adapter(text)
    elif provider == "ibm":
        return ibm_adapter(text)
    elif provider == "cohere":
        return cohere_adapter(text)
    else:
        return stub_adapter(text)

@app.post("/analyze/")
def analyze_text(req: TextRequest):
    result = analyze_text_adapter(req.text, req.provider)
    return {"analysis": result, "provider": req.provider}
