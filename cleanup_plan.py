"""AEON Cleanup Plan Script
Lista itens marcados como LEGACY / HEAVY_ENV / GENERATED e opcionalmente move para archive/ ou advanced/.
Somente lista por padrão. Passe argumento --apply para executar movimentações.
"""
from __future__ import annotations
import os
import shutil
import argparse
from pathlib import Path

# Categorias de ação
LEGACY_PATHS = [
    'bagunca/AEON.py',
    'bagunca/AEON1.py',
    'bagunca/AEON12.py',
    'bagunca/AEON3.py',
    'bagunca/AEONCOSMA_ENGINE_v1',
    'AEONCOSMA_WINDOWS_PACKAGE',
    'aeoncosma_simulation_bundle',
    'aeoncosma',
    'frontend',
    'IA p2p trader',
    'GovTech',
    'visualizations',
    'data',
    'aeoncosma_security_report.pdf',
]

ADVANCED_GROUP = [
    'digital_twin',  # mover para advanced/
    'Digital Twin',  # duplicado / antigo
]

ARCHIVE_DIR = Path('archive')
ADVANCED_DIR = Path('advanced')

CORE_KEEP = {
    'README.md', 'requirements.txt', 'aeon_launcher.py', 'aeon_dashboard.py',
    'aeon_dashboard_simples.py', 'start_dashboard.bat', 'teste_entropia.py',
    'teste_simples.py', 'teste_cosmologia.py', 'teste_aeon_cosma.py', 'MODULE_AUDIT.md',
    'cleanup_plan.py'
}


def classify(path: Path) -> str:
    if path.name in CORE_KEEP:
        return 'CORE'
    rel = path.as_posix()
    if any(rel == p or rel.startswith(p.rstrip('/')) for p in LEGACY_PATHS):
        return 'LEGACY'
    if any(rel == p or rel.startswith(p.rstrip('/')) for p in ADVANCED_GROUP):
        return 'ADVANCED'
    return 'OTHER'


def plan():
    root = Path('.')
    rows = []
    for item in root.iterdir():
        if item.name.startswith('.'):
            continue
        rows.append((item.name, classify(item)))
    return rows


def move_paths(paths, dest: Path):
    dest.mkdir(exist_ok=True)
    for p in paths:
        src = Path(p)
        if not src.exists():
            continue
        target = dest / src.name
        if target.exists():
            print(f'[skip] {src} -> {target} (já existe)')
            continue
        print(f'[move] {src} -> {target}')
        shutil.move(str(src), str(target))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--apply', action='store_true', help='Executa movimentações')
    args = parser.parse_args()

    rows = plan()
    print('\n=== AEON CLEANUP PLAN ===')
    for name, cls in rows:
        print(f'{name:35} | {cls}')

    if not args.apply:
        print('\nModo de simulação. Use --apply para mover LEGACY e digital_twin.')
        return

    # Mover legacy
    legacy_to_move = [p for p in LEGACY_PATHS if Path(p).exists()]
    move_paths(legacy_to_move, ARCHIVE_DIR)

    # Mover advanced
    advanced_to_move = [p for p in ADVANCED_GROUP if Path(p).exists()]
    move_paths(advanced_to_move, ADVANCED_DIR)

    print('\nConcluído. Revise e faça commit se tudo ok.')


if __name__ == '__main__':
    main()
