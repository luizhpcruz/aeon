# aeoncosma/gpu/node_brain.py
"""
🧠 AEONCOSMA Node Brain - IA Neural para Decisões P2P
Rede neural leve para cada nó P2P com decisões autônomas
Desenvolvido por Luiz Cruz - 2025
"""

try:
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
    import numpy as np
    TORCH_AVAILABLE = True
except ImportError:
    print("⚠️ PyTorch não disponível - usando simulação")
    TORCH_AVAILABLE = False
    
    # Fallback para numpy se disponível
    try:
        import numpy as np
        NUMPY_AVAILABLE = True
    except ImportError:
        NUMPY_AVAILABLE = False
    
    # Mock classes para compatibilidade
    class nn:
        class Module:
            def __init__(self):
                pass
            def parameters(self):
                return []
            def named_parameters(self):
                return []
            def state_dict(self):
                return {}
            def load_state_dict(self, state_dict):
                pass
            def zero_grad(self):
                pass
        
        class Linear:
            def __init__(self, *args, **kwargs):
                pass
        
        class ReLU:
            def __init__(self):
                pass
        
        class Dropout:
            def __init__(self, *args):
                pass
        
        class Sigmoid:
            def __init__(self):
                pass
        
        @staticmethod
        def init():
            class Init:
                @staticmethod
                def xavier_uniform_(tensor):
                    pass
            return Init()
        
        init = init()
    
    # Mock torch
    class torch:
        @staticmethod
        def tensor(data):
            if NUMPY_AVAILABLE:
                return np.array(data)
            else:
                return data
        
        @staticmethod
        def zeros(size):
            if NUMPY_AVAILABLE:
                if isinstance(size, int):
                    return np.zeros(size)
                else:
                    return np.zeros(size)
            else:
                return [0.0] * size
        
        @staticmethod
        def cat(tensors):
            if NUMPY_AVAILABLE:
                return np.concatenate(tensors)
            else:
                result = []
                for t in tensors:
                    if isinstance(t, list):
                        result.extend(t)
                    else:
                        result.append(t)
                return result

class NodeBrain(nn.Module):
    """
    Rede neural leve para decisões do nó P2P
    Entrada: 7 features (peer info + network state)
    Saída: 1 valor [0,1] (probabilidade de aceitar peer)
    """
    
    def __init__(self, input_size=7, hidden_size=16, dropout=0.2):
        if TORCH_AVAILABLE:
            super(NodeBrain, self).__init__()
        
        self.input_size = input_size
        self.hidden_size = hidden_size
        
        if TORCH_AVAILABLE:
            # Camadas da rede neural
            self.fc1 = nn.Linear(input_size, hidden_size)
            self.fc2 = nn.Linear(hidden_size, hidden_size // 2)
            self.fc3 = nn.Linear(hidden_size // 2, 1)
            
            self.dropout = nn.Dropout(dropout)
            self.activation = nn.ReLU()
            self.output_activation = nn.Sigmoid()
            
            # Inicialização Xavier
            nn.init.xavier_uniform_(self.fc1.weight)
            nn.init.xavier_uniform_(self.fc2.weight)
            nn.init.xavier_uniform_(self.fc3.weight)
        else:
            # Simulação sem PyTorch
            self.fc1 = nn.Linear()
            self.fc2 = nn.Linear()
            self.fc3 = nn.Linear()
            self.dropout = nn.Dropout()
            self.activation = nn.ReLU()
            self.output_activation = nn.Sigmoid()
        
        # Estatísticas da rede
        self.decision_count = 0
        self.acceptance_rate = 0.0
        
    def forward(self, x):
        """Forward pass da rede neural"""
        if not TORCH_AVAILABLE:
            # Simulação simples sem PyTorch
            return torch.tensor([0.5])
        
        x = self.activation(self.fc1(x))
        x = self.dropout(x)
        x = self.activation(self.fc2(x))
        x = self.dropout(x)
        x = self.output_activation(self.fc3(x))
        
        return x
    
    def make_decision(self, peer_features, network_state=None):
        """
        Toma decisão sobre aceitar/rejeitar peer
        
        Args:
            peer_features: Tensor/lista com características do peer
            network_state: Estado atual da rede (opcional)
        
        Returns:
            dict: {"decision": bool, "confidence": float, "reasoning": str}
        """
        if not TORCH_AVAILABLE:
            # Fallback sem PyTorch usando lógica simples
            if NUMPY_AVAILABLE:
                try:
                    if isinstance(peer_features, list):
                        features_array = np.array(peer_features)
                    else:
                        features_array = peer_features
                    
                    # Simula rede neural com soma ponderada simples
                    weights = np.array([0.2, 0.15, 0.25, 0.2, 0.1, 0.05, 0.05])[:len(features_array)]
                    confidence = np.sum(features_array * weights)
                    confidence = 1 / (1 + np.exp(-confidence))  # Sigmoid
                    
                except:
                    confidence = 0.5
            else:
                # Fallback simples sem numpy
                if isinstance(peer_features, list) and len(peer_features) > 0:
                    confidence = sum(peer_features) / len(peer_features)
                else:
                    confidence = 0.5
            
            # Adiciona um pouco de aleatoriedade
            import random
            confidence = confidence * 0.8 + random.random() * 0.2
            
            decision = confidence > 0.5
            
            self.decision_count += 1
            if decision:
                self.acceptance_rate = (self.acceptance_rate * (self.decision_count - 1) + 1) / self.decision_count
            else:
                self.acceptance_rate = (self.acceptance_rate * (self.decision_count - 1)) / self.decision_count
            
            # Gera reasoning baseado na confiança
            if confidence > 0.8:
                reasoning = "High confidence acceptance (simulated neural network)"
            elif confidence > 0.6:
                reasoning = "Moderate confidence acceptance (simulated)"
            elif confidence > 0.4:
                reasoning = "Low confidence rejection (simulated)"
            else:
                reasoning = "High confidence rejection (simulated)"
            
            return {
                "decision": decision,
                "confidence": float(confidence),
                "reasoning": reasoning,
                "network_stats": {
                    "total_decisions": self.decision_count,
                    "acceptance_rate": self.acceptance_rate
                },
                "simulation_mode": True
            }
        
        # Código PyTorch original
        with torch.no_grad():
            # Combina features do peer com estado da rede
            if network_state is not None:
                combined_input = torch.cat([peer_features, network_state])
            else:
                # Padding se não tiver network_state
                padding_size = self.input_size - peer_features.size(0)
                if padding_size > 0:
                    padding = torch.zeros(padding_size, device=peer_features.device)
                    combined_input = torch.cat([peer_features, padding])
                else:
                    combined_input = peer_features[:self.input_size]
            
            # Garante que tem o tamanho correto
            if combined_input.size(0) != self.input_size:
                combined_input = combined_input[:self.input_size]
                if combined_input.size(0) < self.input_size:
                    padding = torch.zeros(self.input_size - combined_input.size(0), 
                                        device=combined_input.device)
                    combined_input = torch.cat([combined_input, padding])
            
            # Adiciona dimensão de batch se necessário
            if combined_input.dim() == 1:
                combined_input = combined_input.unsqueeze(0)
            
            # Executa rede neural
            confidence = self.forward(combined_input).item()
            decision = confidence > 0.5
            
            # Atualiza estatísticas
            self.decision_count += 1
            if decision:
                self.acceptance_rate = (self.acceptance_rate * (self.decision_count - 1) + 1) / self.decision_count
            else:
                self.acceptance_rate = (self.acceptance_rate * (self.decision_count - 1)) / self.decision_count
            
            # Gera reasoning baseado na confiança
            if confidence > 0.8:
                reasoning = "High confidence acceptance - strong peer signals"
            elif confidence > 0.6:
                reasoning = "Moderate confidence acceptance - good peer profile"
            elif confidence > 0.4:
                reasoning = "Low confidence rejection - weak peer signals"
            else:
                reasoning = "High confidence rejection - poor peer profile"
            
            return {
                "decision": decision,
                "confidence": confidence,
                "reasoning": reasoning,
                "network_stats": {
                    "total_decisions": self.decision_count,
                    "acceptance_rate": self.acceptance_rate
                },
                "simulation_mode": False
            }
    
    def learn_from_feedback(self, peer_features, network_state, actual_outcome, learning_rate=0.001):
        """
        Aprendizado online baseado em feedback
        
        Args:
            peer_features: Features do peer que foi avaliado
            network_state: Estado da rede quando a decisão foi tomada
            actual_outcome: Resultado real (True = peer foi bom, False = peer foi ruim)
            learning_rate: Taxa de aprendizado
        """
        if not TORCH_AVAILABLE:
            return
        
        # Prepara input
        if network_state is not None:
            combined_input = torch.cat([peer_features, network_state])
        else:
            padding_size = self.input_size - peer_features.size(0)
            if padding_size > 0:
                padding = torch.zeros(padding_size, device=peer_features.device)
                combined_input = torch.cat([peer_features, padding])
            else:
                combined_input = peer_features[:self.input_size]
        
        if combined_input.dim() == 1:
            combined_input = combined_input.unsqueeze(0)
        
        # Target baseado no outcome real
        target = torch.tensor([[1.0 if actual_outcome else 0.0]], 
                            device=combined_input.device)
        
        # Forward pass
        prediction = self.forward(combined_input)
        
        # Calcula loss
        loss = F.binary_cross_entropy(prediction, target)
        
        # Backward pass simplificado (gradiente manual)
        self.zero_grad()
        loss.backward()
        
        # Atualiza pesos manualmente
        with torch.no_grad():
            for param in self.parameters():
                if param.grad is not None:
                    param -= learning_rate * param.grad
    
    def get_brain_stats(self):
        """Retorna estatísticas do cérebro do nó"""
        stats = {
            "total_decisions": self.decision_count,
            "acceptance_rate": self.acceptance_rate,
            "torch_available": TORCH_AVAILABLE,
            "model_parameters": sum(p.numel() for p in self.parameters()) if TORCH_AVAILABLE else 0
        }
        
        if TORCH_AVAILABLE:
            # Adiciona informações dos pesos
            stats["weight_stats"] = {}
            for name, param in self.named_parameters():
                stats["weight_stats"][name] = {
                    "mean": param.data.mean().item(),
                    "std": param.data.std().item(),
                    "min": param.data.min().item(),
                    "max": param.data.max().item()
                }
        
        return stats
    
    def save_brain(self, filepath):
        """Salva o estado do cérebro"""
        if not TORCH_AVAILABLE:
            return False
        
        try:
            torch.save({
                'model_state_dict': self.state_dict(),
                'decision_count': self.decision_count,
                'acceptance_rate': self.acceptance_rate,
                'input_size': self.input_size,
                'hidden_size': self.hidden_size
            }, filepath)
            return True
        except Exception as e:
            print(f"❌ Erro ao salvar cérebro: {e}")
            return False
    
    def load_brain(self, filepath):
        """Carrega o estado do cérebro"""
        if not TORCH_AVAILABLE:
            return False
        
        try:
            checkpoint = torch.load(filepath)
            self.load_state_dict(checkpoint['model_state_dict'])
            self.decision_count = checkpoint.get('decision_count', 0)
            self.acceptance_rate = checkpoint.get('acceptance_rate', 0.0)
            return True
        except Exception as e:
            print(f"❌ Erro ao carregar cérebro: {e}")
            return False

class CollectiveIntelligence:
    """
    Inteligência coletiva da rede - combina decisões de múltiplos nós
    """
    
    def __init__(self):
        self.node_brains = {}
        self.collective_decisions = []
        
    def add_node_brain(self, node_id, brain):
        """Adiciona cérebro de um nó à inteligência coletiva"""
        self.node_brains[node_id] = brain
        
    def collective_decision(self, peer_features, network_state=None):
        """
        Decisão coletiva baseada em múltiplos cérebros
        
        Returns:
            dict: Decisão coletiva com consenso
        """
        if not self.node_brains:
            return {"decision": False, "confidence": 0.0, "consensus": 0.0}
        
        decisions = []
        confidences = []
        
        for node_id, brain in self.node_brains.items():
            result = brain.make_decision(peer_features, network_state)
            decisions.append(result["decision"])
            confidences.append(result["confidence"])
        
        # Calcula consenso
        acceptance_votes = sum(decisions)
        total_votes = len(decisions)
        consensus_ratio = acceptance_votes / total_votes
        
        # Decisão coletiva (maioria simples)
        collective_decision = consensus_ratio > 0.5
        average_confidence = sum(confidences) / len(confidences)
        
        result = {
            "decision": collective_decision,
            "confidence": average_confidence,
            "consensus": consensus_ratio,
            "individual_votes": {
                node_id: {"decision": decisions[i], "confidence": confidences[i]}
                for i, node_id in enumerate(self.node_brains.keys())
            },
            "total_nodes": total_votes
        }
        
        self.collective_decisions.append(result)
        return result
    
    def get_collective_stats(self):
        """Estatísticas da inteligência coletiva"""
        if not self.collective_decisions:
            return {"total_decisions": 0}
        
        total_decisions = len(self.collective_decisions)
        acceptances = sum(1 for d in self.collective_decisions if d["decision"])
        
        avg_consensus = sum(d["consensus"] for d in self.collective_decisions) / total_decisions
        avg_confidence = sum(d["confidence"] for d in self.collective_decisions) / total_decisions
        
        return {
            "total_decisions": total_decisions,
            "acceptance_rate": acceptances / total_decisions,
            "average_consensus": avg_consensus,
            "average_confidence": avg_confidence,
            "active_brains": len(self.node_brains)
        }

def test_node_brain():
    """Teste básico do NodeBrain"""
    print("🧠 Testando NodeBrain...")
    
    brain = NodeBrain()
    
    # Cria features fictícias de um peer
    if TORCH_AVAILABLE:
        peer_features = torch.rand(5)  # 5 features do peer
        network_state = torch.rand(2)  # 2 features do estado da rede
    else:
        peer_features = [0.5, 0.3, 0.8, 0.1, 0.9]
        network_state = [0.6, 0.4]
    
    # Testa decisão
    decision_result = brain.make_decision(peer_features, network_state)
    print(f"📊 Resultado da decisão: {decision_result}")
    
    # Testa estatísticas
    stats = brain.get_brain_stats()
    print(f"📈 Estatísticas do cérebro: {stats}")
    
    return brain

if __name__ == "__main__":
    test_node_brain()
