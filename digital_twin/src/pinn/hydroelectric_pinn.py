# -*- coding: utf-8 -*-
"""
Physics-Informed Neural Networks (PINNs) para Digital Twin de Hidrelétricas - Projeto AEON.

Este módulo implementa PINNs para modelagem física de turbinas hidrelétricas,
integrando equações diferenciais da mecânica dos fluidos com aprendizado de máquina.

PRIORIDADE: CRÍTICA
Integração: Digital Twin + Análise Bayesiana + PINNs
"""

import torch
import torch.nn as nn
import torch.autograd as autograd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import logging
import sys
from typing import Tuple, Dict, Optional
import pickle
from datetime import datetime

# Adicionar path do projeto para importar módulos AEON
current_dir = Path(__file__).parent.parent.parent
sys.path.append(str(current_dir))

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class HydroelectricPINN(nn.Module):
    """
    Physics-Informed Neural Network para modelagem de turbinas hidrelétricas.
    
    Variáveis:
    - t: tempo
    - g: gradiente hidráulico (diferença de altura)
    - Q: vazão da água
    - V: vibração/deslocamento da turbina (saída)
    
    Física integrada:
    - Equação de movimento: m*d²V/dt² + c*dV/dt + k*V = F(g, Q)
    - Conservação de energia
    - Dinâmica de fluidos
    """
    
    def __init__(self, layers: list, device: str = 'cpu'):
        """
        Inicializa a PINN.
        
        Args:
            layers: Lista com número de neurônios por camada [input, hidden1, hidden2, ..., output]
            device: 'cpu' ou 'cuda'
        """
        super(HydroelectricPINN, self).__init__()
        self.device = device
        self.layers = layers
        self.model = self.build_model(layers).to(device)
        
        # Parâmetros físicos aprendíveis (podem ser ajustados durante treinamento)
        self.m = nn.Parameter(torch.tensor(1000.0))  # massa efetiva (kg)
        self.c = nn.Parameter(torch.tensor(50.0))    # amortecimento (N⋅s/m)
        self.k = nn.Parameter(torch.tensor(1e5))     # rigidez (N/m)
        
        logging.info(f"PINN inicializada com arquitetura: {layers}")
        logging.info(f"Dispositivo: {device}")

    def build_model(self, layers: list) -> nn.Sequential:
        """Constrói a arquitetura da rede neural."""
        net = []
        for i in range(len(layers) - 1):
            net.append(nn.Linear(layers[i], layers[i+1]))
            if i < len(layers) - 2:
                net.append(nn.Tanh())  # Função de ativação
        return nn.Sequential(*net)

    def forward(self, t: torch.Tensor, g: torch.Tensor, Q: torch.Tensor) -> torch.Tensor:
        """
        Forward pass da rede.
        
        Args:
            t: tempo
            g: gradiente hidráulico
            Q: vazão
            
        Returns:
            V: vibração/deslocamento predito
        """
        x = torch.cat([t, g, Q], dim=1)
        return self.model(x)

    def physics_loss(self, t: torch.Tensor, g: torch.Tensor, Q: torch.Tensor) -> torch.Tensor:
        """
        Calcula a perda baseada nas leis físicas.
        
        Implementa a equação de movimento:
        m * d²V/dt² + c * dV/dt + k * V = F(g, Q)
        """
        # Habilitar gradientes para cálculo das derivadas
        t.requires_grad = True
        g.requires_grad = True
        Q.requires_grad = True
        
        # Predição da rede
        V = self.forward(t, g, Q)
        
        # Primeira derivada: dV/dt
        dV_dt = autograd.grad(
            V, t, 
            grad_outputs=torch.ones_like(V), 
            create_graph=True,
            retain_graph=True
        )[0]
        
        # Segunda derivada: d²V/dt²
        d2V_dt2 = autograd.grad(
            dV_dt, t, 
            grad_outputs=torch.ones_like(dV_dt), 
            create_graph=True,
            retain_graph=True
        )[0]
        
        # Força externa baseada na física de hidrelétricas
        # F = α * g * Q² (força proporcional ao quadrado da vazão e gradiente)
        alpha = 0.1  # coeficiente de acoplamento
        F = alpha * g * Q**2
        
        # Equação de movimento
        residual = self.m * d2V_dt2 + self.c * dV_dt + self.k * V - F
        
        # Perda quadrática média
        physics_loss = torch.mean(residual**2)
        
        return physics_loss

    def data_loss(self, t_data: torch.Tensor, g_data: torch.Tensor, 
                  Q_data: torch.Tensor, V_data: torch.Tensor) -> torch.Tensor:
        """
        Calcula a perda baseada nos dados observados.
        """
        V_pred = self.forward(t_data, g_data, Q_data)
        return torch.mean((V_pred - V_data)**2)

    def boundary_loss(self, t_boundary: torch.Tensor, g_boundary: torch.Tensor, 
                     Q_boundary: torch.Tensor) -> torch.Tensor:
        """
        Implementa condições de contorno físicas.
        """
        # Condição: no tempo inicial (t=0), vibração deve ser zero
        V_initial = self.forward(t_boundary, g_boundary, Q_boundary)
        return torch.mean(V_initial**2)

    def conservation_loss(self, t: torch.Tensor, g: torch.Tensor, Q: torch.Tensor) -> torch.Tensor:
        """
        Implementa conservação de energia.
        """
        t.requires_grad = True
        V = self.forward(t, g, Q)
        
        dV_dt = autograd.grad(
            V, t, 
            grad_outputs=torch.ones_like(V), 
            create_graph=True,
            retain_graph=True
        )[0]
        
        # Energia cinética + potencial deve variar suavemente
        kinetic_energy = 0.5 * self.m * dV_dt**2
        potential_energy = 0.5 * self.k * V**2
        total_energy = kinetic_energy + potential_energy
        
        # Penalizar variações bruscas de energia
        energy_variation = torch.std(total_energy)
        return energy_variation

    def total_loss(self, t_data: torch.Tensor, g_data: torch.Tensor, Q_data: torch.Tensor, V_data: torch.Tensor,
                   t_phys: torch.Tensor, g_phys: torch.Tensor, Q_phys: torch.Tensor,
                   t_boundary: torch.Tensor, g_boundary: torch.Tensor, Q_boundary: torch.Tensor,
                   lambda_data: float = 1.0, lambda_physics: float = 1.0, 
                   lambda_boundary: float = 0.1, lambda_conservation: float = 0.1) -> Dict[str, torch.Tensor]:
        """
        Calcula a perda total combinando todas as componentes.
        
        Returns:
            Dict com todas as perdas individuais e total
        """
        loss_data = self.data_loss(t_data, g_data, Q_data, V_data)
        loss_physics = self.physics_loss(t_phys, g_phys, Q_phys)
        loss_boundary = self.boundary_loss(t_boundary, g_boundary, Q_boundary)
        loss_conservation = self.conservation_loss(t_phys, g_phys, Q_phys)
        
        total_loss = (lambda_data * loss_data + 
                     lambda_physics * loss_physics + 
                     lambda_boundary * loss_boundary + 
                     lambda_conservation * loss_conservation)
        
        return {
            'total': total_loss,
            'data': loss_data,
            'physics': loss_physics,
            'boundary': loss_boundary,
            'conservation': loss_conservation
        }

class HydroelectricDigitalTwin:
    """
    Digital Twin completo integrando PINN com análise Bayesiana.
    """
    
    def __init__(self, pinn_layers: list = [3, 64, 64, 64, 1], device: str = 'cpu'):
        """
        Inicializa o Digital Twin.
        
        Args:
            pinn_layers: Arquitetura da PINN
            device: Dispositivo de computação
        """
        self.device = device
        self.pinn = HydroelectricPINN(pinn_layers, device)
        self.optimizer = torch.optim.Adam(self.pinn.parameters(), lr=0.001)
        self.scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(self.optimizer, patience=500)
        
        self.training_history = {
            'total_loss': [],
            'data_loss': [],
            'physics_loss': [],
            'boundary_loss': [],
            'conservation_loss': []
        }
        
        logging.info("Digital Twin inicializado com sucesso")

    def generate_synthetic_data(self, n_samples: int = 1000) -> Dict[str, torch.Tensor]:
        """
        Gera dados sintéticos para treinamento e teste.
        """
        logging.info(f"Gerando {n_samples} amostras sintéticas...")
        
        # Parâmetros de tempo
        t_max = 10.0  # 10 segundos
        t = torch.linspace(0, t_max, n_samples).reshape(-1, 1)
        
        # Gradiente hidráulico (varia entre 10-100 metros)
        g = 50 + 30 * torch.sin(0.5 * t) + 10 * torch.randn_like(t)
        g = torch.clamp(g, 10, 100)
        
        # Vazão (varia entre 100-500 m³/s)
        Q = 300 + 100 * torch.cos(0.3 * t) + 20 * torch.randn_like(t)
        Q = torch.clamp(Q, 100, 500)
        
        # Vibração "real" baseada em modelo físico simplificado
        m, c, k = 1000.0, 50.0, 1e5
        alpha = 0.1
        F = alpha * g * Q**2
        
        # Solução aproximada da EDO
        omega = torch.sqrt(k/m)
        gamma = c/(2*m)
        
        V = (F/k) * (1 - torch.exp(-gamma * t) * torch.cos(omega * t))
        V += 0.01 * torch.randn_like(V)  # Ruído
        
        return {
            't': t.to(self.device),
            'g': g.to(self.device),
            'Q': Q.to(self.device),
            'V': V.to(self.device)
        }

    def prepare_training_data(self, data: Dict[str, torch.Tensor], 
                            train_ratio: float = 0.8) -> Tuple[Dict, Dict, Dict]:
        """
        Prepara dados para treinamento, física e condições de contorno.
        """
        n_total = len(data['t'])
        n_train = int(train_ratio * n_total)
        n_physics = n_total  # Usar todos os pontos para física
        n_boundary = 50     # Pontos de contorno
        
        # Dados de treinamento (supervisionado)
        indices_train = torch.randperm(n_total)[:n_train]
        data_train = {
            't': data['t'][indices_train],
            'g': data['g'][indices_train],
            'Q': data['Q'][indices_train],
            'V': data['V'][indices_train]
        }
        
        # Pontos para física (podem ser diferentes dos dados)
        physics_data = {
            't': data['t'],
            'g': data['g'],
            'Q': data['Q']
        }
        
        # Condições de contorno (t=0)
        boundary_data = {
            't': torch.zeros(n_boundary, 1).to(self.device),
            'g': data['g'][:n_boundary],
            'Q': data['Q'][:n_boundary]
        }
        
        return data_train, physics_data, boundary_data

    def train(self, epochs: int = 5000, print_freq: int = 500):
        """
        Treina a PINN.
        """
        logging.info(f"Iniciando treinamento por {epochs} épocas...")
        
        # Gerar dados
        data = self.generate_synthetic_data(1000)
        data_train, physics_data, boundary_data = self.prepare_training_data(data)
        
        self.pinn.train()
        
        for epoch in range(epochs):
            self.optimizer.zero_grad()
            
            # Calcular perdas
            losses = self.pinn.total_loss(
                data_train['t'], data_train['g'], data_train['Q'], data_train['V'],
                physics_data['t'], physics_data['g'], physics_data['Q'],
                boundary_data['t'], boundary_data['g'], boundary_data['Q']
            )
            
            # Backpropagation
            losses['total'].backward()
            self.optimizer.step()
            self.scheduler.step(losses['total'])
            
            # Armazenar histórico
            for key, value in losses.items():
                self.training_history[key + '_loss'].append(value.item())
            
            # Print progresso
            if epoch % print_freq == 0:
                print(f"Época {epoch}/{epochs}:")
                print(f"  Perda Total: {losses['total'].item():.6f}")
                print(f"  Perda Dados: {losses['data'].item():.6f}")
                print(f"  Perda Física: {losses['physics'].item():.6f}")
                print(f"  Parâmetros: m={self.pinn.m.item():.2f}, c={self.pinn.c.item():.2f}, k={self.pinn.k.item():.0f}")
                print(f"  LR: {self.optimizer.param_groups[0]['lr']:.2e}")
                print("-" * 50)
        
        logging.info("Treinamento concluído!")

    def evaluate(self, test_data: Optional[Dict[str, torch.Tensor]] = None) -> Dict[str, float]:
        """
        Avalia o desempenho da PINN.
        """
        self.pinn.eval()
        
        if test_data is None:
            test_data = self.generate_synthetic_data(200)
        
        with torch.no_grad():
            V_pred = self.pinn.forward(test_data['t'], test_data['g'], test_data['Q'])
            mse = torch.mean((V_pred - test_data['V'])**2).item()
            mae = torch.mean(torch.abs(V_pred - test_data['V'])).item()
            r2 = 1 - mse / torch.var(test_data['V']).item()
        
        metrics = {
            'mse': mse,
            'mae': mae,
            'r2': r2,
            'rmse': np.sqrt(mse)
        }
        
        print("\n" + "="*50)
        print("📊 AVALIAÇÃO DA PINN - DIGITAL TWIN")
        print("="*50)
        print(f"MSE:  {metrics['mse']:.6f}")
        print(f"MAE:  {metrics['mae']:.6f}")
        print(f"RMSE: {metrics['rmse']:.6f}")
        print(f"R²:   {metrics['r2']:.6f}")
        print("="*50)
        
        return metrics

    def predict(self, t: torch.Tensor, g: torch.Tensor, Q: torch.Tensor) -> torch.Tensor:
        """
        Faz predições com a PINN treinada.
        """
        self.pinn.eval()
        with torch.no_grad():
            return self.pinn.forward(t, g, Q)

    def save_model(self, filepath: str):
        """
        Salva o modelo treinado.
        """
        torch.save({
            'model_state_dict': self.pinn.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'training_history': self.training_history,
            'layers': self.pinn.layers
        }, filepath)
        logging.info(f"Modelo salvo em: {filepath}")

    def load_model(self, filepath: str):
        """
        Carrega um modelo treinado.
        """
        checkpoint = torch.load(filepath, map_location=self.device)
        self.pinn.load_state_dict(checkpoint['model_state_dict'])
        self.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        self.training_history = checkpoint['training_history']
        logging.info(f"Modelo carregado de: {filepath}")

    def plot_results(self, save_path: str = "pinn_results.png"):
        """
        Gera gráficos dos resultados.
        """
        try:
            fig, axes = plt.subplots(2, 2, figsize=(15, 10))
            
            # 1. Histórico de treinamento
            axes[0, 0].plot(self.training_history['total_loss'], label='Total')
            axes[0, 0].plot(self.training_history['data_loss'], label='Dados')
            axes[0, 0].plot(self.training_history['physics_loss'], label='Física')
            axes[0, 0].set_yscale('log')
            axes[0, 0].set_xlabel('Época')
            axes[0, 0].set_ylabel('Perda')
            axes[0, 0].set_title('Histórico de Treinamento')
            axes[0, 0].legend()
            axes[0, 0].grid(True)
            
            # 2. Predições vs Real
            test_data = self.generate_synthetic_data(200)
            with torch.no_grad():
                V_pred = self.predict(test_data['t'], test_data['g'], test_data['Q'])
            
            axes[0, 1].scatter(test_data['V'].cpu(), V_pred.cpu(), alpha=0.6)
            axes[0, 1].plot([test_data['V'].min(), test_data['V'].max()], 
                           [test_data['V'].min(), test_data['V'].max()], 'r--')
            axes[0, 1].set_xlabel('Vibração Real')
            axes[0, 1].set_ylabel('Vibração Predita')
            axes[0, 1].set_title('Predições vs Real')
            axes[0, 1].grid(True)
            
            # 3. Série temporal
            t_plot = test_data['t'][:100].cpu()
            V_real = test_data['V'][:100].cpu()
            V_pred_plot = V_pred[:100].cpu()
            
            axes[1, 0].plot(t_plot, V_real, 'b-', label='Real', linewidth=2)
            axes[1, 0].plot(t_plot, V_pred_plot, 'r--', label='PINN', linewidth=2)
            axes[1, 0].set_xlabel('Tempo (s)')
            axes[1, 0].set_ylabel('Vibração')
            axes[1, 0].set_title('Série Temporal')
            axes[1, 0].legend()
            axes[1, 0].grid(True)
            
            # 4. Parâmetros físicos aprendidos
            params = {
                'Massa (kg)': self.pinn.m.item(),
                'Amortecimento (N⋅s/m)': self.pinn.c.item(),
                'Rigidez (N/m)': self.pinn.k.item()
            }
            
            axes[1, 1].bar(params.keys(), params.values())
            axes[1, 1].set_title('Parâmetros Físicos Aprendidos')
            axes[1, 1].tick_params(axis='x', rotation=45)
            
            plt.tight_layout()
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            plt.close()
            logging.info(f"Gráficos salvos em: {save_path}")
            
        except Exception as e:
            logging.warning(f"Erro ao gerar gráficos: {e}")


# --- Funções de conveniência ---
def train_pinn_model(epochs: int = 5000, device: str = 'cpu') -> HydroelectricDigitalTwin:
    """
    Função de conveniência para treinar um modelo PINN.
    """
    print("🚀 AEON - Physics-Informed Neural Networks para Digital Twin")
    print("=" * 60)
    
    # Detectar CUDA se disponível
    if device == 'auto':
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
    
    print(f"🖥️  Dispositivo: {device}")
    print(f"⚙️  Épocas: {epochs}")
    
    # Criar e treinar modelo
    digital_twin = HydroelectricDigitalTwin(device=device)
    digital_twin.train(epochs=epochs)
    
    # Avaliar
    metrics = digital_twin.evaluate()
    
    # Salvar modelo
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    model_path = f"hydroelectric_pinn_{timestamp}.pth"
    digital_twin.save_model(model_path)
    
    # Gerar gráficos
    digital_twin.plot_results(f"pinn_results_{timestamp}.png")
    
    print(f"\n✅ Modelo treinado e salvo em: {model_path}")
    
    return digital_twin


# --- Bloco de execução principal ---
if __name__ == '__main__':
    logging.info("--- Iniciando PINN para Digital Twin Hidrelétrico ---")
    
    try:
        # Treinar modelo
        digital_twin = train_pinn_model(epochs=3000, device='auto')
        
        print("\n🎯 INTEGRAÇÃO COM ANÁLISE BAYESIANA:")
        print("   • Use os parâmetros físicos aprendidos (m, c, k) como priors")
        print("   • Combine predições PINN com incerteza Bayesiana")
        print("   • Digital Twin completo: PINN + MCMC + Dados reais")
        
        print("\n📁 Arquivos gerados:")
        print("   • Modelo PINN salvo (.pth)")
        print("   • Gráficos de resultados (.png)")
        print("   • Logs de treinamento")
        
    except Exception as e:
        logging.error(f"Erro durante execução: {e}")
        print(f"❌ Erro: {e}")
    
    logging.info("--- PINN Digital Twin finalizado ---")
