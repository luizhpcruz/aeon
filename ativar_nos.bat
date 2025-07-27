@echo off
echo 🌐 ATIVANDO NÓS AEONCOSMA P2P
echo ============================

echo.
echo 🚀 Iniciando Nó Principal...
start "NÓ PRINCIPAL" cmd /k "cd /d "%~dp0" && python aeoncosma\main.py"

echo.
echo ⏰ Aguardando 3 segundos...
timeout /t 3 /nobreak >nul

echo.
echo 🚀 Iniciando Segundo Nó (Porta 9001)...
start "SEGUNDO NÓ" cmd /k "cd /d "%~dp0" && python aeoncosma\networking\p2p_node.py --port 9001 --node-id segundo_no"

echo.
echo ⏰ Aguardando 3 segundos...
timeout /t 3 /nobreak >nul

echo.
echo 🚀 Iniciando Terceiro Nó (Porta 9002)...
start "TERCEIRO NÓ" cmd /k "cd /d "%~dp0" && python aeoncosma\networking\p2p_node.py --port 9002 --node-id terceiro_no"

echo.
echo ✅ TODOS OS NÓS FORAM INICIADOS!
echo 💡 Cada nó está rodando em uma janela separada
echo 🔗 Nó Principal: localhost:9000
echo 🔗 Segundo Nó: localhost:9001  
echo 🔗 Terceiro Nó: localhost:9002
echo.
echo Pressione qualquer tecla para fechar este launcher...
pause >nul
