# Microserviço de Processamento (Orquestrador)

Endpoint: `/process/`

**Método:** POST

**Parâmetros:**
- `file`: Upload do arquivo (form-data)

**Funcionamento:**
- Detecta o tipo de arquivo (áudio, vídeo, texto, imagem) via mimetype.
- Encaminha o arquivo para o microserviço correspondente:
    - Áudio: Transcrição (Whisper)
    - Vídeo: Corte de vídeo (FFmpeg)
    - Imagem: Análise multimodal (CLIP)
    - Texto: Análise de texto (LLM)
- Retorna o resultado do microserviço chamado.

**Exemplo de uso (curl):**
```
curl -X POST "http://localhost:5007/process/" -F "file=@arquivo.ext"
```

**Observações:**
- O serviço espera que os microserviços estejam acessíveis via rede/Docker Compose.
- Para novos tipos, basta adicionar no dicionário `MICROSERVICES`.
