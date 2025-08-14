import streamlit as st
import chromadb
import os

# --- Configuração da Página ---
st.set_page_config(page_title="AgenciaAutomata Dashboard", layout="wide")
st.title("🤖 Motor de Busca de Conteúdo IA")
st.write("Busque no acervo de conteúdo usando linguagem natural.")

# --- Conexão com o ChromaDB ---
# O nome 'chromadb' é o nome do serviço no docker-compose.yml
CHROMA_HOST = os.getenv("CHROMA_HOST", "chromadb") 
try:
    chroma_client = chromadb.HttpClient(host=CHROMA_HOST, port=8000)
    # Ping para verificar a conexão
    chroma_client.heartbeat() 
    st.sidebar.success("Conectado ao ChromaDB!")
    # Tenta pegar a coleção. Se não existir, pode ser criada pelo script de processamento.
    collection = chroma_client.get_or_create_collection(name="media_content")
except Exception as e:
    st.sidebar.error(f"Não foi possível conectar ao ChromaDB: {e}")
    st.error("A conexão com o banco de dados vetorial falhou. Verifique se os serviços estão rodando.")
    collection = None

# --- Interface de Busca ---
if collection:
    search_query = st.text_input(
        "O que você está buscando?", 
        placeholder="Ex: trechos de vídeo sobre superar desafios"
    )

    if st.button("Buscar Conteúdo"):
        if search_query:
            with st.spinner("Buscando no acervo..."):
                results = collection.query(
                    query_texts=[search_query],
                    n_results=5,
                    include=["metadatas", "documents"]
                )
                
                st.subheader("Resultados da Busca:")

                if not results or not results.get('ids')[0]:
                    st.warning("Nenhum resultado encontrado para sua busca.")
                else:
                    for i, doc_id in enumerate(results['ids'][0]):
                        doc_text = results['documents'][0][i]
                        metadata = results['metadatas'][0][i]
                        
                        with st.container(border=True):
                            st.write(f"**Fonte:** `{metadata.get('source_file', 'N/A')}`")
                            st.write(f"**Timestamp:** `{metadata.get('timestamp', 'N/A')}`")
                            st.info(f"**Trecho:** {doc_text}")
        else:
            st.warning("Por favor, digite algo para buscar.")