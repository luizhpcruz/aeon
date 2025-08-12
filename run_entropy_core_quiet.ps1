# Runs the core entropy module directly with enforced 5 tapes and >= 40 cycles
$ErrorActionPreference = 'SilentlyContinue'
$env:AEON_QUIET = '1'
Set-Location -Path $PSScriptRoot
if (Test-Path "$PSScriptRoot\venv\Scripts\Activate.ps1") { . "$PSScriptRoot\venv\Scripts\Activate.ps1" }
py core/entropy.py --quiet --seed 42 --ciclos 10 --fitas 1 --celulas 32 --out logs/entropy_reanimate.json
