@echo off
title AEON Digital Twin

echo.
echo  ████████╗     █████╗     ███████╗    ██████╗    ███╗    ██╗
echo  ╚══██╔══╝    ██╔══██╗    ██╔════╝   ██╔═══██╗   ████╗   ██║
echo     ██║       ███████║    █████╗     ██║   ██║   ██╔██╗  ██║
echo     ██║       ██╔══██║    ██╔══╝     ██║   ██║   ██║╚██╗ ██║
echo     ██║       ██║  ██║    ███████╗   ╚██████╔╝   ██║ ╚████║
echo     ╚═╝       ╚═╝  ╚═╝    ╚══════╝    ╚═════╝    ╚═╝  ╚═══╝
echo.
echo                   🚀 Digital Twin System 🚀
echo              💎 Preparado para ser UNICÓRNIO! 🦄🇧🇷
echo.
echo ================================================================

echo 🔍 Verificando status da rede AEON...
py status_checker.py

echo.
echo � Iniciando interface web...
echo 🌐 Acesse: http://localhost:8501
echo.
echo ⚠️  Pressione Ctrl+C para parar o servidor
echo.

py -m streamlit run aeon_app.py
