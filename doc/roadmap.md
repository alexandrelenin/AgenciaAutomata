# Roadmap de Implementação - AgenciaAutomata (Componentizado)

## Fase 0: Fundação e Infraestrutura
- [x] Dockerfile e docker-compose para todos os serviços (N8N, ChromaDB, App Python).
- [x] Estrutura de pastas e arquivos.
- [x] Subir containers e validar acesso aos serviços (N8N, ChromaDB, App Python/Streamlit).
- [x] Planejar cada etapa crítica como um microserviço independente:
    - Microserviço de Transcrição (Whisper)
    - Microserviço de Análise de Texto (LLM)
    - Microserviço de Vetorização (Embeddings)
    - Microserviço de Corte de Vídeo (FFmpeg)
    - Microserviço de Geração de Carrossel (LLM + Imagem)
    - Microserviço de Análise Multimodal (Imagem)

## Fase 1: MVP - Ingestão e Análise
- [ ] Workflow N8N: trigger para novo arquivo no Drive, download e chamada do microserviço de processamento.
- [ ] Microserviço de Processamento:
    - [ ] Detectar tipo de arquivo (áudio, vídeo, texto, imagem).
    - [ ] Transcrever áudio/vídeo (Whisper API/local) como serviço separado.
    - [ ] Dividir transcrição em segmentos/timestamps.
    - [ ] Analisar texto com LLM (API/local) como serviço separado.
    - [ ] Gerar embeddings e salvar no ChromaDB (serviço dedicado).
    - [ ] Para imagens: microserviço de análise multimodal e embeddings.
- [ ] Dashboard Streamlit desacoplado, comunicando-se via API com os microserviços.

## Fase 2: Geração de Conteúdo e Interface Interativa
- [ ] Dashboard: seleção de trechos, checkboxes e botões de ação.
- [ ] Integração com N8N via webhooks para acionar microserviços de geração de artigos, clipes, carrosséis.
- [ ] Microserviço para cortes de vídeo (FFmpeg) usando timestamps.
- [ ] Microserviço para geração de artigos via LLM.
- [ ] Microserviço para geração de carrosséis: roteiro (LLM), imagens (API/local), montagem (Pillow).

## Fase 3: Otimização e Expansão
- [ ] Migrar para modelos locais (Whisper, Llama 3 via Ollama) em microserviços dedicados.
- [ ] Otimizar segmentação automática de transcrições.
- [ ] Suporte completo a análise multimodal (imagens) como microserviço.
- [ ] Implementar logging robusto e monitoramento (Grafana) para cada microserviço.
- [ ] Rotinas de backup para volumes dos serviços.

## Fase 4: Manutenção e Melhoria Contínua
- [ ] Refatoração e otimização de código.
- [ ] Testes unitários e integração contínua para cada microserviço.
- [ ] Evolução da interface e novas funcionalidades conforme feedback dos usuários.

---

## Sugestões para Componentização

- Separe cada etapa crítica do pipeline em microserviços independentes, cada um com seu Dockerfile e API/CLI.
- O dashboard deve consumir APIs dos microserviços, nunca acessar diretamente o backend.
- O N8N deve orquestrar o fluxo entre microserviços, facilitando manutenção e expansão.
- Documente as APIs e fluxos para facilitar integração e deploy.
- Considere usar ferramentas como FastAPI para expor os microserviços Python.