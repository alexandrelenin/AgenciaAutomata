# AgenciaAutomata - Motor de Conteúdo IA

Este projeto é a implementação da arquitetura para um motor de conteúdo semiautomatizado para agências de marketing digital. O objetivo é ingerir, analisar, catalogar e transformar um grande acervo de mídias (vídeos, textos, áudios) em conteúdo pronto para publicação em diversas plataformas.

## Arquitetura

O sistema opera com uma arquitetura de microsserviços orquestrada exclusivamente via Docker Compose (use sempre docker compose, sem hífen). Todos os serviços, incluindo o microserviço de análise de texto, devem ser iniciados e testados via Docker, nunca manualmente com uvicorn.

Fluxo recomendado:

1.  **N8N:** O orquestrador de workflows. Ele monitora fontes de dados (ex: Google Drive) e aciona os scripts de processamento.
2.  **App (Python/Streamlit):** O cérebro do sistema. Contém:
    * Scripts de processamento para transcrição, análise por IA e vetorização.
    * Uma interface de usuário (dashboard) construída com Streamlit para busca semântica e acionamento de geração de conteúdo.
3.  **ChromaDB:** Um banco de dados vetorial para armazenar e permitir a busca por similaridade semântica no conteúdo analisado.

No diretório app, execute:
docker compose up

Para subir apenas um microserviço (exemplo: análise de texto):
docker compose up text-analysis-service

Nunca execute uvicorn manualmente. Todas as dependências e comandos já estão definidos nos Dockerfiles e no docker-compose.yml.

```mermaid
graph TD
    A[Drive com Conteúdo Bruto] -->|Novo Arquivo| B(N8N);
    B -->|Aciona Script| C{App: process_new_file.py};
    C -->|1. Transcreve| D[Whisper];
    C -->|2. Analisa| E[LLM: GPT-4o/Llama3];
    C -->|3. Vetoriza| F[SentenceTransformer];
    C -->|4. Armazena| G[(ChromaDB)];
    
    subgraph "Dashboard de Interação"
        H[Usuário] <--> I{Streamlit Dashboard};
    end
    
    I -->|Busca Semântica| G;
    G -->|Retorna Resultados| I;
    I -->|Aciona Geração| B;