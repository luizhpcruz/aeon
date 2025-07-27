# aeoncosma/gpu/gpu_accelerated_node.py
"""
🧠 AEONCOSMA GPU-Accelerated P2P Node
Sistema de nós com IA embarcada e processamento GPU massivo
Desenvolvido por Luiz Cruz - 2025
"""

import torch
import cupy as cp
import numpy as np
import threading
import time
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
import sys
import os

# Adiciona path para importações
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

try:
    from networking.p2p_node import P2PNode
    from gpu.node_brain import NodeBrain
    from gpu.gpu_utils import GPUManager
    GPU_AVAILABLE = torch.cuda.is_available()
    CUPY_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Módulos GPU não encontrados: {e}")
    GPU_AVAILABLE = False
    CUPY_AVAILABLE = False

class GPUAcceleratedNode(P2PNode):
    """
    Nó P2P com aceleração GPU e IA embarcada
    Herda funcionalidades básicas e adiciona processamento paralelo
    """
    
    def __init__(self, host="127.0.0.1", port=9000, node_id="gpu_node_001", 
                 aeon_address="http://127.0.0.1:8000/validate", gpu_id=0):
        super().__init__(host, port, node_id, aeon_address)
        
        self.gpu_id = gpu_id
        self.device = torch.device(f'cuda:{gpu_id}' if GPU_AVAILABLE else 'cpu')
        
        # Inicializa componentes GPU
        if GPU_AVAILABLE:
            self.gpu_manager = GPUManager(gpu_id)
            self.node_brain = NodeBrain().to(self.device)
            self.parallel_validator = ParallelValidator(self.device)
            
            # Estado da rede em tensores GPU
            self.network_tensor = torch.zeros((1000, 5), device=self.device)  # Max 1000 nós
            self.connection_matrix = torch.zeros((1000, 1000), device=self.device)
            
            print(f"🎮 [{self.node_id}] GPU {gpu_id} inicializada: {torch.cuda.get_device_name(gpu_id)}")
            print(f"💾 VRAM disponível: {torch.cuda.get_device_properties(gpu_id).total_memory / 1024**3:.1f} GB")
        else:
            print(f"⚠️ [{self.node_id}] GPU não disponível - usando CPU")
            self.gpu_manager = None
            self.node_brain = None
            self.parallel_validator = None
        
        # Estatísticas GPU
        self.gpu_stats = {
            "gpu_validations": 0,
            "parallel_broadcasts": 0,
            "ai_decisions": 0,
            "tensor_operations": 0,
            "gpu_memory_peak": 0,
            "computation_time": 0
        }
        
        # Thread para monitoramento GPU
        if GPU_AVAILABLE:
            gpu_monitor = threading.Thread(target=self.gpu_monitor, daemon=True)
            gpu_monitor.start()

    def handle_peer_gpu(self, conn, addr):
        """Processamento de peer com aceleração GPU"""
        if not GPU_AVAILABLE:
            return super().handle_peer(conn, addr)
        
        start_time = time.time()
        
        try:
            print(f"🎮 [{self.node_id}] GPU peer handling: {addr}")
            
            # Recebe dados
            data = conn.recv(4096).decode('utf-8')
            if not data:
                return
            
            peer_info = json.loads(data)
            self.stats["messages_received"] += 1
            
            # Converte informações do peer para tensor
            peer_tensor = self.encode_peer_to_tensor(peer_info)
            
            # IA decide usando rede neural
            with torch.no_grad():
                ai_input = torch.cat([
                    peer_tensor,
                    torch.tensor([len(self.peers) / 1000.0], device=self.device),  # Densidade da rede
                    torch.tensor([self.get_uptime() / 3600.0], device=self.device)  # Uptime normalizado
                ]).unsqueeze(0)
                
                ai_decision = self.node_brain(ai_input)
                confidence = ai_decision.item()
                
            self.gpu_stats["ai_decisions"] += 1
            
            # Decisão baseada na IA
            is_valid = confidence > 0.5
            
            if is_valid:
                self.peers.append(peer_info)
                self.stats["peers_validated"] += 1
                self.gpu_stats["gpu_validations"] += 1
                
                # Atualiza tensor da rede
                peer_idx = len(self.peers) - 1
                if peer_idx < 1000:
                    self.network_tensor[peer_idx] = peer_tensor
                
                response = {
                    "status": "accepted",
                    "node_id": self.node_id,
                    "timestamp": datetime.now().isoformat(),
                    "peer_count": len(self.peers),
                    "validation_type": "gpu_ai_neural",
                    "ai_confidence": confidence,
                    "gpu_id": self.gpu_id,
                    "computation_time": time.time() - start_time
                }
                
                print(f"🧠 [{self.node_id}] GPU-AI aceitou nó: {peer_info['node_id']} (confiança: {confidence:.3f})")
                
            else:
                self.stats["peers_rejected"] += 1
                
                response = {
                    "status": "rejected",
                    "node_id": self.node_id,
                    "reason": "GPU-AI validation failed",
                    "timestamp": datetime.now().isoformat(),
                    "validation_type": "gpu_ai_neural",
                    "ai_confidence": confidence,
                    "gpu_id": self.gpu_id
                }
                
                print(f"❌ [{self.node_id}] GPU-AI rejeitou nó: {peer_info['node_id']} (confiança: {confidence:.3f})")
            
            # Envia resposta
            conn.send(json.dumps(response).encode('utf-8'))
            self.stats["messages_sent"] += 1
            
            # Atualiza estatísticas de tempo
            computation_time = time.time() - start_time
            self.gpu_stats["computation_time"] += computation_time
            
        except Exception as e:
            print(f"❌ [{self.node_id}] Erro GPU peer handling: {e}")
        finally:
            conn.close()

    def encode_peer_to_tensor(self, peer_info: Dict) -> torch.Tensor:
        """Converte informações do peer para tensor GPU"""
        features = torch.zeros(5, device=self.device)
        
        try:
            # Feature 1: Hash do node_id (normalizado)
            features[0] = hash(peer_info.get("node_id", "")) % 1000 / 1000.0
            
            # Feature 2: Porta normalizada
            features[1] = peer_info.get("port", 9000) / 65535.0
            
            # Feature 3: Timestamp recency (últimas 24h)
            timestamp = peer_info.get("timestamp", datetime.now().isoformat())
            try:
                peer_time = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                age_hours = (datetime.now() - peer_time).total_seconds() / 3600
                features[2] = max(0, 1 - age_hours / 24.0)  # Mais recente = valor maior
            except:
                features[2] = 0.5
            
            # Feature 4: Context score
            context = peer_info.get("context", {})
            features[3] = min(context.get("peers_count", 0) / 100.0, 1.0)
            
            # Feature 5: Uptime score
            features[4] = min(context.get("uptime", 0) / 3600.0, 1.0)
            
        except Exception as e:
            print(f"⚠️ [{self.node_id}] Erro ao codificar peer: {e}")
            features.fill_(0.5)  # Valores neutros em caso de erro
        
        self.gpu_stats["tensor_operations"] += 1
        return features

    def parallel_broadcast_gpu(self, message: Dict):
        """Broadcast paralelo usando GPU"""
        if not GPU_AVAILABLE or len(self.peers) == 0:
            return super().broadcast_message(message)
        
        start_time = time.time()
        
        try:
            print(f"🎮 [{self.node_id}] GPU parallel broadcast para {len(self.peers)} peers")
            
            # Cria batch de conexões paralelas
            peer_batch = torch.tensor([
                [hash(p.get("node_id", "")) % 1000, p.get("port", 9000)] 
                for p in self.peers[:100]  # Limita a 100 por segurança
            ], device=self.device, dtype=torch.float32)
            
            # Simula processamento paralelo de broadcast
            with torch.no_grad():
                # Calcula "custo" de broadcast para cada peer
                broadcast_costs = torch.sum(peer_batch, dim=1) / 1000.0
                success_prob = torch.sigmoid(-broadcast_costs + 1.0)
                
                # Determina sucessos baseado em probabilidade
                successes = torch.bernoulli(success_prob)
                success_count = torch.sum(successes).item()
            
            self.gpu_stats["parallel_broadcasts"] += 1
            self.gpu_stats["tensor_operations"] += 3
            
            # Executa broadcast real para peers selecionados
            successful_peers = []
            for i, peer in enumerate(self.peers[:len(successes)]):
                if successes[i] == 1:
                    try:
                        response = self.connect_to_peer(
                            peer["host"], 
                            peer["port"], 
                            self.node_id
                        )
                        if response:
                            successful_peers.append(peer["node_id"])
                    except:
                        pass
            
            computation_time = time.time() - start_time
            self.gpu_stats["computation_time"] += computation_time
            
            result = {
                "success_rate": len(successful_peers) / len(self.peers) if self.peers else 0,
                "successful_peers": successful_peers,
                "total_peers": len(self.peers),
                "gpu_computation_time": computation_time,
                "gpu_predictions": success_count
            }
            
            print(f"📡 [{self.node_id}] GPU broadcast resultado: {len(successful_peers)}/{len(self.peers)} sucessos")
            return result
            
        except Exception as e:
            print(f"❌ [{self.node_id}] Erro GPU broadcast: {e}")
            return {"success_rate": 0, "error": str(e)}

    def simulate_massive_network(self, num_nodes=10000):
        """Simula rede massiva com GPU"""
        if not GPU_AVAILABLE:
            print(f"⚠️ [{self.node_id}] GPU não disponível para simulação massiva")
            return
        
        print(f"🎮 [{self.node_id}] Iniciando simulação de {num_nodes} nós...")
        
        start_time = time.time()
        
        try:
            # Estados dos nós (ativo/inativo)
            node_states = torch.randint(0, 2, (num_nodes,), device=self.device)
            active_nodes = torch.sum(node_states).item()
            
            # Matriz de conexões
            if num_nodes <= 5000:  # Limite de memória
                conn_matrix = torch.randint(0, 2, (num_nodes, num_nodes), device=self.device)
                total_connections = torch.sum(conn_matrix).item()
            else:
                # Para redes maiores, simula em chunks
                chunk_size = 1000
                total_connections = 0
                for i in range(0, num_nodes, chunk_size):
                    end_i = min(i + chunk_size, num_nodes)
                    chunk = torch.randint(0, 2, (end_i - i, end_i - i), device=self.device)
                    total_connections += torch.sum(chunk).item()
            
            # Consenso distribuído
            consensus_votes = torch.randint(0, 2, (active_nodes,), device=self.device)
            consensus_result = torch.sum(consensus_votes).item() > active_nodes // 2
            
            computation_time = time.time() - start_time
            
            result = {
                "total_nodes": num_nodes,
                "active_nodes": active_nodes,
                "total_connections": total_connections,
                "consensus_achieved": consensus_result,
                "computation_time": computation_time,
                "gpu_memory_used": torch.cuda.memory_allocated(self.device) / 1024**2,  # MB
                "gpu_id": self.gpu_id
            }
            
            print(f"✅ [{self.node_id}] Simulação concluída em {computation_time:.2f}s")
            print(f"   📊 Nós ativos: {active_nodes}/{num_nodes}")
            print(f"   🔗 Conexões: {total_connections:,}")
            print(f"   🗳️ Consenso: {'Atingido' if consensus_result else 'Falhado'}")
            print(f"   💾 GPU Memória: {result['gpu_memory_used']:.1f} MB")
            
            self.gpu_stats["tensor_operations"] += 5
            return result
            
        except Exception as e:
            print(f"❌ [{self.node_id}] Erro na simulação massiva: {e}")
            return {"error": str(e)}

    def gpu_monitor(self):
        """Monitor de recursos GPU"""
        while self.running:
            try:
                if GPU_AVAILABLE:
                    memory_used = torch.cuda.memory_allocated(self.device) / 1024**2  # MB
                    memory_peak = torch.cuda.max_memory_allocated(self.device) / 1024**2
                    
                    self.gpu_stats["gpu_memory_peak"] = max(
                        self.gpu_stats["gpu_memory_peak"], 
                        memory_peak
                    )
                    
                    if self.gpu_stats["ai_decisions"] > 0 and self.gpu_stats["ai_decisions"] % 50 == 0:
                        print(f"🎮 [{self.node_id}] GPU Stats:")
                        print(f"   🧠 AI Decisions: {self.gpu_stats['ai_decisions']}")
                        print(f"   ✅ GPU Validations: {self.gpu_stats['gpu_validations']}")
                        print(f"   📡 Parallel Broadcasts: {self.gpu_stats['parallel_broadcasts']}")
                        print(f"   ⚡ Tensor Ops: {self.gpu_stats['tensor_operations']}")
                        print(f"   💾 Memória atual: {memory_used:.1f} MB")
                        print(f"   🔝 Pico de memória: {memory_peak:.1f} MB")
                
                time.sleep(60)  # Monitora a cada minuto
                
            except Exception as e:
                print(f"⚠️ [{self.node_id}] Erro no monitor GPU: {e}")
                time.sleep(30)

    def get_gpu_info(self):
        """Retorna informações detalhadas da GPU"""
        if not GPU_AVAILABLE:
            return {"gpu_available": False}
        
        return {
            "gpu_available": True,
            "gpu_id": self.gpu_id,
            "gpu_name": torch.cuda.get_device_name(self.gpu_id),
            "gpu_memory_total": torch.cuda.get_device_properties(self.gpu_id).total_memory / 1024**3,
            "gpu_memory_allocated": torch.cuda.memory_allocated(self.device) / 1024**2,
            "gpu_memory_reserved": torch.cuda.memory_reserved(self.device) / 1024**2,
            "gpu_stats": self.gpu_stats,
            "node_brain_active": self.node_brain is not None,
            "cupy_available": CUPY_AVAILABLE
        }

    def export_gpu_metrics(self):
        """Exporta métricas GPU para análise"""
        metrics = {
            "node_id": self.node_id,
            "timestamp": datetime.now().isoformat(),
            "gpu_info": self.get_gpu_info(),
            "network_info": self.get_network_info(),
            "gpu_stats": self.gpu_stats
        }
        
        return json.dumps(metrics, indent=2)

class ParallelValidator:
    """Validador paralelo usando GPU"""
    
    def __init__(self, device):
        self.device = device
    
    def validate_batch(self, peer_batch):
        """Valida múltiplos peers em paralelo"""
        # Implementação de validação em lote
        pass

def main():
    """Teste do nó GPU"""
    import argparse
    
    parser = argparse.ArgumentParser(description='AEONCOSMA GPU-Accelerated P2P Node')
    parser.add_argument('--port', type=int, default=9000, help='Porta do nó')
    parser.add_argument('--node-id', default='gpu_node_001', help='ID do nó')
    parser.add_argument('--host', default='127.0.0.1', help='Host do nó')
    parser.add_argument('--gpu-id', type=int, default=0, help='ID da GPU')
    parser.add_argument('--simulate', type=int, help='Simular N nós')
    
    args = parser.parse_args()
    
    # Cria nó GPU
    node = GPUAcceleratedNode(
        host=args.host,
        port=args.port,
        node_id=args.node_id,
        gpu_id=args.gpu_id
    )
    
    try:
        node.start()
        
        # Simulação opcional
        if args.simulate:
            time.sleep(2)  # Aguarda inicialização
            node.simulate_massive_network(args.simulate)
        
        print(f"🚀 [{args.node_id}] Nó GPU em execução. Pressione Ctrl+C para parar.")
        
        while node.running:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print(f"\n🛑 [{args.node_id}] Interrompido pelo usuário")
    finally:
        node.stop()

if __name__ == "__main__":
    main()
