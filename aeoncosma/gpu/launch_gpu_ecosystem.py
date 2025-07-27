# aeoncosma/gpu/launch_gpu_ecosystem.py
"""
🚀 AEONCOSMA GPU Ecosystem Launcher
Launcher principal para ecosystem GPU com 100k+ nós
Desenvolvido por Luiz Cruz - 2025
"""

import time
import json
import argparse
import threading
from datetime import datetime
from typing import Dict, List
import sys
import os

# Adiciona path para importações
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Importações condicionais
try:
    from gpu.gpu_accelerated_node import GPUAcceleratedNode
    from gpu.gpu_simulator import MassiveP2PSimulator
    from gpu.stable_diffusion_visualizer import NetworkArtGenerator
    from gpu.gpu_utils import GPUManager, PerformanceProfiler
    GPU_ECOSYSTEM_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Módulos GPU ecosystem não disponíveis: {e}")
    GPU_ECOSYSTEM_AVAILABLE = False

# Fallback para modo básico
try:
    from networking.p2p_node import P2PNode
    BASIC_P2P_AVAILABLE = True
except ImportError:
    print("⚠️ Módulos P2P básicos não disponíveis")
    BASIC_P2P_AVAILABLE = False

class GPUEcosystemLauncher:
    """
    Launcher principal do ecosystem GPU AEONCOSMA
    Orquestra nós GPU, simulação massiva e visualização artística
    """
    
    def __init__(self, config_file=None):
        self.config = self.load_config(config_file)
        self.running = False
        self.components = {}
        
        # Threads ativas
        self.active_threads = []
        
        # Estatísticas globais
        self.global_stats = {
            "start_time": None,
            "gpu_nodes_launched": 0,
            "simulations_run": 0,
            "art_generated": 0,
            "total_p2p_connections": 0
        }
        
        print(f"🚀 AEONCOSMA GPU Ecosystem Launcher inicializado")
        print(f"🔧 Configuração: {self.config}")

    def load_config(self, config_file):
        """Carrega configuração do ecosystem"""
        default_config = {
            "gpu": {
                "enabled": True,
                "device_ids": [0],
                "max_nodes_per_gpu": 1000,
                "simulation_nodes": 10000
            },
            "network": {
                "base_port": 9000,
                "host": "127.0.0.1",
                "discovery_enabled": True
            },
            "simulation": {
                "massive_scale": True,
                "max_nodes": 100000,
                "discovery_rounds": 10,
                "consensus_rounds": 5,
                "visualization_duration": 60
            },
            "art_generation": {
                "enabled": False,  # Disabled by default devido aos requisitos
                "model_id": "runwayml/stable-diffusion-v1-5",
                "auto_generate": False,
                "generation_interval": 300  # 5 minutos
            },
            "monitoring": {
                "stats_interval": 30,
                "performance_profiling": True,
                "export_logs": True
            }
        }
        
        if config_file and os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    user_config = json.load(f)
                    # Merge configs
                    default_config.update(user_config)
            except Exception as e:
                print(f"⚠️ Erro ao carregar config: {e} - usando default")
        
        return default_config

    def check_gpu_availability(self):
        """Verifica disponibilidade e capacidade das GPUs"""
        gpu_info = {"available": False, "devices": []}
        
        if not GPU_ECOSYSTEM_AVAILABLE:
            print("⚠️ Ecosystem GPU não disponível - modo compatibilidade")
            return gpu_info
        
        try:
            import torch
            if torch.cuda.is_available():
                gpu_info["available"] = True
                
                for i in range(torch.cuda.device_count()):
                    device_props = torch.cuda.get_device_properties(i)
                    device_info = {
                        "id": i,
                        "name": device_props.name,
                        "memory_total": device_props.total_memory / 1024**3,  # GB
                        "memory_available": (device_props.total_memory - torch.cuda.memory_allocated(i)) / 1024**3,
                        "compute_capability": f"{device_props.major}.{device_props.minor}"
                    }
                    gpu_info["devices"].append(device_info)
                    
                    print(f"🎮 GPU {i}: {device_info['name']} - {device_info['memory_total']:.1f}GB")
            else:
                print("⚠️ CUDA não disponível - usando CPU")
                
        except Exception as e:
            print(f"❌ Erro ao verificar GPU: {e}")
        
        return gpu_info

    def launch_gpu_nodes(self, num_nodes=5, start_port=9000):
        """Lança múltiplos nós GPU"""
        print(f"🚀 Lançando {num_nodes} nós GPU...")
        
        gpu_info = self.check_gpu_availability()
        
        for i in range(num_nodes):
            node_id = f"gpu_node_{i:03d}"
            port = start_port + i
            gpu_id = i % len(gpu_info["devices"]) if gpu_info["devices"] else 0
            
            try:
                if GPU_ECOSYSTEM_AVAILABLE:
                    # Nó GPU avançado
                    node = GPUAcceleratedNode(
                        host=self.config["network"]["host"],
                        port=port,
                        node_id=node_id,
                        gpu_id=gpu_id
                    )
                elif BASIC_P2P_AVAILABLE:
                    # Fallback para nó básico
                    node = P2PNode(
                        host=self.config["network"]["host"],
                        port=port,
                        node_id=node_id
                    )
                else:
                    print(f"❌ Nenhum tipo de nó disponível")
                    continue
                
                # Inicia nó em thread separada
                node_thread = threading.Thread(
                    target=self.run_node,
                    args=(node,),
                    daemon=True
                )
                node_thread.start()
                self.active_threads.append(node_thread)
                
                self.components[node_id] = node
                self.global_stats["gpu_nodes_launched"] += 1
                
                print(f"✅ Nó {node_id} lançado na porta {port}")
                time.sleep(0.5)  # Pequena pausa entre launches
                
            except Exception as e:
                print(f"❌ Erro ao lançar nó {node_id}: {e}")
        
        print(f"🌐 {len(self.components)} nós ativos")

    def run_node(self, node):
        """Executa um nó em thread separada"""
        try:
            node.start()
            while self.running:
                time.sleep(1)
        except Exception as e:
            print(f"❌ Erro na execução do nó {node.node_id}: {e}")
        finally:
            if hasattr(node, 'stop'):
                node.stop()

    def launch_massive_simulation(self):
        """Lança simulação massiva"""
        if not GPU_ECOSYSTEM_AVAILABLE:
            print("⚠️ Simulação massiva requer módulos GPU")
            return None
        
        try:
            print(f"🎮 Iniciando simulação massiva...")
            
            simulator = MassiveP2PSimulator(
                num_nodes=self.config["simulation"]["max_nodes"],
                gpu_id=0
            )
            
            # Executa simulação em thread separada
            sim_thread = threading.Thread(
                target=self.run_simulation,
                args=(simulator,),
                daemon=True
            )
            sim_thread.start()
            self.active_threads.append(sim_thread)
            
            self.components["massive_simulator"] = simulator
            self.global_stats["simulations_run"] += 1
            
            return simulator
            
        except Exception as e:
            print(f"❌ Erro na simulação massiva: {e}")
            return None

    def run_simulation(self, simulator):
        """Executa simulação em thread separada"""
        try:
            results = simulator.run_full_simulation(
                discovery_rounds=self.config["simulation"]["discovery_rounds"],
                consensus_rounds=self.config["simulation"]["consensus_rounds"],
                duration=self.config["simulation"]["visualization_duration"]
            )
            
            # Salva resultados
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            results_file = f"massive_simulation_results_{timestamp}.json"
            
            with open(results_file, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            
            print(f"📁 Resultados da simulação salvos: {results_file}")
            
        except Exception as e:
            print(f"❌ Erro na execução da simulação: {e}")

    def launch_art_generator(self):
        """Lança gerador de arte da rede"""
        if not self.config["art_generation"]["enabled"]:
            print("🎨 Geração de arte desabilitada na configuração")
            return None
        
        try:
            print(f"🎨 Iniciando gerador de arte...")
            
            art_generator = NetworkArtGenerator(
                model_id=self.config["art_generation"]["model_id"]
            )
            
            if self.config["art_generation"]["auto_generate"]:
                # Thread para geração automática
                art_thread = threading.Thread(
                    target=self.auto_generate_art,
                    args=(art_generator,),
                    daemon=True
                )
                art_thread.start()
                self.active_threads.append(art_thread)
            
            self.components["art_generator"] = art_generator
            
            return art_generator
            
        except Exception as e:
            print(f"❌ Erro no gerador de arte: {e}")
            return None

    def auto_generate_art(self, art_generator):
        """Geração automática de arte baseada no estado da rede"""
        interval = self.config["art_generation"]["generation_interval"]
        
        while self.running:
            try:
                # Coleta estado atual da rede
                network_state = self.collect_network_state()
                
                # Gera arte
                result = art_generator.generate_network_art(network_state)
                
                if result["success"]:
                    self.global_stats["art_generated"] += 1
                    print(f"🎨 Arte automática gerada: {result['metadata']['filename']}")
                
                time.sleep(interval)
                
            except Exception as e:
                print(f"❌ Erro na geração automática de arte: {e}")
                time.sleep(60)  # Espera mais em caso de erro

    def collect_network_state(self):
        """Coleta estado atual da rede para arte/análise"""
        # Coleta informações dos nós ativos
        active_nodes = 0
        total_connections = 0
        ai_decisions = []
        
        for node_id, node in self.components.items():
            if hasattr(node, 'get_network_info'):
                info = node.get_network_info()
                active_nodes += 1
                total_connections += info.get("peers_count", 0)
                
                # Coleta decisões de IA se disponível
                if hasattr(node, 'gpu_stats'):
                    ai_decisions.append(node.gpu_stats.get("ai_decisions", 0))
        
        # Estado da simulação massiva se disponível
        simulation_data = {}
        if "massive_simulator" in self.components:
            simulator = self.components["massive_simulator"]
            if hasattr(simulator, 'stats'):
                simulation_data = simulator.stats
        
        network_state = {
            "timestamp": datetime.now().isoformat(),
            "total_nodes": len(self.components),
            "active_nodes": active_nodes,
            "total_connections": total_connections,
            "consensus_strength": sum(ai_decisions) / len(ai_decisions) if ai_decisions else 0.5,
            "ai_confidence": 0.7,  # Placeholder
            "connections_density": total_connections / max(active_nodes, 1) / 10.0,
            "simulation_data": simulation_data,
            "global_stats": self.global_stats
        }
        
        return network_state

    def start_monitoring(self):
        """Inicia monitoramento do ecosystem"""
        monitor_thread = threading.Thread(
            target=self.monitor_ecosystem,
            daemon=True
        )
        monitor_thread.start()
        self.active_threads.append(monitor_thread)

    def monitor_ecosystem(self):
        """Monitor contínuo do ecosystem"""
        interval = self.config["monitoring"]["stats_interval"]
        
        while self.running:
            try:
                # Coleta estatísticas
                network_state = self.collect_network_state()
                
                # Atualiza conexões totais
                self.global_stats["total_p2p_connections"] = network_state["total_connections"]
                
                # Log de status
                uptime = time.time() - self.global_stats["start_time"] if self.global_stats["start_time"] else 0
                
                print(f"📊 ECOSYSTEM STATUS [{datetime.now().strftime('%H:%M:%S')}]")
                print(f"   ⏱️ Uptime: {uptime:.0f}s")
                print(f"   🎮 GPU Nodes: {self.global_stats['gpu_nodes_launched']}")
                print(f"   🔗 P2P Connections: {network_state['total_connections']}")
                print(f"   🧠 AI Confidence: {network_state['ai_confidence']:.2f}")
                print(f"   🎨 Art Generated: {self.global_stats['art_generated']}")
                
                # Exporta logs se configurado
                if self.config["monitoring"]["export_logs"]:
                    self.export_ecosystem_state(network_state)
                
                time.sleep(interval)
                
            except Exception as e:
                print(f"❌ Erro no monitoramento: {e}")
                time.sleep(30)

    def export_ecosystem_state(self, network_state):
        """Exporta estado do ecosystem para arquivo"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"ecosystem_state_{timestamp}.json"
            
            with open(filename, 'w') as f:
                json.dump({
                    "ecosystem_stats": self.global_stats,
                    "network_state": network_state,
                    "config": self.config,
                    "components": list(self.components.keys())
                }, f, indent=2, default=str)
                
        except Exception as e:
            print(f"⚠️ Erro ao exportar estado: {e}")

    def run_complete_ecosystem(self, duration=None):
        """Executa ecosystem completo"""
        print(f"🚀 INICIANDO AEONCOSMA GPU ECOSYSTEM COMPLETO")
        print(f"=" * 60)
        
        self.running = True
        self.global_stats["start_time"] = time.time()
        
        try:
            # 1. Verificar GPU
            gpu_info = self.check_gpu_availability()
            
            # 2. Lançar nós GPU
            self.launch_gpu_nodes(
                num_nodes=5,
                start_port=self.config["network"]["base_port"]
            )
            
            # 3. Lançar simulação massiva
            if self.config["simulation"]["massive_scale"]:
                self.launch_massive_simulation()
            
            # 4. Lançar gerador de arte
            self.launch_art_generator()
            
            # 5. Iniciar monitoramento
            self.start_monitoring()
            
            # 6. Aguardar ou executar por duração especificada
            if duration:
                print(f"🕐 Executando por {duration} segundos...")
                time.sleep(duration)
            else:
                print(f"🔄 Ecosystem em execução. Pressione Ctrl+C para parar.")
                while self.running:
                    time.sleep(1)
                    
        except KeyboardInterrupt:
            print(f"\n🛑 Ecosystem interrompido pelo usuário")
        except Exception as e:
            print(f"❌ Erro crítico no ecosystem: {e}")
        finally:
            self.shutdown_ecosystem()

    def shutdown_ecosystem(self):
        """Shutdown graceful do ecosystem"""
        print(f"🛑 Iniciando shutdown do ecosystem...")
        
        self.running = False
        
        # Para todos os componentes
        for name, component in self.components.items():
            try:
                if hasattr(component, 'stop'):
                    component.stop()
                elif hasattr(component, 'running'):
                    component.running = False
                print(f"✅ {name} parado")
            except Exception as e:
                print(f"⚠️ Erro ao parar {name}: {e}")
        
        # Aguarda threads terminarem
        for thread in self.active_threads:
            if thread.is_alive():
                thread.join(timeout=5)
        
        # Estatísticas finais
        if self.global_stats["start_time"]:
            total_uptime = time.time() - self.global_stats["start_time"]
            print(f"\n📊 ESTATÍSTICAS FINAIS:")
            print(f"   ⏱️ Uptime total: {total_uptime:.1f}s")
            print(f"   🎮 Nós GPU lançados: {self.global_stats['gpu_nodes_launched']}")
            print(f"   🎯 Simulações executadas: {self.global_stats['simulations_run']}")
            print(f"   🎨 Artes geradas: {self.global_stats['art_generated']}")
            print(f"   🔗 Total conexões P2P: {self.global_stats['total_p2p_connections']}")
        
        print(f"✅ Ecosystem shutdown concluído")

def main():
    """Execução principal do launcher"""
    parser = argparse.ArgumentParser(description='AEONCOSMA GPU Ecosystem Launcher')
    parser.add_argument('--config', help='Arquivo de configuração JSON')
    parser.add_argument('--duration', type=int, help='Duração em segundos (0 = infinito)')
    parser.add_argument('--nodes', type=int, default=5, help='Número de nós GPU')
    parser.add_argument('--simulate', type=int, help='Número de nós para simulação massiva')
    parser.add_argument('--art', action='store_true', help='Habilita geração de arte')
    parser.add_argument('--port', type=int, default=9000, help='Porta base')
    
    args = parser.parse_args()
    
    # Cria launcher
    launcher = GPUEcosystemLauncher(config_file=args.config)
    
    # Atualiza configuração com argumentos
    if args.simulate:
        launcher.config["simulation"]["max_nodes"] = args.simulate
        launcher.config["simulation"]["massive_scale"] = True
    
    if args.art:
        launcher.config["art_generation"]["enabled"] = True
    
    launcher.config["network"]["base_port"] = args.port
    
    # Executa ecosystem
    launcher.run_complete_ecosystem(duration=args.duration)

if __name__ == "__main__":
    main()
