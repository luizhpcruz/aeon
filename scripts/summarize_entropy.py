#!/usr/bin/env python3
"""
Summarize entropy results from a JSON file produced by core/entropy.py
Usage:
  python scripts/summarize_entropy.py [path_to_json]
Defaults to logs/entropy_reanimate.json
"""
from __future__ import annotations
import sys, json
from pathlib import Path

def main(argv):
    path = Path(argv[0]) if argv else Path('logs/entropy_reanimate.json')
    if not path.exists():
        print(f"Arquivo não encontrado: {path}")
        return 1
    data = json.loads(path.read_text(encoding='utf-8'))
    cfg = data.get('config', {})
    res = data.get('resultados', {})
    print(f"Resumo Entropia | fitas={cfg.get('n_fitas')} ciclos={cfg.get('n_ciclos')} "
          f"| H̄={res.get('entropia_global_media'):.4f} "
          f"| C̄={res.get('complexidade_global_media'):.4f} "
          f"| Hmax={res.get('entropia_maxima'):.4f}")
    return 0

if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1:]))
