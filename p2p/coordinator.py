from __future__ import annotations
import json
import asyncio
from pathlib import Path
from typing import Dict
from .node import Node

class Coordinator:
    """Centraliza outputs e dá feedback resumido.
    - Agrega resultados por módulo
    - Persiste um resumo em logs/p2p_summary.json
    - Persiste arquivos específicos quando útil (ex.: logs/p2p_entropy_result.json)
    - Imprime uma linha compacta por resultado recebido
    """

    def __init__(self) -> None:
        self.results: Dict[str, dict] = {}
        self.logs_dir = Path("logs")
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        self.summary_path = self.logs_dir / "p2p_summary.json"

    def wire(self, nodes: Dict[str, Node], coord_name: str = "coordenador") -> None:
        nodes[coord_name].on("result:entropy", self._on_result_entropy)
        nodes[coord_name].on("result:cosmologia", self._on_result_cosmologia)
        nodes[coord_name].on("result:verna", self._on_result_verna)
        nodes[coord_name].on("result:cosma", self._on_result_cosma)

    def _write_summary(self) -> None:
        self.summary_path.write_text(
            json.dumps(self.results, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    async def _on_result_entropy(self, msg):
        # Armazena e persiste o resultado específico
        self.results["entropy"] = msg.payload
        (self.logs_dir / "p2p_entropy_result.json").write_text(
            json.dumps(msg.payload, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        # Atualiza resumo geral
        self._write_summary()
        # Feedback curto
        p = msg.payload
        if p.get("ok"):
            try:
                print(
                    f"[coord] entropy ok | fitas={p['n_fitas']} ciclos={p['n_ciclos']} "
                    f"H̄={p['entropia_media']:.4f} C̄={p['complexidade_media']:.4f} Hmax={p['entropia_max']:.4f}"
                )
            except Exception:
                print("[coord] entropy ok")
        else:
            print("[coord] entropy erro")
        # pequena rendição ao loop (estabilidade)
        await asyncio.sleep(0)

    async def _on_result_cosmologia(self, msg):
        self.results["cosmologia"] = msg.payload
        (self.logs_dir / "p2p_cosmo_result.json").write_text(
            json.dumps(msg.payload, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        self._write_summary()
        p = msg.payload
        if p.get("ok"):
            try:
                print(
                    f"[coord] cosmologia ok | z~{p['z_median']:.2f} defl̄={p['deflexao_media']:.4f} n={p['n_obs']}"
                )
            except Exception:
                print("[coord] cosmologia ok")
        else:
            print("[coord] cosmologia erro")
        await asyncio.sleep(0)

    async def _on_result_verna(self, msg):
        self.results["verna"] = msg.payload
        (self.logs_dir / "p2p_verna_result.json").write_text(
            json.dumps(msg.payload, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        self._write_summary()
        p = msg.payload
        if p.get("ok"):
            try:
                print(
                    f"[coord] verna ok | CL={p['cl']:.3f} K={p['k']:.3f} gen={p['geracoes']}"
                )
            except Exception:
                print("[coord] verna ok")
        else:
            print("[coord] verna erro")
        await asyncio.sleep(0)

    async def _on_result_cosma(self, msg):
        self.results["cosma"] = msg.payload
        (self.logs_dir / "p2p_cosma_result.json").write_text(
            json.dumps(msg.payload, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        self._write_summary()
        p = msg.payload
        if p.get("ok"):
            try:
                print(
                    f"[coord] cosma ok | genomas={p['genomas']} coer={p['coerencia']:.3f}"
                )
            except Exception:
                print("[coord] cosma ok")
        else:
            print("[coord] cosma erro")
        await asyncio.sleep(0)
