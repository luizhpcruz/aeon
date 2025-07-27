# test_p2p_network.py
"""
🧪 TESTE AEONCOSMA P2P NETWORK
Script para testar a rede P2P com múltiplos nós
Desenvolvido por Luiz Cruz - 2025
"""

import sys
import os
import time
import threading
from datetime import datetime

# Adiciona path para importações
sys.path.append(os.path.join(os.path.dirname(__file__), 'aeoncosma'))

try:
    from aeoncosma.networking.p2p_node import P2PNode
    from aeoncosma.networking.validation_logic import validate_network_integrity
    MODULES_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Módulos P2P não disponíveis: {e}")
    MODULES_AVAILABLE = False

def create_test_node(node_id, port, delay=0):
    """Cria e inicia um nó de teste"""
    if delay > 0:
        print(f"⏱️ Aguardando {delay}s antes de iniciar {node_id}...")
        time.sleep(delay)
    
    node = P2PNode(
        host="127.0.0.1",
        port=port,
        node_id=node_id
    )
    
    node.start()
    return node

def test_node_connection(node1, node2):
    """Testa conexão entre dois nós"""
    print(f"🔗 Testando conexão {node1.node_id} → {node2.node_id}")
    
    response = node1.connect_to_peer(
        node2.host, 
        node2.port, 
        node1.node_id
    )
    
    if response:
        print(f"✅ Conexão bem-sucedida: {response}")
        return True
    else:
        print(f"❌ Falha na conexão")
        return False

def simulate_network_growth():
    """Simula crescimento progressivo da rede"""
    print("🌱 Simulando crescimento da rede P2P...")
    
    nodes = []
    
    try:
        # Nó 1 (primeiro da rede)
        print("\n1. Criando primeiro nó...")
        node1 = create_test_node("genesis_node", 9001)
        nodes.append(node1)
        time.sleep(2)
        
        # Nó 2 (conecta ao primeiro)
        print("\n2. Adicionando segundo nó...")
        node2 = create_test_node("node_002", 9002, delay=1)
        nodes.append(node2)
        time.sleep(1)
        
        # Teste de conexão
        test_node_connection(node2, node1)
        time.sleep(2)
        
        # Nó 3 (conecta ao segundo)
        print("\n3. Adicionando terceiro nó...")
        node3 = create_test_node("node_003", 9003, delay=1)
        nodes.append(node3)
        time.sleep(1)
        
        test_node_connection(node3, node2)
        time.sleep(2)
        
        # Mostra status da rede
        print("\n📊 Status da rede:")
        for i, node in enumerate(nodes, 1):
            info = node.get_network_info()
            print(f"   Nó {i}: {info['node_id']} - {info['peers_count']} peers")
        
        # Teste de broadcast
        print("\n📢 Testando broadcast...")
        if nodes:
            nodes[0].broadcast_message({
                "type": "test_broadcast",
                "message": "Olá rede AEONCOSMA!",
                "timestamp": datetime.now().isoformat()
            })
        
        # Mantém rede ativa por um tempo
        print("\n⏰ Mantendo rede ativa por 30 segundos...")
        time.sleep(30)
        
    except KeyboardInterrupt:
        print("\n🛑 Teste interrompido pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro durante teste: {e}")
    finally:
        # Para todos os nós
        print("\n🛑 Parando todos os nós...")
        for node in nodes:
            try:
                node.stop()
            except:
                pass

def test_validation_logic():
    """Testa apenas a lógica de validação"""
    print("🔍 Testando lógica de validação...")
    
    from aeoncosma.networking.validation_logic import validate_node, validate_network_integrity
    
    # Dados de teste
    test_nodes = [
        {
            "node_id": "test_001",
            "host": "127.0.0.1",
            "port": 9001,
            "timestamp": datetime.now().isoformat(),
            "previous": None,
            "context": {"peers_count": 0}
        },
        {
            "node_id": "test_002", 
            "host": "127.0.0.1",
            "port": 9002,
            "timestamp": datetime.now().isoformat(),
            "previous": "test_001",
            "context": {"peers_count": 1}
        }
    ]
    
    existing_peers = []
    
    # Testa validação sequencial
    for i, node_data in enumerate(test_nodes, 1):
        print(f"\n--- Validando nó {i} ---")
        
        result = validate_node(
            node_data, 
            f"validator_{i:03d}", 
            existing_peers, 
            "http://localhost:8000/validate"
        )
        
        if result:
            existing_peers.append(node_data)
            print(f"✅ Nó {node_data['node_id']} validado e adicionado")
        else:
            print(f"❌ Nó {node_data['node_id']} rejeitado")
    
    # Testa integridade da rede
    print(f"\n--- Integridade da rede ---")
    integrity = validate_network_integrity(existing_peers)
    print(f"Status: {'✅ Válida' if integrity['valid'] else '❌ Inválida'}")
    print(f"Saúde: {integrity['network_health']}%")
    print(f"Total de peers: {integrity['total_peers']}")
    
    if integrity['issues']:
        print(f"Problemas encontrados: {integrity['issues']}")

def simple_socket_test():
    """Teste simples de socket sem dependências"""
    import socket
    import json
    
    print("🔌 Teste simples de socket P2P...")
    
    def server():
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(('127.0.0.1', 9999))
        server_socket.listen(1)
        
        print("🎧 Servidor ouvindo na porta 9999...")
        
        try:
            conn, addr = server_socket.accept()
            print(f"🤝 Conexão recebida de {addr}")
            
            data = conn.recv(1024).decode('utf-8')
            if data:
                print(f"📨 Dados recebidos: {data}")
                
                response = {
                    "status": "received",
                    "timestamp": datetime.now().isoformat(),
                    "message": "Socket test successful!"
                }
                
                conn.send(json.dumps(response).encode('utf-8'))
                print("📤 Resposta enviada")
            
            conn.close()
            
        except Exception as e:
            print(f"❌ Erro no servidor: {e}")
        finally:
            server_socket.close()
    
    def client():
        time.sleep(1)  # Aguarda servidor iniciar
        
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect(('127.0.0.1', 9999))
            
            message = {
                "node_id": "test_client",
                "host": "127.0.0.1",
                "port": 8888,
                "timestamp": datetime.now().isoformat(),
                "message": "Hello P2P network!"
            }
            
            client_socket.send(json.dumps(message).encode('utf-8'))
            print("📤 Mensagem enviada para servidor")
            
            response = client_socket.recv(1024).decode('utf-8')
            if response:
                response_data = json.loads(response)
                print(f"📨 Resposta do servidor: {response_data}")
                
            client_socket.close()
            
        except Exception as e:
            print(f"❌ Erro no cliente: {e}")
    
    # Executa servidor e cliente em threads
    server_thread = threading.Thread(target=server, daemon=True)
    client_thread = threading.Thread(target=client, daemon=True)
    
    server_thread.start()
    client_thread.start()
    
    # Aguarda conclusão
    client_thread.join()
    time.sleep(1)
    
    print("✅ Teste de socket concluído")

def main():
    """Função principal do teste"""
    print("🚀 AEONCOSMA P2P Network Test Suite")
    print("=" * 50)
    
    if not MODULES_AVAILABLE:
        print("📦 Módulos P2P não disponíveis. Executando testes básicos...")
        
        # Testa apenas validação se disponível
        try:
            test_validation_logic()
        except ImportError:
            print("⚠️ Validação não disponível")
        
        # Teste simples de socket
        simple_socket_test()
        
    else:
        print("📦 Módulos P2P disponíveis. Executando teste completo...")
        
        try:
            print("\n1. Testando lógica de validação...")
            test_validation_logic()
            
            print("\n2. Testando rede P2P completa...")
            simulate_network_growth()
            
        except Exception as e:
            print(f"❌ Erro durante teste: {e}")
            print("🔄 Executando teste simples...")
            simple_socket_test()
    
    print("\n✅ Testes concluídos!")

if __name__ == "__main__":
    main()
