"""
AEON Evolution - Sistema de Simulação Evolutiva
===============================================

Implementação da Equação AEON para simulação de cadeias evolutivas.
Desenvolvido por Luiz Cruz - 2025
"""

from .engine import AeonEngine
from .simulator import AeonSimulator
from .dynamics import ChainDynamics

__version__ = "1.0.0"
__author__ = "Luiz Cruz"

__all__ = [
    "AeonEngine",
    "AeonSimulator", 
    "ChainDynamics"
]
