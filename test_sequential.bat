@echo off
echo 🧪 TESTE SEQUENCIAL DOS NOS P2P
echo ================================================
echo.

echo 🔬 1. Executando Entropy Node...
py -3 run_node_entropy.py
echo.

echo 🌌 2. Executando Cosmologia Node...
py -3 run_node_cosmologia.py
echo.

echo 🧠 3. Executando V.E.R.N.A. Node...
py -3 run_node_verna.py
echo.

echo 🤖 4. Executando AEON Cosma Node...
py -3 run_node_cosma.py
echo.

echo 🎯 5. Executando Coordinator para agregar resultados...
py -3 run_coordinator.py
echo.

echo 📁 Verificando arquivos gerados...
dir logs\node_*.json
echo.

echo 📊 Verificando resumo do coordinator...
if exist logs\coordinator_summary.json (
    type logs\coordinator_summary.json
) else (
    echo ❌ Arquivo coordinator_summary.json nao encontrado
)

echo.
pause
