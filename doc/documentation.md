# Documentação do Projeto: AgenciaAutomata
**Versão:** 1.0
**Data:** 13 de Agosto de 2025
**Autor/Proprietário:** [Seu Nome/Nome da Agência]

## 1. Visão Geral do Projeto

O **AgenciaAutomata** é um sistema de automação e inteligência de conteúdo projetado para transformar o acervo de mídias de uma agência de marketing digital (vídeos, áudios, textos) em um ativo pesquisável e pronto para a geração de novas mídias.

O objetivo final é reduzir drasticamente o tempo de produção de conteúdo, aumentar a qualidade e a relevância das postagens e maximizar o aproveitamento de materiais já existentes.

## 2. O Problema

Agências de marketing digital frequentemente acumulam um vasto volume de conteúdo bruto para seus clientes (horas de vídeo, transcrições, artigos, fotos). Esse material é subutilizado devido à dificuldade e ao tempo necessários para:
* Revisar e encontrar trechos relevantes.
* Identificar ideias com potencial viral.
* Adaptar um conteúdo de formato longo para formatos curtos (Reels, Carrosséis, etc.).
* Manter a consistência da mensagem em diferentes plataformas.

Esse processo manual é lento, caro e ineficiente.

## 3. A Solução Proposta

O AgenciaAutomata resolve este problema através de um pipeline automatizado que:
1.  **Ingere** automaticamente novos conteúdos de um drive virtual.
2.  **Analisa** o conteúdo usando IA para transcrever áudios, identificar tópicos, analisar sentimentos e detectar trechos de alto impacto.
3.  **Cataloga** o conteúdo de forma inteligente em um banco de dados vetorial, permitindo buscas por significado (busca semântica), não apenas por palavras-chave.
4.  **Disponibiliza** uma interface simples (Dashboard) onde a equipe pode pesquisar o acervo com linguagem natural (ex: "encontrar clipes onde o cliente parece feliz ao falar de sucesso") e acionar a geração de novas mídias.

## 4. Arquitetura do Sistema

O sistema é construído sobre uma arquitetura de microsserviços gerenciada pelo Docker, garantindo portabilidade e escalabilidade.

```mermaid
graph TD
    A[Drive com Conteúdo Bruto] -->|Novo Arquivo| B(N8N);
    B -->|Aciona Script de Análise| C{App Python};
    
    subgraph "App Python (Cérebro da IA)"
        C -->|1. Transcreve| D[Whisper];
        C -->|2. Analisa Texto| E[LLM: GPT-4o/Llama3];
        C -->|3. Vetoriza| F[SentenceTransformer];
    end
    
    C -->|4. Armazena| G[(ChromaDB)];
    
    subgraph "Interface do Usuário"
        H[Equipe de Marketing] <--> I{Streamlit Dashboard};
    end
    
    I -->|Busca Semântica no Acervo| G;
    G -->|Retorna Resultados| I;
    I -->|Aciona Geração de Conteúdo| B;