#!/usr/bin/env python3
"""
🌐 AEONCOSMA P2P Network - Demo Interativo
Demonstração da rede P2P em funcionamento
Copyright 2025 - Luiz H. P. Cruz
"""

import asyncio
import sys
import os
import time
from datetime import datetime

# Adicionar o path do aeoncosma
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from aeoncosma.p2p.p2p_node import P2PNode
from aeoncosma.utils.helpers import Logger

class P2PNetworkDemo:
    """Demo interativo da rede P2P AEONCOSMA"""
    
    def __init__(self):
        self.logger = Logger("P2P_DEMO")
        self.nodes = {}
        self.running = True
        
    async def create_network(self, num_nodes=5):
        """Criar rede P2P com múltiplos nós"""
        print("🌐 Inicializando Rede P2P AEONCOSMA...")
        print(f"📡 Criando {num_nodes} nós...")
        
        # Criar nós
        for i in range(num_nodes):
            node_id = f"node_{i+1}"
            node = P2PNode(node_id)
            self.nodes[node_id] = node
            
            # Simular conexão com outros nós
            for other_id, other_node in self.nodes.items():
                if other_id != node_id:
                    await node.connect_peer(other_id, f"192.168.1.{i+10}")
                    await other_node.connect_peer(node_id, f"192.168.1.{i+20}")
            
            print(f"✅ Nó {node_id} criado e conectado")
            await asyncio.sleep(0.1)  # Simular tempo de rede
        
        print(f"🎉 Rede P2P criada com {len(self.nodes)} nós!")
        return True
    
    async def show_network_status(self):
        """Mostrar status da rede"""
        print("\n" + "="*60)
        print("📊 STATUS DA REDE P2P AEONCOSMA")
        print("="*60)
        
        total_peers = 0
        total_messages = 0
        
        for node_id, node in self.nodes.items():
            status = node.get_status()
            total_peers += status.get('connected_peers', 0)
            total_messages += status.get('messages_sent', 0) + status.get('messages_received', 0)
            
            print(f"🔵 {node_id.upper()}:")
            print(f"   Peers: {status.get('connected_peers', 0)}")
            print(f"   Enviadas: {status.get('messages_sent', 0)}")
            print(f"   Recebidas: {status.get('messages_received', 0)}")
            print(f"   Status: {'🟢 Online' if status.get('is_online') else '🔴 Offline'}")
            print()
        
        print(f"📈 RESUMO DA REDE:")
        print(f"   Total de Nós: {len(self.nodes)}")
        print(f"   Total de Conexões: {total_peers}")
        print(f"   Total de Mensagens: {total_messages}")
        print(f"   Uptime: {datetime.now().strftime('%H:%M:%S')}")
        print("="*60)
    
    async def broadcast_message(self, sender_id, message):
        """Transmitir mensagem na rede"""
        if sender_id in self.nodes:
            node = self.nodes[sender_id]
            print(f"📡 {sender_id} transmitindo: '{message}'")
            
            result = await node.broadcast(message, "user_message", 5)
            
            # Simular recepção nos outros nós
            for other_id, other_node in self.nodes.items():
                if other_id != sender_id:
                    await other_node.receive_message({
                        'sender': sender_id,
                        'content': message,
                        'message_type': 'user_message',
                        'timestamp': datetime.now().isoformat()
                    })
            
            print(f"✅ Mensagem transmitida para {len(self.nodes)-1} nós!")
            return result
        else:
            print(f"❌ Nó {sender_id} não encontrado")
            return None
    
    async def simulate_network_activity(self):
        """Simular atividade automática na rede"""
        messages = [
            "Dados de temperatura: 25.3°C",
            "Status do equipamento: Operacional",
            "Alerta: Consumo acima do normal",
            "Sincronização de dados concluída",
            "Backup automático realizado",
            "Monitoramento em tempo real ativo"
        ]
        
        print("🤖 Iniciando simulação de atividade automática...")
        
        for i, message in enumerate(messages):
            if not self.running:
                break
                
            # Escolher nó aleatório
            import random
            sender = random.choice(list(self.nodes.keys()))
            
            await self.broadcast_message(sender, message)
            await asyncio.sleep(2)  # Intervalo entre mensagens
        
        print("✅ Simulação de atividade concluída!")
    
    async def interactive_mode(self):
        """Modo interativo para o usuário"""
        print("\n🎮 MODO INTERATIVO ATIVADO!")
        print("Comandos disponíveis:")
        print("  📤 'send <nó> <mensagem>' - Enviar mensagem")
        print("  📊 'status' - Ver status da rede")
        print("  🤖 'auto' - Atividade automática")
        print("  ❌ 'quit' - Sair")
        print()
        
        while self.running:
            try:
                command = input("🌐 P2P> ").strip()
                
                if command == 'quit':
                    self.running = False
                    break
                elif command == 'status':
                    await self.show_network_status()
                elif command == 'auto':
                    await self.simulate_network_activity()
                elif command.startswith('send '):
                    parts = command.split(' ', 2)
                    if len(parts) >= 3:
                        node_id = parts[1]
                        message = parts[2]
                        await self.broadcast_message(node_id, message)
                    else:
                        print("❌ Formato: send <nó> <mensagem>")
                elif command == 'help':
                    print("📋 Comandos: send, status, auto, quit")
                elif command == '':
                    continue
                else:
                    print("❌ Comando não reconhecido. Digite 'help' para ajuda.")
                    
            except KeyboardInterrupt:
                print("\n⚠️ Interrompido pelo usuário")
                self.running = False
                break
            except Exception as e:
                print(f"❌ Erro: {e}")
    
    async def run_demo(self):
        """Executar demonstração completa"""
        try:
            print("🚀 AEONCOSMA P2P Network Demo")
            print("Created by Luiz H. P. Cruz")
            print("="*50)
            
            # Criar rede
            await self.create_network(5)
            
            # Mostrar status inicial
            await self.show_network_status()
            
            # Demonstração automática
            print("📡 Iniciando demonstração automática...")
            await asyncio.sleep(1)
            
            # Algumas mensagens de teste
            await self.broadcast_message("node_1", "Olá rede AEONCOSMA P2P!")
            await asyncio.sleep(1)
            await self.broadcast_message("node_3", "Sistema de energia operacional")
            await asyncio.sleep(1)
            await self.broadcast_message("node_5", "Dados sincronizados com sucesso")
            
            # Status após demo
            await self.show_network_status()
            
            # Modo interativo
            await self.interactive_mode()
            
        except Exception as e:
            print(f"❌ Erro na demonstração: {e}")
        finally:
            print("🔄 Finalizando rede P2P...")
            for node in self.nodes.values():
                node.shutdown()
            print("✅ Demo finalizada!")

async def main():
    """Função principal"""
    demo = P2PNetworkDemo()
    await demo.run_demo()

if __name__ == "__main__":
    print("🌐 Iniciando AEONCOSMA P2P Network Demo...")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Demo encerrada pelo usuário")
    except Exception as e:
        print(f"❌ Erro fatal: {e}")
    finally:
        print("🔄 Programa finalizado")
