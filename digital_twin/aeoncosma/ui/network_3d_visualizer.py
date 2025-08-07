#!/usr/bin/env python3
"""
🌐 AEONCOSMA 3D Network Visualizer
Visualizador 3D em tempo real da rede P2P usando NetworkX + Streamlit
Autor: Luiz H. P. Cruz
Copyright 2025
"""

import streamlit as st
import networkx as nx
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import json
import time
import random
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple
import math
from collections import defaultdict

# Configuração da página
st.set_page_config(
    page_title="AEONCOSMA 3D Network Visualizer",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NetworkNode:
    """Representa um nó na rede"""
    
    def __init__(self, node_id: str, node_type: str, position: Tuple[float, float, float] = None):
        self.node_id = node_id
        self.node_type = node_type
        self.position = position or (random.uniform(-10, 10), random.uniform(-10, 10), random.uniform(-10, 10))
        self.connections = set()
        self.status = "online"
        self.cpu_usage = random.uniform(20, 80)
        self.memory_usage = random.uniform(30, 70)
        self.bandwidth_usage = random.uniform(10, 90)
        self.latency = random.uniform(15, 100)
        self.consensus_participation = random.choice([True, False])
        self.last_seen = datetime.now()
        self.metrics_history = []
        self.anomaly_score = 0.0
        
    def update_metrics(self):
        """Atualiza métricas do nó"""
        # Simulação de variação natural
        self.cpu_usage = max(0, min(100, self.cpu_usage + random.uniform(-5, 5)))
        self.memory_usage = max(0, min(100, self.memory_usage + random.uniform(-3, 3)))
        self.bandwidth_usage = max(0, min(100, self.bandwidth_usage + random.uniform(-10, 10)))
        self.latency = max(5, self.latency + random.uniform(-10, 10))
        self.consensus_participation = random.random() < 0.85
        self.last_seen = datetime.now()
        
        # Adicionar à história
        self.metrics_history.append({
            "timestamp": datetime.now(),
            "cpu": self.cpu_usage,
            "memory": self.memory_usage,
            "bandwidth": self.bandwidth_usage,
            "latency": self.latency
        })
        
        # Manter apenas últimas 100 entradas
        if len(self.metrics_history) > 100:
            self.metrics_history = self.metrics_history[-100:]
        
        # Calcular score de anomalia
        self._calculate_anomaly_score()
    
    def _calculate_anomaly_score(self):
        """Calcula score de anomalia baseado nas métricas"""
        score = 0.0
        
        # CPU muito alto ou muito baixo
        if self.cpu_usage > 90 or self.cpu_usage < 5:
            score += 0.3
        
        # Memória muito alta
        if self.memory_usage > 85:
            score += 0.2
        
        # Latência muito alta
        if self.latency > 150:
            score += 0.3
        
        # Não participação no consenso
        if not self.consensus_participation:
            score += 0.2
        
        # Análise de tendência (se há histórico)
        if len(self.metrics_history) >= 10:
            recent_cpu = [m["cpu"] for m in self.metrics_history[-10:]]
            cpu_trend = np.polyfit(range(len(recent_cpu)), recent_cpu, 1)[0]
            if cpu_trend > 5:  # CPU crescendo rapidamente
                score += 0.1
        
        self.anomaly_score = min(1.0, score)
    
    def get_color(self) -> str:
        """Retorna cor baseada no tipo e status do nó"""
        if self.status != "online":
            return "#8B0000"  # Vermelho escuro para offline
        
        type_colors = {
            # Tipos principais
            "master": "#FF6B6B",     # Vermelho
            "energy": "#4ECDC4",     # Azul-verde
            "ai": "#45B7D1",         # Azul
            "crypto": "#96CEB4",     # Verde
            "quantum": "#FFEAA7",    # Amarelo
            "cosmos": "#DDA0DD",     # Roxo
            "validator": "#98D8C8",  # Verde claro
            
            # Tipos de infraestrutura
            "storage": "#FF9F43",    # Laranja
            "compute": "#546DE5",    # Azul escuro
            "gateway": "#26DE81",    # Verde brilhante
            "oracle": "#FD79A8",     # Rosa
            "relay": "#FDCB6E",      # Amarelo dourado
            "monitor": "#6C5CE7",    # Roxo azulado
            "analyzer": "#A29BFE",   # Lavanda
            "guardian": "#00B894",   # Verde escuro
            "beacon": "#FDCB6E",     # Dourado
            
            # Tipos especializados
            "hub": "#E17055",        # Coral
            "bridge": "#81ECEC",     # Ciano
            "mesh": "#55A3FF",       # Azul médio
            "sensor": "#FD79A8",     # Rosa claro
            "actuator": "#FDCB6E",   # Amarelo suave
            "controller": "#6C5CE7", # Roxo médio
            "processor": "#74B9FF",  # Azul céu
            "transformer": "#00CEC9" # Turquesa
        }
        
        return type_colors.get(self.node_type, "#95A5A6")  # Cinza padrão
    
    def get_size(self) -> float:
        """Retorna tamanho baseado na importância e métricas"""
        # Tamanhos base por tipo de nó
        base_sizes = {
            "master": 25,        # Maior - nós centrais
            "guardian": 22,      # Muito grande - protetor da rede
            "beacon": 18,        # Grande - pontos de referência
            "validator": 16,     # Médio-grande - validação crítica
            "gateway": 15,       # Médio-grande - pontos de acesso
            "hub": 14,           # Médio - centros de conexão
            "ai": 13,            # Médio - processamento inteligente
            "crypto": 12,        # Médio - segurança
            "energy": 12,        # Médio - energia
            "compute": 11,       # Médio - processamento
            "storage": 11,       # Médio - armazenamento
            "quantum": 10,       # Médio-pequeno - especializado
            "cosmos": 10,        # Médio-pequeno - especializado
            "oracle": 10,        # Médio-pequeno - dados
            "relay": 9,          # Pequeno-médio - retransmissão
            "bridge": 9,         # Pequeno-médio - conexão
            "monitor": 8,        # Pequeno-médio - observação
            "analyzer": 8,       # Pequeno-médio - análise
            "controller": 8,     # Pequeno-médio - controle
            "processor": 7,      # Pequeno - processamento local
            "transformer": 7,    # Pequeno - transformação
            "mesh": 6,           # Pequeno - rede básica
            "sensor": 5,         # Muito pequeno - sensoriamento
            "actuator": 5        # Muito pequeno - atuação
        }
        
        base_size = base_sizes.get(self.node_type, 8)
        
        # Aumentar com base na conectividade
        connection_bonus = len(self.connections) * 1.5
        
        # Diminuir se há anomalias
        anomaly_penalty = self.anomaly_score * 8
        
        # Bonus para nós ativos no consenso
        consensus_bonus = 3 if self.consensus_participation else 0
        
        final_size = base_size + connection_bonus + consensus_bonus - anomaly_penalty
        
        return max(3, final_size)  # Tamanho mínimo de 3

class AEONCOSMA3DVisualizer:
    """Visualizador 3D da rede AEONCOSMA"""
    
    def __init__(self):
        self.graph = nx.Graph()
        self.nodes = {}
        self.connections = []
        # Expandindo tipos de nós para uma rede mais rica
        self.node_types = [
            "master", "energy", "ai", "crypto", "quantum", "cosmos", "validator",
            "storage", "compute", "gateway", "oracle", "relay", "monitor", 
            "analyzer", "guardian", "beacon", "hub", "bridge", "mesh",
            "sensor", "actuator", "controller", "processor", "transformer"
        ]
        self.simulation_running = False
        self.metrics_history = []
        self.initialize_network()
    
    def initialize_network(self, num_nodes: int = 75):  # Aumentando de 25 para 75 nós
        """Inicializa a rede com nós distribuídos em 3D"""
        self.nodes.clear()
        self.graph.clear()
        
        # Distribuição específica por tipo de nó - expandida
        node_distribution = {
            "master": 1,        # Nó central principal
            "guardian": 2,      # Nós guardiões
            "beacon": 3,        # Nós beacon de referência
            "validator": 8,     # Nós validadores
            "gateway": 4,       # Gateways de acesso
            "hub": 3,           # Hubs de conexão
            "ai": 6,            # Nós de inteligência artificial
            "crypto": 5,        # Nós de criptografia
            "energy": 6,        # Nós de energia/power
            "compute": 5,       # Nós de computação
            "storage": 4,       # Nós de armazenamento
            "quantum": 4,       # Nós quânticos
            "cosmos": 4,        # Nós cosmológicos
            "oracle": 3,        # Oráculos de dados
            "relay": 5,         # Nós de retransmissão
            "bridge": 3,        # Pontes de conexão
            "monitor": 4,       # Nós de monitoramento
            "analyzer": 3,      # Nós de análise
            "controller": 3,    # Controladores
            "processor": 4,     # Processadores
            "transformer": 3,   # Transformadores
            "mesh": 5,          # Nós de malha
            "sensor": 6,        # Sensores
            "actuator": 4       # Atuadores
        }
        
        node_counter = 0
        
        # Criar nós com distribuição espacial otimizada
        for node_type, count in node_distribution.items():
            for i in range(count):
                pos = self._get_position_by_type(node_type, i, count)
                
                node = NetworkNode(f"{node_type}_{i:03d}", node_type, pos)
                self.nodes[node.node_id] = node
                self.graph.add_node(node.node_id, **self._node_to_dict(node))
                node_counter += 1
        
        # Adicionar nós aleatórios restantes se necessário
        while node_counter < num_nodes:
            node_type = random.choice(["mesh", "sensor", "actuator", "controller", "processor", "transformer"])
            pos = (
                random.uniform(-15, 15),
                random.uniform(-15, 15),
                random.uniform(-15, 15)
            )
            
            node = NetworkNode(f"ext_{node_counter:03d}", node_type, pos)
            self.nodes[node.node_id] = node
            self.graph.add_node(node.node_id, **self._node_to_dict(node))
            node_counter += 1
        
        # Criar conexões inteligentes
        self._create_intelligent_connections()
    
    def _get_position_by_type(self, node_type: str, index: int, total: int) -> Tuple[float, float, float]:
        """Calcula posição 3D baseada no tipo de nó"""
        
        if node_type == "master":
            # Nós master no centro em formação triangular
            if index == 0:
                return (0, 0, 0)
            elif index == 1:
                return (2, 2, 1)
            else:
                return (-2, -2, -1)
        
        elif node_type == "guardian":
            # Guardião no topo
            return (0, 0, 15)
        
        elif node_type == "beacon":
            # Beacons nas extremidades
            if index == 0:
                return (12, 0, 8)
            else:
                return (-12, 0, 8)
        
        elif node_type in ["energy", "cosmos"]:
            # Camada externa em esfera
            radius = 12 + random.uniform(-2, 2)
            theta = (index / total) * 2 * math.pi + random.uniform(-0.3, 0.3)
            phi = math.pi * 0.5 + random.uniform(-0.5, 0.5)
            return (
                radius * math.sin(phi) * math.cos(theta),
                radius * math.sin(phi) * math.sin(theta),
                radius * math.cos(phi)
            )
        
        elif node_type in ["ai", "crypto", "quantum"]:
            # Camada intermediária
            radius = 8 + random.uniform(-2, 2)
            theta = (index / total) * 2 * math.pi + random.uniform(-0.2, 0.2)
            phi = random.uniform(0.3, 2.8)
            return (
                radius * math.sin(phi) * math.cos(theta),
                radius * math.sin(phi) * math.sin(theta),
                radius * math.cos(phi)
            )
        
        elif node_type in ["validator", "storage", "compute"]:
            # Camada interna
            radius = 5 + random.uniform(-1, 1)
            theta = (index / total) * 2 * math.pi
            z = random.uniform(-5, 5)
            return (
                radius * math.cos(theta),
                radius * math.sin(theta),
                z
            )
        
        elif node_type in ["gateway", "relay", "bridge"]:
            # Pontos de acesso nas bordas e pontes
            side = index % 6
            if side == 0:  # Norte
                return (random.uniform(-3, 3), 12, random.uniform(-3, 3))
            elif side == 1:  # Sul
                return (random.uniform(-3, 3), -12, random.uniform(-3, 3))
            elif side == 2:  # Leste
                return (12, random.uniform(-3, 3), random.uniform(-3, 3))
            elif side == 3:  # Oeste
                return (-12, random.uniform(-3, 3), random.uniform(-3, 3))
            elif side == 4:  # Topo
                return (random.uniform(-5, 5), random.uniform(-5, 5), 10)
            else:  # Base
                return (random.uniform(-5, 5), random.uniform(-5, 5), -10)
        
        elif node_type in ["hub", "controller", "processor"]:
            # Nós de processamento e controle em posições intermediárias
            radius = 6 + random.uniform(-1.5, 1.5)
            theta = (index / total) * 2 * math.pi + random.uniform(-0.4, 0.4)
            z = random.uniform(-7, 7)
            return (
                radius * math.cos(theta),
                radius * math.sin(theta),
                z
            )
        
        elif node_type in ["monitor", "analyzer", "oracle"]:
            # Nós de observação e análise em posições elevadas
            radius = 9 + random.uniform(-1, 1)
            theta = (index / total) * 2 * math.pi
            z = random.uniform(5, 12)
            return (
                radius * math.cos(theta),
                radius * math.sin(theta),
                z
            )
        
        elif node_type in ["sensor", "actuator"]:
            # Sensores e atuadores distribuídos na periferia
            radius = 14 + random.uniform(-2, 2)
            theta = random.uniform(0, 2 * math.pi)
            phi = random.uniform(0, math.pi)
            return (
                radius * math.sin(phi) * math.cos(theta),
                radius * math.sin(phi) * math.sin(theta),
                radius * math.cos(phi) * random.uniform(0.7, 1.3)
            )
        
        elif node_type in ["mesh", "transformer"]:
            # Nós de malha e transformação em grid organizado
            grid_size = int(math.ceil(math.sqrt(total)))
            row = index // grid_size
            col = index % grid_size
            
            x = (col - grid_size/2) * 3
            y = (row - grid_size/2) * 3
            z = random.uniform(-3, 3)
            
            return (x, y, z)
        
        else:
            # Distribuição padrão para outros tipos
            return (
                random.uniform(-10, 10),
                random.uniform(-10, 10),
                random.uniform(-10, 10)
            )
        
        # Criar conexões inteligentes
        self._create_intelligent_connections()
    
    def _node_to_dict(self, node: NetworkNode) -> Dict[str, Any]:
        """Converte nó para dicionário"""
        return {
            "type": node.node_type,
            "position": node.position,
            "status": node.status,
            "cpu_usage": node.cpu_usage,
            "memory_usage": node.memory_usage,
            "bandwidth_usage": node.bandwidth_usage,
            "latency": node.latency,
            "consensus_participation": node.consensus_participation,
            "anomaly_score": node.anomaly_score
        }
    
    def _create_intelligent_connections(self):
        """Cria conexões inteligentes baseadas em proximidade, tipo e hierarquia"""
        node_list = list(self.nodes.values())
        
        # Primeiro, criar conexões hierárquicas
        self._create_hierarchical_connections()
        
        # Depois, criar conexões por proximidade
        for node in node_list:
            # Definir número de conexões baseado no tipo
            min_connections, max_connections = self._get_connection_limits(node.node_type)
            
            # Calcular distâncias para outros nós
            distances = []
            for other_node in node_list:
                if other_node.node_id != node.node_id and other_node.node_id not in node.connections:
                    distance = self._calculate_distance(node.position, other_node.position)
                    type_affinity = self._get_type_affinity(node.node_type, other_node.node_type)
                    weighted_distance = distance / type_affinity
                    distances.append((other_node, weighted_distance))
            
            # Ordenar por distância ponderada
            distances.sort(key=lambda x: x[1])
            
            # Conectar aos nós mais próximos
            connections_made = len(node.connections)
            for other_node, _ in distances:
                if connections_made >= max_connections:
                    break
                
                other_min, other_max = self._get_connection_limits(other_node.node_type)
                if len(other_node.connections) < other_max:
                    self._add_connection(node, other_node)
                    connections_made += 1
            
            # Garantir conectividade mínima
            while len(node.connections) < min_connections and distances:
                for other_node, _ in distances:
                    if other_node.node_id not in node.connections:
                        other_min, other_max = self._get_connection_limits(other_node.node_type)
                        if len(other_node.connections) < other_max:
                            self._add_connection(node, other_node)
                            break
                        distances.remove((other_node, _))
                        break
                else:
                    break
    
    def _create_hierarchical_connections(self):
        """Cria conexões hierárquicas entre tipos específicos"""
        masters = [n for n in self.nodes.values() if n.node_type == "master"]
        guardians = [n for n in self.nodes.values() if n.node_type == "guardian"]
        beacons = [n for n in self.nodes.values() if n.node_type == "beacon"]
        validators = [n for n in self.nodes.values() if n.node_type == "validator"]
        gateways = [n for n in self.nodes.values() if n.node_type == "gateway"]
        
        # Conectar guardian aos masters
        for guardian in guardians:
            for master in masters:
                self._add_connection(guardian, master)
        
        # Conectar masters entre si
        for i, master1 in enumerate(masters):
            for master2 in masters[i+1:]:
                self._add_connection(master1, master2)
        
        # Conectar beacons aos masters
        for beacon in beacons:
            for master in masters:
                self._add_connection(beacon, master)
        
        # Conectar validators aos masters
        for validator in validators:
            if masters:
                closest_master = min(masters, key=lambda m: self._calculate_distance(validator.position, m.position))
                self._add_connection(validator, closest_master)
        
        # Conectar gateways aos relays
        relays = [n for n in self.nodes.values() if n.node_type == "relay"]
        for gateway in gateways:
            for relay in relays:
                self._add_connection(gateway, relay)
    
    def _get_connection_limits(self, node_type: str) -> Tuple[int, int]:
        """Retorna limites mínimo e máximo de conexões por tipo de nó"""
        limits = {
            "master": (8, 15),      # Nós centrais altamente conectados
            "guardian": (5, 10),    # Guardian monitora muitos nós
            "beacon": (4, 8),       # Beacons como pontos de referência
            "validator": (3, 6),    # Validadores moderadamente conectados
            "energy": (2, 5),       # Nós de energia
            "ai": (3, 7),           # IAs precisam de boa conectividade
            "crypto": (2, 6),       # Nós de criptografia
            "quantum": (2, 4),      # Nós quânticos especializados
            "cosmos": (2, 4),       # Nós cosmológicos especializados
            "storage": (3, 6),      # Storage precisa de acesso múltiplo
            "compute": (2, 5),      # Nós de computação
            "gateway": (4, 8),      # Gateways conectam muitos
            "oracle": (2, 4),       # Oráculos especializados
            "relay": (3, 6),        # Relays retransmitem
            "monitor": (3, 5),      # Monitores observam vários nós
            "analyzer": (2, 4),     # Analisadores especializados
            "hub": (5, 10),         # Hubs altamente conectados
            "bridge": (4, 6),       # Bridges conectam redes
            "mesh": (2, 4),         # Nós mesh básicos
            "sensor": (1, 3),       # Sensores conexão mínima
            "actuator": (1, 3),     # Atuadores conexão mínima
            "controller": (2, 5),   # Controladores moderados
            "processor": (2, 4),    # Processadores especializados
            "transformer": (2, 4)   # Transformadores especializados
        }
        
        return limits.get(node_type, (2, 4))  # Padrão: 2-4 conexões
    
    def _calculate_distance(self, pos1: Tuple[float, float, float], pos2: Tuple[float, float, float]) -> float:
        """Calcula distância euclidiana 3D"""
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(pos1, pos2)))
    
    def _get_type_affinity(self, type1: str, type2: str) -> float:
        """Retorna afinidade entre tipos de nós (menor = mais afinidade)"""
        affinities = {
            # Conexões hierárquicas principais
            ("master", "guardian"): 0.3,
            ("master", "validator"): 0.4,
            ("master", "beacon"): 0.5,
            ("guardian", "monitor"): 0.4,
            
            # Conexões funcionais especializadas
            ("ai", "quantum"): 0.6,
            ("ai", "analyzer"): 0.5,
            ("ai", "processor"): 0.6,
            ("crypto", "validator"): 0.5,
            ("crypto", "guardian"): 0.6,
            ("energy", "cosmos"): 0.6,
            ("energy", "transformer"): 0.5,
            
            # Conexões de infraestrutura
            ("storage", "compute"): 0.5,
            ("storage", "validator"): 0.6,
            ("gateway", "relay"): 0.4,
            ("gateway", "bridge"): 0.5,
            ("hub", "mesh"): 0.5,
            ("bridge", "relay"): 0.6,
            
            # Conexões de dados e análise
            ("oracle", "analyzer"): 0.4,
            ("oracle", "ai"): 0.6,
            ("monitor", "analyzer"): 0.5,
            ("sensor", "controller"): 0.4,
            ("controller", "actuator"): 0.4,
            
            # Conexões de processamento
            ("compute", "processor"): 0.5,
            ("processor", "transformer"): 0.6,
            ("ai", "compute"): 0.6,
            
            # Conexões quânticas e cosmológicas
            ("quantum", "cosmos"): 0.7,
            ("quantum", "crypto"): 0.6,
            ("cosmos", "analyzer"): 0.7,
            
            # Conexões de rede mesh
            ("mesh", "relay"): 0.6,
            ("mesh", "sensor"): 0.7,
            ("hub", "gateway"): 0.5,
            
            # Conexões especiais de alta prioridade
            ("master", "crypto"): 0.5,
            ("master", "ai"): 0.6,
            ("validator", "storage"): 0.6,
            ("beacon", "relay"): 0.7,
        }
        
        # Verificar ambas as direções da tupla
        key1 = tuple(sorted([type1, type2]))
        key2 = (type1, type2)
        key3 = (type2, type1)
        
        return affinities.get(key1, affinities.get(key2, affinities.get(key3, 1.0)))
    
    def _add_connection(self, node1: NetworkNode, node2: NetworkNode):
        """Adiciona conexão bidirecional entre dois nós"""
        node1.connections.add(node2.node_id)
        node2.connections.add(node1.node_id)
        self.graph.add_edge(node1.node_id, node2.node_id)
    
    def update_network_state(self):
        """Atualiza estado da rede"""
        for node in self.nodes.values():
            node.update_metrics()
            self.graph.nodes[node.node_id].update(self._node_to_dict(node))
        
        # Simular eventos ocasionais
        if random.random() < 0.05:  # 5% chance
            self._simulate_network_event()
        
        # Registrar métricas globais
        self._record_global_metrics()
    
    def _simulate_network_event(self):
        """Simula eventos de rede"""
        event_type = random.choice(["node_failure", "high_traffic", "attack_simulation", "node_recovery"])
        
        if event_type == "node_failure":
            online_nodes = [n for n in self.nodes.values() if n.status == "online"]
            if online_nodes:
                node = random.choice(online_nodes)
                node.status = "offline"
                logger.info(f"Simulação: Nó {node.node_id} ficou offline")
        
        elif event_type == "node_recovery":
            offline_nodes = [n for n in self.nodes.values() if n.status == "offline"]
            if offline_nodes:
                node = random.choice(offline_nodes)
                node.status = "online"
                logger.info(f"Simulação: Nó {node.node_id} voltou online")
        
        elif event_type == "high_traffic":
            # Aumentar latência em alguns nós
            affected_nodes = random.sample(list(self.nodes.values()), min(5, len(self.nodes)))
            for node in affected_nodes:
                node.latency += random.uniform(50, 150)
                node.bandwidth_usage = min(100, node.bandwidth_usage + random.uniform(20, 40))
            logger.info(f"Simulação: Tráfego alto afetou {len(affected_nodes)} nós")
        
        elif event_type == "attack_simulation":
            # Simular ataque aumentando anomaly scores
            target_nodes = random.sample(list(self.nodes.values()), min(3, len(self.nodes)))
            for node in target_nodes:
                node.anomaly_score = min(1.0, node.anomaly_score + random.uniform(0.3, 0.7))
                node.cpu_usage = min(100, node.cpu_usage + random.uniform(20, 50))
            logger.info(f"Simulação: Ataque detectado em {len(target_nodes)} nós")
    
    def _record_global_metrics(self):
        """Registra métricas globais da rede"""
        online_nodes = [n for n in self.nodes.values() if n.status == "online"]
        
        if online_nodes:
            metrics = {
                "timestamp": datetime.now(),
                "total_nodes": len(self.nodes),
                "online_nodes": len(online_nodes),
                "avg_cpu": sum(n.cpu_usage for n in online_nodes) / len(online_nodes),
                "avg_memory": sum(n.memory_usage for n in online_nodes) / len(online_nodes),
                "avg_latency": sum(n.latency for n in online_nodes) / len(online_nodes),
                "consensus_participation": sum(1 for n in online_nodes if n.consensus_participation) / len(online_nodes),
                "avg_anomaly_score": sum(n.anomaly_score for n in online_nodes) / len(online_nodes),
                "total_connections": sum(len(n.connections) for n in online_nodes) // 2  # Dividir por 2 pois são bidirecionais
            }
            
            self.metrics_history.append(metrics)
            
            # Manter apenas últimas 200 entradas
            if len(self.metrics_history) > 200:
                self.metrics_history = self.metrics_history[-200:]
    
    def create_3d_visualization(self) -> go.Figure:
        """Cria visualização 3D da rede"""
        fig = go.Figure()
        
        # Preparar dados dos nós
        node_positions = []
        node_colors = []
        node_sizes = []
        node_texts = []
        node_ids = []
        
        for node in self.nodes.values():
            if node.status == "online":
                node_positions.append(node.position)
                node_colors.append(node.get_color())
                node_sizes.append(node.get_size())
                node_texts.append(
                    f"ID: {node.node_id}<br>"
                    f"Tipo: {node.node_type}<br>"
                    f"CPU: {node.cpu_usage:.1f}%<br>"
                    f"Memória: {node.memory_usage:.1f}%<br>"
                    f"Latência: {node.latency:.1f}ms<br>"
                    f"Consenso: {'Sim' if node.consensus_participation else 'Não'}<br>"
                    f"Anomalia: {node.anomaly_score:.2f}"
                )
                node_ids.append(node.node_id)
        
        if node_positions:
            x_coords, y_coords, z_coords = zip(*node_positions)
            
            # Adicionar nós
            fig.add_trace(go.Scatter3d(
                x=x_coords,
                y=y_coords,
                z=z_coords,
                mode='markers+text',
                marker=dict(
                    size=node_sizes,
                    color=node_colors,
                    opacity=0.8,
                    line=dict(width=2, color='white')
                ),
                text=node_ids,
                textposition="top center",
                hovertext=node_texts,
                hoverinfo='text',
                name="Nós da Rede"
            ))
        
        # Adicionar conexões
        for node in self.nodes.values():
            if node.status == "online":
                for connected_id in node.connections:
                    connected_node = self.nodes.get(connected_id)
                    if connected_node and connected_node.status == "online":
                        # Linha de conexão
                        fig.add_trace(go.Scatter3d(
                            x=[node.position[0], connected_node.position[0]],
                            y=[node.position[1], connected_node.position[1]],
                            z=[node.position[2], connected_node.position[2]],
                            mode='lines',
                            line=dict(
                                color='rgba(100, 100, 100, 0.3)',
                                width=2
                            ),
                            showlegend=False,
                            hoverinfo='skip'
                        ))
        
        # Configurar layout
        fig.update_layout(
            title="AEONCOSMA - Rede 3D em Tempo Real",
            scene=dict(
                xaxis_title="X",
                yaxis_title="Y",
                zaxis_title="Z",
                bgcolor="black",
                xaxis=dict(gridcolor="white", showbackground=True, backgroundcolor="rgb(20, 20, 20)"),
                yaxis=dict(gridcolor="white", showbackground=True, backgroundcolor="rgb(20, 20, 20)"),
                zaxis=dict(gridcolor="white", showbackground=True, backgroundcolor="rgb(20, 20, 20)"),
                camera=dict(
                    eye=dict(x=1.5, y=1.5, z=1.5)
                )
            ),
            paper_bgcolor="black",
            plot_bgcolor="black",
            font=dict(color="white"),
            height=600
        )
        
        return fig
    
    def create_network_stats_charts(self) -> List[go.Figure]:
        """Cria gráficos de estatísticas da rede"""
        charts = []
        
        if not self.metrics_history:
            return charts
        
        # Gráfico de métricas temporais
        df = pd.DataFrame(self.metrics_history)
        
        # Chart 1: Métricas de sistema
        fig1 = make_subplots(
            rows=2, cols=2,
            subplot_titles=('CPU Médio', 'Memória Média', 'Latência Média', 'Participação no Consenso'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        fig1.add_trace(
            go.Scatter(x=df['timestamp'], y=df['avg_cpu'], name='CPU %', line=dict(color='#FF6B6B')),
            row=1, col=1
        )
        
        fig1.add_trace(
            go.Scatter(x=df['timestamp'], y=df['avg_memory'], name='Memória %', line=dict(color='#4ECDC4')),
            row=1, col=2
        )
        
        fig1.add_trace(
            go.Scatter(x=df['timestamp'], y=df['avg_latency'], name='Latência ms', line=dict(color='#45B7D1')),
            row=2, col=1
        )
        
        fig1.add_trace(
            go.Scatter(x=df['timestamp'], y=df['consensus_participation'] * 100, name='Consenso %', line=dict(color='#96CEB4')),
            row=2, col=2
        )
        
        fig1.update_layout(
            title="Métricas Temporais da Rede",
            height=400,
            showlegend=False,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        
        charts.append(fig1)
        
        # Chart 2: Distribuição de tipos de nós
        node_types = [node.node_type for node in self.nodes.values()]
        type_counts = pd.Series(node_types).value_counts()
        
        fig2 = go.Figure(data=[
            go.Pie(
                labels=type_counts.index,
                values=type_counts.values,
                hole=0.3,
                marker_colors=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8']
            )
        ])
        
        fig2.update_layout(
            title="Distribuição de Tipos de Nós",
            height=400,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        
        charts.append(fig2)
        
        # Chart 3: Status da rede
        online_count = len([n for n in self.nodes.values() if n.status == "online"])
        offline_count = len(self.nodes) - online_count
        
        fig3 = go.Figure(data=[
            go.Bar(
                x=['Online', 'Offline'],
                y=[online_count, offline_count],
                marker_color=['#96CEB4', '#FF6B6B']
            )
        ])
        
        fig3.update_layout(
            title="Status dos Nós",
            height=300,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        
        charts.append(fig3)
        
        return charts
    
    def get_network_summary(self) -> Dict[str, Any]:
        """Retorna resumo da rede"""
        online_nodes = [n for n in self.nodes.values() if n.status == "online"]
        
        if not online_nodes:
            return {"error": "Nenhum nó online"}
        
        return {
            "total_nodes": len(self.nodes),
            "online_nodes": len(online_nodes),
            "uptime_ratio": len(online_nodes) / len(self.nodes) * 100,
            "avg_cpu": sum(n.cpu_usage for n in online_nodes) / len(online_nodes),
            "avg_memory": sum(n.memory_usage for n in online_nodes) / len(online_nodes),
            "avg_latency": sum(n.latency for n in online_nodes) / len(online_nodes),
            "consensus_participation": sum(1 for n in online_nodes if n.consensus_participation) / len(online_nodes) * 100,
            "high_anomaly_nodes": len([n for n in online_nodes if n.anomaly_score > 0.7]),
            "total_connections": sum(len(n.connections) for n in online_nodes) // 2,
            "node_types": {
                node_type: len([n for n in online_nodes if n.node_type == node_type])
                for node_type in self.node_types
            }
        }

def main():
    """Função principal da aplicação Streamlit"""
    
    # Título principal
    st.title("🌐 AEONCOSMA 3D Network Visualizer")
    st.markdown("**Visualização em tempo real da rede P2P Digital Twin**")
    
    # Inicializar visualizador na sessão
    if 'visualizer' not in st.session_state:
        st.session_state.visualizer = AEONCOSMA3DVisualizer()
        st.session_state.auto_update = False
    
    # Sidebar
    st.sidebar.header("🎛️ Controles")
    
    # Controles de simulação
    if st.sidebar.button("🔄 Reinicializar Rede"):
        num_nodes = st.sidebar.slider("Número de Nós", 10, 50, 25)
        st.session_state.visualizer.initialize_network(num_nodes)
        st.success(f"Rede reinicializada com {num_nodes} nós")
    
    # Auto-update
    auto_update = st.sidebar.checkbox("🔄 Atualização Automática", value=st.session_state.auto_update)
    st.session_state.auto_update = auto_update
    
    if auto_update:
        update_interval = st.sidebar.slider("Intervalo (segundos)", 1, 10, 3)
        time.sleep(update_interval)
        st.session_state.visualizer.update_network_state()
        st.rerun()
    
    # Atualização manual
    if st.sidebar.button("🔄 Atualizar Agora"):
        st.session_state.visualizer.update_network_state()
        st.rerun()
    
    # Filtros
    st.sidebar.subheader("🎯 Filtros")
    show_node_types = st.sidebar.multiselect(
        "Tipos de Nós",
        st.session_state.visualizer.node_types,
        default=st.session_state.visualizer.node_types
    )
    
    show_offline = st.sidebar.checkbox("Mostrar Nós Offline", value=False)
    
    # Layout principal
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🌐 Visualização 3D da Rede")
        
        # Criar e exibir visualização 3D
        fig_3d = st.session_state.visualizer.create_3d_visualization()
        st.plotly_chart(fig_3d, use_container_width=True)
    
    with col2:
        st.subheader("📊 Resumo da Rede")
        
        # Obter e exibir resumo
        summary = st.session_state.visualizer.get_network_summary()
        
        if "error" not in summary:
            # Métricas principais
            st.metric("Nós Online", f"{summary['online_nodes']}/{summary['total_nodes']}", 
                     f"{summary['uptime_ratio']:.1f}%")
            
            col_a, col_b = st.columns(2)
            with col_a:
                st.metric("CPU Médio", f"{summary['avg_cpu']:.1f}%")
                st.metric("Latência Média", f"{summary['avg_latency']:.1f}ms")
            
            with col_b:
                st.metric("Memória Média", f"{summary['avg_memory']:.1f}%")
                st.metric("Consenso", f"{summary['consensus_participation']:.1f}%")
            
            # Alertas
            if summary['high_anomaly_nodes'] > 0:
                st.warning(f"⚠️ {summary['high_anomaly_nodes']} nós com anomalias detectadas")
            
            if summary['uptime_ratio'] < 80:
                st.error("🚨 Baixa disponibilidade da rede")
            
            # Distribuição de tipos
            st.subheader("📈 Tipos de Nós")
            for node_type, count in summary['node_types'].items():
                if count > 0:
                    st.write(f"**{node_type.title()}:** {count}")
        
        else:
            st.error(summary['error'])
    
    # Gráficos de estatísticas
    st.subheader("📊 Estatísticas Temporais")
    
    charts = st.session_state.visualizer.create_network_stats_charts()
    
    if charts:
        # Organizar gráficos em colunas
        if len(charts) >= 2:
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(charts[0], use_container_width=True)
            with col2:
                st.plotly_chart(charts[1], use_container_width=True)
        
        if len(charts) >= 3:
            st.plotly_chart(charts[2], use_container_width=True)
    else:
        st.info("Coletando dados... Execute algumas atualizações para ver os gráficos.")
    
    # Tabela de nós detalhada
    st.subheader("🔍 Detalhes dos Nós")
    
    # Preparar dados para tabela
    node_data = []
    for node in st.session_state.visualizer.nodes.values():
        if node.node_type in show_node_types and (show_offline or node.status == "online"):
            node_data.append({
                "ID": node.node_id,
                "Tipo": node.node_type,
                "Status": "🟢 Online" if node.status == "online" else "🔴 Offline",
                "CPU %": f"{node.cpu_usage:.1f}",
                "Memória %": f"{node.memory_usage:.1f}",
                "Latência ms": f"{node.latency:.1f}",
                "Consenso": "✅" if node.consensus_participation else "❌",
                "Anomalia": f"{node.anomaly_score:.2f}",
                "Conexões": len(node.connections)
            })
    
    if node_data:
        df_nodes = pd.DataFrame(node_data)
        st.dataframe(df_nodes, use_container_width=True)
    else:
        st.info("Nenhum nó corresponde aos filtros selecionados.")
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center'>
        <small>AEONCOSMA Digital Twin Network Visualizer | Developed by Luiz H. P. Cruz</small>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
