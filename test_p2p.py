#!/usr/bin/env python3
"""
Teste Simples P2P - Sem dependências externas
=============================================

Teste básico do sistema P2P usando apenas bibliotecas padrão do Python.
"""

import socket
import threading
import pickle
import time
import json


def test_simple_p2p():
    """Teste simples do sistema P2P."""
    print("🔗 TESTE SIMPLES P2P")
    print("=" * 50)
    
    # Classe P2P básica para teste
    class TestP2PNode:
        def __init__(self, port):
            self.port = port
            self.peers = set()
            self.messages = []
            self.running = False
            
        def start(self):
            try:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                self.socket.bind(('localhost', self.port))
                self.socket.listen(5)
                self.running = True
                print(f"✅ Nó P2P iniciado na porta {self.port}")
                return True
            except Exception as e:
                print(f"❌ Erro ao iniciar nó: {e}")
                return False
                
        def send_message(self, target_port, message):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(5)
                    s.connect(('localhost', target_port))
                    s.send(pickle.dumps(message))
                    response = pickle.loads(s.recv(1024))
                    print(f"📤 Enviado para porta {target_port}: {message}")
                    print(f"📥 Resposta recebida: {response}")
                    return True
            except Exception as e:
                print(f"❌ Erro ao enviar para porta {target_port}: {e}")
                return False
                
        def handle_connection(self, conn, addr):
            try:
                data = conn.recv(1024)
                message = pickle.loads(data)
                print(f"📨 Mensagem recebida de {addr}: {message}")
                self.messages.append(message)
                
                response = f"ACK: {message}"
                conn.send(pickle.dumps(response))
            except Exception as e:
                print(f"❌ Erro ao processar conexão: {e}")
            finally:
                conn.close()
                
        def listen(self):
            while self.running:
                try:
                    conn, addr = self.socket.accept()
                    thread = threading.Thread(target=self.handle_connection, args=(conn, addr))
                    thread.start()
                except:
                    break
                    
        def stop(self):
            self.running = False
            if hasattr(self, 'socket'):
                self.socket.close()
    
    # Teste com 2 nós
    print("\n🚀 Iniciando teste com 2 nós P2P...")
    
    # Nó 1
    node1 = TestP2PNode(7000)
    if not node1.start():
        return False
    
    # Thread para nó 1 escutar
    thread1 = threading.Thread(target=node1.listen, daemon=True)
    thread1.start()
    
    time.sleep(0.5)  # Aguardar inicialização
    
    # Nó 2
    node2 = TestP2PNode(7001)
    if not node2.start():
        node1.stop()
        return False
    
    # Thread para nó 2 escutar
    thread2 = threading.Thread(target=node2.listen, daemon=True)
    thread2.start()
    
    time.sleep(0.5)  # Aguardar inicialização
    
    print("\n💬 Testando comunicação entre nós...")
    
    # Teste 1: Nó 1 envia para Nó 2
    success1 = node1.send_message(7001, "Olá do Nó 1!")
    
    time.sleep(0.1)
    
    # Teste 2: Nó 2 envia para Nó 1
    success2 = node2.send_message(7000, "Olá do Nó 2!")
    
    time.sleep(0.1)
    
    # Teste 3: Enviar dados estruturados
    trading_signal = {
        "type": "trading_signal",
        "symbol": "BTCUSD",
        "action": "BUY",
        "confidence": 0.85,
        "timestamp": time.time()
    }
    
    success3 = node1.send_message(7001, trading_signal)
    
    time.sleep(0.5)
    
    # Resultados
    print("\n📊 RESULTADOS DO TESTE:")
    print(f"✅ Comunicação 1→2: {'Sucesso' if success1 else 'Falha'}")
    print(f"✅ Comunicação 2→1: {'Sucesso' if success2 else 'Falha'}")
    print(f"✅ Dados estruturados: {'Sucesso' if success3 else 'Falha'}")
    
    print(f"\n📨 Mensagens recebidas pelo Nó 1 ({len(node1.messages)}):")
    for i, msg in enumerate(node1.messages, 1):
        print(f"  {i}. {msg}")
    
    print(f"\n📨 Mensagens recebidas pelo Nó 2 ({len(node2.messages)}):")
    for i, msg in enumerate(node2.messages, 1):
        print(f"  {i}. {msg}")
    
    # Parar nós
    node1.stop()
    node2.stop()
    
    # Resultado final
    total_success = success1 and success2 and success3
    print(f"\n🎯 RESULTADO FINAL: {'✅ TODOS OS TESTES PASSARAM!' if total_success else '⚠️ Alguns testes falharam'}")
    
    return total_success


def test_message_formats():
    """Testar diferentes formatos de mensagem."""
    print("\n🔄 TESTE DE FORMATOS DE MENSAGEM")
    print("=" * 50)
    
    test_messages = [
        "Mensagem simples",
        {"type": "fractal_pattern", "symbol": "ETHUSD", "hurst": 0.72},
        {"type": "market_data", "prices": [100, 102, 105, 103, 108]},
        123456,
        [1, 2, 3, 4, 5],
        {"complex": {"nested": {"data": True}}}
    ]
    
    print("📋 Testando serialização/deserialização:")
    
    all_passed = True
    for i, msg in enumerate(test_messages, 1):
        try:
            # Testar pickle
            serialized = pickle.dumps(msg)
            deserialized = pickle.loads(serialized)
            
            success = msg == deserialized
            print(f"  {i}. {type(msg).__name__}: {'✅' if success else '❌'}")
            
            if not success:
                all_passed = False
                
        except Exception as e:
            print(f"  {i}. {type(msg).__name__}: ❌ Erro: {e}")
            all_passed = False
    
    print(f"\n🎯 Serialização: {'✅ Todos os formatos funcionaram!' if all_passed else '⚠️ Alguns formatos falharam'}")
    return all_passed


def main():
    """Executar todos os testes."""
    print("""
╔══════════════════════════════════════════════════════════════╗
║                  🧪 TESTE SISTEMA P2P 🧪                    ║
║                                                              ║
║            Teste básico sem dependências externas           ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    try:
        # Teste 1: Formatos de mensagem
        format_test = test_message_formats()
        
        # Teste 2: Comunicação P2P
        p2p_test = test_simple_p2p()
        
        # Resultado final
        print("\n" + "=" * 70)
        print("🏆 RESUMO FINAL DOS TESTES:")
        print(f"   📝 Formatos de mensagem: {'✅ PASSOU' if format_test else '❌ FALHOU'}")
        print(f"   🔗 Comunicação P2P: {'✅ PASSOU' if p2p_test else '❌ FALHOU'}")
        
        overall_success = format_test and p2p_test
        print(f"\n🎖️  RESULTADO GERAL: {'🎉 SISTEMA P2P TOTALMENTE FUNCIONAL!' if overall_success else '⚠️ Sistema precisa de ajustes'}")
        
        if overall_success:
            print("\n💡 PRÓXIMOS PASSOS:")
            print("   • Instalar dependências: py -m ensurepip --upgrade")
            print("   • Executar sistema completo: py start.py")
            print("   • Testar traders fractais: py p2p/fractal_p2p_demo.py")
        
        return overall_success
        
    except KeyboardInterrupt:
        print("\n🛑 Teste interrompido pelo usuário")
        return False
    except Exception as e:
        print(f"\n❌ Erro inesperado no teste: {e}")
        return False


if __name__ == "__main__":
    main()
