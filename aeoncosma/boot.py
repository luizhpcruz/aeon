import os
import sys
from .core.aeon_entity import AeonEntity
from .core.symbolic_engine import SymbolicEngine
from .core.memory_core import MemoryCore
from .core.logic_layer import LogicLayer

# Inicialização do sistema
if __name__ == "__main__":
    print("🔮 Iniciando AeonCosma...")
    npc = AeonEntity(name="Guardian Sigma")
    intent = {
        "query": "Qual é sua missão?",
        "symbols": ["qua", "le", "su", "mi", "ssã", "o"],
        "weight": 1.2
    }
    print(npc.respond(intent))
