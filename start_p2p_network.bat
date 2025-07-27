@echo off
echo ============================================================
echo 🌌 AEONCOSMA P2P TRADING NETWORK
echo 🚀 Sistema Distribuído de Trading com IA
echo ⚡ Fase 1: Núcleo P2P com Validação Backend
echo ============================================================

cd /d "%~dp0"

echo 🔧 Ativando ambiente virtual...
call .venv\Scripts\activate.bat

echo 🚀 Iniciando sistema P2P AEONCOSMA...
python start_p2p_system.py

pause
