#!/usr/bin/env python3
"""
Scan the repository for large files to help keep the repo lean.

Usage (examples):
  python scripts/scan_large_files.py                # top 50 files >= 5 MB
  python scripts/scan_large_files.py --min 1 --top 100
  python scripts/scan_large_files.py --tracked      # only files tracked by Git

Outputs a simple table and writes a report to large_files_report.txt.
"""
from __future__ import annotations

import os
import sys
import argparse
import subprocess
from pathlib import Path
from typing import Iterable, List, Tuple

DEFAULT_MIN_MB = 5
DEFAULT_TOP = 50

EXCLUDE_DIRS = {
    ".git",
    "node_modules",
    "venv",
    ".venv",
    "python_env",
    "__pycache__",
    "archive",
    "advanced",
    "logs",
    "data",
    "visualizations",
    "aeon_model_export",
    "aeon_historico",
    "AEONCOSMA_WINDOWS_PACKAGE",
    "aeoncosma_simulation_bundle",
    "Digital Twin",
    "GovTech",
    "IA p2p trader",
}

def is_git_repo(root: Path) -> bool:
    return (root / ".git").exists()

def get_tracked_files(root: Path) -> List[Path]:
    try:
        out = subprocess.check_output(["git", "ls-files"], cwd=root, stderr=subprocess.DEVNULL, text=True)
    except Exception:
        return []
    files = [root / line.strip() for line in out.splitlines() if line.strip()]
    return [p for p in files if p.exists() and p.is_file()]

def walk_files(root: Path) -> Iterable[Path]:
    for dirpath, dirnames, filenames in os.walk(root):
        # prune excluded dirs
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        for fn in filenames:
            p = Path(dirpath) / fn
            yield p

def human(nbytes: int) -> str:
    units = ["B", "KB", "MB", "GB", "TB"]
    x = float(nbytes)
    for u in units:
        if x < 1024 or u == units[-1]:
            return f"{x:.2f} {u}"
        x /= 1024
    return f"{nbytes} B"

def main(argv: List[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--min", dest="min_mb", type=float, default=DEFAULT_MIN_MB, help="Minimum size in MB")
    ap.add_argument("--top", dest="top", type=int, default=DEFAULT_TOP, help="Top N files to show")
    ap.add_argument("--tracked", action="store_true", help="Only include files tracked by Git")
    args = ap.parse_args(argv)

    root = Path(__file__).resolve().parents[1]
    min_bytes = int(args.min_mb * 1024 * 1024)

    if args.tracked and not is_git_repo(root):
        print("Not a Git repository; --tracked ignored.", file=sys.stderr)
        args.tracked = False

    if args.tracked:
        files = get_tracked_files(root)
    else:
        files = list(walk_files(root))

    sized: List[Tuple[int, Path]] = []
    for p in files:
        try:
            sz = p.stat().st_size
        except OSError:
            continue
        if sz >= min_bytes:
            sized.append((sz, p))

    sized.sort(key=lambda t: t[0], reverse=True)
    top = sized[: args.top]

    if not top:
        print("No files found meeting the criteria.")
        return 0

    print(f"Top {len(top)} files >= {args.min_mb} MB" + (" (tracked)" if args.tracked else ""))
    print("-" * 80)
    for sz, p in top:
        rel = p.relative_to(root)
        print(f"{human(sz):>10}  |  {rel}")

    report = root / "large_files_report.txt"
    with report.open("w", encoding="utf-8") as f:
        f.write(f"Top {len(top)} large files (>= {args.min_mb} MB)\n")
        for sz, p in top:
            rel = p.relative_to(root)
            f.write(f"{sz}\t{rel}\n")
    print(f"\nReport written to {report}")
    print("Next: untrack any unwanted large files and commit; consider a history purge if needed.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
