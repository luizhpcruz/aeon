@echo off
title 🚀 AEON - Launch All Nodes
echo.
echo 🚀 INICIANDO TODOS OS NÓS P2P...
echo ================================================
echo.

echo 🎯 1. Iniciando Coordinator...
start "Coordinator" start_coordinator.bat

timeout /t 2 /nobreak >nul

echo 🔬 2. Iniciando Entropy Node...
start "Entropy" start_node_entropy.bat

timeout /t 1 /nobreak >nul

echo 🌌 3. Iniciando Cosmologia Node...
start "Cosmologia" start_node_cosmologia.bat

timeout /t 1 /nobreak >nul

echo 🧠 4. Iniciando V.E.R.N.A. Node...
start "V.E.R.N.A." start_node_verna.bat

timeout /t 1 /nobreak >nul

echo 🤖 5. Iniciando AEON Cosma Node...
start "AEON Cosma" start_node_cosma.bat

echo.
echo ✅ Todos os nós foram iniciados!
echo 📊 Verifique a janela do Coordinator para o relatório final.
echo 📁 Resultados em: logs\coordinator_summary.json
echo.
echo ⏸️  Pressione qualquer tecla para sair...
pause >nul
