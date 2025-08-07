"""
AEONCOSMA Vector Store Setup
============================
Script para inicializar e popular o vector store com conhecimento AEONCOSMA
100% GRATUITO - Sem APIs pagas
"""

import os
import sys
from pathlib import Path

# Adicionar diretório atual ao path
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

try:
    from vector_store import AEONCOSMAVectorStore
    from db.database import DatabaseManager
    from knowledge_base import get_aeoncosma_knowledge_base, generate_sample_conversations
    DEPS_AVAILABLE = True
except ImportError as e:
    print(f"❌ Dependências não encontradas: {e}")
    DEPS_AVAILABLE = False

def setup_vector_store():
    """Configurar e popular o vector store"""
    
    if not DEPS_AVAILABLE:
        print("⚠️ Execute: pip install langchain chromadb")
        return False
    
    try:
        print("🚀 Inicializando AEONCOSMA Vector Store...")
        
        # Inicializar database manager
        db_manager = DatabaseManager()
        print("✅ Database Manager inicializado")
        
        # Inicializar vector store
        vector_store = AEONCOSMAVectorStore()
        print("✅ Vector Store inicializado")
        
        # Carregar knowledge base
        knowledge_base = get_aeoncosma_knowledge_base()
        print(f"📚 Carregando {len(knowledge_base)} documentos...")
        
        # Adicionar documentos ao vector store
        for i, doc in enumerate(knowledge_base):
            try:
                vector_store.add_document(
                    doc["content"],
                    metadata={
                        "title": doc["title"],
                        "category": doc["category"],
                        "tags": ",".join(doc["tags"])
                    }
                )
                print(f"  ✅ {i+1}/{len(knowledge_base)}: {doc['title']}")
            except Exception as e:
                print(f"  ❌ Erro ao adicionar {doc['title']}: {e}")
        
        # Adicionar conversas de exemplo
        conversations = generate_sample_conversations()
        print(f"💬 Adicionando {len(conversations)} conversas de exemplo...")
        
        # Criar conversa principal
        conversation_id = vector_store.create_conversation("system", "Knowledge Base Training")
        
        for i, conv in enumerate(conversations):
            try:
                # Adicionar pergunta do usuário
                vector_store.add_conversation_message(
                    conversation_id, "user", conv["user"]
                )
                
                # Adicionar resposta do assistente
                vector_store.add_conversation_message(
                    conversation_id, "assistant", conv["assistant"]
                )
                
                print(f"  ✅ {i+1}/{len(conversations)}: Conversa adicionada")
            except Exception as e:
                print(f"  ❌ Erro ao adicionar conversa {i+1}: {e}")
        
        # Verificar status final
        try:
            count = vector_store.collection.count()
            print(f"📊 Total de documentos no vector store: {count}")
        except:
            print("📊 Contagem de documentos indisponível")
        
        print("🎉 Setup do Vector Store concluído com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ Erro durante setup: {e}")
        return False

def test_vector_store():
    """Testar funcionamento do vector store"""
    
    if not DEPS_AVAILABLE:
        print("⚠️ Dependências não disponíveis para teste")
        return False
    
    try:
        print("\n🧪 Testando Vector Store...")
        
        vector_store = AEONCOSMAVectorStore()
        
        # Teste de busca
        test_queries = [
            "Como está a rede?",
            "Performance do sistema",
            "Módulo quantum",
            "Segurança AEONCOSMA"
        ]
        
        for query in test_queries:
            try:
                results = vector_store.similarity_search(query, k=2)
                print(f"  🔍 '{query}': {len(results)} resultados encontrados")
                
                if results:
                    for i, result in enumerate(results[:1]):  # Mostrar apenas o primeiro
                        content_preview = result.page_content[:100] + "..."
                        print(f"    • {content_preview}")
                
            except Exception as e:
                print(f"  ❌ Erro na busca '{query}': {e}")
        
        print("✅ Testes concluídos!")
        return True
        
    except Exception as e:
        print(f"❌ Erro durante testes: {e}")
        return False

def main():
    """Função principal"""
    
    print("🌟 AEONCOSMA Vector Store Setup")
    print("=" * 50)
    print("💡 Sistema 100% GRATUITO - Sem APIs pagas")
    print("🧠 Nova funcionalidade: Análise Bayesiana Real implementada!")
    print()
    
    # Verificar dependências
    if not DEPS_AVAILABLE:
        print("❌ Dependências não instaladas")
        print("💻 Execute: pip install langchain chromadb")
        return
    
    # Setup
    setup_success = setup_vector_store()
    
    if setup_success:
        # Testar
        test_vector_store()
        
        print("\n🚀 Próximos passos:")
        print("1. Execute: streamlit run streamlit_app.py")
        print("2. Acesse: http://localhost:8501")
        print("3. Teste o chat com memória contextual!")
        print("4. 🆕 Experimente: python src\\bayesian\\mcmc_real.py")
        print("\n💡 Dica: Pergunte sobre 'status da rede' ou 'performance'")
        print("🧠 Nova funcionalidade: Análise Bayesiana com PyMC disponível!")
    else:
        print("\n❌ Setup falhou. Verifique os erros acima.")

if __name__ == "__main__":
    main()
