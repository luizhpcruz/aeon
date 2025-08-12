from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Any, List
import math
import random
import argparse
import json
from pathlib import Path

@dataclass
class EntropyConfig:
    n_ciclos: int = 40  # mínimo exigido: 40+ ciclos
    n_fitas: int = 5    # fixo: 5 fitas
    n_celulas: int = 32


def simulate_entropy(cfg: EntropyConfig) -> Dict[str, Any]:
    """Pure function returning deterministic-shaped structure using simple stochastic model."""
    ciclos = list(range(cfg.n_ciclos))
    # generate base evolutions
    entropia_values: List[float] = []
    complexidade_values: List[float] = []
    for i in ciclos:
        base_entropy = 3.5 + 0.5 * math.sin(i * 0.3) + random.gauss(0, 0.1)
        base_complex = 0.6 + 0.2 * math.cos(i * 0.2) + random.gauss(0, 0.05)
        entropia_values.append(max(0.0, base_entropy))
        complexidade_values.append(max(0.0, min(1.0, base_complex)))

    fitas_data = []
    for fita_id in range(cfg.n_fitas):
        evol_ent = [e + random.gauss(0, 0.05) for e in entropia_values]
        evol_cmp = [c + random.gauss(0, 0.02) for c in complexidade_values]
        fita_data = {
            "fita_id": fita_id,
            "entropia_media": sum(evol_ent) / len(evol_ent),
            "complexidade_media": sum(evol_cmp) / len(evol_cmp),
            "evolucao_temporal": {
                "ciclos": ciclos,
                "entropia": evol_ent,
                "complexidade": evol_cmp,
            },
        }
        fitas_data.append(fita_data)

    return {
        "tipo": "entropy_analysis",
        "config": {
            "n_ciclos": cfg.n_ciclos,
            "n_fitas": cfg.n_fitas,
            "n_celulas": cfg.n_celulas,
        },
        "resultados": {
            "entropia_global_media": sum(entropia_values) / len(entropia_values),
            "complexidade_global_media": sum(complexidade_values) / len(complexidade_values),
            "entropia_maxima": max(entropia_values),
            "evolucao_temporal": {
                "ciclos": ciclos,
                "entropia_media": entropia_values,
                "complexidade_media": complexidade_values,
            },
            "fitas": fitas_data,
        },
    }


def _main() -> int:
    ap = argparse.ArgumentParser(description="Entropy simulation runner")
    ap.add_argument("--ciclos", type=int, default=40, help="Número de ciclos (mínimo 40)")
    ap.add_argument("--fitas", type=int, default=5, help="Número de fitas (fixo em 5)")
    ap.add_argument("--celulas", type=int, default=32, help="Número de células por fita")
    ap.add_argument("--seed", type=int, help="Semente para reprodutibilidade")
    ap.add_argument("--out", type=str, default="logs/entropy_run.json", help="Arquivo de saída (JSON)")
    ap.add_argument("--quiet", action="store_true", help="Saída compacta no console")
    args = ap.parse_args()

    if args.seed is not None:
        random.seed(args.seed)

    # Aplicar restrições: 5 fitas e pelo menos 40 ciclos
    ciclos = max(40, int(args.ciclos))
    fitas = 5
    cfg = EntropyConfig(n_ciclos=ciclos, n_fitas=fitas, n_celulas=args.celulas)
    result = simulate_entropy(cfg)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    if args.quiet:
        print(f"✅ Entropia salva em {out_path} | fitas={fitas} ciclos={ciclos}")
    else:
        print(json.dumps({
            "ok": True,
            "arquivo": str(out_path),
            "n_fitas": fitas,
            "n_ciclos": ciclos,
            "entropia_media": round(result["resultados"]["entropia_global_media"], 4),
            "complexidade_media": round(result["resultados"]["complexidade_global_media"], 4),
        }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
