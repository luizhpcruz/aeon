# aeoncosma/gpu/gpu_utils.py
"""
🛠️ AEONCOSMA GPU Utilities - Ferramentas GPU para P2P
Utilitários para gerenciamento de GPU e otimização
Desenvolvido por Luiz Cruz - 2025
"""

import time
import json
from datetime import datetime
from typing import Dict, List, Any, Optional

try:
    import torch
    import cupy as cp
    import numpy as np
    GPU_AVAILABLE = torch.cuda.is_available()
    CUPY_AVAILABLE = True
except ImportError:
    print("⚠️ Bibliotecas GPU não disponíveis - usando simulação")
    GPU_AVAILABLE = False
    CUPY_AVAILABLE = False
    
    # Mock classes para compatibilidade
    class MockTensor:
        def __init__(self, data):
            self.data = data
        def item(self):
            return self.data
        def to(self, device):
            return self
    
    class torch:
        @staticmethod
        def tensor(data, device=None):
            return MockTensor(data[0] if isinstance(data, list) else data)
        
        @staticmethod
        def cuda():
            class MockCuda:
                @staticmethod
                def is_available():
                    return False
                @staticmethod
                def get_device_name(gpu_id):
                    return "Mock GPU"
                @staticmethod
                def memory_allocated(device):
                    return 0
                @staticmethod
                def get_device_properties(gpu_id):
                    class Props:
                        total_memory = 8 * 1024**3  # 8GB
                    return Props()
            return MockCuda()

class GPUManager:
    """Gerenciador de recursos GPU para nós P2P"""
    
    def __init__(self, gpu_id=0):
        self.gpu_id = gpu_id
        self.device = f'cuda:{gpu_id}' if GPU_AVAILABLE else 'cpu'
        self.memory_usage = []
        self.computation_times = []
        
        if GPU_AVAILABLE:
            self.gpu_name = torch.cuda.get_device_name(gpu_id)
            self.total_memory = torch.cuda.get_device_properties(gpu_id).total_memory
            print(f"🎮 GPU Manager inicializado: {self.gpu_name}")
        else:
            self.gpu_name = "CPU (GPU not available)"
            self.total_memory = 0
            print(f"⚠️ GPU Manager em modo CPU")
    
    def get_memory_info(self):
        """Retorna informações de memória GPU"""
        if not GPU_AVAILABLE:
            return {
                "allocated": 0,
                "reserved": 0,
                "total": 0,
                "free": 0,
                "utilization": 0.0
            }
        
        allocated = torch.cuda.memory_allocated(self.gpu_id)
        reserved = torch.cuda.memory_reserved(self.gpu_id)
        total = self.total_memory
        free = total - allocated
        
        return {
            "allocated": allocated / 1024**2,  # MB
            "reserved": reserved / 1024**2,    # MB
            "total": total / 1024**2,          # MB
            "free": free / 1024**2,            # MB
            "utilization": (allocated / total) * 100 if total > 0 else 0
        }
    
    def monitor_computation(self, func, *args, **kwargs):
        """Monitora tempo e memória de uma computação"""
        start_time = time.time()
        
        if GPU_AVAILABLE:
            start_memory = torch.cuda.memory_allocated(self.gpu_id)
        
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            print(f"❌ Erro na computação GPU: {e}")
            return None
        
        end_time = time.time()
        computation_time = end_time - start_time
        
        if GPU_AVAILABLE:
            end_memory = torch.cuda.memory_allocated(self.gpu_id)
            memory_delta = (end_memory - start_memory) / 1024**2  # MB
        else:
            memory_delta = 0
        
        self.computation_times.append(computation_time)
        self.memory_usage.append(memory_delta)
        
        return {
            "result": result,
            "computation_time": computation_time,
            "memory_delta": memory_delta,
            "memory_info": self.get_memory_info()
        }
    
    def optimize_memory(self):
        """Otimiza uso de memória GPU"""
        if not GPU_AVAILABLE:
            return {"status": "CPU mode - no optimization needed"}
        
        try:
            # Limpa cache
            torch.cuda.empty_cache()
            
            # Força garbage collection
            import gc
            gc.collect()
            
            memory_info = self.get_memory_info()
            
            return {
                "status": "optimization_complete",
                "memory_freed": "cache_cleared",
                "current_memory": memory_info
            }
        except Exception as e:
            return {"status": "optimization_failed", "error": str(e)}
    
    def get_stats(self):
        """Retorna estatísticas do GPU Manager"""
        stats = {
            "gpu_id": self.gpu_id,
            "gpu_name": self.gpu_name,
            "device": self.device,
            "gpu_available": GPU_AVAILABLE,
            "cupy_available": CUPY_AVAILABLE,
            "total_computations": len(self.computation_times),
            "memory_info": self.get_memory_info()
        }
        
        if self.computation_times:
            stats["computation_stats"] = {
                "avg_time": sum(self.computation_times) / len(self.computation_times),
                "min_time": min(self.computation_times),
                "max_time": max(self.computation_times),
                "total_time": sum(self.computation_times)
            }
        
        if self.memory_usage:
            stats["memory_stats"] = {
                "avg_usage": sum(self.memory_usage) / len(self.memory_usage),
                "peak_usage": max(self.memory_usage),
                "total_allocations": len(self.memory_usage)
            }
        
        return stats

class NetworkVisualizer:
    """Visualizador de rede P2P usando GPU"""
    
    def __init__(self, gpu_manager: GPUManager):
        self.gpu_manager = gpu_manager
        self.visualization_data = []
    
    def generate_network_layout(self, num_nodes, connection_matrix=None):
        """Gera layout visual da rede"""
        if not GPU_AVAILABLE:
            # Simulação sem GPU
            positions = []
            for i in range(num_nodes):
                import random
                positions.append([random.random(), random.random()])
            return positions
        
        # Layout usando GPU
        def compute_layout():
            # Posições aleatórias iniciais
            positions = torch.rand((num_nodes, 2), device=self.gpu_manager.device)
            
            if connection_matrix is not None:
                # Força-direcionada simples usando conexões
                for iteration in range(10):  # 10 iterações de otimização
                    forces = torch.zeros_like(positions)
                    
                    # Calcula forças entre nós conectados
                    for i in range(min(num_nodes, connection_matrix.shape[0])):
                        for j in range(min(num_nodes, connection_matrix.shape[1])):
                            if connection_matrix[i][j] > 0 and i != j:
                                diff = positions[j] - positions[i]
                                distance = torch.norm(diff) + 1e-6
                                force = diff / distance * 0.01
                                forces[i] += force
                    
                    positions += forces * 0.1  # Taxa de aprendizado
                    
                    # Mantém dentro dos limites [0,1]
                    positions = torch.clamp(positions, 0, 1)
            
            return positions.cpu().numpy().tolist()
        
        result = self.gpu_manager.monitor_computation(compute_layout)
        
        if result and result["result"]:
            self.visualization_data.append({
                "timestamp": datetime.now().isoformat(),
                "num_nodes": num_nodes,
                "positions": result["result"],
                "computation_time": result["computation_time"]
            })
            return result["result"]
        
        return []
    
    def create_network_snapshot(self, nodes_info, connections):
        """Cria snapshot visual da rede"""
        snapshot = {
            "timestamp": datetime.now().isoformat(),
            "total_nodes": len(nodes_info),
            "total_connections": len(connections),
            "nodes": [],
            "edges": []
        }
        
        # Gera layout
        positions = self.generate_network_layout(len(nodes_info))
        
        # Adiciona nós
        for i, node in enumerate(nodes_info):
            node_data = {
                "id": node.get("node_id", f"node_{i}"),
                "position": positions[i] if i < len(positions) else [0.5, 0.5],
                "status": node.get("status", "active"),
                "peers_count": node.get("peers_count", 0),
                "ai_confidence": node.get("ai_confidence", 0.5)
            }
            snapshot["nodes"].append(node_data)
        
        # Adiciona conexões
        for connection in connections:
            edge_data = {
                "source": connection.get("source"),
                "target": connection.get("target"),
                "strength": connection.get("strength", 1.0),
                "type": connection.get("type", "peer")
            }
            snapshot["edges"].append(edge_data)
        
        return snapshot
    
    def export_visualization_data(self):
        """Exporta dados de visualização"""
        return {
            "total_snapshots": len(self.visualization_data),
            "visualization_history": self.visualization_data,
            "gpu_stats": self.gpu_manager.get_stats()
        }

class PerformanceProfiler:
    """Profiler de performance para operações GPU"""
    
    def __init__(self):
        self.profiles = []
    
    def profile_operation(self, operation_name, func, *args, **kwargs):
        """Perfila uma operação específica"""
        start_time = time.time()
        
        if GPU_AVAILABLE:
            start_memory = torch.cuda.memory_allocated()
            torch.cuda.synchronize()  # Sincroniza GPU
        
        try:
            result = func(*args, **kwargs)
            success = True
            error = None
        except Exception as e:
            result = None
            success = False
            error = str(e)
        
        if GPU_AVAILABLE:
            torch.cuda.synchronize()  # Sincroniza GPU
            end_memory = torch.cuda.memory_allocated()
            memory_delta = (end_memory - start_memory) / 1024**2
        else:
            memory_delta = 0
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        profile_data = {
            "operation": operation_name,
            "timestamp": datetime.now().isoformat(),
            "execution_time": execution_time,
            "memory_delta": memory_delta,
            "success": success,
            "error": error,
            "gpu_available": GPU_AVAILABLE
        }
        
        self.profiles.append(profile_data)
        return {"profile": profile_data, "result": result}
    
    def get_performance_summary(self):
        """Retorna resumo de performance"""
        if not self.profiles:
            return {"no_data": True}
        
        successful_ops = [p for p in self.profiles if p["success"]]
        failed_ops = [p for p in self.profiles if not p["success"]]
        
        summary = {
            "total_operations": len(self.profiles),
            "successful_operations": len(successful_ops),
            "failed_operations": len(failed_ops),
            "success_rate": len(successful_ops) / len(self.profiles) * 100
        }
        
        if successful_ops:
            execution_times = [op["execution_time"] for op in successful_ops]
            memory_deltas = [op["memory_delta"] for op in successful_ops]
            
            summary["performance_stats"] = {
                "avg_execution_time": sum(execution_times) / len(execution_times),
                "min_execution_time": min(execution_times),
                "max_execution_time": max(execution_times),
                "avg_memory_delta": sum(memory_deltas) / len(memory_deltas),
                "peak_memory_delta": max(memory_deltas)
            }
        
        # Agrupa por operação
        operations = {}
        for profile in self.profiles:
            op_name = profile["operation"]
            if op_name not in operations:
                operations[op_name] = []
            operations[op_name].append(profile)
        
        summary["operations_breakdown"] = {}
        for op_name, ops in operations.items():
            successful = [op for op in ops if op["success"]]
            summary["operations_breakdown"][op_name] = {
                "total_calls": len(ops),
                "successful_calls": len(successful),
                "success_rate": len(successful) / len(ops) * 100 if ops else 0
            }
            
            if successful:
                times = [op["execution_time"] for op in successful]
                summary["operations_breakdown"][op_name]["avg_time"] = sum(times) / len(times)
        
        return summary

def test_gpu_utils():
    """Teste das utilidades GPU"""
    print("🛠️ Testando GPU Utilities...")
    
    # Testa GPU Manager
    gpu_manager = GPUManager()
    print(f"📊 GPU Info: {gpu_manager.get_memory_info()}")
    
    # Testa Performance Profiler
    profiler = PerformanceProfiler()
    
    def dummy_computation():
        if GPU_AVAILABLE:
            return torch.rand(1000, 1000, device=gpu_manager.device).sum()
        else:
            import random
            return sum(random.random() for _ in range(1000))
    
    # Perfila operação
    result = profiler.profile_operation("dummy_computation", dummy_computation)
    print(f"📈 Profile resultado: {result['profile']}")
    
    # Testa Visualizer
    visualizer = NetworkVisualizer(gpu_manager)
    positions = visualizer.generate_network_layout(100)
    print(f"🎨 Geradas {len(positions)} posições para visualização")
    
    # Resumo final
    stats = gpu_manager.get_stats()
    performance = profiler.get_performance_summary()
    
    print(f"📊 GPU Manager Stats: {json.dumps(stats, indent=2)}")
    print(f"⚡ Performance Summary: {json.dumps(performance, indent=2)}")

if __name__ == "__main__":
    test_gpu_utils()
