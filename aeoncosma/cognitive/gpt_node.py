# aeoncosma/cognitive/gpt_node.py
"""
🧠 AEONCOSMA GPT NODE - O Sentido Cognitivo
Interface primária do nó com o conhecimento e base de dados interna
Desenvolvido por Luiz Cruz - 2025
"""

import os
import json
import hashlib
import sqlite3
from datetime import datetime
from typing import Dict, List, Any, Optional
import requests
import logging

# Configuração opcional de segurança
try:
    from ..security.aeoncosma_security_lock import AeonSecurityLock
    SECURITY_ENABLED = True
except ImportError:
    SECURITY_ENABLED = False
    print("⚠️ Security lock não disponível para GPT Node")

class KnowledgeBase:
    """
    🗃️ Base de conhecimento vetorial local
    Armazena e busca contexto relevante para consultas
    """
    
    def __init__(self, db_path: str = "data/knowledge.db"):
        self.db_path = db_path
        self.ensure_directory()
        self.init_database()
        
    def ensure_directory(self):
        """Garante que o diretório existe"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
    def init_database(self):
        """Inicializa base de dados SQLite"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS knowledge_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                content_hash TEXT UNIQUE NOT NULL,
                metadata TEXT,
                relevance_score REAL DEFAULT 0.5,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                accessed_count INTEGER DEFAULT 0
            )
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_content_hash ON knowledge_entries(content_hash);
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_relevance ON knowledge_entries(relevance_score DESC);
        """)
        
        conn.commit()
        conn.close()
        
    def add_entry(self, content: str, metadata: Dict = None) -> str:
        """Adiciona entrada à base de conhecimento"""
        content_hash = hashlib.sha256(content.encode()).hexdigest()
        metadata_json = json.dumps(metadata or {})
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT OR REPLACE INTO knowledge_entries 
                (content, content_hash, metadata) 
                VALUES (?, ?, ?)
            """, (content, content_hash, metadata_json))
            
            conn.commit()
            return content_hash
            
        except Exception as e:
            logging.error(f"Erro ao adicionar entrada: {e}")
            return None
        finally:
            conn.close()
            
    def search(self, query: str, top_k: int = 3) -> List[Dict]:
        """
        Busca contexto relevante (implementação básica com SQLite)
        Para produção, usar ChromaDB, FAISS ou similar
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Busca básica por keywords (pode ser melhorada com embeddings)
        query_words = query.lower().split()
        like_conditions = " OR ".join([f"LOWER(content) LIKE ?" for _ in query_words])
        like_params = [f"%{word}%" for word in query_words]
        
        cursor.execute(f"""
            SELECT content, metadata, relevance_score, accessed_count
            FROM knowledge_entries 
            WHERE {like_conditions}
            ORDER BY relevance_score DESC, accessed_count DESC
            LIMIT ?
        """, like_params + [top_k])
        
        results = []
        for row in cursor.fetchall():
            content, metadata_json, relevance_score, accessed_count = row
            
            # Atualiza contador de acesso
            content_hash = hashlib.sha256(content.encode()).hexdigest()
            cursor.execute("""
                UPDATE knowledge_entries 
                SET accessed_count = accessed_count + 1 
                WHERE content_hash = ?
            """, (content_hash,))
            
            results.append({
                "content": content,
                "metadata": json.loads(metadata_json),
                "relevance_score": relevance_score,
                "accessed_count": accessed_count
            })
        
        conn.commit()
        conn.close()
        
        return results

class LLMInterface:
    """
    🤖 Interface com modelos de linguagem
    Suporta APIs externas e modelos locais
    """
    
    def __init__(self, api_key: str = None, local_model_path: str = None, model_type: str = "openai"):
        self.api_key = api_key
        self.local_model_path = local_model_path
        self.model_type = model_type
        self.session_history = []
        
    def generate(self, prompt: str, max_tokens: int = 500, temperature: float = 0.7) -> str:
        """
        Gera resposta usando LLM configurado
        """
        if self.model_type == "openai" and self.api_key:
            return self._generate_openai(prompt, max_tokens, temperature)
        elif self.model_type == "local" and self.local_model_path:
            return self._generate_local(prompt, max_tokens, temperature)
        else:
            return self._generate_fallback(prompt)
            
    def _generate_openai(self, prompt: str, max_tokens: int, temperature: float) -> str:
        """Geração via API OpenAI"""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": "gpt-3.5-turbo",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": max_tokens,
                "temperature": temperature
            }
            
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            else:
                return f"Erro na API: {response.status_code}"
                
        except Exception as e:
            logging.error(f"Erro OpenAI: {e}")
            return self._generate_fallback(prompt)
            
    def _generate_local(self, prompt: str, max_tokens: int, temperature: float) -> str:
        """Geração com modelo local (implementação futura)"""
        # TODO: Implementar interface com modelos locais (Ollama, llama.cpp, etc)
        return f"[LOCAL MODEL] Processando: {prompt[:100]}..."
        
    def _generate_fallback(self, prompt: str) -> str:
        """Fallback quando LLM não disponível"""
        return f"[FALLBACK] Consulta recebida: {prompt[:100]}... (LLM não configurado)"

class GPTNode:
    """
    🧠 Nó GPT - Interface Cognitiva Principal
    Combina conhecimento local com capacidades de LLM
    """
    
    def __init__(self, node_id: str, api_key: str = None, local_model_path: str = None):
        self.node_id = node_id
        
        # 🛡️ Verificações de segurança
        if SECURITY_ENABLED:
            self.security_lock = AeonSecurityLock()
            self.security_lock.log_execution("gpt_node_init", {
                "node_id": node_id,
                "has_api_key": api_key is not None,
                "has_local_model": local_model_path is not None
            })
            print(f"🔒 [{node_id}] GPT Node com segurança ativa")
        
        # Inicializa componentes
        self.knowledge_base = KnowledgeBase(f"data/{node_id}_knowledge.db")
        self.llm = LLMInterface(api_key, local_model_path)
        
        # Filtros de relevância e sandbox
        self.relevance_filters = {
            "min_confidence": 0.3,
            "max_context_length": 2000,
            "forbidden_patterns": ["password", "api_key", "secret", "token"]
        }
        
        # Estatísticas
        self.stats = {
            "queries_processed": 0,
            "knowledge_entries": 0,
            "security_blocks": 0,
            "context_retrievals": 0
        }
        
        print(f"🧠 [{node_id}] GPT Node inicializado")
        
    def query(self, prompt: str, include_context: bool = True, max_context: int = 3) -> Dict[str, Any]:
        """
        Consulta principal do GPT Node
        Combina contexto da base de conhecimento com capacidades LLM
        """
        self.stats["queries_processed"] += 1
        
        # 🛡️ Verificações de segurança no prompt
        if SECURITY_ENABLED:
            if self._is_prompt_safe(prompt):
                self.security_lock.log_execution("gpt_query", {
                    "node_id": self.node_id,
                    "prompt_length": len(prompt),
                    "include_context": include_context
                })
            else:
                self.stats["security_blocks"] += 1
                return {
                    "response": "🚫 Consulta bloqueada por política de segurança",
                    "status": "blocked",
                    "reason": "Padrões suspeitos detectados no prompt"
                }
        
        result = {
            "timestamp": datetime.now().isoformat(),
            "node_id": self.node_id,
            "prompt": prompt,
            "context_used": [],
            "response": "",
            "status": "processing"
        }
        
        try:
            # 1. Busca contexto relevante se solicitado
            context_entries = []
            if include_context:
                context_entries = self.knowledge_base.search(prompt, max_context)
                self.stats["context_retrievals"] += len(context_entries)
                result["context_used"] = [entry["content"][:200] + "..." for entry in context_entries]
            
            # 2. Constrói prompt enriquecido
            enhanced_prompt = self._build_enhanced_prompt(prompt, context_entries)
            
            # 3. Aplica filtros de relevância
            if self._passes_relevance_filters(enhanced_prompt):
                # 4. Gera resposta com LLM
                llm_response = self.llm.generate(enhanced_prompt)
                
                # 5. Pós-processamento de segurança
                safe_response = self._sanitize_response(llm_response)
                
                result["response"] = safe_response
                result["status"] = "success"
                
                # 6. Armazena aprendizado na base de conhecimento
                self._store_interaction(prompt, safe_response)
                
            else:
                result["response"] = "🚫 Consulta não atende aos filtros de relevância"
                result["status"] = "filtered"
                
        except Exception as e:
            logging.error(f"Erro no GPTNode.query: {e}")
            result["response"] = f"❌ Erro interno: {str(e)}"
            result["status"] = "error"
            
        return result
        
    def add_knowledge(self, content: str, metadata: Dict = None) -> str:
        """Adiciona conhecimento à base local"""
        entry_hash = self.knowledge_base.add_entry(content, metadata)
        if entry_hash:
            self.stats["knowledge_entries"] += 1
            print(f"📚 [{self.node_id}] Conhecimento adicionado: {entry_hash[:8]}...")
        return entry_hash
        
    def _build_enhanced_prompt(self, original_prompt: str, context_entries: List[Dict]) -> str:
        """Constrói prompt enriquecido com contexto"""
        if not context_entries:
            return original_prompt
            
        context_text = "\n".join([
            f"Contexto {i+1}: {entry['content']}" 
            for i, entry in enumerate(context_entries)
        ])
        
        enhanced = f"""Contexto Relevante:
{context_text}

Pergunta: {original_prompt}

Responda baseando-se no contexto fornecido quando relevante, mas não se limite apenas a ele."""
        
        # Limita tamanho total
        if len(enhanced) > self.relevance_filters["max_context_length"]:
            enhanced = enhanced[:self.relevance_filters["max_context_length"]] + "..."
            
        return enhanced
        
    def _is_prompt_safe(self, prompt: str) -> bool:
        """Verifica se prompt é seguro"""
        prompt_lower = prompt.lower()
        
        for forbidden in self.relevance_filters["forbidden_patterns"]:
            if forbidden in prompt_lower:
                return False
                
        return True
        
    def _passes_relevance_filters(self, prompt: str) -> bool:
        """Aplica filtros de relevância"""
        # Filtro básico de tamanho
        if len(prompt) > self.relevance_filters["max_context_length"] * 2:
            return False
            
        return True
        
    def _sanitize_response(self, response: str) -> str:
        """Remove informações sensíveis da resposta"""
        sanitized = response
        
        # Remove padrões suspeitos
        for pattern in self.relevance_filters["forbidden_patterns"]:
            if pattern in sanitized.lower():
                sanitized = sanitized.replace(pattern, "[REDACTED]")
                
        return sanitized
        
    def _store_interaction(self, prompt: str, response: str):
        """Armazena interação para aprendizado futuro"""
        interaction_content = f"Q: {prompt}\nA: {response}"
        metadata = {
            "type": "interaction",
            "timestamp": datetime.now().isoformat(),
            "node_id": self.node_id
        }
        
        self.knowledge_base.add_entry(interaction_content, metadata)
        
    def get_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas do nó"""
        return {
            "node_id": self.node_id,
            "stats": self.stats,
            "knowledge_base_size": self._get_kb_size(),
            "security_enabled": SECURITY_ENABLED,
            "llm_configured": self.llm.api_key is not None or self.llm.local_model_path is not None
        }
        
    def _get_kb_size(self) -> int:
        """Conta entradas na base de conhecimento"""
        conn = sqlite3.connect(self.knowledge_base.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM knowledge_entries")
        count = cursor.fetchone()[0]
        conn.close()
        return count
        
    def export_knowledge(self) -> str:
        """Exporta conhecimento em formato JSON"""
        conn = sqlite3.connect(self.knowledge_base.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT content, metadata, relevance_score, created_at 
            FROM knowledge_entries 
            ORDER BY created_at DESC
        """)
        
        entries = []
        for row in cursor.fetchall():
            content, metadata_json, relevance_score, created_at = row
            entries.append({
                "content": content,
                "metadata": json.loads(metadata_json),
                "relevance_score": relevance_score,
                "created_at": created_at
            })
            
        conn.close()
        
        export_data = {
            "node_id": self.node_id,
            "export_timestamp": datetime.now().isoformat(),
            "total_entries": len(entries),
            "entries": entries
        }
        
        return json.dumps(export_data, indent=2, ensure_ascii=False)

def main():
    """Teste do GPT Node"""
    # Exemplo de uso
    gpt_node = GPTNode("test_cognitive_node")
    
    # Adiciona conhecimento base
    gpt_node.add_knowledge(
        "AEONCOSMA é um sistema P2P descentralizado com IA avançada para trading.",
        {"category": "system_info", "priority": "high"}
    )
    
    gpt_node.add_knowledge(
        "O sistema utiliza validação sequencial e redes neurais para decisões.",
        {"category": "technical", "priority": "medium"}
    )
    
    # Teste de consulta
    result = gpt_node.query("O que é AEONCOSMA?")
    print("\n🧠 RESULTADO DA CONSULTA:")
    print(f"Status: {result['status']}")
    print(f"Resposta: {result['response']}")
    print(f"Contexto usado: {len(result['context_used'])} entradas")
    
    # Estatísticas
    stats = gpt_node.get_stats()
    print(f"\n📊 ESTATÍSTICAS:")
    print(json.dumps(stats, indent=2))

if __name__ == "__main__":
    main()
