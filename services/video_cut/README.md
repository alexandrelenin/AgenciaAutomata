# Microserviço de Corte de Vídeo

Endpoint: `/cut_video/`

**Método:** POST

**Parâmetros:**
- `file`: Upload do vídeo (form-data)
- `start`: Timestamp inicial (segundos, float)
- `end`: Timestamp final (segundos, float)

**Retorno:**
- `filename`: Nome do arquivo cortado
- `file`: Arquivo cortado em hex

**Exemplo de uso (curl):**
```
curl -X POST "http://localhost:5005/cut_video/" \
  -F "file=@input.mp4" \
  -F "start=10" \
  -F "end=20"
```
