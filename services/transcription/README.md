# Microserviço de Transcrição (Whisper)

Endpoint: `/transcribe/`

**Método:** POST

**Parâmetros:**
- `file`: Upload do áudio/vídeo (form-data)

**Retorno:**
- `transcription`: Texto completo transcrito
- `segments`: Lista de segmentos/frases com timestamps
    - Cada segmento: `{ "text": ..., "start": ..., "end": ... }`

**Exemplo de uso (curl):**
```
curl -X POST "http://localhost:5001/transcribe/" -F "file=@audio.mp3"
```

**Observações:**
- Utiliza Whisper para transcrição e segmentação automática.
- Ideal para gerar cortes, carrosséis, ou análise detalhada por trecho.
