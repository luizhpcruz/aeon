#!/usr/bin/env python3
"""
AEONCOSMA Integrity Validator - Backend Mode (ASCII Version)
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
from datetime import datetime
from typing import Dict, List, Any

# Configuração de logging sem emojis
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('aeoncosma_integrity.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AEONCOSMAIntegrityValidator:
    """Sistema de validação de integridade para rede AEONCOSMA"""
    
    def __init__(self, config_file: str = None):
        self.config = self.load_config(config_file)
        self.alerts = []
        self.cycle_count = 0
        
        # Garantir que diretório existe
        os.makedirs(self.config["data_dir"], exist_ok=True)
        
        logger.info("AEONCOSMA Integrity Validator iniciado")
        logger.info(f"Diretorio de dados: {self.config['data_dir']}")
    
    def load_config(self, config_file: str = None) -> Dict[str, Any]:
        """Carrega configuração do sistema"""
        return {
            "max_latency_ms": 100,
            "min_packet_ratio": 0.8,
            "data_dir": "integrity_data",
            "node_count_range": [15, 25],
            "consensus_quorum": 0.67,
            "network_stability_threshold": 0.80
        }
    
    def generate_digital_signature(self, data: Dict[str, Any]) -> str:
        """Gera assinatura digital SHA-256 para integridade"""
        data_str = json.dumps(data, sort_keys=True, default=str)
        return hashlib.sha256(data_str.encode()).hexdigest()
    
    def simulate_node_status(self) -> Dict[str, Any]:
        """Simula status detalhado de um nó da rede"""
        node_types = ["master", "energy", "ai", "crypto", "quantum", "cosmos", "validator"]
        node_type = random.choice(node_types)
        
        # Modificadores por tipo de nó
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
            "node_id": f"aeon-{random.randint(1000,9999)}",
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
        }
        
        # Métricas derivadas
        if status["packets_sent"] > 0:
            status["packet_loss_ratio"] = max(0, 1 - (status["packets_received"] / status["packets_sent"]))
        else:
            status["packet_loss_ratio"] = 0
            
        status["health_score"] = self.calculate_health_score(status)
        status["is_healthy"] = status["health_score"] >= 0.7
        status["can_participate_consensus"] = (
            status["online"] and 
            status["is_healthy"] and 
            status["consensus_participation"] and
            status["blockchain_sync"]
        )
        
        status["data_signature"] = self.generate_digital_signature(status)
        return status
    
    def calculate_health_score(self, status: Dict[str, Any]) -> float:
        """Calcula score de saúde do nó (0.0 a 1.0)"""
        if not status["online"]:
            return 0.0
        
        factors = []
        
        # Fator de latência
        latency_score = max(0, 1 - (status["latency_ms"] / 200))
        factors.append(latency_score * 0.25)
        
        # Fator de perda de pacotes
        packet_score = 1 - status["packet_loss_ratio"]
        factors.append(packet_score * 0.25)
        
        # Fator de CPU (ideal entre 20-60%)
        cpu_optimal = 40
        cpu_score = 1 - abs(status["cpu_usage"] - cpu_optimal) / 100
        factors.append(max(0, cpu_score) * 0.15)
        
        # Fator de memória
        memory_score = max(0, 1 - status["memory_usage"] / 100)
        factors.append(memory_score * 0.15)
        
        # Fatores de participação
        consensus_score = 1.0 if status["consensus_participation"] else 0.0
        factors.append(consensus_score * 0.10)
        
        sync_score = 1.0 if status["blockchain_sync"] else 0.0
        factors.append(sync_score * 0.10)
        
        return min(1.0, sum(factors))
    
    def validate_node_integrity(self, status: Dict[str, Any]) -> List[str]:
        """Validação interna de integridade do nó"""
        alerts = []
        
        if not status["online"]:
            alerts.append(f"CRITICO: No {status['node_id']} ({status['node_type']}) offline")
        
        if status["latency_ms"] > self.config["max_latency_ms"]:
            alerts.append(f"ALERTA: Latencia alta ({status['latency_ms']}ms) no no {status['node_id']}")
        
        if status["packet_loss_ratio"] > (1 - self.config["min_packet_ratio"]):
            alerts.append(f"ALERTA: Alta perda de pacotes ({status['packet_loss_ratio']:.2%}) no no {status['node_id']}")
        
        if status["cpu_usage"] > 90:
            alerts.append(f"ALERTA: CPU em sobrecarga ({status['cpu_usage']}%) no no {status['node_id']}")
        
        if status["memory_usage"] > 95:
            alerts.append(f"CRITICO: Memoria esgotada ({status['memory_usage']}%) no no {status['node_id']}")
        
        if not status["consensus_participation"] and status["online"]:
            alerts.append(f"ALERTA: No {status['node_id']} nao participa do consenso")
        
        if not status["blockchain_sync"] and status["online"]:
            alerts.append(f"ALERTA: No {status['node_id']} dessincronizado da blockchain")
        
        return alerts
    
    def run_integrity_cycle(self) -> Dict[str, Any]:
        """Executa ciclo completo de validação de integridade"""
        cycle_start = datetime.now()
        self.cycle_count += 1
        
        cycle_data = {
            "cycle_id": self.cycle_count,
            "start_time": cycle_start.isoformat(),
            "nodes": [],
            "alerts": [],
            "summary": {},
            "consensus_analysis": {}
        }
        
        # Simular rede
        node_count = random.randint(*self.config["node_count_range"])
        healthy_nodes = 0
        consensus_participants = 0
        total_latency = 0
        total_health_score = 0
        node_types_count = {}
        
        logger.info(f"Iniciando verificacao de integridade - Ciclo #{self.cycle_count}")
        logger.info(f"Analisando {node_count} nos da rede...")
        
        # Analisar cada nó
        for i in range(node_count):
            status = self.simulate_node_status()
            cycle_data["nodes"].append(status)
            
            if status["is_healthy"]:
                healthy_nodes += 1
            
            if status["can_participate_consensus"]:
                consensus_participants += 1
            
            total_latency += status["latency_ms"]
            total_health_score += status["health_score"]
            
            # Contar tipos
            node_type = status["node_type"]
            node_types_count[node_type] = node_types_count.get(node_type, 0) + 1
            
            # Validações
            node_alerts = self.validate_node_integrity(status)
            cycle_data["alerts"].extend(node_alerts)
        
        # Análise de consenso
        quorum_threshold = int(node_count * self.config["consensus_quorum"])
        quorum_reached = consensus_participants >= quorum_threshold
        
        cycle_data["consensus_analysis"] = {
            "total_nodes": node_count,
            "eligible_for_consensus": consensus_participants,
            "quorum_threshold": quorum_threshold,
            "quorum_reached": quorum_reached,
            "consensus_percentage": round((consensus_participants / node_count) * 100, 2) if node_count > 0 else 0
        }
        
        # Métricas gerais
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
            "node_types_distribution": node_types_count
        }
        
        cycle_data["end_time"] = datetime.now().isoformat()
        cycle_data["duration_seconds"] = (datetime.now() - cycle_start).total_seconds()
        
        # Salvar dados
        self.save_cycle_data(cycle_data)
        return cycle_data
    
    def save_cycle_data(self, cycle_data: Dict[str, Any]):
        """Salva dados do ciclo"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"integrity_cycle_{timestamp}_{cycle_data['cycle_id']}.json"
        filepath = os.path.join(self.config["data_dir"], filename)
        
        with open(filepath, 'w') as f:
            json.dump(cycle_data, f, indent=2, default=str)
        
        logger.debug(f"Dados do ciclo salvos: {filename}")
    
    def print_cycle_report(self, cycle_data: Dict[str, Any]):
        """Imprime relatório detalhado do ciclo"""
        print("\n" + "="*80)
        print(f"AEONCOSMA INTEGRITY REPORT - Ciclo #{cycle_data['cycle_id']}")
        print(f"Inicio: {cycle_data['start_time']} | Duracao: {cycle_data['duration_seconds']:.2f}s")
        print("="*80)
        
        # Resumo da rede
        summary = cycle_data["summary"]
        print(f"RESUMO DA REDE:")
        print(f"  * Nos totais: {summary['total_nodes']}")
        print(f"  * Nos saudaveis: {summary['healthy_nodes']} ({summary['health_percentage']:.1f}%)")
        print(f"  * Score medio de saude: {summary['avg_health_score']:.3f}")
        print(f"  * Latencia media: {summary['avg_latency_ms']:.1f} ms")
        print(f"  * Rede estavel: {'SIM' if summary['network_stable'] else 'NAO'}")
        
        # Análise de consenso
        consensus = cycle_data["consensus_analysis"]
        print(f"\nANALISE DE CONSENSO:")
        print(f"  * Participantes elegiveis: {consensus['eligible_for_consensus']}/{consensus['total_nodes']}")
        print(f"  * Threshold de quorum: {consensus['quorum_threshold']}")
        print(f"  * Quorum atingido: {'SIM' if consensus['quorum_reached'] else 'NAO'}")
        print(f"  * Participacao no consenso: {consensus['consensus_percentage']:.1f}%")
        
        # Distribuição de tipos
        print(f"\nTIPOS DE NOS:")
        for node_type, count in summary["node_types_distribution"].items():
            print(f"  * {node_type}: {count}")
        
        # Alertas críticos
        if cycle_data["alerts"]:
            print(f"\nALERTAS ({len(cycle_data['alerts'])}):")
            for alert in cycle_data["alerts"][:5]:  # Mostrar apenas os 5 primeiros
                print(f"  * {alert}")
            
            if len(cycle_data["alerts"]) > 5:
                print(f"  ... e mais {len(cycle_data['alerts']) - 5} alertas")
        
        # Status geral
        print(f"\nSTATUS GERAL:")
        if summary["network_stable"] and consensus["quorum_reached"] and len(cycle_data["alerts"]) == 0:
            print("  [OK] SISTEMA OPERACIONAL - Todos os parametros dentro da normalidade")
        elif summary["network_stable"] and consensus["quorum_reached"]:
            print("  [AVISO] SISTEMA ESTAVEL - Alertas menores detectados")
        elif consensus["quorum_reached"]:
            print("  [INSTAVEL] SISTEMA INSTAVEL - Rede com problemas, mas consenso mantido")
        else:
            print("  [CRITICO] SISTEMA CRITICO - Quorum nao atingido, intervencao necessaria")
        
        print("="*80)
    
    def run_continuous_monitoring(self, interval_seconds: int = 30, max_cycles: int = None):
        """Executa monitoramento contínuo"""
        logger.info(f"Iniciando monitoramento continuo (intervalo: {interval_seconds}s)")
        
        try:
            cycle_count = 0
            while max_cycles is None or cycle_count < max_cycles:
                cycle_data = self.run_integrity_cycle()
                self.print_cycle_report(cycle_data)
                
                cycle_count += 1
                
                if max_cycles is None or cycle_count < max_cycles:
                    logger.info(f"Aguardando {interval_seconds} segundos para proximo ciclo...")
                    time.sleep(interval_seconds)
                    
        except KeyboardInterrupt:
            logger.info("Monitoramento interrompido pelo usuario")
        except Exception as e:
            logger.error(f"Erro durante monitoramento: {e}")
        finally:
            logger.info(f"Monitoramento finalizado apos {cycle_count} ciclos")

def main():
    """Função principal"""
    parser = argparse.ArgumentParser(description="AEONCOSMA Integrity Validator Backend")
    parser.add_argument("--config", "-c", help="Arquivo de configuracao JSON")
    parser.add_argument("--interval", "-i", type=int, default=30, help="Intervalo entre verificacoes (segundos)")
    parser.add_argument("--cycles", "-n", type=int, help="Numero maximo de ciclos")
    parser.add_argument("--single", "-s", action="store_true", help="Executar apenas um ciclo")
    parser.add_argument("--verbose", "-v", action="store_true", help="Modo verboso")
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Inicializar validador
    validator = AEONCOSMAIntegrityValidator(args.config)
    
    if args.single:
        # Executar apenas um ciclo
        cycle_data = validator.run_integrity_cycle()
        validator.print_cycle_report(cycle_data)
        
        # Mostrar exemplo de uso do protocolo de consenso
        print("\n" + "="*80)
        print("PROTOCOLO DE CONSENSO AEONCOSMA")
        print("="*80)
        
        consensus = cycle_data["consensus_analysis"]
        summary = cycle_data["summary"]
        
        if consensus["quorum_reached"]:
            print("STATUS: CONSENSO ATIVO")
            print(f"- {consensus['eligible_for_consensus']} nos participando do consenso")
            print(f"- Quorum de {consensus['quorum_threshold']} nos atingido")
            print("- Blockchain pode processar transacoes")
            print("- Novos blocos podem ser minerados")
            print("- Validacao de transacoes ativa")
        else:
            print("STATUS: CONSENSO INATIVO")
            print(f"- Apenas {consensus['eligible_for_consensus']} nos disponiveis")
            print(f"- Quorum de {consensus['quorum_threshold']} nos NAO atingido")
            print("- Blockchain em modo somente leitura")
            print("- Mineracao de blocos suspensa")
            print("- Sistema aguardando recuperacao da rede")
        
        print("\nMETRICAS DE SEGURANCA:")
        print(f"- Integridade da rede: {summary['health_percentage']:.1f}%")
        print(f"- Latencia media: {summary['avg_latency_ms']:.1f}ms")
        print(f"- Alertas detectados: {summary['total_alerts']}")
        print(f"- Score de saude medio: {summary['avg_health_score']:.3f}")
        
        # Simulação de sabotagem/ataque
        if summary['total_alerts'] > 10:
            print("\nPOSSIVEL ATAQUE DETECTADO:")
            print("- Numero anormal de alertas detectados")
            print("- Recomendacao: Investigar logs detalhados")
            print("- Acao: Isolar nos suspeitos")
            print("- Protocolo: Ativar modo de emergencia")
    else:
        # Executar monitoramento contínuo
        validator.run_continuous_monitoring(args.interval, args.cycles)

if __name__ == "__main__":
    main()
