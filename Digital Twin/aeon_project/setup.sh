#!/bin/bash

echo "🚀 AEON Digital Twin - Setup Linux/macOS"
echo "========================================"

echo ""
echo "🔍 Verificando Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 não encontrado! Instale Python 3.10+"
    exit 1
fi

python3 --version

echo ""
echo "🔄 Executando setup..."
python3 setup.py

echo ""
echo "✅ Setup concluído!"
echo ""
echo "🚀 Para executar o AEON:"
echo "   python3 -m streamlit run aeon_app.py"
echo ""
echo "🔍 Para verificar a rede:"
echo "   python3 status_checker.py"
echo ""
