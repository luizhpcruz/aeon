#!/usr/bin/env python3
"""
🧪 AEONCOSMA Stress Test Suite
Sistema de testes de stress para validação de resiliência da rede
Autor: Luiz H. P. Cruz
Copyright 2025
"""

import json
import time
import random
import logging
import argparse
import threading
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple
import concurrent.futures
import statistics

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('aeoncosma_stress_test.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AEONCOSMAStressTest:
    """Sistema de stress test para rede AEONCOSMA"""
    
    def __init__(self):
        self.test_results = []
        self.active_attacks = []
        self.baseline_metrics = None
        
    def establish_baseline(self, duration_seconds: int = 30) -> Dict[str, Any]:
        """Estabelece métricas baseline da rede em condições normais"""
        logger.info(f"Estabelecendo baseline da rede por {duration_seconds} segundos...")
        
        baseline_data = {
            "latencies": [],
            "cpu_usage": [],
            "memory_usage": [],
            "packet_loss": [],
            "consensus_participation": [],
            "uptime_rates": []
        }
        
        start_time = time.time()
        sample_count = 0
        
        while time.time() - start_time < duration_seconds:
            # Simular condições normais da rede
            network_state = self.simulate_normal_network(node_count=20)
            
            for node in network_state:
                baseline_data["latencies"].append(node["latency_ms"])
                baseline_data["cpu_usage"].append(node["cpu_usage"])
                baseline_data["memory_usage"].append(node["memory_usage"])
                baseline_data["packet_loss"].append(node["packet_loss_ratio"])
                baseline_data["consensus_participation"].append(1 if node["consensus_participation"] else 0)
                baseline_data["uptime_rates"].append(1 if node["online"] else 0)
            
            sample_count += 1
            time.sleep(1)
        
        # Calcular métricas baseline
        self.baseline_metrics = {
            "avg_latency": statistics.mean(baseline_data["latencies"]),
            "max_latency": max(baseline_data["latencies"]),
            "avg_cpu": statistics.mean(baseline_data["cpu_usage"]),
            "avg_memory": statistics.mean(baseline_data["memory_usage"]),
            "avg_packet_loss": statistics.mean(baseline_data["packet_loss"]),
            "consensus_rate": statistics.mean(baseline_data["consensus_participation"]),
            "uptime_rate": statistics.mean(baseline_data["uptime_rates"]),
            "samples": sample_count * 20,  # 20 nós por amostra
            "duration": duration_seconds
        }
        
        logger.info("Baseline estabelecido:")
        logger.info(f"  Latência média: {self.baseline_metrics['avg_latency']:.2f}ms")
        logger.info(f"  CPU médio: {self.baseline_metrics['avg_cpu']:.1f}%")
        logger.info(f"  Taxa de consenso: {self.baseline_metrics['consensus_rate']:.2%}")
        logger.info(f"  Taxa de uptime: {self.baseline_metrics['uptime_rate']:.2%}")
        
        return self.baseline_metrics
    
    def simulate_normal_network(self, node_count: int = 20) -> List[Dict[str, Any]]:
        """Simula rede em condições normais"""
        nodes = []
        node_types = ["master", "energy", "ai", "crypto", "quantum", "cosmos", "validator"]
        
        for i in range(node_count):
            node_type = random.choice(node_types)
            node = {
                "node_id": f"stress-test-{i:03d}",
                "node_type": node_type,
                "online": random.random() < 0.95,  # 95% uptime normal
                "latency_ms": random.uniform(15, 45),  # Latência normal
                "cpu_usage": random.uniform(10, 60),  # CPU normal
                "memory_usage": random.uniform(20, 70),  # Memória normal
                "packet_loss_ratio": random.uniform(0, 0.05),  # Perda baixa
                "consensus_participation": random.random() < 0.90,
                "blockchain_sync": random.random() < 0.98
            }
            nodes.append(node)
        
        return nodes
    
    def ddos_attack_simulation(self, intensity: float, duration: int) -> Dict[str, Any]:
        """Simula ataque DDoS com intensidade variável"""
        logger.info(f"Iniciando simulação de ataque DDoS - Intensidade: {intensity}, Duração: {duration}s")
        
        test_data = {
            "test_type": "DDoS_ATTACK",
            "intensity": intensity,
            "duration": duration,
            "start_time": datetime.now().isoformat(),
            "samples": [],
            "performance_degradation": {}
        }
        
        start_time = time.time()
        
        while time.time() - start_time < duration:
            nodes = []
            node_count = random.randint(18, 25)
            
            for i in range(node_count):
                # Simular efeitos do DDoS
                latency_multiplier = 1 + (intensity * random.uniform(2, 8))
                cpu_multiplier = 1 + (intensity * random.uniform(1, 3))
                
                node = {
                    "node_id": f"ddos-test-{i:03d}",
                    "online": random.random() < (0.95 - intensity * 0.3),
                    "latency_ms": random.uniform(15, 45) * latency_multiplier,
                    "cpu_usage": min(100, random.uniform(10, 60) * cpu_multiplier),
                    "memory_usage": random.uniform(20, 70) + intensity * 20,
                    "packet_loss_ratio": random.uniform(0, 0.05) + intensity * 0.4,
                    "consensus_participation": random.random() < (0.90 - intensity * 0.4),
                    "blockchain_sync": random.random() < (0.98 - intensity * 0.2)
                }
                nodes.append(node)
            
            test_data["samples"].append({
                "timestamp": datetime.now().isoformat(),
                "nodes": nodes,
                "active_nodes": sum(1 for n in nodes if n["online"]),
                "avg_latency": statistics.mean(n["latency_ms"] for n in nodes),
                "consensus_nodes": sum(1 for n in nodes if n["consensus_participation"])
            })
            
            time.sleep(1)
        
        # Calcular degradação de performance
        if self.baseline_metrics and test_data["samples"]:
            final_sample = test_data["samples"][-1]
            test_data["performance_degradation"] = {
                "latency_increase": (final_sample["avg_latency"] / self.baseline_metrics["avg_latency"] - 1) * 100,
                "consensus_decrease": (1 - final_sample["consensus_nodes"] / (len(final_sample["nodes"]) * self.baseline_metrics["consensus_rate"])) * 100,
                "uptime_decrease": (1 - final_sample["active_nodes"] / len(final_sample["nodes"]) / self.baseline_metrics["uptime_rate"]) * 100
            }
        
        test_data["end_time"] = datetime.now().isoformat()
        logger.info(f"Ataque DDoS simulado concluído. Degradação de latência: {test_data['performance_degradation'].get('latency_increase', 0):.1f}%")
        
        return test_data
    
    def node_failure_cascade(self, failure_rate: float, duration: int) -> Dict[str, Any]:
        """Simula falha em cascata de nós"""
        logger.info(f"Iniciando simulação de falha em cascata - Taxa: {failure_rate}, Duração: {duration}s")
        
        test_data = {
            "test_type": "CASCADE_FAILURE",
            "failure_rate": failure_rate,
            "duration": duration,
            "start_time": datetime.now().isoformat(),
            "samples": [],
            "cascade_progression": []
        }
        
        start_time = time.time()
        failed_nodes = set()
        total_nodes = 20
        
        while time.time() - start_time < duration:
            # Simular falhas em cascata
            if random.random() < failure_rate:
                new_failures = random.randint(1, 3)
                for _ in range(new_failures):
                    if len(failed_nodes) < total_nodes:
                        failed_nodes.add(random.randint(0, total_nodes - 1))
            
            nodes = []
            for i in range(total_nodes):
                is_failed = i in failed_nodes
                node = {
                    "node_id": f"cascade-{i:03d}",
                    "online": not is_failed,
                    "latency_ms": random.uniform(15, 45) if not is_failed else 0,
                    "cpu_usage": random.uniform(10, 60) if not is_failed else 0,
                    "memory_usage": random.uniform(20, 70) if not is_failed else 0,
                    "packet_loss_ratio": random.uniform(0, 0.05) if not is_failed else 1.0,
                    "consensus_participation": (not is_failed) and random.random() < 0.90,
                    "blockchain_sync": (not is_failed) and random.random() < 0.98
                }
                nodes.append(node)
            
            test_data["samples"].append({
                "timestamp": datetime.now().isoformat(),
                "nodes": nodes,
                "failed_count": len(failed_nodes),
                "failure_percentage": len(failed_nodes) / total_nodes * 100
            })
            
            test_data["cascade_progression"].append(len(failed_nodes))
            
            time.sleep(1)
        
        test_data["end_time"] = datetime.now().isoformat()
        test_data["final_failure_rate"] = len(failed_nodes) / total_nodes * 100
        
        logger.info(f"Falha em cascata concluída. Taxa final de falha: {test_data['final_failure_rate']:.1f}%")
        
        return test_data
    
    def consensus_attack_simulation(self, malicious_percentage: float, duration: int) -> Dict[str, Any]:
        """Simula ataque ao mecanismo de consenso"""
        logger.info(f"Iniciando ataque ao consenso - Nós maliciosos: {malicious_percentage:.1%}, Duração: {duration}s")
        
        test_data = {
            "test_type": "CONSENSUS_ATTACK",
            "malicious_percentage": malicious_percentage,
            "duration": duration,
            "start_time": datetime.now().isoformat(),
            "samples": [],
            "consensus_disruption": []
        }
        
        start_time = time.time()
        total_nodes = 25
        malicious_count = int(total_nodes * malicious_percentage)
        malicious_nodes = set(random.sample(range(total_nodes), malicious_count))
        
        while time.time() - start_time < duration:
            nodes = []
            honest_consensus = 0
            malicious_consensus = 0
            
            for i in range(total_nodes):
                is_malicious = i in malicious_nodes
                
                # Nós maliciosos tentam disromper o consenso
                if is_malicious:
                    consensus_behavior = random.choice([False, False, True])  # Mostly non-cooperative
                    if consensus_behavior:
                        malicious_consensus += 1
                else:
                    consensus_behavior = random.random() < 0.95  # Honest nodes
                    if consensus_behavior:
                        honest_consensus += 1
                
                node = {
                    "node_id": f"consensus-{i:03d}",
                    "node_type": "malicious" if is_malicious else "honest",
                    "online": True,
                    "latency_ms": random.uniform(15, 45),
                    "consensus_participation": consensus_behavior,
                    "blockchain_sync": not is_malicious or random.random() < 0.3,  # Malicious nodes often desync
                    "malicious": is_malicious
                }
                nodes.append(node)
            
            consensus_ratio = honest_consensus / (total_nodes - malicious_count) if (total_nodes - malicious_count) > 0 else 0
            
            test_data["samples"].append({
                "timestamp": datetime.now().isoformat(),
                "nodes": nodes,
                "honest_consensus": honest_consensus,
                "malicious_consensus": malicious_consensus,
                "total_consensus": honest_consensus + malicious_consensus,
                "consensus_ratio": consensus_ratio
            })
            
            test_data["consensus_disruption"].append({
                "honest_participating": honest_consensus,
                "malicious_participating": malicious_consensus,
                "network_compromised": (honest_consensus + malicious_consensus) < (total_nodes * 0.67)
            })
            
            time.sleep(1)
        
        test_data["end_time"] = datetime.now().isoformat()
        
        # Calcular estatísticas do ataque
        compromised_moments = sum(1 for d in test_data["consensus_disruption"] if d["network_compromised"])
        test_data["compromise_percentage"] = compromised_moments / len(test_data["consensus_disruption"]) * 100
        
        logger.info(f"Ataque ao consenso concluído. Rede comprometida {test_data['compromise_percentage']:.1f}% do tempo")
        
        return test_data
    
    def resource_exhaustion_test(self, resource_type: str, intensity: float, duration: int) -> Dict[str, Any]:
        """Simula esgotamento de recursos (CPU, memória, rede)"""
        logger.info(f"Teste de esgotamento de {resource_type} - Intensidade: {intensity}, Duração: {duration}s")
        
        test_data = {
            "test_type": f"RESOURCE_EXHAUSTION_{resource_type.upper()}",
            "resource_type": resource_type,
            "intensity": intensity,
            "duration": duration,
            "start_time": datetime.now().isoformat(),
            "samples": []
        }
        
        start_time = time.time()
        
        while time.time() - start_time < duration:
            nodes = []
            node_count = 20
            
            for i in range(node_count):
                base_cpu = random.uniform(10, 60)
                base_memory = random.uniform(20, 70)
                base_latency = random.uniform(15, 45)
                
                # Aplicar stress baseado no tipo de recurso
                if resource_type == "cpu":
                    cpu_usage = min(100, base_cpu + intensity * random.uniform(30, 80))
                    memory_usage = base_memory
                    latency_ms = base_latency * (1 + intensity * 0.5)
                elif resource_type == "memory":
                    cpu_usage = base_cpu
                    memory_usage = min(100, base_memory + intensity * random.uniform(20, 60))
                    latency_ms = base_latency * (1 + intensity * 0.3)
                elif resource_type == "network":
                    cpu_usage = base_cpu
                    memory_usage = base_memory
                    latency_ms = base_latency * (1 + intensity * random.uniform(3, 10))
                
                # Determinar se o nó falha devido ao stress
                failure_threshold = 0.05 + intensity * 0.3
                node_online = random.random() > failure_threshold
                
                node = {
                    "node_id": f"stress-{resource_type}-{i:03d}",
                    "online": node_online,
                    "cpu_usage": cpu_usage if node_online else 0,
                    "memory_usage": memory_usage if node_online else 0,
                    "latency_ms": latency_ms if node_online else 0,
                    "packet_loss_ratio": random.uniform(0, 0.05) + intensity * 0.2,
                    "consensus_participation": node_online and (cpu_usage < 90) and (memory_usage < 90),
                    "blockchain_sync": node_online and random.random() < (0.95 - intensity * 0.3)
                }
                nodes.append(node)
            
            test_data["samples"].append({
                "timestamp": datetime.now().isoformat(),
                "nodes": nodes,
                "active_nodes": sum(1 for n in nodes if n["online"]),
                "avg_cpu": statistics.mean(n["cpu_usage"] for n in nodes if n["online"]) if any(n["online"] for n in nodes) else 0,
                "avg_memory": statistics.mean(n["memory_usage"] for n in nodes if n["online"]) if any(n["online"] for n in nodes) else 0,
                "avg_latency": statistics.mean(n["latency_ms"] for n in nodes if n["online"]) if any(n["online"] for n in nodes) else 0
            })
            
            time.sleep(1)
        
        test_data["end_time"] = datetime.now().isoformat()
        
        logger.info(f"Teste de esgotamento de {resource_type} concluído")
        
        return test_data
    
    def run_comprehensive_stress_test(self, output_file: str = None) -> Dict[str, Any]:
        """Executa bateria completa de testes de stress"""
        logger.info("Iniciando bateria completa de testes de stress AEONCOSMA")
        
        comprehensive_results = {
            "test_suite": "AEONCOSMA_COMPREHENSIVE_STRESS_TEST",
            "start_time": datetime.now().isoformat(),
            "baseline": None,
            "tests": [],
            "summary": {}
        }
        
        try:
            # 1. Estabelecer baseline
            comprehensive_results["baseline"] = self.establish_baseline(30)
            
            # 2. Teste DDoS (baixa, média, alta intensidade)
            for intensity in [0.3, 0.6, 0.9]:
                logger.info(f"Executando teste DDoS - Intensidade {intensity}")
                ddos_result = self.ddos_attack_simulation(intensity, 60)
                comprehensive_results["tests"].append(ddos_result)
            
            # 3. Teste de falha em cascata
            logger.info("Executando teste de falha em cascata")
            cascade_result = self.node_failure_cascade(0.1, 90)
            comprehensive_results["tests"].append(cascade_result)
            
            # 4. Teste de ataque ao consenso
            for mal_percentage in [0.2, 0.35, 0.49]:  # 20%, 35%, 49% malicious
                logger.info(f"Executando ataque ao consenso - {mal_percentage:.1%} maliciosos")
                consensus_result = self.consensus_attack_simulation(mal_percentage, 60)
                comprehensive_results["tests"].append(consensus_result)
            
            # 5. Testes de esgotamento de recursos
            for resource in ["cpu", "memory", "network"]:
                logger.info(f"Executando teste de esgotamento de {resource}")
                resource_result = self.resource_exhaustion_test(resource, 0.8, 60)
                comprehensive_results["tests"].append(resource_result)
            
            # 6. Gerar resumo
            comprehensive_results["summary"] = self.generate_test_summary(comprehensive_results)
            comprehensive_results["end_time"] = datetime.now().isoformat()
            
            # 7. Salvar resultados
            if output_file:
                with open(output_file, 'w') as f:
                    json.dump(comprehensive_results, f, indent=2, default=str)
                logger.info(f"Resultados salvos em: {output_file}")
            
            logger.info("Bateria de testes de stress concluída com sucesso")
            
            return comprehensive_results
            
        except Exception as e:
            logger.error(f"Erro durante testes de stress: {e}")
            comprehensive_results["error"] = str(e)
            comprehensive_results["end_time"] = datetime.now().isoformat()
            return comprehensive_results
    
    def generate_test_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Gera resumo dos testes executados"""
        summary = {
            "total_tests": len(results["tests"]),
            "test_types": {},
            "worst_case_scenarios": {},
            "resilience_scores": {},
            "recommendations": []
        }
        
        # Analisar cada teste
        for test in results["tests"]:
            test_type = test["test_type"]
            
            if test_type not in summary["test_types"]:
                summary["test_types"][test_type] = 0
            summary["test_types"][test_type] += 1
            
            # Identificar cenários mais críticos
            if "performance_degradation" in test:
                latency_increase = test["performance_degradation"].get("latency_increase", 0)
                if latency_increase > summary["worst_case_scenarios"].get("max_latency_degradation", 0):
                    summary["worst_case_scenarios"]["max_latency_degradation"] = latency_increase
                    summary["worst_case_scenarios"]["worst_latency_test"] = test_type
            
            if "compromise_percentage" in test:
                if test["compromise_percentage"] > summary["worst_case_scenarios"].get("max_consensus_compromise", 0):
                    summary["worst_case_scenarios"]["max_consensus_compromise"] = test["compromise_percentage"]
                    summary["worst_case_scenarios"]["worst_consensus_test"] = test_type
        
        # Calcular scores de resilência
        if results["baseline"]:
            baseline = results["baseline"]
            
            # Score baseado na manutenção de consenso sob stress
            consensus_resilience = 100 - summary["worst_case_scenarios"].get("max_consensus_compromise", 0)
            summary["resilience_scores"]["consensus_resilience"] = max(0, consensus_resilience)
            
            # Score baseado na degradação de performance
            max_degradation = summary["worst_case_scenarios"].get("max_latency_degradation", 0)
            performance_resilience = max(0, 100 - max_degradation / 10)  # Cada 10% de degradação = -1 ponto
            summary["resilience_scores"]["performance_resilience"] = performance_resilience
            
            # Score geral
            overall_resilience = (consensus_resilience + performance_resilience) / 2
            summary["resilience_scores"]["overall_resilience"] = overall_resilience
        
        # Gerar recomendações
        if summary["resilience_scores"].get("consensus_resilience", 100) < 70:
            summary["recommendations"].append("Implementar mecanismos adicionais de validação de consenso")
        
        if summary["resilience_scores"].get("performance_resilience", 100) < 60:
            summary["recommendations"].append("Otimizar algoritmos de rede para melhor performance sob stress")
        
        if summary["worst_case_scenarios"].get("max_latency_degradation", 0) > 200:
            summary["recommendations"].append("Implementar QoS e priorização de tráfego crítico")
        
        return summary

def main():
    """Função principal"""
    parser = argparse.ArgumentParser(description="AEONCOSMA Stress Test Suite")
    parser.add_argument("--test", "-t", choices=["ddos", "cascade", "consensus", "resource", "comprehensive"], 
                       default="comprehensive", help="Tipo de teste a executar")
    parser.add_argument("--intensity", "-i", type=float, default=0.7, help="Intensidade do teste (0.0-1.0)")
    parser.add_argument("--duration", "-d", type=int, default=60, help="Duração do teste em segundos")
    parser.add_argument("--output", "-o", help="Arquivo de saída para resultados")
    parser.add_argument("--resource", "-r", choices=["cpu", "memory", "network"], default="cpu",
                       help="Tipo de recurso para teste de esgotamento")
    
    args = parser.parse_args()
    
    stress_tester = AEONCOSMAStressTest()
    
    if args.test == "comprehensive":
        output_file = args.output or f"stress_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        results = stress_tester.run_comprehensive_stress_test(output_file)
        
        # Exibir resumo
        print("\n" + "="*80)
        print("RELATÓRIO DE TESTES DE STRESS AEONCOSMA")
        print("="*80)
        
        if "summary" in results:
            summary = results["summary"]
            print(f"Total de testes executados: {summary['total_tests']}")
            print(f"Tipos de teste: {', '.join(summary['test_types'].keys())}")
            
            if "resilience_scores" in summary:
                scores = summary["resilience_scores"]
                print(f"\nSCORES DE RESILÊNCIA:")
                print(f"  Resilência de Consenso: {scores.get('consensus_resilience', 0):.1f}%")
                print(f"  Resilência de Performance: {scores.get('performance_resilience', 0):.1f}%")
                print(f"  Resilência Geral: {scores.get('overall_resilience', 0):.1f}%")
            
            if summary["recommendations"]:
                print(f"\nRECOMENDAÇÕES:")
                for rec in summary["recommendations"]:
                    print(f"  • {rec}")
        
        print("="*80)
        
    else:
        # Executar teste específico
        if args.test == "ddos":
            results = stress_tester.ddos_attack_simulation(args.intensity, args.duration)
        elif args.test == "cascade":
            results = stress_tester.node_failure_cascade(args.intensity, args.duration)
        elif args.test == "consensus":
            results = stress_tester.consensus_attack_simulation(args.intensity, args.duration)
        elif args.test == "resource":
            results = stress_tester.resource_exhaustion_test(args.resource, args.intensity, args.duration)
        
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            print(f"Resultados salvos em: {args.output}")

if __name__ == "__main__":
    main()
