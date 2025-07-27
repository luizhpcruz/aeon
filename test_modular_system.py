# test_modular_system.py
"""
🧪 TESTE DO SISTEMA MODULAR AEONCOSMA
Teste rápido dos componentes modulares implementados
Desenvolvido por Luiz Cruz - 2025
"""

import sys
import os
import asyncio
import time

# Adiciona path para importações
sys.path.append(os.path.join(os.path.dirname(__file__), 'aeoncosma'))

def test_imports():
    """Testa importação de todos os módulos"""
    print("🧪 [TESTE] Testando importações dos módulos...")
    
    try:
        from aeoncosma.core.aeon_core_simplified import AeonCoreSimplified
        print("✅ AeonCoreSimplified importado")
        
        from aeoncosma.core.feedback_module import FeedbackModule
        print("✅ FeedbackModule importado")
        
        from aeoncosma.networking.network_handler import NetworkHandler
        print("✅ NetworkHandler importado")
        
        from aeoncosma.networking.peer_discovery import PeerDiscovery
        print("✅ PeerDiscovery importado")
        
        from aeoncosma.main import AeonCosmaOrchestrator
        print("✅ AeonCosmaOrchestrator importado")
        
        return True
        
    except ImportError as e:
        print(f"❌ Erro na importação: {e}")
        return False

def test_aeon_core():
    """Testa AEON Core Simplified"""
    print("\n🧠 [TESTE] Testando AEON Core...")
    
    try:
        from aeoncosma.core.aeon_core_simplified import AeonCoreSimplified
        
        aeon = AeonCoreSimplified("test_node")
        
        # Teste de decisão
        context = {
            "node_id": "peer_001",
            "host": "192.168.1.100",
            "port": 9001,
            "timestamp": "2025-07-27T10:30:00",
            "reputation_score": 0.8
        }
        
        decision = aeon.make_decision(context)
        print(f"✅ Decisão tomada: {'APROVADO' if decision['approved'] else 'REJEITADO'}")
        print(f"   Score: {decision['final_score']:.3f}")
        print(f"   Confiança: {decision['confidence']:.3f}")
        
        # Métricas
        metrics = aeon.get_performance_metrics()
        print(f"   Decisões: {metrics['stats']['decisions_made']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no AEON Core: {e}")
        return False

def test_feedback_module():
    """Testa Feedback Module"""
    print("\n🧬 [TESTE] Testando Feedback Module...")
    
    try:
        from aeoncosma.core.feedback_module import FeedbackModule
        
        feedback = FeedbackModule()
        
        # Simula interações
        test_nodes = ["node_alpha", "node_beta", "node_gamma"]
        
        for node in test_nodes:
            feedback.update_score(node, "validation", True)
            feedback.update_score(node, "connection", True)
            feedback.update_score(node, "broadcast", False)  # Uma falha
        
        # Análise da rede
        health = feedback.get_network_health()
        print(f"✅ Saúde da rede: {health['network_health_score']}%")
        print(f"   Nós rastreados: {health['total_nodes']}")
        print(f"   Score médio: {health['average_score']:.3f}")
        
        # Top nós
        top = feedback.get_top_nodes(2)
        print(f"   Top 2 nós: {[n['node_id'] for n in top]}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no Feedback Module: {e}")
        return False

async def test_orchestrator():
    """Testa o orquestrador principal"""
    print("\n🚀 [TESTE] Testando AeonCosmaOrchestrator...")
    
    try:
        from aeoncosma.main import AeonCosmaOrchestrator
        
        # Cria orquestrador
        orchestrator = AeonCosmaOrchestrator(
            node_id="test_aeon",
            host="127.0.0.1",
            port=9900  # Porta de teste
        )
        
        # Inicializa
        if await orchestrator.initialize():
            print("✅ Orquestrador inicializado")
            
            # Testa início rápido
            if await orchestrator.start():
                print("✅ Sistema iniciado")
                
                # Aguarda um pouco
                await asyncio.sleep(3)
                
                # Status
                status = orchestrator.get_system_status()
                print(f"   Status: {status['running']}")
                print(f"   Uptime: {status['uptime']}s")
                print(f"   Peers: {len(orchestrator.network_handler.peers) if orchestrator.network_handler else 0}")
                
                # Para sistema
                await orchestrator.stop()
                print("✅ Sistema parado com sucesso")
                
                return True
            else:
                print("❌ Falha ao iniciar sistema")
                return False
        else:
            print("❌ Falha ao inicializar sistema")
            return False
            
    except Exception as e:
        print(f"❌ Erro no Orquestrador: {e}")
        return False

async def main():
    """Função principal de teste"""
    print("🚀 TESTE COMPLETO DO SISTEMA MODULAR AEONCOSMA")
    print("=" * 60)
    
    # Contadores
    tests_passed = 0
    tests_total = 4
    
    # Teste 1: Importações
    if test_imports():
        tests_passed += 1
    
    # Teste 2: AEON Core
    if test_aeon_core():
        tests_passed += 1
    
    # Teste 3: Feedback Module
    if test_feedback_module():
        tests_passed += 1
    
    # Teste 4: Orquestrador (assíncrono)
    if await test_orchestrator():
        tests_passed += 1
    
    # Resultado final
    print(f"\n📊 RESULTADO DOS TESTES")
    print("=" * 30)
    print(f"✅ Testes passaram: {tests_passed}/{tests_total}")
    print(f"📈 Taxa de sucesso: {tests_passed/tests_total:.1%}")
    
    if tests_passed == tests_total:
        print("🎯 SISTEMA MODULAR 100% FUNCIONAL!")
        print("🚀 Pronto para lançamento!")
    elif tests_passed >= 3:
        print("🟡 Sistema funcional com pequenos ajustes necessários")
    else:
        print("🔴 Sistema requer ajustes antes do lançamento")
    
    return tests_passed == tests_total

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
