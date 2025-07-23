#!/bin/bash

echo "🧬 AEON - Sistema de Simulação Complexa"
echo "======================================"

# Ativar ambiente virtual se existir
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✅ Ambiente virtual ativado"
fi

echo ""
echo "Escolha uma opção:"
echo "1. 🔬 Executar análise de entropia (4.py)"
echo "2. 🌌 Executar modelo cosmológico (NMD.py)"
echo "3. 🤖 Executar motor AEON Cosma"
echo "4. 🧠 Executar sistema V.E.R.N.A."
echo "5. 📊 Executar todas as simulações"
echo "6. 🚀 Instalar dependências"
echo ""

read -p "Digite sua escolha (1-6): " choice

case $choice in
    1)
        echo "🔬 Executando análise de entropia..."
        python scripts/4.py
        ;;
    2)
        echo "🌌 Executando modelo cosmológico..."
        python scripts/NMD.py
        ;;
    3)
        echo "🤖 Executando motor AEON Cosma..."
        cd bagunça/AEONCOSMA_ENGINE_v1
        python aeon_interface.py
        ;;
    4)
        echo "🧠 Executando sistema V.E.R.N.A..."
        python teoria/verna.py
        ;;
    5)
        echo "📊 Executando todas as simulações..."
        python scripts/1.py
        python scripts/2.py
        python scripts/3.py
        python scripts/4.py
        python scripts/5.py
        ;;
    6)
        echo "🚀 Instalando dependências..."
        pip install -r requirements.txt
        ;;
    *)
        echo "❌ Opção inválida"
        ;;
esac

echo ""
echo "✨ Execução concluída!"
