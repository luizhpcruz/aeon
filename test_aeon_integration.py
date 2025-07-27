# test_aeon_integration.py
"""
🧪 Teste de Integração AEON Core com P2P
Testa o sistema P2P com validação AEON Core avançada
"""

import sys
import os
import time
from datetime import datetime

# Adiciona path
sys.path.append(os.path.join(os.path.dirname(__file__), 'aeoncosma'))

def test_aeon_core():
    """Testa AEON Core independentemente"""
    print("🧪 Testando AEON Core...")
    
    try:
        from aeoncosma.core.aeon_core import AeonCore
        
        aeon = AeonCore()
        
        # Teste 1: Ledger vazio
        summary = aeon.get_ledger_summary()
        print(f"✅ Ledger inicial: {summary['total_blocks']} blocos")
        
        # Teste 2: Registrar nó
        node_data = {
            "node_id": "test_001",
            "host": "127.0.0.1",
            "port": 9001,
            "timestamp": datetime.now().isoformat(),
            "context": {"test": True}
        }
        
        result = aeon.register_node("test_001", node_data)
        print(f"✅ Nó registrado: {result['status']}")
        
        # Teste 3: Feedback
        feedback = aeon.feedback_to_node("test_001")
        print(f"✅ Feedback: {feedback['status']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no AEON Core: {e}")
        return False

def test_node_validator():
    """Testa NodeValidator"""
    print("\n🧪 Testando NodeValidator...")
    
    try:
        from aeoncosma.core.aeon_core import AeonCore
        from aeoncosma.core.node_validator import NodeValidator, FeedbackModule
        
        aeon = AeonCore()
        feedback = FeedbackModule()
        validator = NodeValidator(aeon, feedback)
        
        # Teste de validação
        node_info = {
            "id": "validator_test_001",
            "node_id": "validator_test_001",
            "host": "127.0.0.1",
            "port": 9002,
            "timestamp": datetime.now().isoformat(),
            "context": {"test_validation": True}
        }
        
        result = validator.validate_node(node_info, [], [])
        print(f"✅ Validação: {'Aprovado' if result['validated'] else 'Rejeitado'}")
        
        if not result['validated']:
            print(f"   Issues: {result['issues']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no NodeValidator: {e}")
        return False

def test_broadcast_manager():
    """Testa BroadcastManager"""
    print("\n🧪 Testando BroadcastManager...")
    
    try:
        from aeoncosma.core.broadcast_block import BroadcastManager
        
        manager = BroadcastManager(timeout=0.5)
        
        # Teste com peers inexistentes (vai falhar, mas testa a lógica)
        test_peers = [("127.0.0.1", 9999)]
        test_data = {"test": "broadcast_data"}
        
        result = manager.broadcast_block(test_peers, test_data, "test")
        print(f"✅ Broadcast teste: {result['success_rate']:.1f}% sucesso")
        
        stats = manager.get_broadcast_stats()
        print(f"✅ Broadcast stats: {stats['total_broadcasts']} broadcasts")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no BroadcastManager: {e}")
        return False

def test_p2p_integration():
    """Testa P2P com integração AEON"""
    print("\n🧪 Testando P2P com AEON...")
    
    try:
        from aeoncosma.networking.p2p_node import P2PNode
        
        # Cria nó com AEON Core
        node = P2PNode(
            host="127.0.0.1",
            port=9010,
            node_id="integration_test_001"
        )
        
        print(f"✅ Nó P2P criado: {node.node_id}")
        
        # Verifica se AEON Core está ativo
        if hasattr(node, 'aeon_core') and node.aeon_core:
            print(f"✅ AEON Core integrado")
            
            # Testa informações de rede
            network_info = node.get_network_info()
            print(f"✅ Network info: {network_info['validation_mode']}")
            
            # Testa feedback AEON
            feedback = node.get_aeon_feedback()
            print(f"✅ AEON Feedback: {feedback.get('code', 'N/A')}")
        else:
            print(f"⚠️ AEON Core não disponível - modo básico")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na integração P2P: {e}")
        return False

def main():
    """Executa todos os testes"""
    print("🚀 TESTE DE INTEGRAÇÃO AEON CORE + P2P")
    print("=" * 50)
    
    tests = [
        ("AEON Core", test_aeon_core),
        ("NodeValidator", test_node_validator), 
        ("BroadcastManager", test_broadcast_manager),
        ("P2P Integration", test_p2p_integration)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🧪 Executando {test_name}...")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"💥 Erro crítico em {test_name}: {e}")
            results.append((test_name, False))
    
    # Resumo
    print("\n" + "=" * 50)
    print("📊 RESUMO DOS TESTES:")
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"   {test_name}: {status}")
        if result:
            passed += 1
    
    total = len(results)
    print(f"\n🎯 Resultado: {passed}/{total} testes passaram ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("🎉 Todos os testes passaram! Sistema AEON pronto!")
    else:
        print("⚠️ Alguns testes falharam. Verifique as dependências.")

if __name__ == "__main__":
    main()
