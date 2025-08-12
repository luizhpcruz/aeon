# Runs only the Entropy subsystem in quiet mode via launcher filters
$ErrorActionPreference = 'SilentlyContinue'
$env:AEON_QUIET = '1'
Set-Location -Path $PSScriptRoot
if (Test-Path "$PSScriptRoot\venv\Scripts\Activate.ps1") { . "$PSScriptRoot\venv\Scripts\Activate.ps1" }
py aeon_launcher.py --only entropia  --quiet --retries 0 --timeout 60 --pause 0
