#!/usr/bin/env python3
"""
🔌 TESTE DE CONECTIVIDADE ENTRE NÓS
Conecta e testa comunicação entre nós P2P ativos
"""

import socket
import json
import time
from datetime import datetime

def test_node_connection(host="127.0.0.1", port=9000, node_id="test_client"):
    """Testa conexão com um nó P2P"""
    try:
        print(f"🔗 Conectando ao nó {host}:{port}...")
        
        # Cria socket de conexão
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect((host, port))
        
        # Prepara dados de teste
        test_data = {
            "node_id": node_id,
            "host": "127.0.0.1",
            "port": 9999,
            "timestamp": datetime.now().isoformat(),
            "context": {
                "type": "connectivity_test",
                "message": "Teste de conectividade do cliente"
            }
        }
        
        # Envia dados
        sock.send(json.dumps(test_data).encode('utf-8'))
        print(f"📤 Dados enviados: {test_data}")
        
        # Recebe resposta
        response = sock.recv(4096).decode('utf-8')
        if response:
            response_data = json.loads(response)
            print(f"📥 Resposta recebida: {response_data}")
            
            if response_data.get("status") == "accepted":
                print(f"✅ Conectividade com {host}:{port} - SUCESSO!")
                return True
            else:
                print(f"⚠️ Conectividade com {host}:{port} - Nó rejeitou conexão")
                return False
        else:
            print(f"❌ Nenhuma resposta do nó {host}:{port}")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao conectar com {host}:{port}: {e}")
        return False
    finally:
        sock.close()

def main():
    """Testa conectividade com múltiplos nós"""
    print("🌐 TESTE DE CONECTIVIDADE - REDE AEONCOSMA")
    print("=" * 50)
    
    # Lista de nós para testar
    nodes_to_test = [
        {"host": "127.0.0.1", "port": 9000, "name": "Nó Principal"},
        {"host": "127.0.0.1", "port": 9001, "name": "Segundo Nó"},
        {"host": "127.0.0.1", "port": 9002, "name": "Terceiro Nó"}
    ]
    
    active_nodes = []
    
    for node in nodes_to_test:
        print(f"\n🔍 Testando {node['name']} ({node['host']}:{node['port']})...")
        
        if test_node_connection(node['host'], node['port'], f"test_client_{int(time.time())}"):
            active_nodes.append(node)
            print(f"✅ {node['name']} está ATIVO")
        else:
            print(f"❌ {node['name']} está INATIVO")
    
    print("\n" + "=" * 50)
    print(f"📊 RESULTADO DO TESTE:")
    print(f"🟢 Nós ativos: {len(active_nodes)}")
    print(f"🔴 Nós inativos: {len(nodes_to_test) - len(active_nodes)}")
    
    if active_nodes:
        print(f"\n✅ NETOS ATIVOS:")
        for node in active_nodes:
            print(f"   🌐 {node['name']}: {node['host']}:{node['port']}")
    
    print(f"\n💡 Para ativar mais nós, execute:")
    print(f"   python aeoncosma\\networking\\p2p_node.py --port PORTA --node-id NOME")

if __name__ == "__main__":
    main()
