"""
🌐 AEONCOSMA Expanded P2P Network - Sistema Multi-Node Escalável
Sistema P2P expandido com simulação de nós reais e virtuais
Copyright 2025 - Luiz H. P. Cruz
"""

import asyncio
import json
import time
import random
import hashlib
import socket
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum
import logging
import struct
import pickle
import networkx as nx
import numpy as np

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class NodeType(Enum):
    MASTER = "master"
    ENERGY = "energy"
    AI = "ai"
    CRYPTO = "crypto"
    QUANTUM = "quantum"
    COSMOS = "cosmos"
    BACKUP = "backup"
    EDGE = "edge"
    VALIDATOR = "validator"
    STORAGE = "storage"

class NodeStatus(Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    WARNING = "warning"
    SYNCHRONIZING = "synchronizing"
    MAINTENANCE = "maintenance"

@dataclass
class NetworkMessage:
    id: str
    sender: str
    receiver: str
    msg_type: str
    content: Dict[str, Any]
    timestamp: datetime
    ttl: int = 10
    priority: int = 5
    signature: Optional[str] = None
    encrypted: bool = False

@dataclass
class NodeMetrics:
    cpu_usage: float
    memory_usage: float
    network_load: float
    disk_usage: float
    uptime: float
    connections: int
    messages_sent: int
    messages_received: int
    bytes_sent: int
    bytes_received: int
    last_activity: datetime

@dataclass
class NodeInfo:
    id: str
    type: NodeType
    status: NodeStatus
    location: str
    coordinates: tuple
    specialty: str
    version: str
    capabilities: List[str]
    metrics: NodeMetrics
    peers: List[str]
    blockchain_height: int = 0
    reputation_score: float = 1.0

class AdvancedP2PNode:
    def __init__(self, node_info: NodeInfo, port: int = None):
        self.info = node_info
        self.port = port or random.randint(8000, 9000)
        self.running = False
        self.socket = None
        self.connections = {}
        self.message_queue = asyncio.Queue()
        self.blockchain = []
        self.pending_transactions = []
        self.ai_models = {}
        self.crypto_keys = {}
        self.quantum_state = {}
        self.cosmos_data = {}
        
        # Buffers de histórico
        self.message_history = []
        self.performance_history = []
        self.error_log = []
        
    async def start(self):
        """Iniciar o nó P2P"""
        self.running = True
        logger.info(f"🚀 Iniciando nó {self.info.id} na porta {self.port}")
        
        # Inicializar serviços específicos do tipo de nó
        await self._initialize_services()
        
        # Iniciar tarefas assíncronas
        tasks = [
            asyncio.create_task(self._network_listener()),
            asyncio.create_task(self._message_processor()),
            asyncio.create_task(self._metrics_updater()),
            asyncio.create_task(self._peer_discovery()),
            asyncio.create_task(self._blockchain_sync()),
        ]
        
        # Adicionar tarefas específicas por tipo
        if self.info.type == NodeType.AI:
            tasks.append(asyncio.create_task(self._ai_training_loop()))
        elif self.info.type == NodeType.CRYPTO:
            tasks.append(asyncio.create_task(self._crypto_operations()))
        elif self.info.type == NodeType.QUANTUM:
            tasks.append(asyncio.create_task(self._quantum_processing()))
        elif self.info.type == NodeType.COSMOS:
            tasks.append(asyncio.create_task(self._cosmos_analysis()))
        
        await asyncio.gather(*tasks)
    
    async def _initialize_services(self):
        """Inicializar serviços específicos do nó"""
        if self.info.type == NodeType.AI:
            self.ai_models = {
                "energy_predictor": {"accuracy": 0.94, "status": "trained"},
                "anomaly_detector": {"accuracy": 0.89, "status": "training"},
                "optimization_engine": {"accuracy": 0.91, "status": "deployed"}
            }
        
        elif self.info.type == NodeType.CRYPTO:
            self.crypto_keys = {
                "aes_key": self._generate_key(32),
                "rsa_private": self._generate_key(256),
                "rsa_public": self._generate_key(256),
                "quantum_key": self._generate_key(64)
            }
        
        elif self.info.type == NodeType.QUANTUM:
            self.quantum_state = {
                "qubits": 256,
                "fidelity": 0.97,
                "entanglement_pairs": 128,
                "noise_level": 0.02
            }
        
        elif self.info.type == NodeType.COSMOS:
            self.cosmos_data = {
                "h0_current": 67.4,
                "omega_m": 0.315,
                "omega_lambda": 0.685,
                "age_universe": 13.8,
                "last_analysis": datetime.now()
            }
    
    def _generate_key(self, length: int) -> str:
        """Gerar chave criptográfica simulada"""
        return hashlib.sha256(f"{self.info.id}{time.time()}{length}".encode()).hexdigest()[:length]
    
    async def _network_listener(self):
        """Escutar conexões de rede"""
        while self.running:
            try:
                # Simular chegada de conexões
                if random.random() < 0.1:  # 10% chance
                    peer_id = f"peer_{random.randint(1000, 9999)}"
                    await self._handle_new_connection(peer_id)
                
                await asyncio.sleep(1)
            except Exception as e:
                logger.error(f"Erro no listener de {self.info.id}: {e}")
    
    async def _handle_new_connection(self, peer_id: str):
        """Processar nova conexão"""
        if peer_id not in self.connections:
            self.connections[peer_id] = {
                "connected_at": datetime.now(),
                "status": "active",
                "messages_exchanged": 0
            }
            self.info.metrics.connections = len(self.connections)
            logger.info(f"🔗 {self.info.id} conectado com {peer_id}")
    
    async def _message_processor(self):
        """Processar mensagens da fila"""
        while self.running:
            try:
                if not self.message_queue.empty():
                    message = await self.message_queue.get()
                    await self._process_message(message)
                
                await asyncio.sleep(0.1)
            except Exception as e:
                logger.error(f"Erro no processador de mensagens de {self.info.id}: {e}")
    
    async def _process_message(self, message: NetworkMessage):
        """Processar mensagem individual"""
        try:
            # Atualizar métricas
            self.info.metrics.messages_received += 1
            self.info.metrics.bytes_received += len(str(message.content))
            self.info.metrics.last_activity = datetime.now()
            
            # Processar por tipo de mensagem
            if message.msg_type == "ping":
                await self._send_pong(message.sender)
            elif message.msg_type == "blockchain_sync":
                await self._sync_blockchain(message.content)
            elif message.msg_type == "ai_training":
                await self._process_ai_training(message.content)
            elif message.msg_type == "crypto_operation":
                await self._process_crypto_operation(message.content)
            elif message.msg_type == "quantum_transmission":
                await self._process_quantum_transmission(message.content)
            elif message.msg_type == "cosmos_data":
                await self._process_cosmos_data(message.content)
            
            # Adicionar ao histórico
            self.message_history.append(message)
            if len(self.message_history) > 1000:  # Limitar histórico
                self.message_history = self.message_history[-1000:]
            
            logger.info(f"📨 {self.info.id} processou mensagem {message.msg_type} de {message.sender}")
            
        except Exception as e:
            logger.error(f"Erro processando mensagem em {self.info.id}: {e}")
            self.error_log.append({"timestamp": datetime.now(), "error": str(e)})
    
    async def _send_pong(self, peer_id: str):
        """Enviar resposta pong"""
        pong_message = NetworkMessage(
            id=f"pong_{int(time.time() * 1000)}",
            sender=self.info.id,
            receiver=peer_id,
            msg_type="pong",
            content={"timestamp": datetime.now().isoformat()},
            timestamp=datetime.now()
        )
        await self._send_message(pong_message)
    
    async def _send_message(self, message: NetworkMessage):
        """Enviar mensagem para a rede"""
        # Simular latência de rede
        latency = random.uniform(0.01, 0.2)
        await asyncio.sleep(latency)
        
        # Atualizar métricas
        self.info.metrics.messages_sent += 1
        self.info.metrics.bytes_sent += len(str(message.content))
        
        logger.info(f"📤 {self.info.id} enviou {message.msg_type} para {message.receiver}")
    
    async def _metrics_updater(self):
        """Atualizar métricas do nó"""
        while self.running:
            try:
                # Simular mudanças nas métricas
                metrics = self.info.metrics
                
                # CPU usage
                metrics.cpu_usage += random.uniform(-5, 5)
                metrics.cpu_usage = max(5, min(95, metrics.cpu_usage))
                
                # Memory usage
                metrics.memory_usage += random.uniform(-3, 3)
                metrics.memory_usage = max(10, min(85, metrics.memory_usage))
                
                # Network load
                metrics.network_load += random.uniform(-10, 10)
                metrics.network_load = max(0, min(100, metrics.network_load))
                
                # Disk usage
                metrics.disk_usage += random.uniform(-1, 1)
                metrics.disk_usage = max(10, min(90, metrics.disk_usage))
                
                # Uptime
                metrics.uptime += 1/60  # Incrementar em minutos
                
                # Adicionar ao histórico de performance
                self.performance_history.append({
                    "timestamp": datetime.now(),
                    "cpu": metrics.cpu_usage,
                    "memory": metrics.memory_usage,
                    "network": metrics.network_load,
                    "disk": metrics.disk_usage
                })
                
                if len(self.performance_history) > 100:
                    self.performance_history = self.performance_history[-100:]
                
                await asyncio.sleep(60)  # Atualizar a cada minuto
                
            except Exception as e:
                logger.error(f"Erro atualizando métricas de {self.info.id}: {e}")
    
    async def _peer_discovery(self):
        """Descobrir novos peers na rede"""
        while self.running:
            try:
                # Simular descoberta de peers
                if len(self.info.peers) < 8 and random.random() < 0.1:
                    new_peer = f"discovered_peer_{random.randint(1000, 9999)}"
                    if new_peer not in self.info.peers:
                        self.info.peers.append(new_peer)
                        logger.info(f"🔍 {self.info.id} descobriu novo peer: {new_peer}")
                
                await asyncio.sleep(30)  # Descobrir a cada 30 segundos
                
            except Exception as e:
                logger.error(f"Erro na descoberta de peers de {self.info.id}: {e}")
    
    async def _blockchain_sync(self):
        """Sincronizar blockchain"""
        while self.running:
            try:
                # Simular sincronização de blockchain
                if random.random() < 0.2:  # 20% chance
                    new_block = {
                        "height": self.info.blockchain_height + 1,
                        "hash": hashlib.sha256(f"{self.info.id}{time.time()}".encode()).hexdigest(),
                        "timestamp": datetime.now().isoformat(),
                        "transactions": len(self.pending_transactions),
                        "miner": self.info.id
                    }
                    
                    self.blockchain.append(new_block)
                    self.info.blockchain_height += 1
                    self.pending_transactions = []
                    
                    logger.info(f"⛓️ {self.info.id} minerou bloco #{self.info.blockchain_height}")
                
                await asyncio.sleep(45)  # Minerar a cada 45 segundos
                
            except Exception as e:
                logger.error(f"Erro na sincronização blockchain de {self.info.id}: {e}")
    
    async def _ai_training_loop(self):
        """Loop de treinamento de IA (apenas para nós AI)"""
        while self.running:
            try:
                for model_name, model_info in self.ai_models.items():
                    if model_info["status"] == "training":
                        # Simular progresso de treinamento
                        model_info["accuracy"] += random.uniform(0.001, 0.01)
                        model_info["accuracy"] = min(0.99, model_info["accuracy"])
                        
                        if model_info["accuracy"] > 0.95:
                            model_info["status"] = "trained"
                            logger.info(f"🧠 {self.info.id} completou treinamento de {model_name}")
                
                await asyncio.sleep(10)
                
            except Exception as e:
                logger.error(f"Erro no loop de IA de {self.info.id}: {e}")
    
    async def _crypto_operations(self):
        """Operações criptográficas (apenas para nós CRYPTO)"""
        while self.running:
            try:
                # Simular operações criptográficas
                operations = ["encrypt", "decrypt", "sign", "verify", "key_exchange"]
                operation = random.choice(operations)
                
                # Simular tempo de processamento
                processing_time = random.uniform(0.1, 2.0)
                await asyncio.sleep(processing_time)
                
                success = random.random() > 0.05  # 95% de sucesso
                
                if success:
                    logger.info(f"🔐 {self.info.id} completou operação {operation}")
                else:
                    logger.warning(f"⚠️ {self.info.id} falhou em operação {operation}")
                
                await asyncio.sleep(5)
                
            except Exception as e:
                logger.error(f"Erro nas operações crypto de {self.info.id}: {e}")
    
    async def _quantum_processing(self):
        """Processamento quântico (apenas para nós QUANTUM)"""
        while self.running:
            try:
                # Simular processamento quântico
                self.quantum_state["fidelity"] += random.uniform(-0.01, 0.01)
                self.quantum_state["fidelity"] = max(0.9, min(0.99, self.quantum_state["fidelity"]))
                
                self.quantum_state["noise_level"] += random.uniform(-0.005, 0.005)
                self.quantum_state["noise_level"] = max(0.01, min(0.1, self.quantum_state["noise_level"]))
                
                if random.random() < 0.1:  # 10% chance de transmissão
                    logger.info(f"📡 {self.info.id} completou transmissão quântica com fidelidade {self.quantum_state['fidelity']:.3f}")
                
                await asyncio.sleep(8)
                
            except Exception as e:
                logger.error(f"Erro no processamento quântico de {self.info.id}: {e}")
    
    async def _cosmos_analysis(self):
        """Análise cosmológica (apenas para nós COSMOS)"""
        while self.running:
            try:
                # Simular análise cosmológica
                self.cosmos_data["h0_current"] += random.uniform(-0.1, 0.1)
                self.cosmos_data["h0_current"] = max(65.0, min(70.0, self.cosmos_data["h0_current"]))
                
                self.cosmos_data["omega_m"] += random.uniform(-0.01, 0.01)
                self.cosmos_data["omega_m"] = max(0.25, min(0.35, self.cosmos_data["omega_m"]))
                
                self.cosmos_data["last_analysis"] = datetime.now()
                
                if random.random() < 0.05:  # 5% chance de análise completa
                    logger.info(f"🌌 {self.info.id} completou análise: H₀={self.cosmos_data['h0_current']:.2f}")
                
                await asyncio.sleep(20)
                
            except Exception as e:
                logger.error(f"Erro na análise cosmológica de {self.info.id}: {e}")
    
    async def _process_ai_training(self, content: Dict[str, Any]):
        """Processar solicitação de treinamento de IA"""
        if self.info.type == NodeType.AI:
            model_name = content.get("model", "default")
            if model_name in self.ai_models:
                self.ai_models[model_name]["status"] = "training"
                logger.info(f"🧠 {self.info.id} iniciou treinamento de {model_name}")
    
    async def _process_crypto_operation(self, content: Dict[str, Any]):
        """Processar operação criptográfica"""
        if self.info.type == NodeType.CRYPTO:
            operation = content.get("operation", "encrypt")
            logger.info(f"🔐 {self.info.id} processando {operation}")
    
    async def _process_quantum_transmission(self, content: Dict[str, Any]):
        """Processar transmissão quântica"""
        if self.info.type == NodeType.QUANTUM:
            qubits = content.get("qubits", 256)
            logger.info(f"📡 {self.info.id} processando {qubits} qubits")
    
    async def _process_cosmos_data(self, content: Dict[str, Any]):
        """Processar dados cosmológicos"""
        if self.info.type == NodeType.COSMOS:
            data_type = content.get("type", "supernovae")
            logger.info(f"🌌 {self.info.id} analisando dados {data_type}")
    
    async def _sync_blockchain(self, content: Dict[str, Any]):
        """Sincronizar blockchain com outros nós"""
        remote_height = content.get("height", 0)
        if remote_height > self.info.blockchain_height:
            # Simular sincronização
            self.info.blockchain_height = remote_height
            logger.info(f"⛓️ {self.info.id} sincronizado até bloco #{remote_height}")
    
    def stop(self):
        """Parar o nó"""
        self.running = False
        logger.info(f"🛑 Parando nó {self.info.id}")
    
    def get_status(self) -> Dict[str, Any]:
        """Obter status completo do nó"""
        return {
            "info": asdict(self.info),
            "connections": len(self.connections),
            "message_queue_size": self.message_queue.qsize(),
            "blockchain_height": self.info.blockchain_height,
            "ai_models": self.ai_models if self.info.type == NodeType.AI else None,
            "crypto_keys": list(self.crypto_keys.keys()) if self.info.type == NodeType.CRYPTO else None,
            "quantum_state": self.quantum_state if self.info.type == NodeType.QUANTUM else None,
            "cosmos_data": self.cosmos_data if self.info.type == NodeType.COSMOS else None,
            "performance_history": self.performance_history[-10:],  # Últimas 10 métricas
            "recent_messages": len(self.message_history[-50:]),  # Últimas 50 mensagens
            "error_count": len(self.error_log)
        }

class ExpandedP2PNetwork:
    def __init__(self):
        self.nodes: Dict[str, AdvancedP2PNode] = {}
        self.network_graph = nx.Graph()
        self.running = False
        self.message_broker = []
        self.global_stats = {
            "total_nodes": 0,
            "active_connections": 0,
            "total_messages": 0,
            "blockchain_height": 0,
            "network_health": 1.0
        }
    
    def create_node_fleet(self, count: int = 50):
        """Criar frota expandida de nós"""
        logger.info(f"🚀 Criando frota de {count} nós...")
        
        # Configurações de nós por tipo
        node_configs = [
            # Nós Master (2)
            {"type": NodeType.MASTER, "count": 2, "locations": ["São Paulo", "Rio de Janeiro"]},
            
            # Nós de Energia (15)
            {"type": NodeType.ENERGY, "count": 15, "locations": [
                "São Paulo", "Rio de Janeiro", "Brasília", "Belo Horizonte", "Salvador",
                "Curitiba", "Porto Alegre", "Recife", "Fortaleza", "Manaus",
                "Goiânia", "Campinas", "Santos", "Guarulhos", "São Bernardo"
            ]},
            
            # Nós de IA (8)
            {"type": NodeType.AI, "count": 8, "locations": [
                "Campinas", "São Carlos", "Florianópolis", "Porto Alegre",
                "Belo Horizonte", "Brasília", "Rio de Janeiro", "São Paulo"
            ]},
            
            # Nós Crypto (6)
            {"type": NodeType.CRYPTO, "count": 6, "locations": [
                "São Paulo", "Rio de Janeiro", "Brasília", "Belo Horizonte",
                "Porto Alegre", "Salvador"
            ]},
            
            # Nós Quantum (4)
            {"type": NodeType.QUANTUM, "count": 4, "locations": [
                "São Paulo", "Rio de Janeiro", "Campinas", "Florianópolis"
            ]},
            
            # Nós Cosmos (3)
            {"type": NodeType.COSMOS, "count": 3, "locations": [
                "São Paulo", "Rio de Janeiro", "Brasília"
            ]},
            
            # Nós de Backup (6)
            {"type": NodeType.BACKUP, "count": 6, "locations": [
                "Salvador", "Recife", "Fortaleza", "Belém", "Manaus", "Cuiabá"
            ]},
            
            # Nós Edge (4)
            {"type": NodeType.EDGE, "count": 4, "locations": [
                "Manaus", "Boa Vista", "Porto Velho", "Rio Branco"
            ]},
            
            # Nós Validator (2)
            {"type": NodeType.VALIDATOR, "count": 2, "locations": [
                "São Paulo", "Brasília"
            ]}
        ]
        
        node_counter = 0
        for config in node_configs:
            for i in range(min(config["count"], len(config["locations"]))):
                if node_counter >= count:
                    break
                
                location = config["locations"][i]
                node_id = f"{config['type'].value}_{location.lower().replace(' ', '_')}_{i+1}"
                
                # Criar métricas iniciais
                metrics = NodeMetrics(
                    cpu_usage=random.uniform(20, 80),
                    memory_usage=random.uniform(30, 70),
                    network_load=random.uniform(10, 90),
                    disk_usage=random.uniform(40, 80),
                    uptime=random.uniform(1, 168),
                    connections=0,
                    messages_sent=0,
                    messages_received=0,
                    bytes_sent=0,
                    bytes_received=0,
                    last_activity=datetime.now()
                )
                
                # Criar informações do nó
                node_info = NodeInfo(
                    id=node_id,
                    type=config["type"],
                    status=NodeStatus.ONLINE if random.random() > 0.1 else NodeStatus.WARNING,
                    location=location,
                    coordinates=self._get_coordinates(location),
                    specialty=self._get_specialty(config["type"]),
                    version="1.0.0",
                    capabilities=self._get_capabilities(config["type"]),
                    metrics=metrics,
                    peers=[],
                    blockchain_height=random.randint(1000, 1500),
                    reputation_score=random.uniform(0.8, 1.0)
                )
                
                # Criar e adicionar nó
                node = AdvancedP2PNode(node_info, port=8000 + node_counter)
                self.nodes[node_id] = node
                self.network_graph.add_node(node_id, **asdict(node_info))
                
                node_counter += 1
        
        self._create_network_topology()
        logger.info(f"✅ Criados {len(self.nodes)} nós na rede expandida")
    
    def _get_coordinates(self, location: str) -> tuple:
        """Obter coordenadas da localização"""
        coords_map = {
            "São Paulo": (-23.5505, -46.6333),
            "Rio de Janeiro": (-22.9068, -43.1729),
            "Brasília": (-15.7942, -47.8822),
            "Belo Horizonte": (-19.9167, -43.9345),
            "Salvador": (-12.9777, -38.5016),
            "Curitiba": (-25.4284, -49.2733),
            "Porto Alegre": (-30.0346, -51.2177),
            "Recife": (-8.0476, -34.8770),
            "Fortaleza": (-3.7319, -38.5267),
            "Manaus": (-3.1190, -60.0217),
            "Goiânia": (-16.6869, -49.2648),
            "Campinas": (-22.9099, -47.0626),
            "Santos": (-23.9618, -46.3322),
            "Guarulhos": (-23.4538, -46.5333),
            "São Bernardo": (-23.6944, -46.5653),
            "São Carlos": (-22.0154, -47.8908),
            "Florianópolis": (-27.5954, -48.5480),
            "Belém": (-1.4558, -48.4902),
            "Cuiabá": (-15.6014, -56.0979),
            "Boa Vista": (2.8235, -60.6758),
            "Porto Velho": (-8.7612, -63.9039),
            "Rio Branco": (-9.9754, -67.8249)
        }
        return coords_map.get(location, (0, 0))
    
    def _get_specialty(self, node_type: NodeType) -> str:
        """Obter especialidade do nó"""
        specialties = {
            NodeType.MASTER: "coordination",
            NodeType.ENERGY: "monitoring",
            NodeType.AI: "machine_learning",
            NodeType.CRYPTO: "security",
            NodeType.QUANTUM: "quantum_comm",
            NodeType.COSMOS: "cosmology",
            NodeType.BACKUP: "redundancy",
            NodeType.EDGE: "remote_processing",
            NodeType.VALIDATOR: "consensus",
            NodeType.STORAGE: "data_persistence"
        }
        return specialties.get(node_type, "general")
    
    def _get_capabilities(self, node_type: NodeType) -> List[str]:
        """Obter capacidades do nó"""
        capabilities_map = {
            NodeType.MASTER: ["coordination", "consensus", "routing", "monitoring"],
            NodeType.ENERGY: ["data_collection", "monitoring", "analysis", "alerting"],
            NodeType.AI: ["training", "inference", "optimization", "prediction"],
            NodeType.CRYPTO: ["encryption", "decryption", "signing", "verification", "key_management"],
            NodeType.QUANTUM: ["quantum_key_distribution", "entanglement", "quantum_teleportation"],
            NodeType.COSMOS: ["data_analysis", "parameter_fitting", "statistical_modeling"],
            NodeType.BACKUP: ["data_replication", "disaster_recovery", "synchronization"],
            NodeType.EDGE: ["local_processing", "caching", "offline_operation"],
            NodeType.VALIDATOR: ["transaction_validation", "consensus_participation", "block_validation"],
            NodeType.STORAGE: ["data_persistence", "replication", "backup", "archival"]
        }
        return capabilities_map.get(node_type, ["basic_operations"])
    
    def _create_network_topology(self):
        """Criar topologia de rede realista"""
        node_ids = list(self.nodes.keys())
        
        # Conectar nós master a muitos outros
        master_nodes = [nid for nid in node_ids if "master" in nid]
        for master in master_nodes:
            # Master conecta com 60-80% dos outros nós
            connection_count = int(len(node_ids) * random.uniform(0.6, 0.8))
            targets = random.sample([nid for nid in node_ids if nid != master], connection_count)
            
            for target in targets:
                self.network_graph.add_edge(master, target)
                self.nodes[master].info.peers.append(target)
                self.nodes[target].info.peers.append(master)
        
        # Conectar nós por região (baseado na proximidade geográfica)
        for node_id, node in self.nodes.items():
            if node_id not in master_nodes:
                # Encontrar nós próximos geograficamente
                nearby_nodes = self._find_nearby_nodes(node_id, max_distance=1000)
                connection_count = random.randint(3, 8)
                
                targets = random.sample(nearby_nodes, min(connection_count, len(nearby_nodes)))
                for target in targets:
                    if not self.network_graph.has_edge(node_id, target):
                        self.network_graph.add_edge(node_id, target)
                        self.nodes[node_id].info.peers.append(target)
                        self.nodes[target].info.peers.append(node_id)
        
        # Conectar nós por tipo (especialidade)
        for node_type in NodeType:
            type_nodes = [nid for nid in node_ids if self.nodes[nid].info.type == node_type]
            
            # Conectar nós do mesmo tipo entre si
            for i, node1 in enumerate(type_nodes):
                for node2 in type_nodes[i+1:]:
                    if random.random() < 0.4:  # 40% chance de conexão
                        if not self.network_graph.has_edge(node1, node2):
                            self.network_graph.add_edge(node1, node2)
                            self.nodes[node1].info.peers.append(node2)
                            self.nodes[node2].info.peers.append(node1)
        
        # Atualizar contador de conexões
        for node_id, node in self.nodes.items():
            node.info.metrics.connections = len(node.info.peers)
        
        logger.info(f"🔗 Topologia criada: {len(self.network_graph.edges)} conexões")
    
    def _find_nearby_nodes(self, node_id: str, max_distance: float = 500) -> List[str]:
        """Encontrar nós próximos geograficamente"""
        node = self.nodes[node_id]
        node_lat, node_lon = node.info.coordinates
        
        nearby = []
        for other_id, other_node in self.nodes.items():
            if other_id == node_id:
                continue
            
            other_lat, other_lon = other_node.info.coordinates
            
            # Calcular distância aproximada em km
            distance = self._calculate_distance(node_lat, node_lon, other_lat, other_lon)
            
            if distance <= max_distance:
                nearby.append(other_id)
        
        return nearby
    
    def _calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calcular distância entre duas coordenadas"""
        import math
        
        R = 6371  # Raio da Terra em km
        
        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)
        
        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad
        
        a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        
        distance = R * c
        return distance
    
    async def start_network(self):
        """Iniciar toda a rede"""
        logger.info("🌐 Iniciando rede P2P expandida...")
        self.running = True
        
        # Iniciar todos os nós
        tasks = []
        for node in self.nodes.values():
            tasks.append(asyncio.create_task(node.start()))
        
        # Iniciar serviços globais
        tasks.append(asyncio.create_task(self._network_monitor()))
        tasks.append(asyncio.create_task(self._message_relay()))
        tasks.append(asyncio.create_task(self._failure_simulation()))
        
        await asyncio.gather(*tasks)
    
    async def _network_monitor(self):
        """Monitorar saúde geral da rede"""
        while self.running:
            try:
                # Atualizar estatísticas globais
                active_nodes = sum(1 for node in self.nodes.values() 
                                 if node.info.status == NodeStatus.ONLINE)
                
                total_connections = sum(len(node.info.peers) for node in self.nodes.values())
                
                total_messages = sum(node.info.metrics.messages_sent + node.info.metrics.messages_received 
                                   for node in self.nodes.values())
                
                avg_blockchain_height = np.mean([node.info.blockchain_height for node in self.nodes.values()])
                
                network_health = active_nodes / len(self.nodes) if self.nodes else 0
                
                self.global_stats.update({
                    "total_nodes": len(self.nodes),
                    "active_nodes": active_nodes,
                    "active_connections": total_connections // 2,  # Dividir por 2 pois são bidirecionais
                    "total_messages": total_messages,
                    "blockchain_height": int(avg_blockchain_height),
                    "network_health": network_health
                })
                
                if active_nodes < len(self.nodes) * 0.8:  # Menos de 80% online
                    logger.warning(f"⚠️ Saúde da rede degradada: {network_health:.1%}")
                
                await asyncio.sleep(30)  # Monitorar a cada 30 segundos
                
            except Exception as e:
                logger.error(f"Erro no monitor de rede: {e}")
    
    async def _message_relay(self):
        """Repassar mensagens entre nós"""
        while self.running:
            try:
                # Simular relay de mensagens
                if random.random() < 0.3:  # 30% chance
                    sender_id = random.choice(list(self.nodes.keys()))
                    sender = self.nodes[sender_id]
                    
                    if sender.info.peers:
                        receiver_id = random.choice(sender.info.peers)
                        
                        message = NetworkMessage(
                            id=f"relay_{int(time.time() * 1000)}",
                            sender=sender_id,
                            receiver=receiver_id,
                            msg_type=random.choice(["ping", "data_sync", "blockchain_sync", "heartbeat"]),
                            content={"relay_timestamp": datetime.now().isoformat()},
                            timestamp=datetime.now()
                        )
                        
                        await sender.message_queue.put(message)
                
                await asyncio.sleep(1)
                
            except Exception as e:
                logger.error(f"Erro no relay de mensagens: {e}")
    
    async def _failure_simulation(self):
        """Simular falhas de rede e recuperação"""
        while self.running:
            try:
                # Simular falhas ocasionais
                if random.random() < 0.02:  # 2% chance de falha
                    online_nodes = [nid for nid, node in self.nodes.items() 
                                  if node.info.status == NodeStatus.ONLINE]
                    
                    if online_nodes:
                        failing_node_id = random.choice(online_nodes)
                        self.nodes[failing_node_id].info.status = NodeStatus.WARNING
                        logger.warning(f"⚠️ Nó {failing_node_id} com problemas")
                
                # Simular recuperação
                if random.random() < 0.1:  # 10% chance de recuperação
                    warning_nodes = [nid for nid, node in self.nodes.items() 
                                   if node.info.status == NodeStatus.WARNING]
                    
                    if warning_nodes:
                        recovering_node_id = random.choice(warning_nodes)
                        self.nodes[recovering_node_id].info.status = NodeStatus.ONLINE
                        logger.info(f"✅ Nó {recovering_node_id} recuperado")
                
                await asyncio.sleep(60)  # Verificar a cada minuto
                
            except Exception as e:
                logger.error(f"Erro na simulação de falhas: {e}")
    
    def stop_network(self):
        """Parar toda a rede"""
        logger.info("🛑 Parando rede P2P...")
        self.running = False
        
        for node in self.nodes.values():
            node.stop()
    
    def get_network_status(self) -> Dict[str, Any]:
        """Obter status completo da rede"""
        return {
            "global_stats": self.global_stats,
            "topology": {
                "nodes": len(self.network_graph.nodes),
                "edges": len(self.network_graph.edges),
                "density": nx.density(self.network_graph),
                "connected_components": nx.number_connected_components(self.network_graph)
            },
            "node_distribution": {
                node_type.value: len([n for n in self.nodes.values() if n.info.type == node_type])
                for node_type in NodeType
            },
            "performance_summary": {
                "avg_cpu": np.mean([n.info.metrics.cpu_usage for n in self.nodes.values()]),
                "avg_memory": np.mean([n.info.metrics.memory_usage for n in self.nodes.values()]),
                "avg_network": np.mean([n.info.metrics.network_load for n in self.nodes.values()]),
                "total_uptime": sum([n.info.metrics.uptime for n in self.nodes.values()])
            }
        }

# Função principal para demonstração
async def run_expanded_network_demo():
    """Executar demonstração da rede expandida"""
    logger.info("🚀 AEONCOSMA Expanded P2P Network Demo")
    
    # Criar rede expandida
    network = ExpandedP2PNetwork()
    network.create_node_fleet(count=25)  # Criar 25 nós para demo
    
    try:
        # Executar por tempo limitado para demo
        await asyncio.wait_for(network.start_network(), timeout=300)  # 5 minutos
    except asyncio.TimeoutError:
        logger.info("⏰ Demo concluída após 5 minutos")
    except KeyboardInterrupt:
        logger.info("⏹️ Demo interrompida pelo usuário")
    finally:
        network.stop_network()
        
        # Mostrar estatísticas finais
        final_stats = network.get_network_status()
        logger.info(f"📊 Estatísticas finais: {json.dumps(final_stats, indent=2, default=str)}")

if __name__ == "__main__":
    asyncio.run(run_expanded_network_demo())
