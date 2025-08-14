# Microserviço de Análise Multimodal

Endpoint: `/analyze_image/`

**Método:** POST

**Parâmetros:**
- `file`: Upload da imagem (form-data)
- `labels`: Lista de labels para classificação (string separada por vírgula, opcional)

**Retorno:**
- `labels`: Labels fornecidos
- `result`: Classificação zero-shot (CLIP)

**Exemplo de uso (curl):**
```
curl -X POST "http://localhost:5006/analyze_image/" \
  -F "file=@imagem.png" \
  -F "labels=imagem, gráfico, texto"
```
