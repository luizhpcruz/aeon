# aeoncosma/gpu/gpu_simulator.py
"""
🎮 AEONCOSMA GPU Massive Simulator - Simulação Massiva com GPU
Simula 100k+ nós P2P com IA embarcada e visualização em tempo real
Desenvolvido por Luiz Cruz - 2025
"""

import time
import json
import threading
from datetime import datetime
from typing import Dict, List, Any
import sys
import os

# Adiciona path para importações
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

try:
    import torch
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.animation as animation
    from matplotlib.colors import LinearSegmentedColormap
    GPU_AVAILABLE = torch.cuda.is_available()
    PLOTTING_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Dependências GPU/Plotting não disponíveis: {e}")
    GPU_AVAILABLE = False
    PLOTTING_AVAILABLE = False

try:
    from gpu.gpu_utils import GPUManager, PerformanceProfiler, NetworkVisualizer
    from gpu.node_brain import NodeBrain, CollectiveIntelligence
    GPU_MODULES_AVAILABLE = True
except ImportError:
    print("⚠️ Módulos GPU não disponíveis - usando simulação básica")
    GPU_MODULES_AVAILABLE = False

class MassiveP2PSimulator:
    """
    Simulador massivo de rede P2P com GPU
    Capaz de simular 100k+ nós com IA embarcada
    """
    
    def __init__(self, num_nodes=10000, gpu_id=0):
        self.num_nodes = num_nodes
        self.gpu_id = gpu_id
        self.running = False
        
        # Componentes GPU
        if GPU_AVAILABLE and GPU_MODULES_AVAILABLE:
            self.device = torch.device(f'cuda:{gpu_id}' if GPU_AVAILABLE else 'cpu')
            self.gpu_manager = GPUManager(gpu_id)
            self.profiler = PerformanceProfiler()
            self.visualizer = NetworkVisualizer(self.gpu_manager)
            self.collective_intelligence = CollectiveIntelligence()
            
            print(f"🎮 Simulador GPU inicializado para {num_nodes:,} nós")
            print(f"🎯 Device: {self.device}")
        else:
            self.device = "cpu"
            self.gpu_manager = None
            self.profiler = None
            self.visualizer = None
            self.collective_intelligence = None
            print(f"⚠️ Simulador em modo CPU para {num_nodes:,} nós")
        
        # Estado da simulação
        self.nodes_state = None
        self.connection_matrix = None
        self.ai_decisions = None
        self.network_history = []
        
        # Estatísticas
        self.stats = {
            "start_time": None,
            "total_operations": 0,
            "total_connections": 0,
            "total_decisions": 0,
            "consensus_rounds": 0,
            "performance_metrics": {}
        }

    def initialize_network(self):
        """Inicializa a rede P2P massiva"""
        print(f"🚀 Inicializando rede de {self.num_nodes:,} nós...")
        
        def init_network():
            if GPU_AVAILABLE:
                # Estados dos nós (ativo/inativo, confiança, etc.)
                self.nodes_state = torch.rand((self.num_nodes, 5), device=self.device)
                
                # Matriz de conexões (limitada por memória)
                max_connections = min(self.num_nodes, 5000)  # Limita por memória
                self.connection_matrix = torch.randint(
                    0, 2, (max_connections, max_connections), 
                    device=self.device, dtype=torch.float32
                )
                
                # Decisões de IA para cada nó
                self.ai_decisions = torch.rand((self.num_nodes,), device=self.device)
                
                return {
                    "nodes_initialized": self.num_nodes,
                    "connections_matrix_size": (max_connections, max_connections),
                    "memory_used": torch.cuda.memory_allocated(self.device) / 1024**2 if GPU_AVAILABLE else 0
                }
            else:
                # Simulação CPU
                self.nodes_state = [[np.random.random() for _ in range(5)] for _ in range(self.num_nodes)]
                self.connection_matrix = np.random.randint(0, 2, (min(self.num_nodes, 1000), min(self.num_nodes, 1000)))
                self.ai_decisions = [np.random.random() for _ in range(self.num_nodes)]
                
                return {
                    "nodes_initialized": self.num_nodes,
                    "connections_matrix_size": self.connection_matrix.shape,
                    "memory_used": 0
                }
        
        if self.profiler:
            result = self.profiler.profile_operation("network_initialization", init_network)
            print(f"✅ Rede inicializada: {result['result']}")
            print(f"⚡ Tempo de inicialização: {result['profile']['execution_time']:.2f}s")
            return result['result']
        else:
            return init_network()

    def simulate_peer_discovery(self, discovery_rounds=10):
        """Simula descoberta de peers em massa"""
        print(f"🔍 Simulando descoberta de peers - {discovery_rounds} rounds...")
        
        def discovery_simulation():
            discoveries = []
            
            for round_num in range(discovery_rounds):
                if GPU_AVAILABLE and self.nodes_state is not None:
                    # Simula broadcast de descoberta
                    active_nodes = torch.sum(self.nodes_state[:, 0] > 0.5).item()
                    
                    # Cada nó ativo tenta descobrir outros
                    discovery_attempts = torch.randint(1, 10, (active_nodes,), device=self.device)
                    successful_discoveries = torch.sum(discovery_attempts).item()
                    
                    round_result = {
                        "round": round_num + 1,
                        "active_nodes": active_nodes,
                        "discovery_attempts": torch.sum(discovery_attempts).item(),
                        "successful_discoveries": successful_discoveries,
                        "discovery_rate": successful_discoveries / active_nodes if active_nodes > 0 else 0
                    }
                else:
                    # Simulação CPU
                    active_nodes = sum(1 for node in self.nodes_state if node[0] > 0.5)
                    discovery_attempts = sum(np.random.randint(1, 10) for _ in range(active_nodes))
                    successful_discoveries = int(discovery_attempts * 0.7)  # 70% de sucesso
                    
                    round_result = {
                        "round": round_num + 1,
                        "active_nodes": active_nodes,
                        "discovery_attempts": discovery_attempts,
                        "successful_discoveries": successful_discoveries,
                        "discovery_rate": successful_discoveries / active_nodes if active_nodes > 0 else 0
                    }
                
                discoveries.append(round_result)
                
                # Atualiza estatísticas
                self.stats["total_connections"] += successful_discoveries
            
            return discoveries
        
        if self.profiler:
            result = self.profiler.profile_operation("peer_discovery", discovery_simulation)
            discoveries = result['result']
            print(f"🔍 Discovery concluído em {result['profile']['execution_time']:.2f}s")
        else:
            discoveries = discovery_simulation()
        
        # Exibe resultados
        total_discoveries = sum(d["successful_discoveries"] for d in discoveries)
        avg_rate = sum(d["discovery_rate"] for d in discoveries) / len(discoveries)
        
        print(f"📊 Total discoveries: {total_discoveries:,}")
        print(f"📈 Taxa média de descoberta: {avg_rate:.3f}")
        
        return discoveries

    def simulate_ai_consensus(self, consensus_rounds=5):
        """Simula consenso distribuído com IA"""
        print(f"🧠 Simulando consenso com IA - {consensus_rounds} rounds...")
        
        def consensus_simulation():
            consensus_results = []
            
            for round_num in range(consensus_rounds):
                if GPU_AVAILABLE and self.ai_decisions is not None:
                    # Cada nó vota baseado em sua IA
                    votes = (self.ai_decisions > 0.5).float()
                    positive_votes = torch.sum(votes).item()
                    total_votes = self.num_nodes
                    
                    # Consenso alcançado se >50% dos votos são positivos
                    consensus_achieved = positive_votes > (total_votes / 2)
                    consensus_strength = positive_votes / total_votes
                    
                    # Simula evolução das decisões de IA
                    learning_rate = 0.01
                    if consensus_achieved:
                        # Reforça decisões que levaram ao consenso
                        self.ai_decisions = torch.clamp(
                            self.ai_decisions + learning_rate * votes, 0, 1
                        )
                    
                    round_result = {
                        "round": round_num + 1,
                        "positive_votes": positive_votes,
                        "total_votes": total_votes,
                        "consensus_achieved": consensus_achieved,
                        "consensus_strength": consensus_strength,
                        "avg_ai_confidence": torch.mean(self.ai_decisions).item()
                    }
                else:
                    # Simulação CPU
                    positive_votes = sum(1 for decision in self.ai_decisions if decision > 0.5)
                    total_votes = len(self.ai_decisions)
                    consensus_achieved = positive_votes > (total_votes / 2)
                    consensus_strength = positive_votes / total_votes
                    
                    # Simula aprendizado
                    for i in range(len(self.ai_decisions)):
                        if consensus_achieved and self.ai_decisions[i] > 0.5:
                            self.ai_decisions[i] = min(1.0, self.ai_decisions[i] + 0.01)
                    
                    round_result = {
                        "round": round_num + 1,
                        "positive_votes": positive_votes,
                        "total_votes": total_votes,
                        "consensus_achieved": consensus_achieved,
                        "consensus_strength": consensus_strength,
                        "avg_ai_confidence": sum(self.ai_decisions) / len(self.ai_decisions)
                    }
                
                consensus_results.append(round_result)
                self.stats["consensus_rounds"] += 1
                
                print(f"  Round {round_num + 1}: {positive_votes}/{total_votes} votos - " +
                      f"Consenso: {'✅' if consensus_achieved else '❌'} ({consensus_strength:.1%})")
            
            return consensus_results
        
        if self.profiler:
            result = self.profiler.profile_operation("ai_consensus", consensus_simulation)
            consensus_results = result['result']
            print(f"🧠 Consenso concluído em {result['profile']['execution_time']:.2f}s")
        else:
            consensus_results = consensus_simulation()
        
        # Estatísticas finais
        successful_consensus = sum(1 for r in consensus_results if r["consensus_achieved"])
        avg_strength = sum(r["consensus_strength"] for r in consensus_results) / len(consensus_results)
        
        print(f"🏆 Consensos bem-sucedidos: {successful_consensus}/{len(consensus_results)}")
        print(f"💪 Força média do consenso: {avg_strength:.1%}")
        
        return consensus_results

    def visualize_network_realtime(self, duration=30, update_interval=1):
        """Visualização em tempo real da rede (se matplotlib disponível)"""
        if not PLOTTING_AVAILABLE:
            print("⚠️ Matplotlib não disponível - pulando visualização")
            return
        
        print(f"🎨 Iniciando visualização em tempo real por {duration}s...")
        
        # Configura matplotlib para visualização
        plt.ion()
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
        fig.suptitle(f'AEONCOSMA P2P Network - {self.num_nodes:,} Nodes', fontsize=16)
        
        # Dados para plotagem
        time_data = []
        active_nodes_data = []
        consensus_data = []
        memory_data = []
        
        start_time = time.time()
        
        try:
            while time.time() - start_time < duration:
                current_time = time.time() - start_time
                
                # Calcula métricas atuais
                if GPU_AVAILABLE and self.nodes_state is not None:
                    active_nodes = torch.sum(self.nodes_state[:, 0] > 0.5).item()
                    avg_confidence = torch.mean(self.ai_decisions).item() if self.ai_decisions is not None else 0
                    memory_usage = torch.cuda.memory_allocated(self.device) / 1024**2 if GPU_AVAILABLE else 0
                else:
                    active_nodes = sum(1 for node in self.nodes_state if node[0] > 0.5)
                    avg_confidence = sum(self.ai_decisions) / len(self.ai_decisions)
                    memory_usage = 0
                
                # Adiciona dados
                time_data.append(current_time)
                active_nodes_data.append(active_nodes)
                consensus_data.append(avg_confidence)
                memory_data.append(memory_usage)
                
                # Limita histórico
                if len(time_data) > 30:
                    time_data.pop(0)
                    active_nodes_data.pop(0)
                    consensus_data.pop(0)
                    memory_data.pop(0)
                
                # Atualiza plots
                ax1.clear()
                ax1.plot(time_data, active_nodes_data, 'b-', linewidth=2)
                ax1.set_title('Active Nodes')
                ax1.set_ylabel('Count')
                ax1.grid(True)
                
                ax2.clear()
                ax2.plot(time_data, consensus_data, 'g-', linewidth=2)
                ax2.set_title('AI Consensus Level')
                ax2.set_ylabel('Confidence')
                ax2.set_ylim(0, 1)
                ax2.grid(True)
                
                ax3.clear()
                if len(time_data) > 1:
                    connections_rate = [active_nodes_data[i] * 2 for i in range(len(active_nodes_data))]
                    ax3.plot(time_data, connections_rate, 'r-', linewidth=2)
                ax3.set_title('Network Connections')
                ax3.set_ylabel('Connections')
                ax3.grid(True)
                
                ax4.clear()
                ax4.plot(time_data, memory_data, 'm-', linewidth=2)
                ax4.set_title('GPU Memory Usage (MB)')
                ax4.set_ylabel('Memory (MB)')
                ax4.grid(True)
                
                plt.tight_layout()
                plt.pause(update_interval)
                
                # Simula evolução da rede
                if GPU_AVAILABLE and self.nodes_state is not None:
                    # Pequenas mudanças aleatórias no estado
                    noise = torch.randn_like(self.nodes_state) * 0.01
                    self.nodes_state = torch.clamp(self.nodes_state + noise, 0, 1)
                
                time.sleep(update_interval)
                
        except KeyboardInterrupt:
            print("\n🛑 Visualização interrompida pelo usuário")
        
        plt.ioff()
        plt.show()
        
        print("✅ Visualização concluída")

    def run_full_simulation(self, discovery_rounds=5, consensus_rounds=3, duration=60):
        """Executa simulação completa"""
        print(f"🚀 Iniciando simulação completa do AEONCOSMA")
        print(f"📊 Parâmetros: {self.num_nodes:,} nós, {discovery_rounds} discovery, {consensus_rounds} consensus")
        
        self.running = True
        self.stats["start_time"] = datetime.now()
        
        try:
            # 1. Inicialização
            init_result = self.initialize_network()
            
            # 2. Descoberta de peers
            discovery_results = self.simulate_peer_discovery(discovery_rounds)
            
            # 3. Consenso com IA
            consensus_results = self.simulate_ai_consensus(consensus_rounds)
            
            # 4. Visualização (opcional)
            if PLOTTING_AVAILABLE and duration > 0:
                print(f"🎨 Iniciando visualização por {duration}s...")
                viz_thread = threading.Thread(
                    target=self.visualize_network_realtime, 
                    args=(duration,),
                    daemon=True
                )
                viz_thread.start()
                viz_thread.join()
            
            # 5. Resultados finais
            final_stats = self.get_final_statistics()
            
            print(f"\n🏆 SIMULAÇÃO CONCLUÍDA")
            print(f"⏱️ Duração total: {(datetime.now() - self.stats['start_time']).total_seconds():.1f}s")
            print(f"🎯 Performance: {final_stats}")
            
            return {
                "initialization": init_result,
                "discovery": discovery_results,
                "consensus": consensus_results,
                "final_stats": final_stats
            }
            
        except Exception as e:
            print(f"❌ Erro na simulação: {e}")
            return {"error": str(e)}
        finally:
            self.running = False

    def get_final_statistics(self):
        """Retorna estatísticas finais da simulação"""
        uptime = (datetime.now() - self.stats["start_time"]).total_seconds() if self.stats["start_time"] else 0
        
        stats = {
            "simulation_duration": uptime,
            "total_nodes": self.num_nodes,
            "total_connections": self.stats["total_connections"],
            "consensus_rounds": self.stats["consensus_rounds"],
            "nodes_per_second": self.num_nodes / uptime if uptime > 0 else 0,
            "connections_per_second": self.stats["total_connections"] / uptime if uptime > 0 else 0
        }
        
        # Adiciona estatísticas GPU se disponível
        if self.gpu_manager:
            stats["gpu_stats"] = self.gpu_manager.get_stats()
        
        if self.profiler:
            stats["performance_profile"] = self.profiler.get_performance_summary()
        
        return stats

def main():
    """Execução principal do simulador"""
    import argparse
    
    parser = argparse.ArgumentParser(description='AEONCOSMA GPU Massive Simulator')
    parser.add_argument('--nodes', type=int, default=10000, help='Número de nós a simular')
    parser.add_argument('--gpu-id', type=int, default=0, help='ID da GPU')
    parser.add_argument('--discovery-rounds', type=int, default=5, help='Rounds de descoberta')
    parser.add_argument('--consensus-rounds', type=int, default=3, help='Rounds de consenso')
    parser.add_argument('--visualization-time', type=int, default=30, help='Tempo de visualização (segundos)')
    parser.add_argument('--no-viz', action='store_true', help='Pula visualização')
    
    args = parser.parse_args()
    
    # Cria simulador
    simulator = MassiveP2PSimulator(
        num_nodes=args.nodes,
        gpu_id=args.gpu_id
    )
    
    # Executa simulação
    viz_time = 0 if args.no_viz else args.visualization_time
    
    results = simulator.run_full_simulation(
        discovery_rounds=args.discovery_rounds,
        consensus_rounds=args.consensus_rounds,
        duration=viz_time
    )
    
    # Salva resultados
    output_file = f"simulation_results_{args.nodes}_nodes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"📁 Resultados salvos em: {output_file}")

if __name__ == "__main__":
    main()
