# aeoncosma/adapters/enterprise_adapter.py
"""
🌍 AEONCOSMA ENTERPRISE ADAPTER - Os Tentáculos no Mundo
Conecta o nó aos sistemas legados e fontes de dados externas
Tradutor universal entre o mundo caótico dos dados e o protocolo AEON
Desenvolvido por Luiz Cruz - 2025
"""

import os
import json
import hashlib
import requests
import time
from datetime import datetime
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, asdict
from abc import ABC, abstractmethod
import logging
import re
import sqlite3

# NLP e processamento de texto
try:
    import nltk
    from nltk.tokenize import word_tokenize, sent_tokenize
    from nltk.corpus import stopwords
    from nltk.stem import PorterStemmer
    NLTK_AVAILABLE = True
except ImportError:
    NLTK_AVAILABLE = False
    print("⚠️ NLTK não disponível - funcionalidades de NLP limitadas")

# Importações internas
try:
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    from security.aeoncosma_security_lock import AeonSecurityLock
    SECURITY_ENABLED = True
except ImportError:
    SECURITY_ENABLED = False
    print("⚠️ Segurança não disponível para Enterprise Adapter")

@dataclass
class DataSource:
    """
    📊 Fonte de dados empresarial
    """
    source_id: str
    source_type: str  # "api", "file", "database", "document", "email"
    name: str
    description: str
    endpoint_url: Optional[str]
    auth_config: Dict[str, Any]
    data_format: str  # "json", "xml", "csv", "pdf", "docx", "html"
    extraction_rules: Dict[str, Any]
    refresh_interval: int  # segundos
    last_accessed: str
    is_active: bool
    metadata: Dict[str, Any]

@dataclass
class ExtractedInsight:
    """
    💡 Insight extraído de dados empresariais
    """
    insight_id: str
    source_id: str
    raw_data: str
    structured_data: Dict[str, Any]
    entities: List[Dict[str, Any]]
    sentiment: Optional[str]
    keywords: List[str]
    confidence: float
    extraction_timestamp: str
    symbolic_representation: Dict[str, Any]
    metadata: Dict[str, Any]

class BaseConnector(ABC):
    """
    🔌 Conector base para diferentes tipos de fontes
    """
    
    def __init__(self, source: DataSource):
        self.source = source
        self.last_error = None
        self.connection_stats = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "last_request_time": None,
            "average_response_time": 0.0
        }
        
    @abstractmethod
    async def connect(self) -> bool:
        """Estabelece conexão com a fonte"""
        pass
        
    @abstractmethod
    async def fetch_data(self, query: str) -> Optional[Dict[str, Any]]:
        """Busca dados da fonte"""
        pass
        
    @abstractmethod
    async def test_connection(self) -> bool:
        """Testa conectividade"""
        pass
        
    def update_stats(self, success: bool, response_time: float):
        """Atualiza estatísticas de conexão"""
        self.connection_stats["total_requests"] += 1
        self.connection_stats["last_request_time"] = datetime.now().isoformat()
        
        if success:
            self.connection_stats["successful_requests"] += 1
        else:
            self.connection_stats["failed_requests"] += 1
            
        # Atualiza tempo médio de resposta
        total_requests = self.connection_stats["total_requests"]
        current_avg = self.connection_stats["average_response_time"]
        self.connection_stats["average_response_time"] = (
            (current_avg * (total_requests - 1) + response_time) / total_requests
        )

class APIConnector(BaseConnector):
    """
    🌐 Conector para APIs REST
    """
    
    def __init__(self, source: DataSource):
        super().__init__(source)
        self.session = requests.Session()
        self._setup_authentication()
        
    def _setup_authentication(self):
        """Configura autenticação baseada no tipo"""
        auth_config = self.source.auth_config
        auth_type = auth_config.get("type", "none")
        
        if auth_type == "bearer":
            self.session.headers.update({
                "Authorization": f"Bearer {auth_config.get('token')}"
            })
        elif auth_type == "api_key":
            if auth_config.get("header_name"):
                self.session.headers.update({
                    auth_config["header_name"]: auth_config.get("api_key")
                })
            else:
                self.session.params.update({
                    "api_key": auth_config.get("api_key")
                })
        elif auth_type == "basic":
            self.session.auth = (
                auth_config.get("username"),
                auth_config.get("password")
            )
            
    async def connect(self) -> bool:
        """Testa conexão inicial"""
        return await self.test_connection()
        
    async def test_connection(self) -> bool:
        """Testa conectividade da API"""
        start_time = time.time()
        
        try:
            # Faz requisição de teste
            test_endpoint = self.source.auth_config.get("test_endpoint", self.source.endpoint_url)
            response = self.session.get(test_endpoint, timeout=10)
            
            response_time = time.time() - start_time
            success = response.status_code == 200
            
            self.update_stats(success, response_time)
            
            if not success:
                self.last_error = f"HTTP {response.status_code}: {response.text[:200]}"
                
            return success
            
        except Exception as e:
            response_time = time.time() - start_time
            self.update_stats(False, response_time)
            self.last_error = str(e)
            return False
            
    async def fetch_data(self, query: str) -> Optional[Dict[str, Any]]:
        """Busca dados da API"""
        start_time = time.time()
        
        try:
            # Constrói URL da consulta
            query_params = {
                "query": query,
                **self.source.extraction_rules.get("default_params", {})
            }
            
            response = self.session.get(
                self.source.endpoint_url,
                params=query_params,
                timeout=30
            )
            
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                self.update_stats(True, response_time)
                
                if self.source.data_format.lower() == "json":
                    return {
                        "raw_data": response.text,
                        "parsed_data": response.json(),
                        "response_time": response_time,
                        "status_code": response.status_code
                    }
                else:
                    return {
                        "raw_data": response.text,
                        "parsed_data": None,
                        "response_time": response_time,
                        "status_code": response.status_code
                    }
            else:
                self.update_stats(False, response_time)
                self.last_error = f"HTTP {response.status_code}: {response.text[:200]}"
                return None
                
        except Exception as e:
            response_time = time.time() - start_time
            self.update_stats(False, response_time)
            self.last_error = str(e)
            return None

class FileConnector(BaseConnector):
    """
    📁 Conector para arquivos locais
    """
    
    async def connect(self) -> bool:
        """Verifica se arquivo existe"""
        file_path = self.source.endpoint_url
        return os.path.exists(file_path) and os.path.isfile(file_path)
        
    async def test_connection(self) -> bool:
        """Testa acesso ao arquivo"""
        return await self.connect()
        
    async def fetch_data(self, query: str) -> Optional[Dict[str, Any]]:
        """Lê dados do arquivo"""
        start_time = time.time()
        
        try:
            file_path = self.source.endpoint_url
            
            if not os.path.exists(file_path):
                self.last_error = f"Arquivo não encontrado: {file_path}"
                return None
                
            # Lê arquivo baseado no formato
            if self.source.data_format.lower() == "json":
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    raw_data = json.dumps(data, ensure_ascii=False)
            elif self.source.data_format.lower() == "csv":
                with open(file_path, 'r', encoding='utf-8') as f:
                    raw_data = f.read()
                    # TODO: Parse CSV para estrutura
                    data = {"csv_content": raw_data}
            else:
                with open(file_path, 'r', encoding='utf-8') as f:
                    raw_data = f.read()
                    data = {"text_content": raw_data}
                    
            response_time = time.time() - start_time
            self.update_stats(True, response_time)
            
            return {
                "raw_data": raw_data,
                "parsed_data": data,
                "response_time": response_time,
                "file_size": os.path.getsize(file_path),
                "file_modified": datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat()
            }
            
        except Exception as e:
            response_time = time.time() - start_time
            self.update_stats(False, response_time)
            self.last_error = str(e)
            return None

class DocumentConnector(BaseConnector):
    """
    📄 Conector para documentos (PDF, Word, etc.)
    """
    
    async def connect(self) -> bool:
        """Verifica se documento existe"""
        doc_path = self.source.endpoint_url
        return os.path.exists(doc_path)
        
    async def test_connection(self) -> bool:
        """Testa acesso ao documento"""
        return await self.connect()
        
    async def fetch_data(self, query: str) -> Optional[Dict[str, Any]]:
        """Extrai texto do documento"""
        start_time = time.time()
        
        try:
            doc_path = self.source.endpoint_url
            
            if not os.path.exists(doc_path):
                self.last_error = f"Documento não encontrado: {doc_path}"
                return None
                
            # Extração básica de texto (pode ser melhorada com PyPDF2, python-docx, etc.)
            if self.source.data_format.lower() == "pdf":
                # Placeholder para extração de PDF
                extracted_text = f"[PDF] Conteúdo do documento: {doc_path}"
            elif self.source.data_format.lower() == "docx":
                # Placeholder para extração de Word
                extracted_text = f"[DOCX] Conteúdo do documento: {doc_path}"
            else:
                # Arquivo de texto simples
                with open(doc_path, 'r', encoding='utf-8') as f:
                    extracted_text = f.read()
                    
            response_time = time.time() - start_time
            self.update_stats(True, response_time)
            
            return {
                "raw_data": extracted_text,
                "parsed_data": {"text_content": extracted_text},
                "response_time": response_time,
                "file_size": os.path.getsize(doc_path),
                "file_type": self.source.data_format
            }
            
        except Exception as e:
            response_time = time.time() - start_time
            self.update_stats(False, response_time)
            self.last_error = str(e)
            return None

class NLPProcessor:
    """
    🧠 Processador de NLP para extração de insights
    """
    
    def __init__(self):
        self.stemmer = PorterStemmer() if NLTK_AVAILABLE else None
        self.stop_words = set(stopwords.words('english')) if NLTK_AVAILABLE else set()
        
        # Patterns para extração de entidades
        self.entity_patterns = {
            "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            "phone": r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            "date": r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',
            "money": r'\$\d+(?:,\d{3})*(?:\.\d{2})?',
            "percentage": r'\d+(?:\.\d+)?%',
            "url": r'https?://[^\s<>"]+|www\.[^\s<>"]+'
        }
        
    def extract_insights(self, raw_text: str, source_id: str) -> ExtractedInsight:
        """Extrai insights estruturados do texto bruto"""
        insight_id = hashlib.sha256(f"{source_id}-{raw_text[:100]}-{time.time()}".encode()).hexdigest()[:16]
        
        # Extração de entidades
        entities = self._extract_entities(raw_text)
        
        # Extração de palavras-chave
        keywords = self._extract_keywords(raw_text)
        
        # Análise de sentimento (básica)
        sentiment = self._analyze_sentiment(raw_text)
        
        # Estruturação de dados
        structured_data = self._structure_data(raw_text, entities, keywords)
        
        # Representação simbólica para protocolo AEON
        symbolic_representation = self._create_symbolic_representation(
            structured_data, entities, keywords, sentiment
        )
        
        return ExtractedInsight(
            insight_id=insight_id,
            source_id=source_id,
            raw_data=raw_text,
            structured_data=structured_data,
            entities=entities,
            sentiment=sentiment,
            keywords=keywords,
            confidence=self._calculate_confidence(entities, keywords, sentiment),
            extraction_timestamp=datetime.now().isoformat(),
            symbolic_representation=symbolic_representation,
            metadata={
                "text_length": len(raw_text),
                "entity_count": len(entities),
                "keyword_count": len(keywords),
                "nlp_available": NLTK_AVAILABLE
            }
        )
        
    def _extract_entities(self, text: str) -> List[Dict[str, Any]]:
        """Extrai entidades nomeadas do texto"""
        entities = []
        
        for entity_type, pattern in self.entity_patterns.items():
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                entities.append({
                    "type": entity_type,
                    "value": match.group(),
                    "start": match.start(),
                    "end": match.end(),
                    "confidence": 0.8  # Confiança básica para regex
                })
                
        return entities
        
    def _extract_keywords(self, text: str) -> List[str]:
        """Extrai palavras-chave relevantes"""
        if not NLTK_AVAILABLE:
            # Fallback simples
            words = text.lower().split()
            return [word for word in words if len(word) > 4][:10]
            
        # Tokenização e limpeza
        tokens = word_tokenize(text.lower())
        
        # Remove stop words e palavras muito curtas
        keywords = [
            self.stemmer.stem(token) for token in tokens
            if token.isalpha() and len(token) > 3 and token not in self.stop_words
        ]
        
        # Conta frequência e retorna mais frequentes
        keyword_freq = {}
        for keyword in keywords:
            keyword_freq[keyword] = keyword_freq.get(keyword, 0) + 1
            
        # Ordena por frequência e retorna top 15
        sorted_keywords = sorted(keyword_freq.items(), key=lambda x: x[1], reverse=True)
        return [keyword for keyword, freq in sorted_keywords[:15]]
        
    def _analyze_sentiment(self, text: str) -> str:
        """Análise básica de sentimento"""
        positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic', 'positive', 'success', 'win', 'profit']
        negative_words = ['bad', 'terrible', 'awful', 'horrible', 'negative', 'loss', 'fail', 'problem', 'issue', 'error']
        
        text_lower = text.lower()
        
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count > negative_count:
            return "positive"
        elif negative_count > positive_count:
            return "negative"
        else:
            return "neutral"
            
    def _structure_data(self, text: str, entities: List[Dict], keywords: List[str]) -> Dict[str, Any]:
        """Estrutura os dados extraídos"""
        return {
            "summary": text[:200] + "..." if len(text) > 200 else text,
            "entity_summary": {
                entity_type: [e["value"] for e in entities if e["type"] == entity_type]
                for entity_type in set(e["type"] for e in entities)
            },
            "top_keywords": keywords[:10],
            "text_statistics": {
                "character_count": len(text),
                "word_count": len(text.split()),
                "sentence_count": len(text.split('.'))
            }
        }
        
    def _create_symbolic_representation(self, structured_data: Dict, entities: List[Dict], 
                                      keywords: List[str], sentiment: str) -> Dict[str, Any]:
        """Cria representação simbólica para protocolo AEON"""
        return {
            "content_type": "extracted_insight",
            "semantic_category": self._categorize_content(keywords, entities),
            "sentiment_polarity": sentiment,
            "key_concepts": keywords[:5],
            "extracted_entities": {
                entity_type: len([e for e in entities if e["type"] == entity_type])
                for entity_type in set(e["type"] for e in entities)
            },
            "relevance_indicators": self._calculate_relevance_indicators(structured_data, keywords),
            "symbolic_encoding": {
                "action": "KNOWLEDGE_SHARE",
                "subject": "EXTRACTED_INSIGHT", 
                "content_hash": hashlib.sha256(json.dumps(structured_data).encode()).hexdigest()[:16]
            }
        }
        
    def _categorize_content(self, keywords: List[str], entities: List[Dict]) -> str:
        """Categoriza o conteúdo baseado em keywords e entidades"""
        financial_terms = ['price', 'market', 'trading', 'profit', 'loss', 'investment', 'stock', 'crypto']
        technical_terms = ['system', 'algorithm', 'data', 'analysis', 'processing', 'network']
        business_terms = ['company', 'business', 'customer', 'product', 'service', 'revenue']
        
        keyword_text = ' '.join(keywords).lower()
        
        if any(term in keyword_text for term in financial_terms):
            return "FINANCIAL"
        elif any(term in keyword_text for term in technical_terms):
            return "TECHNICAL"
        elif any(term in keyword_text for term in business_terms):
            return "BUSINESS"
        else:
            return "GENERAL"
            
    def _calculate_relevance_indicators(self, structured_data: Dict, keywords: List[str]) -> Dict[str, float]:
        """Calcula indicadores de relevância"""
        return {
            "keyword_density": len(keywords) / max(structured_data["text_statistics"]["word_count"], 1),
            "entity_richness": len(structured_data.get("entity_summary", {})) / 10.0,  # Normalizado
            "content_depth": min(structured_data["text_statistics"]["character_count"] / 1000.0, 1.0)
        }
        
    def _calculate_confidence(self, entities: List[Dict], keywords: List[str], sentiment: str) -> float:
        """Calcula confiança geral da extração"""
        base_confidence = 0.5
        
        # Bonus por entidades encontradas
        entity_bonus = min(len(entities) * 0.1, 0.3)
        
        # Bonus por keywords relevantes
        keyword_bonus = min(len(keywords) * 0.02, 0.2)
        
        # Bonus se sentimento foi determinado
        sentiment_bonus = 0.1 if sentiment != "neutral" else 0.0
        
        return min(base_confidence + entity_bonus + keyword_bonus + sentiment_bonus, 1.0)

class EnterpriseAdapter:
    """
    🌍 Adaptador Empresarial Principal
    Orquestra conexões com múltiplas fontes de dados empresariais
    """
    
    def __init__(self, node_id: str, config_path: str = "config/enterprise_sources.json"):
        self.node_id = node_id
        self.config_path = config_path
        
        # 🛡️ Segurança
        if SECURITY_ENABLED:
            self.security_lock = AeonSecurityLock()
            self.security_lock.log_execution("enterprise_adapter_init", {
                "node_id": node_id,
                "config_path": config_path
            })
            print(f"🔒 [{node_id}] Enterprise Adapter com segurança ativa")
            
        # Componentes
        self.nlp_processor = NLPProcessor()
        self.connectors = {}
        self.data_sources = {}
        
        # Base de dados de insights
        self.insights_db_path = f"data/{node_id}_enterprise_insights.db"
        self.init_insights_database()
        
        # Cache de dados
        self.data_cache = {}
        self.cache_ttl = 300  # 5 minutos
        
        # Estatísticas
        self.stats = {
            "sources_configured": 0,
            "successful_connections": 0,
            "failed_connections": 0,
            "data_fetches": 0,
            "insights_extracted": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "adapter_start_time": datetime.now().isoformat()
        }
        
        # Carrega configurações de fontes
        self.load_data_sources()
        
        print(f"🌍 [{node_id}] Enterprise Adapter inicializado com {len(self.data_sources)} fontes")
        
    def init_insights_database(self):
        """Inicializa base de dados de insights"""
        os.makedirs(os.path.dirname(self.insights_db_path), exist_ok=True)
        
        conn = sqlite3.connect(self.insights_db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS extracted_insights (
                insight_id TEXT PRIMARY KEY,
                source_id TEXT NOT NULL,
                raw_data TEXT NOT NULL,
                structured_data TEXT NOT NULL,
                entities TEXT NOT NULL,
                sentiment TEXT,
                keywords TEXT NOT NULL,
                confidence REAL NOT NULL,
                extraction_timestamp TEXT NOT NULL,
                symbolic_representation TEXT NOT NULL,
                metadata TEXT NOT NULL
            )
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_source_timestamp ON extracted_insights(source_id, extraction_timestamp DESC);
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_confidence ON extracted_insights(confidence DESC);
        """)
        
        conn.commit()
        conn.close()
        
    def load_data_sources(self):
        """Carrega configurações de fontes de dados"""
        if not os.path.exists(self.config_path):
            self.create_default_config()
            
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                sources_config = json.load(f)
                
            for source_data in sources_config.get("data_sources", []):
                source = DataSource(**source_data)
                self.data_sources[source.source_id] = source
                
                # Cria conector apropriado
                connector = self.create_connector(source)
                if connector:
                    self.connectors[source.source_id] = connector
                    
            self.stats["sources_configured"] = len(self.data_sources)
            
        except Exception as e:
            print(f"❌ [{self.node_id}] Erro ao carregar fontes: {e}")
            
    def create_default_config(self):
        """Cria configuração padrão de fontes"""
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        
        default_config = {
            "data_sources": [
                {
                    "source_id": "sample_api",
                    "source_type": "api",
                    "name": "API de Exemplo",
                    "description": "API de demonstração",
                    "endpoint_url": "https://jsonplaceholder.typicode.com/posts",
                    "auth_config": {"type": "none"},
                    "data_format": "json",
                    "extraction_rules": {"default_params": {}},
                    "refresh_interval": 3600,
                    "last_accessed": "",
                    "is_active": True,
                    "metadata": {"example": True}
                },
                {
                    "source_id": "local_documents",
                    "source_type": "file",
                    "name": "Documentos Locais",
                    "description": "Arquivos de texto locais",
                    "endpoint_url": "data/sample_document.txt",
                    "auth_config": {"type": "none"},
                    "data_format": "text",
                    "extraction_rules": {},
                    "refresh_interval": 1800,
                    "last_accessed": "",
                    "is_active": True,
                    "metadata": {"directory": "data/"}
                }
            ]
        }
        
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, indent=2, ensure_ascii=False)
            
        print(f"📝 [{self.node_id}] Configuração padrão criada em {self.config_path}")
        
    def create_connector(self, source: DataSource) -> Optional[BaseConnector]:
        """Factory para criar conectores apropriados"""
        try:
            if source.source_type == "api":
                return APIConnector(source)
            elif source.source_type == "file":
                if source.data_format in ["pdf", "docx", "doc"]:
                    return DocumentConnector(source)
                else:
                    return FileConnector(source)
            elif source.source_type == "document":
                return DocumentConnector(source)
            else:
                print(f"⚠️ [{self.node_id}] Tipo de fonte não suportado: {source.source_type}")
                return None
                
        except Exception as e:
            print(f"❌ [{self.node_id}] Erro ao criar conector para {source.source_id}: {e}")
            return None
            
    async def fetch_data(self, source_id: str, query: str) -> Optional[ExtractedInsight]:
        """
        Busca dados de uma fonte empresarial específica
        """
        # Verifica cache primeiro
        cache_key = f"{source_id}-{hashlib.sha256(query.encode()).hexdigest()[:8]}"
        
        if cache_key in self.data_cache:
            cache_entry = self.data_cache[cache_key]
            if time.time() - cache_entry["timestamp"] < self.cache_ttl:
                self.stats["cache_hits"] += 1
                return cache_entry["insight"]
                
        self.stats["cache_misses"] += 1
        
        # Verifica se fonte existe
        if source_id not in self.connectors:
            print(f"❌ [{self.node_id}] Fonte não encontrada: {source_id}")
            return None
            
        connector = self.connectors[source_id]
        source = self.data_sources[source_id]
        
        try:
            # Busca dados brutos
            raw_data_result = await connector.fetch_data(query)
            
            if not raw_data_result:
                self.stats["failed_connections"] += 1
                return None
                
            self.stats["successful_connections"] += 1
            self.stats["data_fetches"] += 1
            
            # Extrai texto para processamento NLP
            if source.data_format == "json" and raw_data_result.get("parsed_data"):
                # Converte JSON para texto para NLP
                text_content = json.dumps(raw_data_result["parsed_data"], ensure_ascii=False)
            else:
                text_content = raw_data_result["raw_data"]
                
            # Processa com NLP e extrai insights
            insight = self.nlp_processor.extract_insights(text_content, source_id)
            
            # Adiciona metadados da fonte
            insight.metadata.update({
                "source_name": source.name,
                "source_type": source.source_type,
                "data_format": source.data_format,
                "response_time": raw_data_result.get("response_time", 0),
                "raw_data_size": len(raw_data_result["raw_data"])
            })
            
            # Salva insight na base de dados
            self.save_insight(insight)
            self.stats["insights_extracted"] += 1
            
            # Atualiza cache
            self.data_cache[cache_key] = {
                "insight": insight,
                "timestamp": time.time()
            }
            
            # Limpa cache antigo
            self.cleanup_cache()
            
            print(f"✅ [{self.node_id}] Insight extraído de {source_id} (confiança: {insight.confidence:.2f})")
            
            return insight
            
        except Exception as e:
            print(f"❌ [{self.node_id}] Erro ao buscar dados de {source_id}: {e}")
            self.stats["failed_connections"] += 1
            return None
            
    def save_insight(self, insight: ExtractedInsight):
        """Salva insight na base de dados"""
        conn = sqlite3.connect(self.insights_db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO extracted_insights 
            (insight_id, source_id, raw_data, structured_data, entities,
             sentiment, keywords, confidence, extraction_timestamp,
             symbolic_representation, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            insight.insight_id, insight.source_id, insight.raw_data,
            json.dumps(insight.structured_data), json.dumps(insight.entities),
            insight.sentiment, json.dumps(insight.keywords), insight.confidence,
            insight.extraction_timestamp, json.dumps(insight.symbolic_representation),
            json.dumps(insight.metadata)
        ))
        
        conn.commit()
        conn.close()
        
    async def test_all_connections(self) -> Dict[str, Any]:
        """Testa conectividade de todas as fontes"""
        results = {}
        
        for source_id, connector in self.connectors.items():
            try:
                is_connected = await connector.test_connection()
                results[source_id] = {
                    "connected": is_connected,
                    "last_error": connector.last_error,
                    "stats": connector.connection_stats
                }
            except Exception as e:
                results[source_id] = {
                    "connected": False,
                    "last_error": str(e),
                    "stats": {}
                }
                
        return results
        
    def cleanup_cache(self):
        """Remove entradas antigas do cache"""
        current_time = time.time()
        
        expired_keys = [
            key for key, entry in self.data_cache.items()
            if current_time - entry["timestamp"] > self.cache_ttl
        ]
        
        for key in expired_keys:
            del self.data_cache[key]
            
    def get_recent_insights(self, limit: int = 10, source_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Recupera insights recentes"""
        conn = sqlite3.connect(self.insights_db_path)
        cursor = conn.cursor()
        
        if source_id:
            cursor.execute("""
                SELECT insight_id, source_id, structured_data, sentiment,
                       keywords, confidence, extraction_timestamp
                FROM extracted_insights
                WHERE source_id = ?
                ORDER BY extraction_timestamp DESC
                LIMIT ?
            """, (source_id, limit))
        else:
            cursor.execute("""
                SELECT insight_id, source_id, structured_data, sentiment,
                       keywords, confidence, extraction_timestamp
                FROM extracted_insights
                ORDER BY extraction_timestamp DESC
                LIMIT ?
            """, (limit,))
            
        insights = []
        for row in cursor.fetchall():
            insights.append({
                "insight_id": row[0],
                "source_id": row[1],
                "structured_data": json.loads(row[2]),
                "sentiment": row[3],
                "keywords": json.loads(row[4]),
                "confidence": row[5],
                "extraction_timestamp": row[6]
            })
            
        conn.close()
        return insights
        
    def get_adapter_status(self) -> Dict[str, Any]:
        """Retorna status completo do adaptador"""
        return {
            "node_id": self.node_id,
            "stats": self.stats,
            "configured_sources": list(self.data_sources.keys()),
            "active_sources": [
                source_id for source_id, source in self.data_sources.items()
                if source.is_active
            ],
            "cache_size": len(self.data_cache),
            "nlp_available": NLTK_AVAILABLE,
            "security_enabled": SECURITY_ENABLED
        }
        
    def export_insights_ledger(self, limit: int = 100) -> str:
        """Exporta ledger de insights em JSON"""
        conn = sqlite3.connect(self.insights_db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT insight_id, source_id, structured_data, entities,
                   sentiment, keywords, confidence, extraction_timestamp,
                   symbolic_representation, metadata
            FROM extracted_insights
            ORDER BY extraction_timestamp DESC
            LIMIT ?
        """, (limit,))
        
        insights = []
        for row in cursor.fetchall():
            insights.append({
                "insight_id": row[0],
                "source_id": row[1],
                "structured_data": json.loads(row[2]),
                "entities": json.loads(row[3]),
                "sentiment": row[4],
                "keywords": json.loads(row[5]),
                "confidence": row[6],
                "extraction_timestamp": row[7],
                "symbolic_representation": json.loads(row[8]),
                "metadata": json.loads(row[9])
            })
            
        conn.close()
        
        ledger = {
            "export_timestamp": datetime.now().isoformat(),
            "adapter_node_id": self.node_id,
            "total_insights": len(insights),
            "insights": insights,
            "adapter_stats": self.stats
        }
        
        return json.dumps(ledger, indent=2, ensure_ascii=False)

# Exemplo de uso
async def main():
    """Teste do Enterprise Adapter"""
    print("🌍 TESTANDO ENTERPRISE ADAPTER")
    print("=" * 50)
    
    # Cria adaptador
    adapter = EnterpriseAdapter("test_enterprise_node")
    
    # Testa conexões
    print("\n🔗 TESTANDO CONEXÕES:")
    connections = await adapter.test_all_connections()
    
    for source_id, result in connections.items():
        status = "✅ CONECTADO" if result["connected"] else "❌ FALHOU"
        print(f"   {source_id}: {status}")
        if not result["connected"] and result["last_error"]:
            print(f"      Erro: {result['last_error']}")
            
    # Testa busca de dados
    print(f"\n📊 TESTANDO BUSCA DE DADOS:")
    
    test_queries = [
        ("sample_api", "posts about technology"),
        ("local_documents", "financial reports")
    ]
    
    for source_id, query in test_queries:
        if source_id in adapter.connectors:
            print(f"\n🔍 Buscando em {source_id}: {query}")
            
            insight = await adapter.fetch_data(source_id, query)
            
            if insight:
                print(f"   ✅ Insight extraído (ID: {insight.insight_id})")
                print(f"   📈 Confiança: {insight.confidence:.2f}")
                print(f"   💭 Sentimento: {insight.sentiment}")
                print(f"   🔑 Keywords: {', '.join(insight.keywords[:5])}")
                print(f"   🏷️ Entidades: {len(insight.entities)}")
            else:
                print(f"   ❌ Falha na extração")
                
    # Status final
    status = adapter.get_adapter_status()
    print(f"\n📊 STATUS DO ADAPTADOR:")
    print(f"   Fontes configuradas: {status['stats']['sources_configured']}")
    print(f"   Conexões bem-sucedidas: {status['stats']['successful_connections']}")
    print(f"   Insights extraídos: {status['stats']['insights_extracted']}")
    print(f"   Cache hits/misses: {status['stats']['cache_hits']}/{status['stats']['cache_misses']}")
    
    # Insights recentes
    recent_insights = adapter.get_recent_insights(limit=5)
    print(f"\n💡 INSIGHTS RECENTES ({len(recent_insights)}):")
    
    for insight in recent_insights[:3]:
        print(f"   • {insight['insight_id'][:8]}... ({insight['source_id']}) - {insight['sentiment']} - {insight['confidence']:.2f}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
