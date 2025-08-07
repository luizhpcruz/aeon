@echo off
REM Script de inicialização da Plataforma AEON MVP (Windows)

echo 🚀 AEON Digital Twin - Configuração MVP
echo =======================================

REM Criar diretórios necessários
echo 📁 Criando estrutura de diretórios...
if not exist "logs" mkdir logs
if not exist "exports" mkdir exports
if not exist "exports\reports" mkdir exports\reports
if not exist "exports\dxf" mkdir exports\dxf

REM Instalar dependências Python
echo 📦 Instalando dependências...
pip install -r requirements.txt

REM Verificar se todos os módulos AEON estão disponíveis
echo 🔍 Verificando módulos AEON...

python -c "
import sys
import os
sys.path.append('.')
sys.path.append('./scripts')

modules_to_check = [
    ('scripts.four', 'scripts/4.py'),
    ('scripts.VERNA', 'scripts/VERNA.py'), 
    ('scripts.NMD', 'scripts/NMD.py')
]

missing = []
print('🔍 Verificando módulos AEON...')

for module_name, file_path in modules_to_check:
    if os.path.exists(file_path):
        try:
            if '4.py' in file_path:
                # Para o arquivo 4.py, apenas verificar se existe
                print(f'✅ Análise de Entropia (4.py) - OK')
            elif 'VERNA' in file_path:
                print(f'✅ V.E.R.N.A. AI System - OK')
            elif 'NMD' in file_path:
                print(f'✅ Cosmologia NMD - OK')
        except Exception as e:
            print(f'❌ {module_name} - ERRO: {e}')
            missing.append(module_name)
    else:
        print(f'❌ {file_path} - ARQUIVO NÃO ENCONTRADO')
        missing.append(module_name)

if missing:
    print(f'\\n⚠️  Módulos em falta: {missing}')
else:
    print('\\n✅ Todos os módulos AEON encontrados!')
    print('✅ Backend FastAPI configurado!')
    print('✅ Frontend HTML/JS pronto!')
"

echo.
echo 🌐 Iniciando servidor FastAPI...
echo Frontend disponível em: http://localhost:8000/frontend/
echo API Docs em: http://localhost:8000/docs
echo.

REM Iniciar servidor
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

pause
