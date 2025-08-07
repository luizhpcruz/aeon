"""
Módulo Bayesian do Projeto AEON
===============================

Este módulo contém implementações de análise Bayesiana real para o sistema AEON,
substituindo simulações por modelos probabilísticos robustos usando PyMC.

Módulos:
- mcmc_real.py: Análise MCMC real para dados de entropia e cosmologia
- bnn.py: Bayesian Neural Networks (a ser implementado)
- hierarchical.py: Modelos hierárquicos (a ser implementado)
"""

from .mcmc_real import BayesianEntropyAnalyzer, BayesianCosmologyAnalyzer

__version__ = "1.0.0"
__author__ = "AEON Project Team"

__all__ = [
    "BayesianEntropyAnalyzer",
    "BayesianCosmologyAnalyzer"
]
