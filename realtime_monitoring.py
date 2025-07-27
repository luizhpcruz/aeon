#!/usr/bin/env python3
"""
📊 AEONCOSMA REAL-TIME MONITORING DASHBOARD
Sistema de Monitoramento em Tempo Real com Métricas Prometheus
Desenvolvido por Luiz Cruz - 2025
"""

import time
import json
import threading
import psutil
import socket
from datetime import datetime, timedelta
from typing import Dict, List, Any
import statistics
from prometheus_client import start_http_server, Gauge, Counter, Histogram, Summary
import logging

# Configuração das métricas Prometheus
PROMETHEUS_PORT = 8001

# Métricas de Sistema
system_cpu_gauge = Gauge('aeoncosma_system_cpu_percent', 'CPU usage percentage')
system_memory_gauge = Gauge('aeoncosma_system_memory_percent', 'Memory usage percentage')
system_network_bytes_sent = Counter('aeoncosma_network_bytes_sent_total', 'Total network bytes sent')
system_network_bytes_recv = Counter('aeoncosma_network_bytes_received_total', 'Total network bytes received')

# Métricas de Rede P2P
active_nodes_gauge = Gauge('aeoncosma_active_nodes', 'Number of active P2P nodes')
peer_connections_gauge = Gauge('aeoncosma_peer_connections_total', 'Total peer connections across all nodes')
successful_connections_counter = Counter('aeoncosma_successful_connections_total', 'Total successful peer connections')
failed_connections_counter = Counter('aeoncosma_failed_connections_total', 'Total failed peer connections')

# Métricas de Trading
transaction_pool_gauge = Gauge('aeoncosma_transaction_pool_size', 'Size of transaction pool')
transactions_processed_counter = Counter('aeoncosma_transactions_processed_total', 'Total transactions processed')
consensus_participations_counter = Counter('aeoncosma_consensus_participations_total', 'Total consensus participations')
order_book_size_gauge = Gauge('aeoncosma_order_book_size', 'Total size of order books')

# Métricas de Performance
message_latency_histogram = Histogram('aeoncosma_message_latency_seconds', 'Message propagation latency')
consensus_time_histogram = Histogram('aeoncosma_consensus_time_seconds', 'Time to reach consensus')
network_health_gauge = Gauge('aeoncosma_network_health_score', 'Network health score (0-1)')

# Métricas de Negócio
commercial_value_gauge = Gauge('aeoncosma_estimated_commercial_value_usd', 'Estimated commercial value in USD')
scalability_score_gauge = Gauge('aeoncosma_scalability_score', 'Scalability score (0-100)')

class PrometheusExporter:
    """Exportador de métricas para Prometheus"""
    
    def __init__(self, port=PROMETHEUS_PORT):
        self.port = port
        self.running = False
        
    def start(self):
        """Inicia servidor de métricas"""
        try:
            start_http_server(self.port)
            self.running = True
            logging.info(f"📊 Prometheus exporter iniciado na porta {self.port}")
            logging.info(f"🌐 Métricas disponíveis em: http://localhost:{self.port}/metrics")
            return True
        except Exception as e:
            logging.error(f"❌ Erro ao iniciar Prometheus exporter: {e}")
            return False
    
    def update_system_metrics(self, metrics: Dict):
        """Atualiza métricas do sistema"""
        system_cpu_gauge.set(metrics.get('cpu_percent', 0))
        system_memory_gauge.set(metrics.get('memory_percent', 0))
        
        # Atualiza contadores de rede (apenas incrementos)
        current_sent = metrics.get('network_bytes_sent', 0)
        current_recv = metrics.get('network_bytes_recv', 0)
        
        # Nota: Em produção, seria necessário armazenar valores anteriores
        # para calcular incrementos corretamente
    
    def update_network_metrics(self, active_nodes: int, peer_connections: int, 
                             successful_conn: int, failed_conn: int):
        """Atualiza métricas de rede"""
        active_nodes_gauge.set(active_nodes)
        peer_connections_gauge.set(peer_connections)
        successful_connections_counter._value._value += successful_conn
        failed_connections_counter._value._value += failed_conn
    
    def update_trading_metrics(self, transaction_pool: int, transactions_processed: int,
                             consensus_count: int, order_book_size: int):
        """Atualiza métricas de trading"""
        transaction_pool_gauge.set(transaction_pool)
        transactions_processed_counter._value._value += transactions_processed
        consensus_participations_counter._value._value += consensus_count
        order_book_size_gauge.set(order_book_size)
    
    def record_message_latency(self, latency_seconds: float):
        """Registra latência de mensagem"""
        message_latency_histogram.observe(latency_seconds)
    
    def record_consensus_time(self, consensus_time_seconds: float):
        """Registra tempo de consenso"""
        consensus_time_histogram.observe(consensus_time_seconds)
    
    def update_business_metrics(self, commercial_value: float, scalability_score: float):
        """Atualiza métricas de negócio"""
        commercial_value_gauge.set(commercial_value)
        scalability_score_gauge.set(scalability_score)
    
    def update_network_health(self, health_score: float):
        """Atualiza score de saúde da rede"""
        network_health_gauge.set(health_score)

class RealTimeMonitor:
    """Monitor em tempo real do sistema AEONCOSMA"""
    
    def __init__(self):
        self.prometheus = PrometheusExporter()
        self.running = False
        self.metrics_history = []
        self.start_time = datetime.now()
        
        # Dados de monitoramento
        self.nodes_data = {}
        self.network_events = []
        self.performance_data = []
        
        # Configuração de logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('realtime_monitoring.log'),
                logging.StreamHandler()
            ]
        )
    
    def start_monitoring(self):
        """Inicia monitoramento em tempo real"""
        logging.info("🚀 INICIANDO MONITORAMENTO EM TEMPO REAL")
        
        # Inicia exportador Prometheus
        if not self.prometheus.start():
            logging.error("❌ Falha ao iniciar exportador Prometheus")
            return False
        
        self.running = True
        
        # Threads de monitoramento
        threading.Thread(target=self._system_monitor, daemon=True).start()
        threading.Thread(target=self._network_scanner, daemon=True).start()
        threading.Thread(target=self._performance_analyzer, daemon=True).start()
        threading.Thread(target=self._business_analyzer, daemon=True).start()
        threading.Thread(target=self._live_dashboard, daemon=True).start()
        
        logging.info("✅ Monitoramento em tempo real iniciado")
        logging.info("📊 Dashboard disponível no terminal")
        logging.info("🌐 Métricas Prometheus em http://localhost:8001/metrics")
        
        return True
    
    def _system_monitor(self):
        """Monitor de recursos do sistema"""
        while self.running:
            try:
                # Coleta métricas do sistema
                cpu_percent = psutil.cpu_percent(interval=1)
                memory = psutil.virtual_memory()
                network = psutil.net_io_counters()
                
                system_metrics = {
                    "timestamp": datetime.now().isoformat(),
                    "cpu_percent": cpu_percent,
                    "memory_percent": memory.percent,
                    "memory_used_gb": memory.used / (1024**3),
                    "network_bytes_sent": network.bytes_sent,
                    "network_bytes_recv": network.bytes_recv,
                    "active_connections": len(psutil.net_connections())
                }
                
                # Atualiza Prometheus
                self.prometheus.update_system_metrics(system_metrics)
                
                # Armazena histórico
                self.metrics_history.append(system_metrics)
                
                # Mantém apenas últimas 1000 entradas
                if len(self.metrics_history) > 1000:
                    self.metrics_history = self.metrics_history[-1000:]
                
                time.sleep(2)
                
            except Exception as e:
                logging.warning(f"⚠️ Erro no monitor de sistema: {e}")
    
    def _network_scanner(self):
        """Scanner de rede P2P"""
        base_port = 20000
        max_port = base_port + 1000
        
        while self.running:
            try:
                active_nodes = 0
                total_connections = 0
                successful_connections = 0
                failed_connections = 0
                
                # Escaneia portas para detectar nós ativos
                for port in range(base_port, max_port, 10):  # Amostra de portas
                    try:
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        sock.settimeout(0.1)
                        result = sock.connect_ex(('127.0.0.1', port))
                        
                        if result == 0:
                            active_nodes += 1
                            successful_connections += 1
                            
                            # Tenta obter informações do nó
                            node_info = self._query_node_info(port)
                            if node_info:
                                self.nodes_data[f"node_{port}"] = node_info
                                total_connections += node_info.get("peer_count", 0)
                        else:
                            failed_connections += 1
                            
                        sock.close()
                        
                    except Exception:
                        failed_connections += 1
                
                # Atualiza métricas de rede
                self.prometheus.update_network_metrics(
                    active_nodes, total_connections, 
                    successful_connections, failed_connections
                )
                
                # Calcula saúde da rede
                if successful_connections + failed_connections > 0:
                    health_score = successful_connections / (successful_connections + failed_connections)
                else:
                    health_score = 0
                
                self.prometheus.update_network_health(health_score)
                
                time.sleep(5)
                
            except Exception as e:
                logging.warning(f"⚠️ Erro no scanner de rede: {e}")
    
    def _query_node_info(self, port: int) -> Dict:
        """Consulta informações de um nó específico"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            sock.connect(('127.0.0.1', port))
            
            # Envia comando de status
            status_request = {
                "type": "status_request",
                "timestamp": datetime.now().isoformat()
            }
            
            sock.send(json.dumps(status_request).encode('utf-8'))
            response = sock.recv(1024).decode('utf-8')
            
            if response:
                return json.loads(response)
            
        except Exception:
            pass
        finally:
            try:
                sock.close()
            except:
                pass
        
        return {}
    
    def _performance_analyzer(self):
        """Analisador de performance"""
        while self.running:
            try:
                if len(self.metrics_history) >= 10:
                    # Análise dos últimos 10 pontos
                    recent_metrics = self.metrics_history[-10:]
                    
                    # Calcula tendências
                    cpu_trend = [m["cpu_percent"] for m in recent_metrics]
                    memory_trend = [m["memory_percent"] for m in recent_metrics]
                    
                    avg_cpu = statistics.mean(cpu_trend)
                    avg_memory = statistics.mean(memory_trend)
                    
                    # Detecta padrões de performance
                    performance_score = self._calculate_performance_score(avg_cpu, avg_memory)
                    
                    self.performance_data.append({
                        "timestamp": datetime.now().isoformat(),
                        "avg_cpu": avg_cpu,
                        "avg_memory": avg_memory,
                        "performance_score": performance_score
                    })
                    
                    # Simula latência de rede (em produção seria medida real)
                    simulated_latency = self._estimate_network_latency()
                    self.prometheus.record_message_latency(simulated_latency)
                
                time.sleep(10)
                
            except Exception as e:
                logging.warning(f"⚠️ Erro no analisador de performance: {e}")
    
    def _calculate_performance_score(self, cpu: float, memory: float) -> float:
        """Calcula score de performance (0-100)"""
        # Score baseado em uso eficiente de recursos
        cpu_score = max(0, 100 - cpu)  # Menos CPU = melhor
        memory_score = max(0, 100 - memory)  # Menos memória = melhor
        
        return (cpu_score + memory_score) / 2
    
    def _estimate_network_latency(self) -> float:
        """Estima latência da rede baseada no número de nós ativos"""
        active_nodes = len(self.nodes_data)
        
        if active_nodes < 10:
            return 0.001  # 1ms
        elif active_nodes < 100:
            return 0.01   # 10ms
        elif active_nodes < 500:
            return 0.05   # 50ms
        else:
            return 0.1    # 100ms
    
    def _business_analyzer(self):
        """Analisador de métricas de negócio"""
        while self.running:
            try:
                active_nodes = len(self.nodes_data)
                
                # Calcula valor comercial baseado na escalabilidade
                commercial_value = self._calculate_commercial_value(active_nodes)
                
                # Calcula score de escalabilidade
                scalability_score = self._calculate_scalability_score(active_nodes)
                
                # Atualiza métricas de negócio
                self.prometheus.update_business_metrics(commercial_value, scalability_score)
                
                time.sleep(30)  # Atualiza a cada 30 segundos
                
            except Exception as e:
                logging.warning(f"⚠️ Erro no analisador de negócio: {e}")
    
    def _calculate_commercial_value(self, active_nodes: int) -> float:
        """Calcula valor comercial estimado baseado na escalabilidade"""
        if active_nodes >= 1000:
            return 10_000_000  # $10M ARR potential
        elif active_nodes >= 500:
            return 5_000_000   # $5M ARR potential  
        elif active_nodes >= 200:
            return 2_000_000   # $2M ARR potential
        elif active_nodes >= 100:
            return 1_000_000   # $1M ARR potential
        elif active_nodes >= 50:
            return 500_000     # $500K ARR potential
        else:
            return 100_000     # $100K ARR potential
    
    def _calculate_scalability_score(self, active_nodes: int) -> float:
        """Calcula score de escalabilidade (0-100)"""
        # Score baseado no número de nós suportados
        if active_nodes >= 1000:
            return 100
        elif active_nodes >= 500:
            return 90
        elif active_nodes >= 200:
            return 75
        elif active_nodes >= 100:
            return 60
        elif active_nodes >= 50:
            return 40
        else:
            return min(40, (active_nodes / 50) * 40)
    
    def _live_dashboard(self):
        """Dashboard ao vivo no terminal"""
        while self.running:
            try:
                # Limpa tela (compatível com Windows/Linux)
                import os
                os.system('cls' if os.name == 'nt' else 'clear')
                
                # Dados atuais
                active_nodes = len(self.nodes_data)
                uptime = (datetime.now() - self.start_time).total_seconds()
                
                # Métricas recentes
                if self.metrics_history:
                    latest_metrics = self.metrics_history[-1]
                    cpu = latest_metrics["cpu_percent"]
                    memory = latest_metrics["memory_percent"]
                    connections = latest_metrics["active_connections"]
                else:
                    cpu = memory = connections = 0
                
                # Calcula valores de negócio
                commercial_value = self._calculate_commercial_value(active_nodes)
                scalability_score = self._calculate_scalability_score(active_nodes)
                
                # Dashboard
                print("🌟 AEONCOSMA REAL-TIME MONITORING DASHBOARD")
                print("=" * 80)
                print(f"⏱️ Uptime: {int(uptime)}s | 📊 Prometheus: http://localhost:8001/metrics")
                print(f"🕒 {datetime.now().strftime('%H:%M:%S')} | 🌐 Monitoramento Ativo")
                print()
                
                print("📊 MÉTRICAS DE SISTEMA:")
                print(f"   🖥️ CPU: {cpu:.1f}% | 💾 RAM: {memory:.1f}% | 🔗 Conexões: {connections}")
                print()
                
                print("🌐 MÉTRICAS DE REDE P2P:")
                print(f"   🌟 Nós Ativos: {active_nodes}")
                print(f"   🤝 Conexões P2P: {sum(node.get('peer_count', 0) for node in self.nodes_data.values())}")
                print(f"   📈 Taxa de Sucesso: {self._get_connection_success_rate():.1f}%")
                print()
                
                print("💰 MÉTRICAS DE NEGÓCIO:")
                print(f"   💵 Valor Comercial Estimado: ${commercial_value:,.0f} ARR")
                print(f"   📊 Score de Escalabilidade: {scalability_score:.1f}/100")
                print()
                
                print("🎯 STATUS DO TESTE:")
                if active_nodes >= 1000:
                    print("   🥇 EXCELENTE: 1000+ nós - TESE COMPROVADA!")
                elif active_nodes >= 500:
                    print("   🥈 MUITO BOM: 500+ nós - Altamente escalável")
                elif active_nodes >= 200:
                    print("   🥉 BOM: 200+ nós - Escalável para empresas")
                elif active_nodes >= 100:
                    print("   📈 BÁSICO: 100+ nós - Proof of concept")
                elif active_nodes >= 50:
                    print("   🌱 INICIAL: 50+ nós - Desenvolvimento")
                else:
                    print("   🚧 BOOTSTRAP: Construindo rede...")
                
                print()
                print("🔄 Atualizando a cada 10 segundos... (Ctrl+C para parar)")
                print("=" * 80)
                
                time.sleep(10)
                
            except Exception as e:
                logging.warning(f"⚠️ Erro no dashboard: {e}")
    
    def _get_connection_success_rate(self) -> float:
        """Calcula taxa de sucesso de conexões"""
        if not self.network_events:
            return 100.0
        
        recent_events = [e for e in self.network_events 
                        if datetime.fromisoformat(e["timestamp"]) > datetime.now() - timedelta(minutes=5)]
        
        if not recent_events:
            return 100.0
        
        successes = sum(1 for e in recent_events if e["type"] == "success")
        total = len(recent_events)
        
        return (successes / total) * 100
    
    def stop_monitoring(self):
        """Para o monitoramento"""
        self.running = False
        logging.info("🛑 Monitoramento em tempo real parado")
    
    def get_summary_report(self) -> str:
        """Gera relatório resumido"""
        active_nodes = len(self.nodes_data)
        uptime = (datetime.now() - self.start_time).total_seconds()
        commercial_value = self._calculate_commercial_value(active_nodes)
        scalability_score = self._calculate_scalability_score(active_nodes)
        
        return f"""
📊 RELATÓRIO DE MONITORAMENTO RESUMIDO
Tempo de execução: {int(uptime)}s
Nós ativos detectados: {active_nodes}
Valor comercial estimado: ${commercial_value:,.0f} ARR
Score de escalabilidade: {scalability_score:.1f}/100
Status: {'SUCESSO' if active_nodes >= 100 else 'EM PROGRESSO'}
"""

def main():
    """Função principal do monitor"""
    print("📊 AEONCOSMA REAL-TIME MONITORING")
    print("Sistema de Monitoramento com Métricas Prometheus")
    print("Desenvolvido por Luiz Cruz - 2025")
    print("=" * 60)
    
    monitor = RealTimeMonitor()
    
    try:
        if monitor.start_monitoring():
            print("✅ Monitoramento iniciado com sucesso!")
            print("📊 Dashboard ao vivo será exibido...")
            print("🌐 Métricas Prometheus: http://localhost:8001/metrics")
            
            # Mantém monitoramento ativo
            while monitor.running:
                time.sleep(1)
        else:
            print("❌ Falha ao iniciar monitoramento")
            
    except KeyboardInterrupt:
        print("\n🛑 Parando monitoramento...")
        monitor.stop_monitoring()
        print("✅ Monitoramento finalizado")
        print(monitor.get_summary_report())

if __name__ == "__main__":
    main()
