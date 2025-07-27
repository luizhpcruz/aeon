# start_p2p_system.py
"""
🚀 AEONCOSMA P2P SYSTEM LAUNCHER
Iniciador completo do sistema P2P com backend e nós
Desenvolvido por Luiz Cruz - 2025
"""

import sys
import os
import time
import threading
import subprocess
import signal
from datetime import datetime

def print_banner():
    """Exibe banner do sistema"""
    print("=" * 60)
    print("🌌 AEONCOSMA P2P TRADING NETWORK")
    print("🚀 Sistema Distribuído de Trading com IA")
    print("⚡ Fase 1: Núcleo P2P com Validação Backend")
    print("=" * 60)
    print(f"📅 Iniciado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

def check_dependencies():
    """Verifica dependências necessárias"""
    print("🔍 Verificando dependências...")
    
    missing_deps = []
    
    try:
        import socket
        print("✅ Socket: OK")
    except ImportError:
        missing_deps.append("socket")
    
    try:
        import json
        print("✅ JSON: OK")
    except ImportError:
        missing_deps.append("json")
    
    try:
        import threading
        print("✅ Threading: OK")
    except ImportError:
        missing_deps.append("threading")
    
    # Dependências opcionais
    optional_deps = []
    
    try:
        import fastapi
        import uvicorn
        print("✅ FastAPI/Uvicorn: OK")
    except ImportError:
        optional_deps.append("fastapi/uvicorn")
    
    try:
        import requests
        print("✅ Requests: OK")
    except ImportError:
        optional_deps.append("requests")
    
    if missing_deps:
        print(f"❌ Dependências faltando: {missing_deps}")
        return False
    
    if optional_deps:
        print(f"⚠️ Dependências opcionais faltando: {optional_deps}")
        print("💡 Sistema funcionará em modo básico")
    
    print("✅ Verificação de dependências concluída")
    return True

def start_backend_api():
    """Inicia o backend FastAPI"""
    print("🌐 Iniciando backend API...")
    
    try:
        # Verifica se FastAPI está disponível
        import fastapi
        import uvicorn
        
        # Importa o backend
        sys.path.append(os.path.join(os.path.dirname(__file__), 'aeoncosma'))
        from aeoncosma.backend.api_feedback import main as api_main
        
        # Executa em thread separada
        api_thread = threading.Thread(target=api_main, daemon=True)
        api_thread.start()
        
        print("✅ Backend API iniciado em http://localhost:8000")
        return True
        
    except ImportError:
        print("⚠️ FastAPI não disponível - usando modo mock")
        return start_mock_backend()
    except Exception as e:
        print(f"❌ Erro ao iniciar backend: {e}")
        return start_mock_backend()

def start_mock_backend():
    """Inicia backend simulado sem FastAPI"""
    print("🔧 Iniciando backend mock...")
    
    import socket
    import json
    
    def mock_server():
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind(('127.0.0.1', 8001))  # Porta diferente
            server.listen(5)
            
            print("🎧 Mock backend ouvindo na porta 8001...")
            
            while True:
                try:
                    conn, addr = server.accept()
                    
                    data = conn.recv(4096).decode('utf-8')
                    if data:
                        # Resposta mock sempre positiva
                        response = {
                            "status": "approved",
                            "score": 85,
                            "percentage": 85.0,
                            "timestamp": datetime.now().isoformat(),
                            "aeon_feedback": {
                                "action": "accept",
                                "confidence": 0.85,
                                "reason": "Mock validation - Score 85/100"
                            }
                        }
                        
                        conn.send(json.dumps(response).encode('utf-8'))
                    
                    conn.close()
                    
                except Exception as e:
                    print(f"⚠️ Erro no mock server: {e}")
                    
        except Exception as e:
            print(f"❌ Erro crítico no mock server: {e}")
    
    # Executa mock em thread
    mock_thread = threading.Thread(target=mock_server, daemon=True)
    mock_thread.start()
    
    print("✅ Mock backend iniciado na porta 8001")
    return True

def start_p2p_nodes():
    """Inicia nós P2P de teste"""
    print("🌐 Iniciando nós P2P...")
    
    nodes = []
    
    try:
        sys.path.append(os.path.join(os.path.dirname(__file__), 'aeoncosma'))
        from aeoncosma.networking.p2p_node import P2PNode
        
        # Nó 1 (Genesis)
        print("🌱 Criando nó genesis...")
        node1 = P2PNode(
            host="127.0.0.1",
            port=9001,
            node_id="genesis_node"
        )
        node1.start()
        nodes.append(node1)
        time.sleep(2)
        
        # Nó 2
        print("🔗 Criando segundo nó...")
        node2 = P2PNode(
            host="127.0.0.1",
            port=9002,
            node_id="node_002"
        )
        node2.start()
        nodes.append(node2)
        time.sleep(1)
        
        # Conecta nó 2 ao nó 1
        node2.connect_to_peer("127.0.0.1", 9001, "genesis_node")
        time.sleep(1)
        
        # Nó 3
        print("🔗 Criando terceiro nó...")
        node3 = P2PNode(
            host="127.0.0.1",
            port=9003,
            node_id="node_003"
        )
        node3.start()
        nodes.append(node3)
        time.sleep(1)
        
        # Conecta nó 3 ao nó 2
        node3.connect_to_peer("127.0.0.1", 9002, "node_002")
        
        print(f"✅ {len(nodes)} nós P2P iniciados com sucesso")
        return nodes
        
    except ImportError:
        print("⚠️ Módulos P2P não disponíveis - criando nós mock")
        return start_mock_nodes()
    except Exception as e:
        print(f"❌ Erro ao iniciar nós P2P: {e}")
        return start_mock_nodes()

def start_mock_nodes():
    """Inicia nós simulados sem módulos P2P"""
    print("🔧 Iniciando nós mock...")
    
    import socket
    import json
    
    def mock_node(node_id, port):
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind(('127.0.0.1', port))
            server.listen(2)
            
            print(f"🎧 Mock {node_id} ouvindo na porta {port}...")
            
            while True:
                try:
                    conn, addr = server.accept()
                    
                    data = conn.recv(1024).decode('utf-8')
                    if data:
                        response = {
                            "status": "accepted",
                            "node_id": node_id,
                            "timestamp": datetime.now().isoformat(),
                            "peer_count": 1
                        }
                        conn.send(json.dumps(response).encode('utf-8'))
                    
                    conn.close()
                    
                except Exception as e:
                    print(f"⚠️ Erro no mock {node_id}: {e}")
                    
        except Exception as e:
            print(f"❌ Erro crítico no mock {node_id}: {e}")
    
    # Cria 3 nós mock
    mock_nodes = []
    for i in range(1, 4):
        node_id = f"mock_node_{i:03d}"
        port = 9000 + i
        
        node_thread = threading.Thread(
            target=mock_node, 
            args=(node_id, port), 
            daemon=True
        )
        node_thread.start()
        mock_nodes.append(f"{node_id}:{port}")
        time.sleep(0.5)
    
    print(f"✅ {len(mock_nodes)} nós mock iniciados")
    return mock_nodes

def show_network_status():
    """Mostra status da rede"""
    print("\n📊 STATUS DA REDE AEONCOSMA P2P")
    print("-" * 40)
    print("🌐 Backend API: http://localhost:8000 (ou 8001 se mock)")
    print("🔗 Nós P2P:")
    print("   - genesis_node: 127.0.0.1:9001")
    print("   - node_002: 127.0.0.1:9002")
    print("   - node_003: 127.0.0.1:9003")
    print("\n📡 Endpoints disponíveis:")
    print("   - GET  /network/stats - Estatísticas da rede")
    print("   - GET  /network/nodes - Lista de nós")
    print("   - POST /validate - Validação de nós")
    print("   - GET  /health - Status do sistema")

def run_interactive_mode():
    """Modo interativo para testes"""
    print("\n🎮 MODO INTERATIVO")
    print("Comandos disponíveis:")
    print("  'status' - Mostra status da rede")
    print("  'test' - Executa teste de conectividade")
    print("  'broadcast' - Envia mensagem broadcast")
    print("  'quit' - Para o sistema")
    
    while True:
        try:
            cmd = input("\n> ").strip().lower()
            
            if cmd == 'quit':
                break
            elif cmd == 'status':
                show_network_status()
            elif cmd == 'test':
                print("🧪 Executando teste de conectividade...")
                run_connectivity_test()
            elif cmd == 'broadcast':
                print("📢 Enviando mensagem de teste...")
                test_broadcast()
            elif cmd == 'help':
                print("Comandos: status, test, broadcast, quit, help")
            else:
                print("❓ Comando desconhecido. Digite 'help' para ajuda.")
                
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"❌ Erro: {e}")

def run_connectivity_test():
    """Testa conectividade entre nós"""
    import socket
    import json
    
    test_ports = [9001, 9002, 9003]
    
    for port in test_ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex(('127.0.0.1', port))
            
            if result == 0:
                print(f"✅ Nó na porta {port}: Conectável")
                
                # Testa comunicação
                test_msg = {
                    "type": "connectivity_test",
                    "timestamp": datetime.now().isoformat()
                }
                
                sock.send(json.dumps(test_msg).encode('utf-8'))
                response = sock.recv(1024).decode('utf-8')
                
                if response:
                    print(f"   📨 Resposta recebida")
                else:
                    print(f"   ⚠️ Sem resposta")
            else:
                print(f"❌ Nó na porta {port}: Não conectável")
            
            sock.close()
            
        except Exception as e:
            print(f"❌ Erro ao testar porta {port}: {e}")

def test_broadcast():
    """Testa envio de broadcast"""
    print("📢 Implementação de broadcast pendente...")
    print("💡 Use a interface dos nós para broadcast real")

def cleanup_and_exit(nodes):
    """Limpa recursos e para o sistema"""
    print("\n🛑 Parando sistema AEONCOSMA P2P...")
    
    if nodes and hasattr(nodes[0], 'stop'):
        # Nós reais P2P
        for node in nodes:
            try:
                node.stop()
            except:
                pass
    
    print("✅ Sistema parado com sucesso")
    print("👋 Até logo!")

def main():
    """Função principal"""
    print_banner()
    
    # Verifica dependências
    if not check_dependencies():
        print("❌ Dependências críticas faltando. Abortando...")
        return
    
    nodes = []
    
    try:
        # 1. Inicia backend
        print("\n🔧 FASE 1: Iniciando Backend...")
        if not start_backend_api():
            print("❌ Falha ao iniciar backend")
            return
        
        time.sleep(3)  # Aguarda backend estabilizar
        
        # 2. Inicia nós P2P
        print("\n🔧 FASE 2: Iniciando Nós P2P...")
        nodes = start_p2p_nodes()
        
        time.sleep(2)  # Aguarda nós estabilizarem
        
        # 3. Mostra status
        show_network_status()
        
        # 4. Modo interativo
        print("\n✅ Sistema AEONCOSMA P2P iniciado com sucesso!")
        print("🎯 Rede P2P operacional com validação backend")
        
        run_interactive_mode()
        
    except KeyboardInterrupt:
        print("\n🛑 Sistema interrompido pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro crítico: {e}")
    finally:
        cleanup_and_exit(nodes)

if __name__ == "__main__":
    main()
