#!/usr/bin/env python3
"""
📊 MONITOR DE NÓS AEONCOSMA
Verifica status dos nós P2P ativos na rede
"""

import socket
import json
import time
import threading
from datetime import datetime

class NodeMonitor:
    """Monitor de nós P2P na rede"""
    
    def __init__(self):
        self.nodes_to_check = [
            {"host": "127.0.0.1", "port": 9000, "name": "Nó Principal"},
            {"host": "127.0.0.1", "port": 9001, "name": "Segundo Nó"},
            {"host": "127.0.0.1", "port": 9002, "name": "Terceiro Nó"}
        ]
        self.active_nodes = []
        
    def check_node_status(self, host, port, node_name):
        """Verifica se um nó está ativo"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex((host, port))
            sock.close()
            
            if result == 0:
                return True
            else:
                return False
                
        except Exception:
            return False
    
    def get_node_info(self, host, port):
        """Obtém informações detalhadas de um nó"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            sock.connect((host, port))
            
            # Envia comando de status (se suportado)
            status_request = {
                "type": "status_request",
                "timestamp": datetime.now().isoformat()
            }
            
            sock.send(json.dumps(status_request).encode('utf-8'))
            response = sock.recv(4096).decode('utf-8')
            
            if response:
                return json.loads(response)
            
        except Exception as e:
            return {"error": str(e)}
        finally:
            sock.close()
    
    def monitor_network(self):
        """Monitora toda a rede de nós"""
        print("🌐 MONITOR DE REDE AEONCOSMA")
        print("=" * 50)
        
        while True:
            active_count = 0
            current_time = datetime.now().strftime("%H:%M:%S")
            
            print(f"\n⏰ [{current_time}] Verificando status da rede...")
            
            for node in self.nodes_to_check:
                is_active = self.check_node_status(node["host"], node["port"], node["name"])
                
                if is_active:
                    print(f"✅ {node['name']} ({node['host']}:{node['port']}) - ATIVO")
                    active_count += 1
                else:
                    print(f"❌ {node['name']} ({node['host']}:{node['port']}) - INATIVO")
            
            print(f"\n📊 Status da Rede: {active_count}/{len(self.nodes_to_check)} nós ativos")
            
            if active_count == 0:
                print("🚨 ALERTA: Nenhum nó ativo na rede!")
                print("💡 Para ativar o nó principal: python aeoncosma\\main.py")
            elif active_count == 1:
                print("⚠️ Apenas 1 nó ativo - Rede não está distribuída")
                print("💡 Para ativar mais nós: python segundo_no_ativo.py")
            else:
                print("🎯 Rede P2P operacional!")
            
            print("-" * 50)
            time.sleep(10)  # Verifica a cada 10 segundos

def main():
    """Inicia monitoramento da rede"""
    monitor = NodeMonitor()
    
    try:
        monitor.monitor_network()
    except KeyboardInterrupt:
        print("\n🛑 Monitor finalizado pelo usuário")

if __name__ == "__main__":
    main()
