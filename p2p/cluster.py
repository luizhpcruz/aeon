from __future__ import annotations
import asyncio
import json
import random
from pathlib import Path
from typing import List, Dict
from .node import Node
from .coordinator import Coordinator

# Message kinds
K_DO_ENTROPY = "do:entropy"
K_RESULT_ENTROPY = "result:entropy"
K_DO_COSMO = "do:cosmologia"
K_RESULT_COSMO = "result:cosmologia"
K_DO_VERNA = "do:verna"
K_RESULT_VERNA = "result:verna"
K_DO_COSMA = "do:cosma"
K_RESULT_COSMA = "result:cosma"

# Cluster composition: one node per module + a coordinator
MODULES = [
    ("entropy", "core.entropy"),
    ("cosmologia", "teste_cosmologia.py"),
    ("verna", "teste_simples.py"),
    ("cosma", "teste_aeon_cosma.py"),
]

def _connect_mesh(nodes: Dict[str, Node]) -> None:
    for a in nodes.values():
        for b in nodes.values():
            if a is not b:
                a.connect(b)

async def run_cluster(names: List[str] | None = None) -> Dict[str, Node]:
    names = ["coordenador"] + (names or [m[0] for m in MODULES])
    nodes = {name: Node(name) for name in names}

    _connect_mesh(nodes)

    # Generic echo for health
    async def on_ping(msg):
        # minimal no-op handler to keep async contract
        await asyncio.sleep(0)

    for n in nodes.values():
        n.on("ping", on_ping)
        n.start()

    # Wire entropy node to execute simulation and report back to coordinator
    try:
        from core.entropy import EntropyConfig as entropy_cfg_type, simulate_entropy
    except Exception:
        entropy_cfg_type = None  # type: ignore
        simulate_entropy = None  # type: ignore

    RESULT_KIND = K_RESULT_ENTROPY

    async def on_entropy_request(msg):
        # Run inside the same process to avoid subprocess/env issues
        if simulate_entropy is None or entropy_cfg_type is None:
            await nodes[msg.src].send("coordenador", RESULT_KIND, {
                "ok": False,
                "erro": "core.entropy indisponível",
            })
            return
        cfg = entropy_cfg_type(
            n_ciclos=max(40, int(msg.payload.get("ciclos", 40))),
            n_fitas=5,
            n_celulas=int(msg.payload.get("celulas", 32)),
        )
        result = simulate_entropy(cfg)
        await nodes["entropy"].send(
            "coordenador",
            RESULT_KIND,
            {
                "ok": True,
                "n_ciclos": result["config"]["n_ciclos"],
                "n_fitas": result["config"]["n_fitas"],
                "entropia_media": result["resultados"]["entropia_global_media"],
                "complexidade_media": result["resultados"]["complexidade_global_media"],
                "entropia_max": result["resultados"]["entropia_maxima"],
            },
        )

    # Register handlers
    nodes["entropy"].on(K_DO_ENTROPY, on_entropy_request)

    # In-process synthetic producers for other modules (stubs)
    # Cosmologia stub
    async def on_cosmo_request(msg):
        try:
            n_obs = int(msg.payload.get("n_obs", 128))
            z_vals = [abs(random.gauss(1.0, 0.4)) for _ in range(n_obs)]
            z_vals.sort()
            z_median = z_vals[len(z_vals)//2] if z_vals else 0.0
            deflexao_media = max(0.0, random.gauss(0.02, 0.01))
            payload = {
                "ok": True,
                "n_obs": n_obs,
                "z_median": z_median,
                "deflexao_media": deflexao_media,
            }
        except Exception as e:
            payload = {"ok": False, "erro": str(e)}
        await nodes["cosmologia"].send("coordenador", K_RESULT_COSMO, payload)

    nodes["cosmologia"].on(K_DO_COSMO, on_cosmo_request)

    # VERNA stub
    async def on_verna_request(msg):
        try:
            geracoes = max(40, int(msg.payload.get("geracoes", 50)))
            cl = min(1.0, max(0.0, random.gauss(0.72, 0.08)))
            k = min(1.0, max(0.0, random.gauss(0.35, 0.1)))
            payload = {
                "ok": True,
                "geracoes": geracoes,
                "cl": cl,
                "k": k,
            }
        except Exception as e:
            payload = {"ok": False, "erro": str(e)}
        await nodes["verna"].send("coordenador", K_RESULT_VERNA, payload)

    nodes["verna"].on(K_DO_VERNA, on_verna_request)

    # COSMA stub
    async def on_cosma_request(msg):
        try:
            genomas = max(5, int(msg.payload.get("genomas", 8)))
            coerencia = min(1.0, max(0.0, random.gauss(0.58, 0.15)))
            payload = {
                "ok": True,
                "genomas": genomas,
                "coerencia": coerencia,
            }
        except Exception as e:
            payload = {"ok": False, "erro": str(e)}
        await nodes["cosma"].send("coordenador", K_RESULT_COSMA, payload)

    nodes["cosma"].on(K_DO_COSMA, on_cosma_request)

    coord = Coordinator()
    coord.wire(nodes, "coordenador")

    # yield to event loop once to ensure tasks start
    await asyncio.sleep(0)
    return nodes

async def run_entropy_once() -> Dict[str, Node]:
    nodes = await run_cluster()
    # Ask the entropy node to run once
    await nodes["coordenador"].send("entropy", K_DO_ENTROPY, {"ciclos": 40, "celulas": 32})

    # Wait briefly for result and then print a compact line
    # We reuse the event defined in run_cluster by checking for the output file
    for _ in range(50):  # ~5s
        await asyncio.sleep(0.1)
        out = Path("logs/p2p_entropy_result.json")
        if out.exists():
            try:
                data = json.loads(out.read_text(encoding="utf-8"))
                if data.get("ok"):
                    print(f"P2P entropy ok | fitas={data['n_fitas']} ciclos={data['n_ciclos']} "
                          f"H̄={data['entropia_media']:.4f} C̄={data['complexidade_media']:.4f} Hmax={data['entropia_max']:.4f}")
                else:
                    print("P2P entropy erro")
            except Exception:
                pass
            break
    return nodes

async def run_all_once() -> Dict[str, Node]:
    nodes = await run_cluster()
    # Trigger all nodes once with minimal payloads
    await nodes["coordenador"].send("entropy", K_DO_ENTROPY, {"ciclos": 40, "celulas": 32})
    await nodes["coordenador"].send("cosmologia", K_DO_COSMO, {"n_obs": 200})
    await nodes["coordenador"].send("verna", K_DO_VERNA, {"geracoes": 60})
    await nodes["coordenador"].send("cosma", K_DO_COSMA, {"genomas": 12})

    # Wait up to ~5s for the coordinator summary including all modules
    summary_path = Path("logs/p2p_summary.json")
    expected = {"entropy", "cosmologia", "verna", "cosma"}
    for _ in range(50):
        await asyncio.sleep(0.1)
        if summary_path.exists():
            try:
                data = json.loads(summary_path.read_text(encoding="utf-8"))
                got = {k for k, v in data.items() if isinstance(v, dict) and v.get("ok") is not None}
                if expected.issubset(got):
                    print("P2P all ok | " + ", ".join(sorted(got)))
                    break
            except Exception:
                pass
    return nodes

async def demo():
    await run_all_once()

if __name__ == "__main__":
    asyncio.run(demo())
