#!/bin/bash
# Script de inicialização da Plataforma AEON MVP

echo "🚀 AEON Digital Twin - Configuração MVP"
echo "======================================="

# Criar diretórios necessários
echo "📁 Criando estrutura de diretórios..."
mkdir -p logs
mkdir -p exports/reports
mkdir -p exports/dxf

# Instalar dependências Python
echo "📦 Instalando dependências..."
pip install -r requirements.txt

# Verificar se todos os módulos AEON estão disponíveis
echo "🔍 Verificando módulos AEON..."

python -c "
import sys
sys.path.append('.')

modules = ['scripts.4', 'VERNA', 'NMD']
missing = []

for module in modules:
    try:
        __import__(module)
        print(f'✅ {module} - OK')
    except ImportError as e:
        print(f'❌ {module} - ERRO: {e}')
        missing.append(module)

if missing:
    print(f'\\n⚠️  Módulos em falta: {missing}')
    print('Verifique se os arquivos estão no diretório correto.')
else:
    print('\\n✅ Todos os módulos AEON carregados com sucesso!')
"

echo ""
echo "🌐 Iniciando servidor FastAPI..."
echo "Frontend disponível em: http://localhost:8000/frontend/"
echo "API Docs em: http://localhost:8000/docs"
echo ""

# Iniciar servidor
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
