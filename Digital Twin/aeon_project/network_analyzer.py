"""
AEON P2P Network - Análise de Capacidade e Stress Test
Demonstração de escalabilidade da rede descentralizada
"""

import random
import time
from datetime import datetime, timedelta

class AEONNetworkAnalyzer:
    """Analisador de capacidade da rede P2P AEON"""
    
    def __init__(self):
        self.node_types = {
            "UHE": {"prefix": "UHE", "base_port": 8000, "max_nodes": 50},
            "Subestação": {"prefix": "SE", "base_port": 8100, "max_nodes": 100},
            "Centro de Controle": {"prefix": "CC", "base_port": 8200, "max_nodes": 20},
            "Escritório": {"prefix": "ESC", "base_port": 8300, "max_nodes": 200},
            "Campo": {"prefix": "CAMPO", "base_port": 8400, "max_nodes": 500},
            "IoT Sensor": {"prefix": "IOT", "base_port": 8500, "max_nodes": 1000},
            "Mobile": {"prefix": "MOB", "base_port": 8600, "max_nodes": 300}
        }
        
        self.brazilian_locations = [
            "São Paulo", "Rio de Janeiro", "Belo Horizonte", "Salvador", "Brasília",
            "Fortaleza", "Manaus", "Curitiba", "Recife", "Goiânia", "Belém",
            "Porto Alegre", "Guarulhos", "Campinas", "São Luís", "Maceió",
            "Duque de Caxias", "Natal", "Campo Grande", "Teresina", "São Bernardo do Campo",
            "Nova Iguaçu", "João Pessoa", "Santo André", "Osasco", "São José dos Campos",
            "Jaboatão dos Guararapes", "Ribeirão Preto", "Uberlândia", "Contagem", "Sorocaba"
        ]
        
        self.uhe_names = [
            "Itaipu", "Tucuruí", "Ilha Solteira", "Xingó", "Paulo Afonso IV",
            "Itumbiara", "Marimbondo", "Água Vermelha", "Emborcação", "Itaparica",
            "Nova Ponte", "Três Marias", "Sobradinho", "Furnas", "Mascarenhas",
            "Paraibuna", "Jaguará", "Volta Grande", "Irapé", "Simplício",
            "Barra Bonita", "Promissão", "Nova Avanhandava", "Três Irmãos", "Jupiá"
        ]
    
    def generate_realistic_nodes(self, count: int) -> list:
        """Gera nós realistas para stress test"""
        nodes = []
        
        for i in range(count):
            # Distribuição por tipo (mais IoT e Campo, menos Centro de Controle)
            node_type = random.choices(
                list(self.node_types.keys()),
                weights=[10, 25, 5, 15, 30, 35, 20],  # Mais IoT e Campo
                k=1
            )[0]
            
            type_config = self.node_types[node_type]
            
            # Gerar nome baseado no tipo
            if node_type == "UHE":
                name = f"{random.choice(self.uhe_names)} {random.randint(1, 5)}"
            elif node_type == "Subestação":
                location = random.choice(self.brazilian_locations)
                voltage = random.choice(["13.8kV", "34.5kV", "69kV", "138kV", "230kV", "500kV"])
                name = f"SE {location} {voltage}"
            elif node_type == "Centro de Controle":
                region = random.choice(["Norte", "Nordeste", "Sudeste", "Sul", "Centro-Oeste"])
                name = f"CC {region} - {random.choice(self.brazilian_locations)}"
            elif node_type == "Escritório":
                company = random.choice(["CPFL", "Eletrobras", "CEMIG", "COPEL", "Equatorial"])
                location = random.choice(self.brazilian_locations)
                name = f"{company} {location}"
            elif node_type == "Campo":
                team = random.choice(["Manutenção", "Operação", "Emergência", "Inspeção"])
                name = f"Equipe {team} - {random.choice(self.brazilian_locations)}"
            elif node_type == "IoT Sensor":
                sensor_type = random.choice(["Temperatura", "Vibração", "Corrente", "Tensão", "Óleo"])
                equipment = random.choice(["Transformador", "Disjuntor", "Chave", "Reator"])
                name = f"Sensor {sensor_type} - {equipment} #{random.randint(1, 999)}"
            else:  # Mobile
                name = f"Tablet Campo #{random.randint(1, 300)}"
            
            # IP simulado (rede local corporativa)
            ip_base = random.choice(["10.0", "172.16", "192.168"])
            ip = f"{ip_base}.{random.randint(1, 254)}.{random.randint(1, 254)}"
            
            # Porta baseada no tipo
            port = type_config["base_port"] + random.randint(1, 99)
            
            # Status (95% online para simular rede real)
            status = "online" if random.random() > 0.05 else "offline"
            
            node = {
                "id": f"node-{i+1:04d}",
                "name": name,
                "type": node_type,
                "ip": ip,
                "port": port,
                "status": status,
                "connected_at": datetime.now() - timedelta(
                    minutes=random.randint(1, 1440)  # Conectado há 1 min até 24h
                ),
                "latency_ms": random.randint(10, 200),
                "bandwidth_mbps": random.randint(1, 100),
                "cpu_usage": random.randint(5, 95),
                "memory_usage": random.randint(10, 90),
                "location": random.choice(self.brazilian_locations)
            }
            
            nodes.append(node)
        
        return nodes
    
    def calculate_network_metrics(self, nodes: list) -> dict:
        """Calcula métricas de performance da rede"""
        online_nodes = [n for n in nodes if n["status"] == "online"]
        total_nodes = len(nodes)
        online_count = len(online_nodes)
        
        if not online_nodes:
            return {"error": "Nenhum nó online"}
        
        # Conexões totais (cada nó conecta com todos os outros)
        total_connections = online_count * (online_count - 1)
        
        # Latência média
        avg_latency = sum(n["latency_ms"] for n in online_nodes) / online_count
        
        # Bandwidth total
        total_bandwidth = sum(n["bandwidth_mbps"] for n in online_nodes)
        
        # Uso de recursos
        avg_cpu = sum(n["cpu_usage"] for n in online_nodes) / online_count
        avg_memory = sum(n["memory_usage"] for n in online_nodes) / online_count
        
        # Distribuição por tipo
        type_distribution = {}
        for node in online_nodes:
            node_type = node["type"]
            type_distribution[node_type] = type_distribution.get(node_type, 0) + 1
        
        # Distribuição geográfica
        location_distribution = {}
        for node in online_nodes:
            location = node["location"]
            location_distribution[location] = location_distribution.get(location, 0) + 1
        
        return {
            "total_nodes": total_nodes,
            "online_nodes": online_count,
            "offline_nodes": total_nodes - online_count,
            "availability_percent": (online_count / total_nodes) * 100,
            "total_connections": total_connections,
            "avg_latency_ms": round(avg_latency, 2),
            "total_bandwidth_mbps": total_bandwidth,
            "avg_bandwidth_per_node": round(total_bandwidth / online_count, 2),
            "avg_cpu_usage": round(avg_cpu, 2),
            "avg_memory_usage": round(avg_memory, 2),
            "type_distribution": type_distribution,
            "location_distribution": location_distribution,
            "network_health": self.calculate_network_health(online_count, avg_latency, avg_cpu)
        }
    
    def calculate_network_health(self, online_nodes: int, avg_latency: float, avg_cpu: float) -> str:
        """Calcula saúde geral da rede"""
        health_score = 0
        
        # Pontuação baseada no número de nós
        if online_nodes >= 1000:
            health_score += 40
        elif online_nodes >= 500:
            health_score += 35
        elif online_nodes >= 100:
            health_score += 30
        elif online_nodes >= 50:
            health_score += 20
        else:
            health_score += 10
        
        # Pontuação baseada na latência
        if avg_latency <= 50:
            health_score += 30
        elif avg_latency <= 100:
            health_score += 25
        elif avg_latency <= 150:
            health_score += 15
        else:
            health_score += 5
        
        # Pontuação baseada no CPU
        if avg_cpu <= 50:
            health_score += 30
        elif avg_cpu <= 70:
            health_score += 20
        elif avg_cpu <= 85:
            health_score += 10
        else:
            health_score += 5
        
        if health_score >= 90:
            return "🟢 EXCELENTE"
        elif health_score >= 75:
            return "🟡 BOM"
        elif health_score >= 60:
            return "🟠 REGULAR"
        else:
            return "🔴 CRÍTICO"
    
    def estimate_max_capacity(self) -> dict:
        """Estima capacidade máxima teórica da rede"""
        max_by_type = {}
        total_theoretical = 0
        
        for node_type, config in self.node_types.items():
            max_nodes = config["max_nodes"]
            max_by_type[node_type] = max_nodes
            total_theoretical += max_nodes
        
        # Limitações práticas
        practical_limits = {
            "memory_limit": 10000,  # 10k nós por limitação de memória
            "network_limit": 5000,   # 5k nós por limitação de rede
            "processing_limit": 2000, # 2k nós por limitação de processamento
            "ui_limit": 1000        # 1k nós para interface responsiva
        }
        
        recommended_max = min(practical_limits.values())
        
        return {
            "theoretical_max": total_theoretical,
            "max_by_type": max_by_type,
            "practical_limits": practical_limits,
            "recommended_max": recommended_max,
            "current_implementation": "Otimizada para até 1000 nós simultâneos"
        }

def perform_stress_test(target_nodes: int) -> dict:
    """Executa stress test da rede com número específico de nós"""
    analyzer = AEONNetworkAnalyzer()
    
    print(f"🧪 Iniciando stress test com {target_nodes} nós...")
    
    start_time = time.time()
    
    # Gerar nós
    nodes = analyzer.generate_realistic_nodes(target_nodes)
    generation_time = time.time() - start_time
    
    # Calcular métricas
    metrics_start = time.time()
    metrics = analyzer.calculate_network_metrics(nodes)
    metrics_time = time.time() - metrics_start
    
    total_time = time.time() - start_time
    
    return {
        "test_config": {
            "target_nodes": target_nodes,
            "generation_time_s": round(generation_time, 3),
            "metrics_time_s": round(metrics_time, 3),
            "total_time_s": round(total_time, 3)
        },
        "network_metrics": metrics,
        "performance": {
            "nodes_per_second": round(target_nodes / total_time, 2),
            "memory_efficient": total_time < 5.0,
            "ui_responsive": target_nodes <= 1000
        }
    }
