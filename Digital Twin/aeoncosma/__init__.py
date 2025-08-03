"""
🚀 AEONCOSMA ENGINE v1.0
Plataforma modular integrando IA, Blockchain, P2P, Quantum e Cosmologia
Copyright 2025 - Luiz H. P. Cruz

Módulos:
- 🧠 IA: Simbólica e Neural
- 🔗 Blockchain: Sistema VERITAS
- 🌐 P2P: Rede descentralizada
- 📡 Quantum: Comunicação quântica simulada
- 📊 Cosmos: Análises cosmológicas com dados reais
"""

__version__ = "1.0.0"
__author__ = "Luiz H. P. Cruz"
__email__ = "luiz@aeon.energy.br"
__license__ = "MIT"

from .core.engine import AeonCosmaEngine
from .crypto.crypto_engine import CryptoEngine
from .p2p.p2p_node import P2PNode
from .quantum.quantum_channel import QuantumChannel
from .cosmos.cosmos_fitter import CosmosFitter

__all__ = [
    'AeonCosmaEngine',
    'CryptoEngine', 
    'P2PNode',
    'QuantumChannel',
    'CosmosFitter'
]

def get_engine():
    """Factory function para criar instância do engine principal"""
    return AeonCosmaEngine()

# Verificação de dependências críticas
try:
    import numpy
    import scipy
    import emcee
    import fastapi
    import streamlit
    import cryptography
except ImportError as e:
    raise ImportError(f"Dependência crítica não encontrada: {e}")

print("🚀 AEONCOSMA Engine v1.0 - Inicializado com sucesso!")
print("💎 Copyright 2025 - Luiz H. P. Cruz")
