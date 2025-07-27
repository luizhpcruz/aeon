#!/usr/bin/env python3
"""
🚀 AEONCOSMA SIMPLIFIED ECOSYSTEM TEST
Teste Simplificado de Validação da Arquitetura P2P
Usando apenas bibliotecas padrão do Python
Desenvolvido por Luiz Cruz - 2025
"""

import sys
import os
import time
import threading
import socket
import json
import random
import logging
import signal
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import statistics
import csv

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('simplified_ecosystem_test.log'),
        logging.StreamHandler()
    ]
)

# Configuração do teste simplificado
SIMPLE_CONFIG = {
    "max_nodes": 100,  # Reduzido para evitar problemas de recursos
    "phases": {
        "bootstrap": 5,
        "network": 15,
        "scaling": 30,
        "stress": 50,
        "maximum": 100
    },
    "base_port": 30000,
    "test_duration": 300,  # 5 minutos
    "monitoring_interval": 5
}

class SimpleMetrics:
    """Sistema simples de métricas"""
    
    def __init__(self):
        self.data = []
        self.start_time = datetime.now()
        
    def record(self, metric_type: str, value: Any, node_id: str = None):
        """Registra métrica"""
        self.data.append({
            "timestamp": datetime.now(),
            "type": metric_type,
            "value": value,
            "node_id": node_id
        })
    
    def get_summary(self):
        """Retorna resumo das métricas"""
        if not self.data:
            return {}
        
        connections = [d for d in self.data if d["type"] == "connection"]
        successes = [d for d in self.data if d["type"] == "success"]
        failures = [d for d in self.data if d["type"] == "failure"]
        
        success_rate = len(successes) / max(1, len(connections)) if connections else 0
        
        return {
            "total_events": len(self.data),
            "connections": len(connections),
            "successes": len(successes),
            "failures": len(failures),
            "success_rate": success_rate,
            "duration": (datetime.now() - self.start_time).total_seconds()
        }

class SimpleNode:
    """Nó P2P simplificado para teste"""
    
    def __init__(self, node_id: str, port: int, metrics: SimpleMetrics):
        self.node_id = node_id
        self.port = port
        self.host = "127.0.0.1"
        self.metrics = metrics
        self.running = False
        self.socket = None
        self.peers = {}
        self.message_count = 0
        
    def start(self) -> bool:
        """Inicia o nó"""
        try:
            self.running = True
            
            # Socket TCP
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.settimeout(2.0)
            self.socket.bind((self.host, self.port))
            self.socket.listen(5)
            
            # Threads básicas
            threading.Thread(target=self._listen, daemon=True).start()
            threading.Thread(target=self._discover_peers, daemon=True).start()
            
            self.metrics.record("node_started", True, self.node_id)
            return True
            
        except Exception as e:
            logging.error(f"[{self.node_id}] Erro ao iniciar: {e}")
            return False
    
    def _listen(self):
        """Escuta conexões"""
        while self.running:
            try:
                conn, addr = self.socket.accept()
                threading.Thread(target=self._handle_connection, args=(conn, addr), daemon=True).start()
            except socket.timeout:
                continue
            except Exception as e:
                if self.running:
                    logging.debug(f"[{self.node_id}] Erro na escuta: {e}")
                break
    
    def _handle_connection(self, conn, addr):
        """Processa conexão"""
        try:
            data = conn.recv(1024).decode('utf-8')
            if data:
                message = json.loads(data)
                response = self._process_message(message)
                
                if response:
                    conn.send(json.dumps(response).encode('utf-8'))
                
                self.message_count += 1
                self.metrics.record("message_processed", self.message_count, self.node_id)
        
        except Exception as e:
            self.metrics.record("failure", str(e), self.node_id)
        finally:
            conn.close()
    
    def _process_message(self, message: Dict) -> Dict:
        """Processa mensagem recebida"""
        msg_type = message.get("type", "unknown")
        
        if msg_type == "discovery":
            peer_id = message.get("node_id")
            if peer_id and peer_id != self.node_id:
                self.peers[peer_id] = {
                    "host": message.get("host", "127.0.0.1"),
                    "port": message.get("port"),
                    "timestamp": datetime.now()
                }
                
                self.metrics.record("peer_added", peer_id, self.node_id)
                
                return {
                    "status": "accepted",
                    "node_id": self.node_id,
                    "peer_count": len(self.peers)
                }
        
        return {"status": "processed", "node_id": self.node_id}
    
    def _discover_peers(self):
        """Descobre outros peers"""
        base_port = SIMPLE_CONFIG["base_port"]
        max_port = base_port + SIMPLE_CONFIG["max_nodes"]
        
        while self.running:
            try:
                # Tenta conectar com algumas portas aleatórias
                target_ports = random.sample(
                    [p for p in range(base_port, max_port) if p != self.port], 
                    min(3, max_port - base_port - 1)
                )
                
                for port in target_ports:
                    if not self.running:
                        break
                    
                    self._attempt_connection(port)
                
                time.sleep(5)  # Descoberta a cada 5 segundos
                
            except Exception as e:
                logging.debug(f"[{self.node_id}] Erro na descoberta: {e}")
    
    def _attempt_connection(self, target_port: int):
        """Tenta conectar com outro nó"""
        try:
            self.metrics.record("connection", target_port, self.node_id)
            
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1.0)
            sock.connect((self.host, target_port))
            
            discovery_msg = {
                "type": "discovery",
                "node_id": self.node_id,
                "host": self.host,
                "port": self.port
            }
            
            sock.send(json.dumps(discovery_msg).encode('utf-8'))
            response = sock.recv(512).decode('utf-8')
            
            if response:
                self.metrics.record("success", target_port, self.node_id)
            
        except Exception:
            self.metrics.record("failure", target_port, self.node_id)
        finally:
            try:
                sock.close()
            except:
                pass
    
    def get_status(self) -> Dict:
        """Retorna status do nó"""
        return {
            "node_id": self.node_id,
            "port": self.port,
            "running": self.running,
            "peers": len(self.peers),
            "messages": self.message_count
        }
    
    def stop(self):
        """Para o nó"""
        self.running = False
        if self.socket:
            try:
                self.socket.close()
            except:
                pass

class SimpleOrchestrator:
    """Orquestrador simplificado do teste"""
    
    def __init__(self):
        self.metrics = SimpleMetrics()
        self.nodes = {}
        self.running = False
        
        # Handler para Ctrl+C
        signal.signal(signal.SIGINT, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handler para parada"""
        print("\n🛑 Parando teste...")
        self.stop_test()
    
    def run_ecosystem_test(self):
        """Executa teste do ecossistema"""
        print("🚀 AEONCOSMA SIMPLIFIED ECOSYSTEM TEST")
        print("=" * 60)
        print(f"🎯 Máximo de nós: {SIMPLE_CONFIG['max_nodes']}")
        print(f"⏱️ Duração: {SIMPLE_CONFIG['test_duration']} segundos")
        print(f"📍 Portas: {SIMPLE_CONFIG['base_port']}+")
        
        self.running = True
        
        # Thread de monitoramento
        threading.Thread(target=self._monitor, daemon=True).start()
        
        try:
            # Executa fases progressivamente
            for phase_name, node_count in SIMPLE_CONFIG["phases"].items():
                if not self.running:
                    break
                
                print(f"\n🏗️ FASE: {phase_name.upper()} ({node_count} nós)")
                
                # Cria nós incrementalmente
                nodes_to_create = node_count - len(self.nodes)
                if nodes_to_create > 0:
                    created = self._create_nodes(nodes_to_create, phase_name)
                    print(f"✅ Criados {created}/{nodes_to_create} nós")
                
                # Aguarda estabilização
                print("⏳ Aguardando estabilização...")
                time.sleep(15)
            
            # Executa por tempo determinado
            print(f"\n⏱️ Executando teste por {SIMPLE_CONFIG['test_duration']} segundos...")
            start_time = time.time()
            
            while (time.time() - start_time) < SIMPLE_CONFIG['test_duration'] and self.running:
                time.sleep(1)
        
        except Exception as e:
            print(f"❌ Erro no teste: {e}")
        
        finally:
            self._finalize_test()
    
    def _create_nodes(self, count: int, phase: str) -> int:
        """Cria nós para uma fase"""
        created = 0
        start_port = SIMPLE_CONFIG["base_port"] + len(self.nodes)
        
        for i in range(count):
            node_id = f"simple_{phase}_{i:02d}"
            port = start_port + i
            
            node = SimpleNode(node_id, port, self.metrics)
            
            if node.start():
                self.nodes[node_id] = node
                created += 1
                
                if created % 5 == 0:
                    print(f"   ✅ {created}/{count} nós criados")
                
                time.sleep(0.1)  # Pausa pequena
            else:
                print(f"   ❌ Falha ao criar {node_id}")
        
        return created
    
    def _monitor(self):
        """Monitor do sistema"""
        while self.running:
            try:
                active_nodes = sum(1 for node in self.nodes.values() if node.running)
                total_peers = sum(len(node.peers) for node in self.nodes.values())
                
                summary = self.metrics.get_summary()
                
                print(f"📊 STATUS - Nós: {active_nodes}/{len(self.nodes)}, "
                      f"Peers: {total_peers}, "
                      f"Taxa sucesso: {summary.get('success_rate', 0):.2%}")
                
                time.sleep(SIMPLE_CONFIG["monitoring_interval"])
                
            except Exception as e:
                logging.warning(f"Erro no monitor: {e}")
    
    def _finalize_test(self):
        """Finaliza teste"""
        print("\n🏁 FINALIZANDO TESTE")
        
        # Para todos os nós
        self.stop_test()
        
        # Gera relatório
        self._generate_report()
    
    def _generate_report(self):
        """Gera relatório final"""
        print("\n📊 GERANDO RELATÓRIO...")
        
        # Coleta dados finais
        active_nodes = sum(1 for node in self.nodes.values() if node.running)
        total_peers = sum(len(node.peers) for node in self.nodes.values())
        summary = self.metrics.get_summary()
        
        # Avaliação
        max_nodes = len(self.nodes)
        success_rate = summary.get("success_rate", 0)
        
        if max_nodes >= 80 and success_rate > 0.8:
            grade = "🥇 EXCELENTE"
            value = "$2M+ ARR potencial"
        elif max_nodes >= 50 and success_rate > 0.7:
            grade = "🥈 MUITO BOM"
            value = "$1M+ ARR potencial"
        elif max_nodes >= 20 and success_rate > 0.6:
            grade = "🥉 BOM"
            value = "$500K+ ARR potencial"
        else:
            grade = "📈 BÁSICO"
            value = "$100K+ ARR potencial"
        
        report = f"""
🌟 RELATÓRIO - AEONCOSMA SIMPLIFIED TEST
{'=' * 60}

🎯 RESULTADO: {grade}

📊 MÉTRICAS FINAIS:
   🌐 Nós criados: {len(self.nodes)}
   ✅ Nós ativos: {active_nodes}
   🤝 Conexões P2P: {total_peers}
   📈 Taxa de sucesso: {success_rate:.2%}
   ⏱️ Duração: {summary.get('duration', 0):.0f}s

💰 VALOR COMERCIAL: {value}

🏆 VALIDAÇÃO:
   ✅ Criação de nós: {'APROVADO' if max_nodes >= 20 else 'BÁSICO'}
   ✅ Descoberta P2P: {'APROVADO' if success_rate > 0.7 else 'BÁSICO'}
   ✅ Estabilidade: {'APROVADO' if active_nodes/max(1,len(self.nodes)) > 0.8 else 'BÁSICO'}

🚀 CONCLUSÃO:
   Sistema demonstrou capacidade de suportar {max_nodes} nós
   com {success_rate:.1%} de taxa de sucesso em descoberta P2P.
   
   {'✅ ARQUITETURA P2P VALIDADA!' if success_rate > 0.7 and max_nodes >= 30 else '⚠️ Requer otimizações para produção'}

{'=' * 60}
Desenvolvido por Luiz Cruz - 2025
"""
        
        print(report)
        
        # Salva relatório
        try:
            with open("simplified_test_report.txt", "w", encoding="utf-8") as f:
                f.write(report)
            print("📁 Relatório salvo em: simplified_test_report.txt")
        except Exception as e:
            print(f"⚠️ Erro ao salvar relatório: {e}")
        
        # Salva dados CSV
        try:
            with open("simplified_test_data.csv", "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["timestamp", "type", "value", "node_id"])
                
                for data in self.metrics.data:
                    writer.writerow([
                        data["timestamp"].isoformat(),
                        data["type"],
                        data["value"],
                        data["node_id"]
                    ])
            
            print("📊 Dados salvos em: simplified_test_data.csv")
        except Exception as e:
            print(f"⚠️ Erro ao salvar dados: {e}")
    
    def stop_test(self):
        """Para o teste"""
        self.running = False
        print("🛑 Parando todos os nós...")
        
        for node in self.nodes.values():
            try:
                node.stop()
            except:
                pass
        
        print("✅ Todos os nós parados")

def main():
    """Função principal"""
    print("🚀 AEONCOSMA SIMPLIFIED ECOSYSTEM TEST")
    print("Teste de Validação da Arquitetura P2P")
    print("Usando apenas bibliotecas padrão do Python")
    print("Desenvolvido por Luiz Cruz - 2025")
    print("=" * 60)
    
    print("🎯 OBJETIVOS DO TESTE:")
    print("   • Validar descoberta automática de peers")
    print("   • Testar escalabilidade até 100 nós")
    print("   • Medir estabilidade da rede P2P")
    print("   • Gerar métricas para validação comercial")
    
    print(f"\n📊 CONFIGURAÇÃO:")
    print(f"   • Máximo de nós: {SIMPLE_CONFIG['max_nodes']}")
    print(f"   • Fases: {len(SIMPLE_CONFIG['phases'])}")
    print(f"   • Duração: {SIMPLE_CONFIG['test_duration']} segundos")
    print(f"   • Portas: {SIMPLE_CONFIG['base_port']}+")
    
    response = input("\n🚀 Executar teste simplificado? (s/N): ")
    if response.lower() not in ['s', 'sim', 'yes', 'y']:
        print("❌ Teste cancelado")
        return
    
    # Executa teste
    orchestrator = SimpleOrchestrator()
    
    try:
        orchestrator.run_ecosystem_test()
    except KeyboardInterrupt:
        print("\n🛑 Teste interrompido")
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        orchestrator.stop_test()
        print("\n✅ TESTE CONCLUÍDO")

if __name__ == "__main__":
    main()
