import os
import openai
import whisper
import chromadb
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# --- Configuração Inicial ---
openai.api_key = os.getenv("OPENAI_API_KEY")

# Inicializa modelos (pode ser pesado, idealmente carregar uma vez)
print("Carregando modelo de embeddings...")
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
print("Modelo de embeddings carregado.")

# Conexão com ChromaDB
CHROMA_HOST = os.getenv("CHROMA_HOST", "chromadb")
chroma_client = chromadb.HttpClient(host=CHROMA_HOST, port=8000)
collection = chroma_client.get_or_create_collection(name="media_content")


def transcribe_audio(file_path):
    """Transcreve um arquivo de áudio/vídeo usando Whisper."""
    print(f"Carregando modelo Whisper para transcrever {file_path}...")
    # 'base' é um modelo rápido. Para maior precisão, use 'medium' ou 'large'.
    whisper_model = whisper.load_model("base") 
    print("Modelo Whisper carregado. Iniciando transcrição...")
    result = whisper_model.transcribe(file_path, fp16=False)
    print("Transcrição concluída.")
    return result['text'] # Retorna o texto completo por enquanto

def get_insights_from_text(text):
    """Usa um LLM para extrair insights, resumos e potenciais virais."""
    # (IMPLEMENTAÇÃO FUTURA)
    # Aqui você faria uma chamada para a API da OpenAI (GPT-4o) ou um LLM local
    # com um prompt estruturado para analisar o texto.
    # Por agora, vamos retornar o próprio texto como insight.
    print("Gerando insights (simulado)...")
    return {
        "summary": text[:200] + "...", # Simula um resumo
        "viral_potential": "Médio",
        "key_topics": ["simulado1", "simulado2"]
    }

def process_media_file(file_path):
    """Função principal que orquestra a análise de um arquivo."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Arquivo não encontrado em {file_path}")

    # Passo 1: Transcrição (se for áudio/vídeo)
    # Simplificação: assumindo que todo arquivo é de áudio/vídeo por enquanto
    transcribed_text = transcribe_audio(file_path)

    # Passo 2: Análise e extração de insights
    insights = get_insights_from_text(transcribed_text)

    # Passo 3: Geração de Embeddings
    print("Gerando embeddings...")
    embedding = embedding_model.encode(transcribed_text).tolist()

    # Passo 4: Armazenamento no ChromaDB
    print("Armazenando no ChromaDB...")
    file_name = os.path.basename(file_path)
    # O ID do documento precisa ser único
    doc_id = f"{file_name}-{hash(transcribed_text)}" 
    
    collection.add(
        documents=[transcribed_text],
        metadatas=[{
            "source_file": file_name,
            "timestamp": "0:00-0:30", # Simulado - idealmente viria dos segmentos do Whisper
            "summary": insights["summary"],
            "viral_potential": insights["viral_potential"]
        }],
        ids=[doc_id]
    )

    return {"status": "success", "doc_id": doc_id}

# Arquivos __init__.py podem ficar em branco
# Crie-os em 'app/src/` e `app/src/processing/`