#!/usr/bin/env python3
"""
🚀 LAUNCHER MULTI-NÓS AEONCOSMA
Inicia múltiplos nós P2P simultaneamente usando threading
"""

import threading
import time
import sys
import os
from datetime import datetime

# Adiciona path para importações
sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.join(os.path.dirname(__file__), 'aeoncosma'))

def start_node(port, node_id, delay=0):
    """Inicia um nó P2P em thread separada"""
    try:
        if delay > 0:
            print(f"⏰ [{node_id}] Aguardando {delay}s antes de iniciar...")
            time.sleep(delay)
        
        from aeoncosma.networking.p2p_node import P2PNode
        
        print(f"🚀 [{node_id}] Iniciando nó na porta {port}...")
        
        # Cria e inicia o nó
        node = P2PNode(
            host="127.0.0.1",
            port=port,
            node_id=node_id
        )
        
        node.start()
        
        # Aguarda um pouco e tenta conectar ao nó principal se não for o principal
        if port != 9000:
            time.sleep(3)
            print(f"🔗 [{node_id}] Tentando conectar ao nó principal...")
            
            response = node.connect_to_peer("127.0.0.1", 9000, node_id)
            if response:
                print(f"✅ [{node_id}] Conectado ao nó principal: {response.get('status')}")
            else:
                print(f"⚠️ [{node_id}] Não conseguiu conectar ao nó principal")
        
        print(f"🌐 [{node_id}] Nó ativo e operacional na porta {port}")
        
        # Mantém o nó rodando
        while node.running:
            time.sleep(1)
            
    except Exception as e:
        print(f"❌ [{node_id}] Erro ao iniciar nó: {e}")

def test_network_connectivity():
    """Testa conectividade da rede após inicialização"""
    print("\n🔍 TESTANDO CONECTIVIDADE DA REDE...")
    time.sleep(10)  # Aguarda nós inicializarem
    
    import socket
    import json
    
    nodes_to_test = [
        (9000, "nó_principal"),
        (9001, "segundo_nó"),
        (9002, "terceiro_nó")
    ]
    
    active_nodes = 0
    
    for port, name in nodes_to_test:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex(('127.0.0.1', port))
            
            if result == 0:
                print(f"✅ {name} (porta {port}): ATIVO")
                active_nodes += 1
            else:
                print(f"❌ {name} (porta {port}): INATIVO")
                
            sock.close()
            
        except Exception as e:
            print(f"⚠️ {name} (porta {port}): Erro - {e}")
    
    print(f"\n📊 RESULTADO: {active_nodes}/{len(nodes_to_test)} nós ativos")
    
    if active_nodes >= 2:
        print("🎯 REDE P2P DISTRIBUÍDA OPERACIONAL!")
    elif active_nodes == 1:
        print("⚠️ Apenas 1 nó ativo - Rede não distribuída")
    else:
        print("❌ Nenhum nó ativo detectado")

def main():
    """Função principal - lança múltiplos nós"""
    print("🌐 LAUNCHER MULTI-NÓS AEONCOSMA P2P")
    print("=" * 50)
    print(f"⏰ Iniciado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Configuração dos nós
    nodes_config = [
        {"port": 9000, "node_id": "aeon_principal", "delay": 0},
        {"port": 9001, "node_id": "segundo_no", "delay": 3},
        {"port": 9002, "node_id": "terceiro_no", "delay": 6}
    ]
    
    threads = []
    
    # Inicia cada nó em thread separada
    for config in nodes_config:
        thread = threading.Thread(
            target=start_node,
            args=(config["port"], config["node_id"], config["delay"]),
            daemon=True
        )
        thread.start()
        threads.append(thread)
        
        print(f"✅ Thread criada para {config['node_id']} (porta {config['port']})")
    
    # Thread para teste de conectividade
    test_thread = threading.Thread(target=test_network_connectivity, daemon=True)
    test_thread.start()
    
    print(f"\n🚀 TODOS OS {len(nodes_config)} NÓS FORAM INICIADOS!")
    print("📡 Aguarde alguns segundos para sincronização...")
    print("🔗 Teste de conectividade será executado automaticamente")
    print("\n💡 Pressione Ctrl+C para parar todos os nós")
    
    try:
        # Mantém o programa principal rodando
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 PARANDO TODOS OS NÓS...")
        print("✅ Sistema finalizado pelo usuário")

if __name__ == "__main__":
    main()
