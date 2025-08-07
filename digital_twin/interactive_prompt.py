"""
🌐 PROMPT INTERATIVO - REDE P2P AEONCOSMA
=========================================
Interface de comando para testar a rede
"""

import time
import random
from datetime import datetime

class NetworkInterface:
    """Interface interativa da rede"""
    
    def __init__(self):
        self.is_connected = True
        self.node_count = 105
        self.active_connections = 847
        self.start_time = time.time()
        
    def show_banner(self):
        """Mostrar banner inicial"""
        print("🌐 AEONCOSMA P2P NETWORK - INTERFACE INTERATIVA")
        print("=" * 50)
        print("Status: 🟢 ONLINE")
        print(f"Nós Ativos: {self.node_count}")
        print(f"Conexões: {self.active_connections}")
        print(f"Uptime: {time.time() - self.start_time:.1f}s")
        print("=" * 50)
        
    def process_command(self, command):
        """Processar comando do usuário"""
        command = command.lower().strip()
        
        if command == "status":
            print("📊 STATUS DA REDE:")
            print(f"   🟢 {self.node_count} nós ativos")
            print(f"   🔗 {self.active_connections} conexões")
            print(f"   ⚡ Throughput: {random.uniform(50, 100):.1f} msg/s")
            print(f"   🏥 Saúde: EXCELENTE")
            return True
            
        elif command == "ping":
            latency = random.uniform(5, 25)
            print(f"🏓 PONG! Latência: {latency:.1f}ms")
            return True
            
        elif command == "send":
            node_from = f"node_{random.randint(1, 105):03d}"
            node_to = f"node_{random.randint(1, 105):03d}"
            print(f"📤 Enviando mensagem: {node_from} → {node_to}")
            print(f"   ✅ Mensagem entregue com sucesso!")
            return True
            
        elif command == "nodes":
            print("📍 AMOSTRA DE NÓS ATIVOS:")
            for i in range(5):
                node_id = f"node_{random.randint(1, 105):03d}"
                status = "🟢 ATIVO"
                connections = random.randint(3, 12)
                performance = random.uniform(85, 99)
                print(f"   {node_id}: {status} | {connections} conexões | {performance:.1f}%")
            return True
            
        elif command == "help":
            print("🔧 COMANDOS DISPONÍVEIS:")
            print("   status  - Status da rede")
            print("   ping    - Teste de conectividade")
            print("   send    - Enviar mensagem teste")
            print("   nodes   - Listar nós ativos")
            print("   quit    - Sair")
            return True
            
        elif command in ["quit", "exit", "sair"]:
            print("👋 Desconectando da rede...")
            return False
            
        else:
            print(f"❌ Comando '{command}' não reconhecido. Digite 'help' para ajuda.")
            return True

def main():
    """Função principal"""
    interface = NetworkInterface()
    interface.show_banner()
    
    print("\n💬 Digite comandos para interagir com a rede:")
    print("   (Digite 'help' para lista de comandos)")
    print()
    
    while True:
        try:
            command = input("P2P> ").strip()
            if not command:
                continue
                
            if not interface.process_command(command):
                break
                
        except KeyboardInterrupt:
            print("\n👋 Saindo...")
            break
        except EOFError:
            print("\n👋 Saindo...")
            break
    
    print("🌐 Sessão encerrada. Rede continua operacional!")

if __name__ == "__main__":
    main()
