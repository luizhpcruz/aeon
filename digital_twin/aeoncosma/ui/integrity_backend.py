#!/usr/bin/env python3
"""
🔐 AEONCOSMA Integrity Validator - Backend Mode
Validador de integridade do sistema sem interface gráfica
Autor: Luiz H. P. Cruz
Copyright 2025
"""

import json
import hashlib
import os
import time
import random
import logging
import argparse
from datetime import datetime, timedelta
from typing import Dict, List, Any

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('aeoncosma_integrity.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AEONCOSMAIntegrityBackend:
    """Sistema de validação de integridade para rede AEONCOSMA"""
    
    def __init__(self, config_file: str = None):
        self.config = self.load_config(config_file)
        self.alerts = []
        self.historical_data = []
        self.benchmarks = self.load_benchmarks()
        self.cycle_count = 0
        
        # Garantir que diretório existe
        os.makedirs(self.config["data_dir"], exist_ok=True)
        
        logger.info("🔐 AEONCOSMA Integrity Validator iniciado")
        logger.info(f"📁 Diretório de dados: {self.config['data_dir']}")
    
    def load_config(self, config_file: str = None) -> Dict[str, Any]:
        """Carrega configuração do sistema"""
        default_config = {
            "max_latency_ms": 100,
            "min_packet_ratio": 0.8,
            "historical_window_hours": 24,
            "alert_threshold": 3,
            "data_dir": "integrity_data",
            "benchmark_file": "network_benchmarks.json",
            "node_count_range": [15, 25],
            "uptime_probability": 0.75,
            "consensus_quorum": 0.67,
            "network_stability_threshold": 0.80
        }
        
        if config_file and os.path.exists(config_file):
            with open(config_file, 'r') as f:
                user_config = json.load(f)
                default_config.update(user_config)
        
        return default_config
    
    def load_benchmarks(self) -> Dict[str, Any]:
        """Carrega benchmarks históricos"""
        benchmark_path = os.path.join(self.config["data_dir"], self.config["benchmark_file"])
        if os.path.exists(benchmark_path):
            with open(benchmark_path, 'r') as f:
                benchmarks = json.load(f)
                logger.info(f"📊 Benchmarks carregados: {benchmark_path}")
                return benchmarks
        
        # Benchmarks padrão
        default_benchmarks = {
            "avg_latency_ms": 45.0,
            "avg_packet_ratio": 0.95,
            "uptime_percentage": 98.5,
            "avg_cpu_usage": 35.0,
            "avg_memory_usage": 55.0,
            "consensus_participation_rate": 0.92,
            "blockchain_sync_rate": 0.98,
            "last_updated": datetime.now().isoformat(),
            "sample_size": 1000
        }
        
        self.save_benchmarks(default_benchmarks)
        return default_benchmarks
    
    def save_benchmarks(self, benchmarks: Dict[str, Any] = None):
        """Salva benchmarks atualizados"""
        if benchmarks is None:
            benchmarks = self.benchmarks
            
        benchmark_path = os.path.join(self.config["data_dir"], self.config["benchmark_file"])
        benchmarks["last_updated"] = datetime.now().isoformat()
        
        with open(benchmark_path, 'w') as f:
            json.dump(benchmarks, f, indent=2)
        
        logger.debug(f"💾 Benchmarks salvos: {benchmark_path}")
    
    def generate_digital_signature(self, data: Dict[str, Any]) -> str:
        """Gera assinatura digital SHA-256 para integridade"""
        data_str = json.dumps(data, sort_keys=True, default=str)
        return hashlib.sha256(data_str.encode()).hexdigest()
    
    def simulate_node_status(self) -> Dict[str, Any]:
        """Simula status detalhado de um nó da rede"""
        node_id = f"aeon-{random.randint(1000,9999)}"
        
        # Simular diferentes tipos de nós com características específicas
        node_types = ["master", "energy", "ai", "crypto", "quantum", "cosmos", "validator"]
        node_type = random.choice(node_types)
        
        # Probabilidades baseadas no tipo do nó
        type_modifiers = {
            "master": {"uptime": 0.95, "latency_factor": 0.8, "cpu_factor": 1.2},
            "energy": {"uptime": 0.90, "latency_factor": 1.0, "cpu_factor": 0.9},
            "ai": {"uptime": 0.85, "latency_factor": 1.2, "cpu_factor": 1.5},
            "crypto": {"uptime": 0.88, "latency_factor": 0.9, "cpu_factor": 1.3},
            "quantum": {"uptime": 0.82, "latency_factor": 1.5, "cpu_factor": 1.1},
            "cosmos": {"uptime": 0.80, "latency_factor": 1.3, "cpu_factor": 1.4},
            "validator": {"uptime": 0.92, "latency_factor": 0.7, "cpu_factor": 0.8}
        }
        
        modifiers = type_modifiers.get(node_type, {"uptime": 0.85, "latency_factor": 1.0, "cpu_factor": 1.0})
        
        status = {
            "node_id": node_id,
            "node_type": node_type,
            "online": random.random() < modifiers["uptime"],
            "latency_ms": round(random.uniform(10, 120) * modifiers["latency_factor"], 2),
            "packets_sent": random.randint(1000, 5000),
            "packets_received": random.randint(800, 4800),
            "cpu_usage": round(random.uniform(5, 85) * modifiers["cpu_factor"], 1),
            "memory_usage": round(random.uniform(15, 90), 1),
            "consensus_participation": random.random() < 0.85,
            "blockchain_sync": random.random() < 0.95,
            "timestamp": datetime.now().isoformat(),
            "uptime_hours": round(random.uniform(1, 720), 2),  # Até 30 dias
            "last_heartbeat": datetime.now().isoformat()
        }
        
        # Calcular métricas derivadas
        if status["packets_sent"] > 0:
            status["packet_loss_ratio"] = max(0, 1 - (status["packets_received"] / status["packets_sent"]))
        else:
            status["packet_loss_ratio"] = 0
            
        # Validação de saúde
        status["health_score"] = self.calculate_health_score(status)
        status["is_healthy"] = status["health_score"] >= 0.7
        status["can_participate_consensus"] = (
            status["online"] and 
            status["is_healthy"] and 
            status["consensus_participation"] and
            status["blockchain_sync"]
        )
        
        # Assinatura digital
        status["data_signature"] = self.generate_digital_signature(status)
        
        return status
    
    def calculate_health_score(self, status: Dict[str, Any]) -> float:
        """Calcula score de saúde do nó (0.0 a 1.0)"""
        if not status["online"]:
            return 0.0
        
        factors = []
        
        # Fator de latência (0.0 a 1.0)
        latency_score = max(0, 1 - (status["latency_ms"] / 200))
        factors.append(latency_score * 0.25)
        
        # Fator de perda de pacotes
        packet_score = 1 - status["packet_loss_ratio"]
        factors.append(packet_score * 0.25)
        
        # Fator de uso de CPU (ideal entre 20-60%)
        cpu_optimal = 40
        cpu_score = 1 - abs(status["cpu_usage"] - cpu_optimal) / 100
        factors.append(max(0, cpu_score) * 0.15)
        
        # Fator de uso de memória (não deve passar de 80%)
        memory_score = max(0, 1 - status["memory_usage"] / 100)
        factors.append(memory_score * 0.15)
        
        # Fator de participação no consenso
        consensus_score = 1.0 if status["consensus_participation"] else 0.0
        factors.append(consensus_score * 0.10)
        
        # Fator de sincronização blockchain
        sync_score = 1.0 if status["blockchain_sync"] else 0.0
        factors.append(sync_score * 0.10)
        
        return min(1.0, sum(factors))
    
    def validate_node_integrity(self, status: Dict[str, Any]) -> List[str]:
        """Validação interna de integridade do nó"""
        alerts = []
        
        # Verificações críticas
        if not status["online"]:
            alerts.append(f"🔴 CRÍTICO: Nó {status['node_id']} ({status['node_type']}) offline")
        
        if status["latency_ms"] > self.config["max_latency_ms"]:
            alerts.append(f"⚠️ ALERTA: Latência alta ({status['latency_ms']}ms) no nó {status['node_id']}")
        
        if status["packet_loss_ratio"] > (1 - self.config["min_packet_ratio"]):
            alerts.append(f"⚠️ ALERTA: Alta perda de pacotes ({status['packet_loss_ratio']:.2%}) no nó {status['node_id']}")
        
        if status["cpu_usage"] > 90:
            alerts.append(f"⚠️ ALERTA: CPU em sobrecarga ({status['cpu_usage']}%) no nó {status['node_id']}")
        
        if status["memory_usage"] > 95:
            alerts.append(f"🔴 CRÍTICO: Memória esgotada ({status['memory_usage']}%) no nó {status['node_id']}")
        
        if not status["consensus_participation"] and status["online"]:
            alerts.append(f"⚠️ ALERTA: Nó {status['node_id']} não participa do consenso")
        
        if not status["blockchain_sync"] and status["online"]:
            alerts.append(f"⚠️ ALERTA: Nó {status['node_id']} dessincronizado da blockchain")
        
        # Verificação de assinatura digital
        expected_signature = self.generate_digital_signature({k: v for k, v in status.items() if k != "data_signature"})
        if status["data_signature"] != expected_signature:
            alerts.append(f"🔴 CRÍTICO: Integridade de dados comprometida no nó {status['node_id']}")
        
        return alerts
    
    def detect_anomalies(self, status: Dict[str, Any]) -> List[str]:
        """Detecção de anomalias comparando com benchmarks"""
        anomalies = []
        
        # Comparações com benchmarks históricos
        if status["latency_ms"] > self.benchmarks["avg_latency_ms"] * 2.0:
            anomalies.append(f"📊 ANOMALIA: Latência 2x acima do benchmark ({status['latency_ms']}ms vs {self.benchmarks['avg_latency_ms']}ms)")
        
        packet_ratio = 1 - status["packet_loss_ratio"]
        if packet_ratio < self.benchmarks["avg_packet_ratio"] * 0.7:
            anomalies.append(f"📊 ANOMALIA: Taxa de pacotes 30% abaixo do benchmark ({packet_ratio:.2%} vs {self.benchmarks['avg_packet_ratio']:.2%})")
        
        if status["cpu_usage"] > self.benchmarks["avg_cpu_usage"] * 2.5:
            anomalies.append(f"📊 ANOMALIA: CPU 2.5x acima do benchmark ({status['cpu_usage']}% vs {self.benchmarks['avg_cpu_usage']}%)")
        
        return anomalies
    
    def run_full_integrity_cycle(self) -> Dict[str, Any]:
        """Executa ciclo completo de validação de integridade"""
        cycle_start = datetime.now()
        self.cycle_count += 1
        
        cycle_data = {
            "cycle_id": self.cycle_count,
            "cycle_hash": self.generate_digital_signature({"cycle": self.cycle_count, "timestamp": cycle_start.isoformat()}),
            "start_time": cycle_start.isoformat(),
            "config_snapshot": self.config.copy(),
            "nodes": [],
            "alerts": [],
            "anomalies": [],
            "summary": {},
            "consensus_analysis": {},
            "network_topology": {}
        }
        
        # Simular rede com número variável de nós
        node_count = random.randint(*self.config["node_count_range"])
        healthy_nodes = 0
        consensus_participants = 0
        total_latency = 0
        total_health_score = 0
        node_types_count = {}
        
        logger.info(f"🔍 Iniciando verificação de integridade - Ciclo #{self.cycle_count}")
        logger.info(f"📊 Analisando {node_count} nós da rede...")
        
        # Analisar cada nó
        for i in range(node_count):
            status = self.simulate_node_status()
            cycle_data["nodes"].append(status)
            
            # Contadores
            if status["is_healthy"]:
                healthy_nodes += 1
            
            if status["can_participate_consensus"]:
                consensus_participants += 1
            
            total_latency += status["latency_ms"]
            total_health_score += status["health_score"]
            
            # Contar tipos de nós
            node_type = status["node_type"]
            node_types_count[node_type] = node_types_count.get(node_type, 0) + 1
            
            # Validações
            node_alerts = self.validate_node_integrity(status)
            cycle_data["alerts"].extend(node_alerts)
            
            node_anomalies = self.detect_anomalies(status)
            cycle_data["anomalies"].extend(node_anomalies)
        
        # Análise de consenso e quorum
        quorum_threshold = int(node_count * self.config["consensus_quorum"])
        quorum_reached = consensus_participants >= quorum_threshold
        
        cycle_data["consensus_analysis"] = {
            "total_nodes": node_count,
            "eligible_for_consensus": consensus_participants,
            "quorum_threshold": quorum_threshold,
            "quorum_reached": quorum_reached,
            "consensus_percentage": round((consensus_participants / node_count) * 100, 2) if node_count > 0 else 0
        }
        
        # Métricas gerais da rede
        avg_latency = total_latency / node_count if node_count > 0 else 0
        avg_health_score = total_health_score / node_count if node_count > 0 else 0
        health_percentage = (healthy_nodes / node_count) * 100 if node_count > 0 else 0
        network_stable = health_percentage >= (self.config["network_stability_threshold"] * 100)
        
        cycle_data["summary"] = {
            "total_nodes": node_count,
            "healthy_nodes": healthy_nodes,
            "health_percentage": round(health_percentage, 2),
            "avg_latency_ms": round(avg_latency, 2),
            "avg_health_score": round(avg_health_score, 3),
            "quorum_reached": quorum_reached,
            "network_stable": network_stable,
            "total_alerts": len(cycle_data["alerts"]),
            "total_anomalies": len(cycle_data["anomalies"]),
            "node_types_distribution": node_types_count
        }
        
        # Topologia da rede
        cycle_data["network_topology"] = {
            "total_connections": node_count * (node_count - 1) // 2,  # Mesh completa teórica
            "active_connections": int((healthy_nodes * (healthy_nodes - 1) // 2) * 0.8),  # 80% das conexões possíveis
            "network_diameter": max(2, int(node_count ** 0.5)),  # Diâmetro estimado
            "clustering_coefficient": 0.85 + random.uniform(-0.1, 0.1)  # Coeficiente de clusterização
        }
        
        cycle_data["end_time"] = datetime.now().isoformat()
        cycle_data["duration_seconds"] = (datetime.now() - cycle_start).total_seconds()
        
        # Salvar dados do ciclo
        self.save_cycle_data(cycle_data)
        
        return cycle_data
    
    def save_cycle_data(self, cycle_data: Dict[str, Any]):
        """Salva dados do ciclo para análise posterior"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"integrity_cycle_{timestamp}_{cycle_data['cycle_id']}.json"
        filepath = os.path.join(self.config["data_dir"], filename)
        
        with open(filepath, 'w') as f:
            json.dump(cycle_data, f, indent=2, default=str)
        
        logger.debug(f"💾 Dados do ciclo salvos: {filename}")
        
        # Manter apenas últimos 100 arquivos para evitar sobrecarga
        self.cleanup_old_files()
    
    def cleanup_old_files(self):
        """Remove arquivos antigos para economizar espaço"""
        pattern = "integrity_cycle_"
        files = [f for f in os.listdir(self.config["data_dir"]) if f.startswith(pattern)]
        
        if len(files) > 100:
            files.sort()
            for old_file in files[:-100]:  # Manter apenas os 100 mais recentes
                os.remove(os.path.join(self.config["data_dir"], old_file))
            
            logger.debug(f"🗑️ Removidos {len(files) - 100} arquivos antigos")
    
    def print_cycle_report(self, cycle_data: Dict[str, Any]):
        """Imprime relatório detalhado do ciclo"""
        print("\n" + "="*80)
        print(f"🔐 AEONCOSMA INTEGRITY REPORT - Ciclo #{cycle_data['cycle_id']}")
        print(f"🕒 {cycle_data['start_time']} | ⏱️ Duração: {cycle_data['duration_seconds']:.2f}s")
        print("="*80)
        
        # Resumo da rede
        summary = cycle_data["summary"]
        print(f"📊 RESUMO DA REDE:")
        print(f"  • Nós totais: {summary['total_nodes']}")
        print(f"  • Nós saudáveis: {summary['healthy_nodes']} ({summary['health_percentage']:.1f}%)")
        print(f"  • Score médio de saúde: {summary['avg_health_score']:.3f}")
        print(f"  • Latência média: {summary['avg_latency_ms']:.1f} ms")
        print(f"  • Rede estável: {'✅ Sim' if summary['network_stable'] else '❌ Não'}")
        
        # Análise de consenso
        consensus = cycle_data["consensus_analysis"]
        print(f"\n🗳️ ANÁLISE DE CONSENSO:")
        print(f"  • Participantes elegíveis: {consensus['eligible_for_consensus']}/{consensus['total_nodes']}")
        print(f"  • Threshold de quorum: {consensus['quorum_threshold']}")
        print(f"  • Quorum atingido: {'✅ Sim' if consensus['quorum_reached'] else '❌ Não'}")
        print(f"  • Participação no consenso: {consensus['consensus_percentage']:.1f}%")
        
        # Distribuição de tipos de nós
        print(f"\n🔧 TIPOS DE NÓS:")
        for node_type, count in summary["node_types_distribution"].items():
            print(f"  • {node_type}: {count}")
        
        # Topologia
        topology = cycle_data["network_topology"]
        print(f"\n🌐 TOPOLOGIA DA REDE:")
        print(f"  • Conexões ativas: {topology['active_connections']}/{topology['total_connections']}")
        print(f"  • Diâmetro da rede: {topology['network_diameter']}")
        print(f"  • Coeficiente de clusterização: {topology['clustering_coefficient']:.3f}")
        
        # Alertas críticos
        if cycle_data["alerts"]:
            print(f"\n🚨 ALERTAS ({len(cycle_data['alerts'])}):")
            for alert in cycle_data["alerts"][:5]:  # Mostrar apenas os 5 primeiros
                print(f"  • {alert}")
            
            if len(cycle_data["alerts"]) > 5:
                print(f"  ... e mais {len(cycle_data['alerts']) - 5} alertas")
        
        # Anomalias detectadas
        if cycle_data["anomalies"]:
            print(f"\n📊 ANOMALIAS ({len(cycle_data['anomalies'])}):")
            for anomaly in cycle_data["anomalies"][:3]:  # Mostrar apenas as 3 primeiras
                print(f"  • {anomaly}")
                
            if len(cycle_data["anomalies"]) > 3:
                print(f"  ... e mais {len(cycle_data['anomalies']) - 3} anomalias")
        
        # Status geral
        print(f"\n✅ STATUS GERAL:")
        if summary["network_stable"] and consensus["quorum_reached"] and len(cycle_data["alerts"]) == 0:
            print("  🟢 SISTEMA OPERACIONAL - Todos os parâmetros dentro da normalidade")
        elif summary["network_stable"] and consensus["quorum_reached"]:
            print("  🟡 SISTEMA ESTÁVEL - Alertas menores detectados")
        elif consensus["quorum_reached"]:
            print("  🟠 SISTEMA INSTÁVEL - Rede com problemas, mas consenso mantido")
        else:
            print("  🔴 SISTEMA CRÍTICO - Quorum não atingido, intervenção necessária")
        
        print("="*80)
    
    def run_continuous_monitoring(self, interval_seconds: int = 30, max_cycles: int = None):
        """Executa monitoramento contínuo"""
        logger.info(f"🚀 Iniciando monitoramento contínuo (intervalo: {interval_seconds}s)")
        
        try:
            cycle_count = 0
            while max_cycles is None or cycle_count < max_cycles:
                cycle_data = self.run_full_integrity_cycle()
                self.print_cycle_report(cycle_data)
                
                cycle_count += 1
                
                if max_cycles is None or cycle_count < max_cycles:
                    logger.info(f"⏱️ Aguardando {interval_seconds} segundos para próximo ciclo...")
                    time.sleep(interval_seconds)
                    
        except KeyboardInterrupt:
            logger.info("🛑 Monitoramento interrompido pelo usuário")
        except Exception as e:
            logger.error(f"❌ Erro durante monitoramento: {e}")
        finally:
            logger.info(f"📊 Monitoramento finalizado após {cycle_count} ciclos")

def main():
    """Função principal"""
    parser = argparse.ArgumentParser(description="AEONCOSMA Integrity Validator Backend")
    parser.add_argument("--config", "-c", help="Arquivo de configuração JSON")
    parser.add_argument("--interval", "-i", type=int, default=30, help="Intervalo entre verificações (segundos)")
    parser.add_argument("--cycles", "-n", type=int, help="Número máximo de ciclos (ilimitado se não especificado)")
    parser.add_argument("--single", "-s", action="store_true", help="Executar apenas um ciclo")
    parser.add_argument("--verbose", "-v", action="store_true", help="Modo verboso")
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Inicializar validador
    validator = AEONCOSMAIntegrityBackend(args.config)
    
    if args.single:
        # Executar apenas um ciclo
        cycle_data = validator.run_full_integrity_cycle()
        validator.print_cycle_report(cycle_data)
    else:
        # Executar monitoramento contínuo
        validator.run_continuous_monitoring(args.interval, args.cycles)

if __name__ == "__main__":
    main()
