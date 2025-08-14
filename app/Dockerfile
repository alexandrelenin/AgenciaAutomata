# Use uma imagem Python oficial como base
FROM python:3.11-slim

# Defina o diretório de trabalho no container
WORKDIR /workspace

# Copie o arquivo de dependências primeiro para aproveitar o cache do Docker
COPY ./requirements.txt .

# Instale as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copie o resto do código do aplicativo para o diretório de trabalho
COPY . .

# A porta que o Streamlit irá expor
EXPOSE 8501

# O comando para iniciar o app será fornecido pelo docker-compose