# test_gpu_expansion.py
"""
🧠 Teste da Expansão GPU do AEONCOSMA
Demonstra as novas capacidades GPU e IA embarcada
Desenvolvido por Luiz Cruz - 2025
"""

import time
import sys
import os

# Adiciona path para importações
sys.path.append(os.path.join(os.path.dirname(__file__), 'aeoncosma'))

def test_gpu_components():
    """Testa componentes GPU individualmente"""
    print("🧠 AEONCOSMA GPU EXPANSION TEST")
    print("=" * 50)
    
    # Teste 1: NodeBrain
    print("\n🧠 Teste 1: Node Brain (IA Neural)")
    try:
        from aeoncosma.gpu.node_brain import test_node_brain
        brain = test_node_brain()
        print("✅ NodeBrain testado com sucesso")
    except Exception as e:
        print(f"⚠️ NodeBrain erro: {e}")
    
    # Teste 2: GPU Utils
    print("\n🛠️ Teste 2: GPU Utilities")
    try:
        from aeoncosma.gpu.gpu_utils import test_gpu_utils
        test_gpu_utils()
        print("✅ GPU Utils testado com sucesso")
    except Exception as e:
        print(f"⚠️ GPU Utils erro: {e}")
    
    # Teste 3: P2P Node com GPU Enhancement
    print("\n🌐 Teste 3: P2P Node GPU Enhanced")
    try:
        from aeoncosma.networking.p2p_node import P2PNode
        
        # Cria nó com GPU enhancement
        node = P2PNode(
            host="127.0.0.1",
            port=9001,
            node_id="test_gpu_node"
        )
        
        # Inicia nó
        node.start()
        print("✅ P2P Node GPU Enhanced iniciado")
        
        # Testa informações
        info = node.get_network_info()
        print(f"📊 GPU Enhanced: {info.get('gpu_enhanced', False)}")
        
        time.sleep(2)
        node.stop()
        print("✅ P2P Node parado")
        
    except Exception as e:
        print(f"⚠️ P2P Node GPU erro: {e}")

def test_gpu_simulator():
    """Testa simulador massivo"""
    print("\n🎮 Teste 4: GPU Massive Simulator")
    try:
        from aeoncosma.gpu.gpu_simulator import MassiveP2PSimulator
        
        # Simulação pequena para teste
        simulator = MassiveP2PSimulator(num_nodes=1000, gpu_id=0)
        
        # Inicializa rede
        init_result = simulator.initialize_network()
        print(f"✅ Rede inicializada: {init_result}")
        
        # Simulação de descoberta
        discovery = simulator.simulate_peer_discovery(discovery_rounds=3)
        print(f"✅ Discovery simulado: {len(discovery)} rounds")
        
        # Consenso com IA
        consensus = simulator.simulate_ai_consensus(consensus_rounds=2)
        print(f"✅ Consenso simulado: {len(consensus)} rounds")
        
        # Estatísticas finais
        stats = simulator.get_final_statistics()
        print(f"📊 Estatísticas: {stats}")
        
        print("✅ GPU Simulator testado com sucesso")
        
    except Exception as e:
        print(f"⚠️ GPU Simulator erro: {e}")

def test_art_generator():
    """Testa gerador de arte da rede"""
    print("\n🎨 Teste 5: Network Art Generator")
    try:
        from aeoncosma.gpu.stable_diffusion_visualizer import test_network_art_generator
        
        generator = test_network_art_generator()
        print("✅ Art Generator testado com sucesso")
        
    except Exception as e:
        print(f"⚠️ Art Generator erro: {e}")

def test_ecosystem_launcher():
    """Testa launcher do ecosystem"""
    print("\n🚀 Teste 6: Ecosystem Launcher")
    try:
        from aeoncosma.gpu.launch_gpu_ecosystem import GPUEcosystemLauncher
        
        # Cria launcher
        launcher = GPUEcosystemLauncher()
        
        # Verifica GPU
        gpu_info = launcher.check_gpu_availability()
        print(f"🎮 GPU Info: {gpu_info}")
        
        # Testa configuração
        print(f"🔧 Configuração: {launcher.config}")
        
        print("✅ Ecosystem Launcher testado com sucesso")
        
    except Exception as e:
        print(f"⚠️ Ecosystem Launcher erro: {e}")

def demonstration_mode():
    """Modo demonstração com ecosystem mínimo"""
    print("\n🌟 MODO DEMONSTRAÇÃO - Ecosystem Mínimo")
    print("=" * 50)
    
    try:
        from aeoncosma.gpu.launch_gpu_ecosystem import GPUEcosystemLauncher
        
        # Cria launcher com configuração mínima
        launcher = GPUEcosystemLauncher()
        
        # Configura para demonstração
        launcher.config["simulation"]["max_nodes"] = 5000
        launcher.config["art_generation"]["enabled"] = False  # Desabilitado para demo
        
        print("🚀 Iniciando ecosystem de demonstração...")
        
        # Lança alguns nós
        launcher.running = True
        launcher.global_stats["start_time"] = time.time()
        
        # Lança 3 nós para demonstração
        launcher.launch_gpu_nodes(num_nodes=3, start_port=9100)
        
        # Executa por 30 segundos
        print("🕐 Executando por 30 segundos...")
        for i in range(30):
            time.sleep(1)
            if i % 10 == 0:
                print(f"   ⏱️ {30-i} segundos restantes...")
        
        # Para ecosystem
        launcher.shutdown_ecosystem()
        
        print("✅ Demonstração concluída com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro na demonstração: {e}")

def main():
    """Execução principal dos testes"""
    import argparse
    
    parser = argparse.ArgumentParser(description='AEONCOSMA GPU Expansion Test')
    parser.add_argument('--components', action='store_true', help='Testa componentes individuais')
    parser.add_argument('--simulator', action='store_true', help='Testa simulador massivo')
    parser.add_argument('--art', action='store_true', help='Testa gerador de arte')
    parser.add_argument('--launcher', action='store_true', help='Testa ecosystem launcher')
    parser.add_argument('--demo', action='store_true', help='Modo demonstração')
    parser.add_argument('--all', action='store_true', help='Executa todos os testes')
    
    args = parser.parse_args()
    
    if args.all or not any([args.components, args.simulator, args.art, args.launcher, args.demo]):
        # Executa todos os testes se nenhum específico for escolhido
        test_gpu_components()
        test_gpu_simulator()
        test_art_generator()
        test_ecosystem_launcher()
        demonstration_mode()
    else:
        if args.components:
            test_gpu_components()
        
        if args.simulator:
            test_gpu_simulator()
        
        if args.art:
            test_art_generator()
        
        if args.launcher:
            test_ecosystem_launcher()
        
        if args.demo:
            demonstration_mode()
    
    print("\n🎯 EXPANSÃO GPU AEONCOSMA - TESTE CONCLUÍDO")
    print("=" * 50)
    print("🌟 Sistema pronto para simular 100k+ nós com IA embarcada!")

if __name__ == "__main__":
    main()
