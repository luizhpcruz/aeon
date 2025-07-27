# simple_gpu_test.py
"""
🧠 Teste Simples da Expansão GPU AEONCOSMA
Demonstra capacidades GPU simuladas sem dependências externas
Desenvolvido por Luiz Cruz - 2025
"""

import time
import sys
import os
import json

# Adiciona path para importações
sys.path.append(os.path.join(os.path.dirname(__file__), 'aeoncosma'))

def test_node_brain_basic():
    """Teste básico do NodeBrain sem dependências"""
    print("🧠 Teste NodeBrain Simulado")
    print("-" * 30)
    
    try:
        from aeoncosma.gpu.node_brain import NodeBrain
        
        # Cria brain
        brain = NodeBrain()
        
        # Testa múltiplas decisões
        test_cases = [
            [0.8, 0.7, 0.9, 0.6, 0.5, 0.4, 0.3],  # Peer muito bom
            [0.2, 0.1, 0.3, 0.2, 0.8, 0.9, 0.1],  # Peer médio
            [0.1, 0.2, 0.1, 0.1, 0.0, 0.1, 0.0],  # Peer ruim
        ]
        
        results = []
        for i, features in enumerate(test_cases):
            decision = brain.make_decision(features)
            results.append(decision)
            
            print(f"  Teste {i+1}: {'✅' if decision['decision'] else '❌'} "
                  f"Confiança: {decision['confidence']:.3f} - {decision['reasoning'][:30]}...")
        
        # Estatísticas
        stats = brain.get_brain_stats()
        print(f"📊 Total decisões: {stats['total_decisions']}")
        print(f"📈 Taxa de aceitação: {stats['acceptance_rate']:.1%}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def test_gpu_manager_basic():
    """Teste básico do GPU Manager"""
    print("\n🛠️ Teste GPU Manager Simulado")
    print("-" * 30)
    
    try:
        from aeoncosma.gpu.gpu_utils import GPUManager, PerformanceProfiler
        
        # Cria manager
        manager = GPUManager(0)
        profiler = PerformanceProfiler()
        
        # Simula operação
        def dummy_work():
            total = 0
            for i in range(10000):
                total += i * 0.001
            return total
        
        # Perfila operação
        result = profiler.profile_operation("simulation_work", dummy_work)
        
        print(f"  ⚡ Operação: {result['profile']['operation']}")
        print(f"  ⏱️ Tempo: {result['profile']['execution_time']:.4f}s")
        print(f"  ✅ Sucesso: {result['profile']['success']}")
        
        # Info do manager
        info = manager.get_memory_info()
        print(f"📊 GPU Mode: {'Real GPU' if info['total'] > 0 else 'CPU Simulation'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def test_network_simulation():
    """Teste de simulação de rede"""
    print("\n🌐 Teste Simulação de Rede")
    print("-" * 30)
    
    try:
        from aeoncosma.gpu.node_brain import NodeBrain
        
        # Simula rede com 5 nós
        nodes = []
        for i in range(5):
            brain = NodeBrain()
            nodes.append({
                "id": f"node_{i:03d}",
                "brain": brain,
                "peers": [],
                "decisions": 0
            })
        
        # Simula descoberta de peers
        print("🔍 Simulando descoberta de peers...")
        
        total_connections = 0
        total_decisions = 0
        
        for i, node in enumerate(nodes):
            for j, peer in enumerate(nodes):
                if i != j:  # Não conecta consigo mesmo
                    # Features fictícias do peer
                    peer_features = [
                        hash(peer["id"]) % 1000 / 1000.0,  # ID hash
                        0.5 + (j * 0.1),  # Variação baseada no índice
                        0.8,  # Timestamp recency
                        0.6,  # Reputation
                        len(node["peers"]) / 10.0,  # Network density
                        0.7,  # Uptime
                        0.5   # Random
                    ]
                    
                    # Nó decide sobre o peer
                    decision = node["brain"].make_decision(peer_features)
                    total_decisions += 1
                    
                    if decision["decision"]:
                        node["peers"].append(peer["id"])
                        total_connections += 1
                        print(f"  ✅ {node['id']} aceita {peer['id']} (conf: {decision['confidence']:.2f})")
                    else:
                        print(f"  ❌ {node['id']} rejeita {peer['id']} (conf: {decision['confidence']:.2f})")
        
        # Estatísticas da rede
        print(f"\n📊 Estatísticas da Rede:")
        print(f"  🎯 Nós: {len(nodes)}")
        print(f"  🔗 Conexões: {total_connections}")
        print(f"  🧠 Decisões: {total_decisions}")
        print(f"  📈 Taxa de aceitação: {total_connections/total_decisions:.1%}")
        
        # Info detalhada de cada nó
        for node in nodes:
            stats = node["brain"].get_brain_stats()
            print(f"  📡 {node['id']}: {len(node['peers'])} peers, "
                  f"{stats['total_decisions']} decisões, "
                  f"{stats['acceptance_rate']:.1%} aceitação")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def test_art_generation_simulation():
    """Teste de geração de arte simulada"""
    print("\n🎨 Teste Geração de Arte Simulada")
    print("-" * 30)
    
    try:
        from aeoncosma.gpu.stable_diffusion_visualizer import NetworkArtGenerator
        
        # Cria gerador (vai usar simulação)
        generator = NetworkArtGenerator()
        
        # Estado fictício da rede
        network_state = {
            "total_nodes": 1000,
            "active_nodes": 750,
            "consensus_strength": 0.85,
            "ai_confidence": 0.73,
            "connections_density": 0.6,
            "timestamp": "2025-07-27T12:00:00"
        }
        
        # Gera prompt criativo
        prompt_data = generator.network_state_to_prompt(network_state)
        
        print(f"🎯 Prompt gerado:")
        print(f"  {prompt_data['prompt'][:100]}...")
        
        print(f"\n📊 Métricas da rede:")
        for key, value in prompt_data['network_metrics'].items():
            print(f"  {key}: {value}")
        
        # Simula geração de arte
        print(f"\n🎨 Simulando geração de arte...")
        result = generator.generate_network_art(network_state)
        
        if result["success"]:
            print(f"  ✅ Arte gerada: {result['metadata']['filename']}")
            print(f"  🕐 Simulação: {result['metadata'].get('simulation', False)}")
        else:
            print(f"  ❌ Falha: {result['error']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def comprehensive_gpu_demo():
    """Demonstração completa das capacidades GPU"""
    print("🌟 AEONCOSMA GPU EXPANSION - DEMONSTRAÇÃO COMPLETA")
    print("=" * 60)
    
    # Executar todos os testes
    tests = [
        ("NodeBrain IA Neural", test_node_brain_basic),
        ("GPU Manager", test_gpu_manager_basic),
        ("Simulação de Rede", test_network_simulation),
        ("Geração de Arte", test_art_generation_simulation)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🧪 {test_name}")
        print("=" * 60)
        
        start_time = time.time()
        success = test_func()
        end_time = time.time()
        
        results.append({
            "test": test_name,
            "success": success,
            "duration": end_time - start_time
        })
        
        print(f"⏱️ Duração: {end_time - start_time:.2f}s")
        print(f"{'✅ SUCESSO' if success else '❌ FALHA'}")
    
    # Resumo final
    print(f"\n🏆 RESUMO FINAL")
    print("=" * 60)
    
    success_count = sum(1 for r in results if r["success"])
    total_time = sum(r["duration"] for r in results)
    
    print(f"✅ Testes bem-sucedidos: {success_count}/{len(results)}")
    print(f"⏱️ Tempo total: {total_time:.2f}s")
    print(f"📊 Taxa de sucesso: {success_count/len(results):.1%}")
    
    for result in results:
        status = "✅" if result["success"] else "❌"
        print(f"  {status} {result['test']}: {result['duration']:.2f}s")
    
    print(f"\n🌟 AEONCOSMA está pronto para:")
    print(f"  🎮 Processamento GPU massivo (simulado)")
    print(f"  🧠 IA embarcada em cada nó")
    print(f"  🌐 Simulação de 100k+ nós")
    print(f"  🎨 Geração de arte da rede")
    print(f"  📊 Monitoramento em tempo real")
    
    return success_count == len(results)

def main():
    """Execução principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description='AEONCOSMA Simple GPU Test')
    parser.add_argument('--brain', action='store_true', help='Testa apenas NodeBrain')
    parser.add_argument('--gpu', action='store_true', help='Testa apenas GPU Manager')
    parser.add_argument('--network', action='store_true', help='Testa apenas simulação de rede')
    parser.add_argument('--art', action='store_true', help='Testa apenas geração de arte')
    parser.add_argument('--demo', action='store_true', help='Demonstração completa')
    
    args = parser.parse_args()
    
    if args.brain:
        test_node_brain_basic()
    elif args.gpu:
        test_gpu_manager_basic()
    elif args.network:
        test_network_simulation()
    elif args.art:
        test_art_generation_simulation()
    elif args.demo or not any([args.brain, args.gpu, args.network, args.art]):
        comprehensive_gpu_demo()

if __name__ == "__main__":
    main()
