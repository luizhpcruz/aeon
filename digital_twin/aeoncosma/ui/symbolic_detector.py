#!/usr/bin/env python3
"""
🔍 AEONCOSMA Symbolic Detection Engine
Sistema de detecção simbólica para análise de padrões e anomalias
Autor: Luiz H. P. Cruz
Copyright 2025
"""

import re
import json
import time
import math
import hashlib
import logging
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple, Optional, Set
from collections import defaultdict, deque
import statistics
import numpy as np

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('symbolic_detector.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class SymbolicPattern:
    """Representa um padrão simbólico detectado"""
    
    def __init__(self, pattern_type: str, symbols: List[str], confidence: float, metadata: Dict[str, Any] = None):
        self.pattern_type = pattern_type
        self.symbols = symbols
        self.confidence = confidence
        self.metadata = metadata or {}
        self.first_seen = datetime.now()
        self.last_seen = datetime.now()
        self.occurrence_count = 1
        self.pattern_hash = self._generate_hash()
    
    def _generate_hash(self) -> str:
        """Gera hash único para o padrão"""
        pattern_str = f"{self.pattern_type}:{':'.join(self.symbols)}"
        return hashlib.sha256(pattern_str.encode()).hexdigest()[:16]
    
    def update_occurrence(self):
        """Atualiza contadores de ocorrência"""
        self.last_seen = datetime.now()
        self.occurrence_count += 1
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário"""
        return {
            "pattern_type": self.pattern_type,
            "symbols": self.symbols,
            "confidence": self.confidence,
            "metadata": self.metadata,
            "first_seen": self.first_seen.isoformat(),
            "last_seen": self.last_seen.isoformat(),
            "occurrence_count": self.occurrence_count,
            "pattern_hash": self.pattern_hash
        }

class AEONCOSMASymbolicDetector:
    """Sistema de detecção simbólica avançado"""
    
    def __init__(self):
        self.detected_patterns = {}
        self.symbol_sequences = deque(maxlen=1000)  # Buffer circular
        self.pattern_rules = self._initialize_pattern_rules()
        self.anomaly_threshold = 0.7
        self.learning_mode = True
        self.baseline_entropy = None
        self.symbol_frequency = defaultdict(int)
        self.sequence_transitions = defaultdict(lambda: defaultdict(int))
        
    def _initialize_pattern_rules(self) -> Dict[str, Dict[str, Any]]:
        """Inicializa regras de detecção de padrões"""
        return {
            "attack_sequence": {
                "patterns": [
                    ["HIGH_LATENCY", "PACKET_LOSS", "NODE_FAILURE"],
                    ["CONSENSUS_FAIL", "BLOCKCHAIN_DESYNC", "NETWORK_PARTITION"],
                    ["CPU_SPIKE", "MEMORY_LEAK", "RESOURCE_EXHAUSTION"],
                    ["DDOS_INDICATOR", "CONNECTION_FLOOD", "BANDWIDTH_EXHAUSTION"]
                ],
                "confidence_threshold": 0.8,
                "window_size": 10,
                "severity": "CRITICAL"
            },
            "anomaly_sequence": {
                "patterns": [
                    ["UNUSUAL_LATENCY", "IRREGULAR_HEARTBEAT"],
                    ["CONSENSUS_DELAY", "VALIDATION_TIMEOUT"],
                    ["CRYPTO_ANOMALY", "SIGNATURE_MISMATCH"],
                    ["NETWORK_OSCILLATION", "ROUTING_INSTABILITY"]
                ],
                "confidence_threshold": 0.6,
                "window_size": 15,
                "severity": "MEDIUM"
            },
            "performance_degradation": {
                "patterns": [
                    ["SLOW_RESPONSE", "QUEUE_BUILDUP", "PROCESSING_DELAY"],
                    ["MEMORY_PRESSURE", "CPU_CONTENTION", "IO_BOTTLENECK"],
                    ["NETWORK_CONGESTION", "BANDWIDTH_LIMITATION"]
                ],
                "confidence_threshold": 0.5,
                "window_size": 20,
                "severity": "LOW"
            },
            "consensus_manipulation": {
                "patterns": [
                    ["DOUBLE_VOTING", "FORK_ATTEMPT", "CHAIN_REORGANIZATION"],
                    ["VALIDATOR_COLLUSION", "STAKE_MANIPULATION"],
                    ["TIMESTAMP_MANIPULATION", "BLOCK_WITHHOLDING"]
                ],
                "confidence_threshold": 0.9,
                "window_size": 8,
                "severity": "CRITICAL"
            },
            "network_intrusion": {
                "patterns": [
                    ["UNAUTHORIZED_NODE", "IDENTITY_SPOOFING", "CERT_INVALID"],
                    ["PROTOCOL_VIOLATION", "MESSAGE_TAMPERING"],
                    ["ENCRYPTION_BYPASS", "KEY_COMPROMISE"]
                ],
                "confidence_threshold": 0.85,
                "window_size": 5,
                "severity": "CRITICAL"
            }
        }
    
    def symbolize_network_state(self, network_data: Dict[str, Any]) -> List[str]:
        """Converte estado da rede em símbolos"""
        symbols = []
        
        # Análise de latência
        if "latency_ms" in network_data:
            latency = network_data["latency_ms"]
            if latency > 200:
                symbols.append("HIGH_LATENCY")
            elif latency > 100:
                symbols.append("MODERATE_LATENCY")
            elif latency < 20:
                symbols.append("LOW_LATENCY")
            
            # Padrões anômalos de latência
            if hasattr(self, 'previous_latency'):
                latency_change = abs(latency - self.previous_latency)
                if latency_change > 50:
                    symbols.append("LATENCY_SPIKE")
                elif latency_change > 100:
                    symbols.append("LATENCY_ANOMALY")
            self.previous_latency = latency
        
        # Análise de CPU
        if "cpu_usage" in network_data:
            cpu = network_data["cpu_usage"]
            if cpu > 90:
                symbols.append("CPU_CRITICAL")
            elif cpu > 75:
                symbols.append("CPU_HIGH")
            elif cpu < 10:
                symbols.append("CPU_IDLE")
            
            # Detecção de spikes de CPU
            if hasattr(self, 'cpu_history'):
                self.cpu_history.append(cpu)
                if len(self.cpu_history) >= 5:
                    cpu_variance = statistics.variance(self.cpu_history[-5:])
                    if cpu_variance > 400:  # Alta variância
                        symbols.append("CPU_SPIKE")
                    self.cpu_history = self.cpu_history[-10:]  # Manter apenas 10 valores
            else:
                self.cpu_history = [cpu]
        
        # Análise de memória
        if "memory_usage" in network_data:
            memory = network_data["memory_usage"]
            if memory > 85:
                symbols.append("MEMORY_CRITICAL")
            elif memory > 70:
                symbols.append("MEMORY_HIGH")
            
            # Detecção de vazamentos de memória
            if hasattr(self, 'memory_trend'):
                self.memory_trend.append(memory)
                if len(self.memory_trend) >= 10:
                    # Regressão linear simples para detectar tendência crescente
                    x = list(range(len(self.memory_trend)))
                    slope = (len(x) * sum(xi * yi for xi, yi in zip(x, self.memory_trend)) - 
                           sum(x) * sum(self.memory_trend)) / (len(x) * sum(xi**2 for xi in x) - sum(x)**2)
                    if slope > 2:  # Crescimento consistente
                        symbols.append("MEMORY_LEAK")
                    self.memory_trend = self.memory_trend[-10:]
            else:
                self.memory_trend = [memory]
        
        # Análise de conectividade
        if "online_nodes" in network_data and "total_nodes" in network_data:
            online_ratio = network_data["online_nodes"] / network_data["total_nodes"]
            if online_ratio < 0.5:
                symbols.append("NETWORK_PARTITION")
            elif online_ratio < 0.7:
                symbols.append("NODE_FAILURES")
            elif online_ratio > 0.95:
                symbols.append("NETWORK_HEALTHY")
        
        # Análise de consenso
        if "consensus_participation" in network_data:
            consensus_ratio = network_data["consensus_participation"]
            if consensus_ratio < 0.51:
                symbols.append("CONSENSUS_FAIL")
            elif consensus_ratio < 0.67:
                symbols.append("CONSENSUS_WEAK")
            elif consensus_ratio > 0.9:
                symbols.append("CONSENSUS_STRONG")
        
        # Análise de sincronização blockchain
        if "blockchain_sync" in network_data:
            sync_ratio = network_data["blockchain_sync"]
            if sync_ratio < 0.8:
                symbols.append("BLOCKCHAIN_DESYNC")
            elif sync_ratio < 0.95:
                symbols.append("SYNC_ISSUES")
        
        # Análise de perda de pacotes
        if "packet_loss_ratio" in network_data:
            packet_loss = network_data["packet_loss_ratio"]
            if packet_loss > 0.1:
                symbols.append("PACKET_LOSS")
            elif packet_loss > 0.05:
                symbols.append("MINOR_PACKET_LOSS")
        
        # Análise de transações
        if "transaction_rate" in network_data:
            tx_rate = network_data["transaction_rate"]
            if hasattr(self, 'baseline_tx_rate'):
                if tx_rate > self.baseline_tx_rate * 5:
                    symbols.append("TX_FLOOD")
                elif tx_rate < self.baseline_tx_rate * 0.1:
                    symbols.append("TX_DROUGHT")
            else:
                self.baseline_tx_rate = tx_rate
        
        # Detecção de padrões criptográficos anômalos
        if "crypto_health" in network_data:
            crypto_health = network_data["crypto_health"]
            if crypto_health < 0.8:
                symbols.append("CRYPTO_ANOMALY")
            elif crypto_health < 0.9:
                symbols.append("CRYPTO_WARNING")
        
        # Análise temporal
        current_time = datetime.now()
        if hasattr(self, 'last_symbol_time'):
            time_delta = (current_time - self.last_symbol_time).total_seconds()
            if time_delta > 300:  # 5 minutos sem símbolos
                symbols.append("LONG_SILENCE")
            elif time_delta < 1:  # Menos de 1 segundo
                symbols.append("RAPID_EVENTS")
        self.last_symbol_time = current_time
        
        return symbols
    
    def add_symbols(self, symbols: List[str]):
        """Adiciona símbolos à sequência e atualiza estatísticas"""
        timestamp = datetime.now()
        
        for symbol in symbols:
            self.symbol_frequency[symbol] += 1
            
            # Atualizar transições
            if self.symbol_sequences:
                last_symbol = self.symbol_sequences[-1]["symbol"]
                self.sequence_transitions[last_symbol][symbol] += 1
            
            self.symbol_sequences.append({
                "symbol": symbol,
                "timestamp": timestamp,
                "sequence_id": len(self.symbol_sequences)
            })
    
    def calculate_sequence_entropy(self, window_size: int = 50) -> float:
        """Calcula entropia da sequência de símbolos"""
        if len(self.symbol_sequences) < window_size:
            return 0.0
        
        recent_symbols = [s["symbol"] for s in list(self.symbol_sequences)[-window_size:]]
        symbol_counts = defaultdict(int)
        
        for symbol in recent_symbols:
            symbol_counts[symbol] += 1
        
        total = len(recent_symbols)
        entropy = 0.0
        
        for count in symbol_counts.values():
            probability = count / total
            if probability > 0:
                entropy -= probability * math.log2(probability)
        
        return entropy
    
    def detect_pattern_sequences(self) -> List[SymbolicPattern]:
        """Detecta sequências de padrões conhecidos"""
        detected = []
        
        if len(self.symbol_sequences) < 5:
            return detected
        
        recent_symbols = [s["symbol"] for s in list(self.symbol_sequences)[-50:]]
        
        for pattern_name, rule in self.pattern_rules.items():
            for pattern_sequence in rule["patterns"]:
                confidence = self._match_pattern_sequence(recent_symbols, pattern_sequence, rule["window_size"])
                
                if confidence >= rule["confidence_threshold"]:
                    metadata = {
                        "severity": rule["severity"],
                        "window_size": rule["window_size"],
                        "detection_time": datetime.now().isoformat(),
                        "sequence_length": len(pattern_sequence)
                    }
                    
                    pattern = SymbolicPattern(
                        pattern_type=pattern_name,
                        symbols=pattern_sequence,
                        confidence=confidence,
                        metadata=metadata
                    )
                    
                    # Verificar se já foi detectado recentemente
                    if pattern.pattern_hash not in self.detected_patterns:
                        self.detected_patterns[pattern.pattern_hash] = pattern
                        detected.append(pattern)
                        logger.warning(f"Padrão detectado: {pattern_name} (confiança: {confidence:.2f})")
                    else:
                        self.detected_patterns[pattern.pattern_hash].update_occurrence()
        
        return detected
    
    def _match_pattern_sequence(self, symbol_sequence: List[str], pattern: List[str], window_size: int) -> float:
        """Calcula confiança de match para uma sequência de padrão"""
        if len(symbol_sequence) < len(pattern):
            return 0.0
        
        best_match_score = 0.0
        
        # Janela deslizante para encontrar melhor match
        for i in range(len(symbol_sequence) - len(pattern) + 1):
            window = symbol_sequence[i:i + len(pattern)]
            match_score = self._calculate_sequence_similarity(window, pattern)
            best_match_score = max(best_match_score, match_score)
        
        # Aplicar peso baseado na proximidade temporal
        current_entropy = self.calculate_sequence_entropy()
        if self.baseline_entropy is None:
            self.baseline_entropy = current_entropy
        
        entropy_factor = 1.0
        if self.baseline_entropy > 0:
            entropy_ratio = current_entropy / self.baseline_entropy
            if entropy_ratio > 1.5:  # Alta entropia = mais anômalo
                entropy_factor = 1.2
            elif entropy_ratio < 0.5:  # Baixa entropia = padrão repetitivo
                entropy_factor = 1.1
        
        return best_match_score * entropy_factor
    
    def _calculate_sequence_similarity(self, sequence1: List[str], sequence2: List[str]) -> float:
        """Calcula similaridade entre duas sequências"""
        if len(sequence1) != len(sequence2):
            return 0.0
        
        exact_matches = sum(1 for s1, s2 in zip(sequence1, sequence2) if s1 == s2)
        partial_matches = 0
        
        # Verificar matches parciais (símbolos relacionados)
        related_symbols = {
            "HIGH_LATENCY": ["LATENCY_SPIKE", "LATENCY_ANOMALY"],
            "CPU_CRITICAL": ["CPU_HIGH", "CPU_SPIKE"],
            "MEMORY_CRITICAL": ["MEMORY_HIGH", "MEMORY_LEAK"],
            "CONSENSUS_FAIL": ["CONSENSUS_WEAK"],
            "NETWORK_PARTITION": ["NODE_FAILURES"]
        }
        
        for s1, s2 in zip(sequence1, sequence2):
            if s1 != s2:
                if s1 in related_symbols and s2 in related_symbols[s1]:
                    partial_matches += 0.7
                elif s2 in related_symbols and s1 in related_symbols[s2]:
                    partial_matches += 0.7
        
        total_score = (exact_matches + partial_matches) / len(sequence1)
        return min(1.0, total_score)
    
    def detect_anomalous_patterns(self) -> List[SymbolicPattern]:
        """Detecta padrões anômalos baseados em desvios estatísticos"""
        anomalous = []
        
        if len(self.symbol_sequences) < 20:
            return anomalous
        
        recent_symbols = [s["symbol"] for s in list(self.symbol_sequences)[-20:]]
        
        # Detecção de repetições anômalas
        symbol_counts = defaultdict(int)
        for symbol in recent_symbols:
            symbol_counts[symbol] += 1
        
        for symbol, count in symbol_counts.items():
            expected_frequency = self.symbol_frequency[symbol] / sum(self.symbol_frequency.values())
            observed_frequency = count / len(recent_symbols)
            
            if observed_frequency > expected_frequency * 3:  # 3x mais frequente que o normal
                anomaly = SymbolicPattern(
                    pattern_type="frequency_anomaly",
                    symbols=[symbol],
                    confidence=min(1.0, observed_frequency / expected_frequency / 3),
                    metadata={
                        "anomaly_type": "high_frequency",
                        "expected_freq": expected_frequency,
                        "observed_freq": observed_frequency,
                        "deviation_factor": observed_frequency / expected_frequency
                    }
                )
                anomalous.append(anomaly)
        
        # Detecção de sequências incomuns
        for i in range(len(recent_symbols) - 2):
            trigram = tuple(recent_symbols[i:i+3])
            
            # Verificar se este trigrama é estatisticamente incomum
            if self._is_unusual_sequence(list(trigram)):
                anomaly = SymbolicPattern(
                    pattern_type="sequence_anomaly",
                    symbols=list(trigram),
                    confidence=0.8,
                    metadata={
                        "anomaly_type": "unusual_sequence",
                        "sequence_position": i,
                        "detection_method": "trigram_analysis"
                    }
                )
                anomalous.append(anomaly)
        
        return anomalous
    
    def _is_unusual_sequence(self, sequence: List[str]) -> bool:
        """Determina se uma sequência é estatisticamente incomum"""
        if len(sequence) < 2:
            return False
        
        # Calcular probabilidade da sequência baseada em transições
        sequence_probability = 1.0
        
        for i in range(len(sequence) - 1):
            current_symbol = sequence[i]
            next_symbol = sequence[i + 1]
            
            total_transitions = sum(self.sequence_transitions[current_symbol].values())
            if total_transitions == 0:
                return True  # Símbolo nunca visto antes
            
            transition_count = self.sequence_transitions[current_symbol][next_symbol]
            transition_probability = transition_count / total_transitions
            
            sequence_probability *= transition_probability
            
            if sequence_probability < 0.01:  # Menos de 1% de probabilidade
                return True
        
        return False
    
    def generate_detection_report(self) -> Dict[str, Any]:
        """Gera relatório completo de detecções"""
        current_time = datetime.now()
        
        report = {
            "report_generated": current_time.isoformat(),
            "detection_summary": {
                "total_patterns_detected": len(self.detected_patterns),
                "symbol_sequence_length": len(self.symbol_sequences),
                "unique_symbols": len(self.symbol_frequency),
                "current_entropy": self.calculate_sequence_entropy(),
                "baseline_entropy": self.baseline_entropy
            },
            "active_patterns": [],
            "pattern_statistics": {},
            "anomaly_alerts": [],
            "recommendations": []
        }
        
        # Processar padrões ativos
        for pattern in self.detected_patterns.values():
            pattern_age = (current_time - pattern.last_seen).total_seconds()
            
            if pattern_age < 3600:  # Ativo nas últimas 1 hora
                report["active_patterns"].append(pattern.to_dict())
        
        # Estatísticas de padrões
        pattern_types = defaultdict(int)
        severity_counts = defaultdict(int)
        
        for pattern in self.detected_patterns.values():
            pattern_types[pattern.pattern_type] += 1
            severity = pattern.metadata.get("severity", "UNKNOWN")
            severity_counts[severity] += 1
        
        report["pattern_statistics"] = {
            "by_type": dict(pattern_types),
            "by_severity": dict(severity_counts)
        }
        
        # Detectar padrões em tempo real
        recent_patterns = self.detect_pattern_sequences()
        recent_anomalies = self.detect_anomalous_patterns()
        
        report["anomaly_alerts"] = [p.to_dict() for p in recent_patterns + recent_anomalies]
        
        # Gerar recomendações
        critical_patterns = sum(1 for p in self.detected_patterns.values() 
                              if p.metadata.get("severity") == "CRITICAL")
        
        if critical_patterns > 0:
            report["recommendations"].append("Investigar imediatamente padrões críticos detectados")
        
        if report["detection_summary"]["current_entropy"] > (self.baseline_entropy or 0) * 2:
            report["recommendations"].append("Alta entropia detectada - possível ataque em andamento")
        
        high_frequency_symbols = [symbol for symbol, count in self.symbol_frequency.items() 
                                if count > len(self.symbol_sequences) * 0.1]
        
        if high_frequency_symbols:
            report["recommendations"].append(f"Investigar símbolos de alta frequência: {', '.join(high_frequency_symbols)}")
        
        return report
    
    def save_detection_data(self, filename: str):
        """Salva dados de detecção em arquivo"""
        data = {
            "patterns": {hash_id: pattern.to_dict() for hash_id, pattern in self.detected_patterns.items()},
            "symbol_frequency": dict(self.symbol_frequency),
            "sequence_transitions": {k: dict(v) for k, v in self.sequence_transitions.items()},
            "baseline_entropy": self.baseline_entropy,
            "last_updated": datetime.now().isoformat()
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        logger.info(f"Dados de detecção salvos em: {filename}")
    
    def load_detection_data(self, filename: str):
        """Carrega dados de detecção de arquivo"""
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            
            # Reconstruir padrões
            self.detected_patterns = {}
            for hash_id, pattern_data in data.get("patterns", {}).items():
                pattern = SymbolicPattern(
                    pattern_type=pattern_data["pattern_type"],
                    symbols=pattern_data["symbols"],
                    confidence=pattern_data["confidence"],
                    metadata=pattern_data["metadata"]
                )
                pattern.first_seen = datetime.fromisoformat(pattern_data["first_seen"])
                pattern.last_seen = datetime.fromisoformat(pattern_data["last_seen"])
                pattern.occurrence_count = pattern_data["occurrence_count"]
                pattern.pattern_hash = pattern_data["pattern_hash"]
                self.detected_patterns[hash_id] = pattern
            
            # Reconstruir estatísticas
            self.symbol_frequency = defaultdict(int, data.get("symbol_frequency", {}))
            
            transition_data = data.get("sequence_transitions", {})
            self.sequence_transitions = defaultdict(lambda: defaultdict(int))
            for k, v in transition_data.items():
                for k2, v2 in v.items():
                    self.sequence_transitions[k][k2] = v2
            
            self.baseline_entropy = data.get("baseline_entropy")
            
            logger.info(f"Dados de detecção carregados de: {filename}")
            
        except Exception as e:
            logger.error(f"Erro ao carregar dados de detecção: {e}")

def main():
    """Função principal para teste"""
    detector = AEONCOSMASymbolicDetector()
    
    # Simular dados de rede para teste
    test_network_states = [
        {"latency_ms": 25, "cpu_usage": 45, "memory_usage": 60, "online_nodes": 18, "total_nodes": 20, "consensus_participation": 0.9},
        {"latency_ms": 180, "cpu_usage": 85, "memory_usage": 75, "online_nodes": 16, "total_nodes": 20, "consensus_participation": 0.7},
        {"latency_ms": 350, "cpu_usage": 95, "memory_usage": 90, "online_nodes": 12, "total_nodes": 20, "consensus_participation": 0.4},
        {"latency_ms": 45, "cpu_usage": 40, "memory_usage": 55, "online_nodes": 19, "total_nodes": 20, "consensus_participation": 0.95},
    ]
    
    print("Iniciando detecção simbólica...")
    
    for i, state in enumerate(test_network_states):
        print(f"\nProcessando estado {i+1}:")
        symbols = detector.symbolize_network_state(state)
        print(f"Símbolos detectados: {symbols}")
        
        detector.add_symbols(symbols)
        
        # Detectar padrões
        patterns = detector.detect_pattern_sequences()
        anomalies = detector.detect_anomalous_patterns()
        
        if patterns:
            print(f"Padrões detectados: {[p.pattern_type for p in patterns]}")
        if anomalies:
            print(f"Anomalias detectadas: {[a.pattern_type for a in anomalies]}")
        
        time.sleep(1)
    
    # Gerar relatório final
    report = detector.generate_detection_report()
    
    print("\n" + "="*60)
    print("RELATÓRIO DE DETECÇÃO SIMBÓLICA")
    print("="*60)
    print(f"Padrões detectados: {report['detection_summary']['total_patterns_detected']}")
    print(f"Símbolos únicos: {report['detection_summary']['unique_symbols']}")
    print(f"Entropia atual: {report['detection_summary']['current_entropy']:.2f}")
    
    if report["anomaly_alerts"]:
        print(f"\nAlertas de anomalia: {len(report['anomaly_alerts'])}")
        for alert in report["anomaly_alerts"]:
            print(f"  - {alert['pattern_type']}: {alert['symbols']} (confiança: {alert['confidence']:.2f})")
    
    if report["recommendations"]:
        print(f"\nRecomendações:")
        for rec in report["recommendations"]:
            print(f"  • {rec}")
    
    # Salvar dados
    detector.save_detection_data("symbolic_detection_data.json")
    
    with open("symbolic_detection_report.json", 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\nRelatório salvo em: symbolic_detection_report.json")

if __name__ == "__main__":
    main()
