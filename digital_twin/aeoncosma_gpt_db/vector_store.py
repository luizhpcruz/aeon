"""
LangChain Vector Store Manager
==============================
Sistema de embeddings e recuperação de contexto com LangChain
"""

import os
import json
from typing import List, Dict, Any, Optional
from datetime import datetime

# LangChain imports
from langchain_community.embeddings import OpenAIEmbeddings, HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain.memory import ConversationBufferWindowMemory

# ChromaDB for vector storage
import chromadb
from chromadb.config import Settings

class AEONCOSMAVectorStore:
    """Sistema de vector store para contexto AEONCOSMA - 100% GRATUITO"""
    
    def __init__(self, openai_api_key: str = None, persist_directory: str = "./data/chroma_db"):
        self.openai_api_key = openai_api_key
        self.persist_directory = persist_directory
        
        # Configurar embeddings (LOCAL GRATUITO por padrão)
        if openai_api_key:
            self.embeddings = OpenAIEmbeddings(
                openai_api_key=openai_api_key,
                model="text-embedding-ada-002"
            )
        else:
            # Usar embeddings locais GRATUITOS
            self.embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2",
                model_kwargs={'device': 'cpu'},
                encode_kwargs={'normalize_embeddings': True}
            )
        
        # Configurar ChromaDB
        self.chroma_client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        
        # Inicializar vector store
        self.vector_store = Chroma(
            client=self.chroma_client,
            embedding_function=self.embeddings,
            collection_name="aeoncosma_context"
        )
        
        # Text splitter para chunks
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        
        # Memory para conversações
        self.conversation_memory = ConversationBufferWindowMemory(
            k=10,  # Manter últimas 10 interações
            return_messages=True
        )
        
        print("✅ AEONCOSMA Vector Store initialized!")
    
    def add_document(self, content: str, metadata: Dict[str, Any] = None) -> str:
        """Adicionar documento ao vector store"""
        if not metadata:
            metadata = {}
        
        # Adicionar timestamp
        metadata.update({
            "timestamp": datetime.utcnow().isoformat(),
            "source": "aeoncosma_system"
        })
        
        # Criar documento
        document = Document(
            page_content=content,
            metadata=metadata
        )
        
        # Dividir em chunks se necessário
        chunks = self.text_splitter.split_documents([document])
        
        # Adicionar ao vector store
        ids = self.vector_store.add_documents(chunks)
        
        return ids[0] if ids else None
    
    def search_similar(self, query: str, k: int = 5) -> List[Document]:
        """Buscar documentos similares"""
        results = self.vector_store.similarity_search(
            query=query,
            k=k
        )
        return results
    
    def search_with_score(self, query: str, k: int = 5) -> List[tuple]:
        """Buscar com scores de similaridade"""
        results = self.vector_store.similarity_search_with_score(
            query=query,
            k=k
        )
        return results
    
    def add_conversation_context(self, user_input: str, ai_response: str):
        """Adicionar contexto de conversação"""
        self.conversation_memory.save_context(
            {"input": user_input},
            {"output": ai_response}
        )
        
        # Salvar no vector store também
        conversation_text = f"User: {user_input}\nAssistant: {ai_response}"
        self.add_document(
            content=conversation_text,
            metadata={
                "type": "conversation",
                "user_input": user_input,
                "ai_response": ai_response
            }
        )
    
    def get_conversation_history(self) -> str:
        """Obter histórico de conversação"""
        return self.conversation_memory.buffer_as_str
    
    def add_aeoncosma_data(self, data_type: str, content: str, metadata: Dict = None):
        """Adicionar dados específicos do AEONCOSMA"""
        if not metadata:
            metadata = {}
        
        metadata.update({
            "aeoncosma_type": data_type,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        return self.add_document(content, metadata)
    
    def search_aeoncosma_context(self, query: str, data_type: str = None) -> List[Document]:
        """Buscar contexto específico do AEONCOSMA"""
        # Filtrar por tipo se especificado
        if data_type:
            # ChromaDB where filter
            results = self.vector_store.similarity_search(
                query=query,
                k=5,
                filter={"aeoncosma_type": data_type}
            )
        else:
            results = self.search_similar(query)
        
        return results
    
    def clear_old_contexts(self, days_old: int = 30):
        """Limpar contextos antigos"""
        # Implementar limpeza baseada em timestamp
        # Por enquanto, placeholder
        pass
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Estatísticas da coleção"""
        collection = self.chroma_client.get_collection("aeoncosma_context")
        count = collection.count()
        
        return {
            "total_documents": count,
            "collection_name": "aeoncosma_context",
            "embedding_model": "text-embedding-ada-002"
        }
    
    def create_conversation(self, user_id: str, conversation_title: str = "Nova Conversa") -> str:
        """Criar nova conversa (método simplificado para compatibilidade)"""
        conversation_id = f"conv_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{user_id}"
        
        # Adicionar início da conversa ao vector store
        self.add_document(
            content=f"Início da conversa: {conversation_title}",
            metadata={
                "type": "conversation_start",
                "conversation_id": conversation_id,
                "user_id": user_id,
                "title": conversation_title
            }
        )
        
        return conversation_id
    
    def add_conversation_message(self, conversation_id: str, role: str, content: str):
        """Adicionar mensagem à conversa"""
        self.add_document(
            content=f"{role}: {content}",
            metadata={
                "type": "conversation_message",
                "conversation_id": conversation_id,
                "role": role,
                "timestamp": datetime.utcnow().isoformat()
            }
        )
    
    def similarity_search(self, query: str, k: int = 3):
        """Alias para search_similar (compatibilidade)"""
        return self.search_similar(query, k)

class ContextualRAG:
    """Sistema RAG (Retrieval-Augmented Generation) contextual"""
    
    def __init__(self, vector_store: AEONCOSMAVectorStore):
        self.vector_store = vector_store
    
    def get_relevant_context(self, query: str, max_context_length: int = 2000) -> str:
        """Obter contexto relevante para uma query"""
        # Buscar documentos similares
        similar_docs = self.vector_store.search_with_score(query, k=5)
        
        # Construir contexto
        context_parts = []
        current_length = 0
        
        for doc, score in similar_docs:
            if score < 0.8:  # Threshold de similaridade
                doc_text = f"[Score: {score:.2f}] {doc.page_content}"
                if current_length + len(doc_text) < max_context_length:
                    context_parts.append(doc_text)
                    current_length += len(doc_text)
                else:
                    break
        
        return "\n\n".join(context_parts)
    
    def enhance_prompt_with_context(self, user_query: str, system_prompt: str = "") -> str:
        """Enriquecer prompt com contexto relevante"""
        # Obter contexto relevante
        relevant_context = self.get_relevant_context(user_query)
        
        # Obter histórico de conversação
        conversation_history = self.vector_store.get_conversation_history()
        
        # Construir prompt enriquecido
        enhanced_prompt = f"""
{system_prompt}

CONTEXTO RELEVANTE:
{relevant_context}

HISTÓRICO DA CONVERSAÇÃO:
{conversation_history}

PERGUNTA DO USUÁRIO: {user_query}

Por favor, responda considerando todo o contexto fornecido acima.
"""
        
        return enhanced_prompt.strip()

# Funções utilitárias
def initialize_aeoncosma_knowledge_base(vector_store: AEONCOSMAVectorStore):
    """Inicializar base de conhecimento do AEONCOSMA"""
    
    # Conhecimento base sobre AEONCOSMA
    aeoncosma_docs = [
        {
            "content": """
            AEONCOSMA é um sistema de Digital Twin avançado que integra:
            - Redes P2P descentralizadas
            - Análise de energia e sustentabilidade
            - Computação quântica simulada
            - Criptografia avançada
            - Visualização 3D interativa
            - Inteligência artificial integrada
            """,
            "type": "system_overview"
        },
        {
            "content": """
            Componentes principais do AEONCOSMA:
            1. Network Visualizer - Visualização 3D de redes
            2. Advanced Visualization Suite - Dashboard multiferramenta
            3. AI Analytics - Sistema de IA com OpenAI
            4. P2P Network - Rede peer-to-peer
            5. Energy Management - Gestão de energia
            6. Quantum Simulator - Simulação quântica
            """,
            "type": "components"
        },
        {
            "content": """
            Arquitetura AEONCOSMA:
            - Frontend: Streamlit applications
            - Backend: FastAPI services
            - Database: SQLite com Vector Store
            - AI: OpenAI GPT + LangChain
            - Visualization: Matplotlib, Plotly, Bokeh
            - Network: NetworkX, 3D visualization
            """,
            "type": "architecture"
        }
    ]
    
    # Adicionar ao vector store
    for doc in aeoncosma_docs:
        vector_store.add_aeoncosma_data(
            data_type=doc["type"],
            content=doc["content"]
        )
    
    print("✅ AEONCOSMA knowledge base initialized!")

if __name__ == "__main__":
    # Teste básico
    import os
    api_key = os.getenv("OPENAI_API_KEY", "sk-test")
    
    vector_store = AEONCOSMAVectorStore(api_key)
    initialize_aeoncosma_knowledge_base(vector_store)
    
    # Teste de busca
    results = vector_store.search_similar("O que é AEONCOSMA?")
    print(f"Encontrados {len(results)} documentos relevantes")
    
    for i, doc in enumerate(results):
        print(f"{i+1}. {doc.page_content[:100]}...")
