@echo off
setlocal
set AEON_QUIET=1
cd /d "%~dp0"
if exist "venv\Scripts\activate.bat" call venv\Scripts\activate.bat
py aeon_launcher.py --retries 0 --timeout 30 --pause 1
endlocal
