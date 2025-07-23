#!/bin/bash

echo "🚀 AEON - Setup do Ambiente de Desenvolvimento"
echo "============================================="

# Criar ambiente virtual
echo "📦 Criando ambiente virtual Python..."
python3 -m venv venv
source venv/bin/activate

# Instalar dependências Python
echo "📚 Instalando dependências Python..."
pip install --upgrade pip
pip install -r requirements.txt

# Verificar instalação
echo "✅ Verificando instalação..."
python -c "import numpy, matplotlib, seaborn, pandas; print('Dependências Python instaladas com sucesso!')"

# Configurar Git (se não estiver configurado)
echo "🔧 Configurando Git..."
git config --global init.defaultBranch main
echo "Git configurado!"

echo ""
echo "🎉 Setup concluído com sucesso!"
echo ""
echo "📋 Para usar o projeto:"
echo "   1. Backend: source venv/bin/activate && python scripts/4.py"
echo "   2. Motor AEON: cd bagunça/AEONCOSMA_ENGINE_v1 && python aeon_interface.py"
echo "   3. Frontend: cd frontend && npm install && npm start"
echo ""
echo "📖 Consulte o README.md para mais informações"
