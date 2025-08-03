import pytest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from aeon_kernel.kernel import AEONKernel, SymbolNet

def test_symbol_net():
    net = SymbolNet()
    net.refine("test", 1.0)
    assert "test" in net.nodes
    assert net.network_strength() > 0

def test_evolve():
    kernel = AEONKernel()
    result = kernel.evolve(1.0, 0.5, 0.2, 0.1, 0.05)
    assert result > 1.0
    assert kernel.symbol_net.network_strength() > 0

def test_kernel_parameters():
    kernel = AEONKernel(alpha=2.0, beta=1.0, gamma=0.5, delta=0.2)
    assert kernel.alpha == 2.0
    assert kernel.beta == 1.0
