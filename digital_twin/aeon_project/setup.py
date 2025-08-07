#!/usr/bin/env python3
"""
🚀 AEON Setup Script
Configuração automática do ambiente AEON Digital Twin
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Executa comando e mostra resultado"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - OK")
            return True
        else:
            print(f"❌ {description} - ERRO: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} - EXCEÇÃO: {e}")
        return False

def check_python_version():
    """Verifica versão do Python"""
    version = sys.version_info
    print(f"🐍 Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 10:
        print("✅ Versão do Python adequada")
        return True
    else:
        print("❌ Python 3.10+ necessário")
        return False

def install_requirements():
    """Instala dependências do requirements.txt"""
    requirements_file = Path("requirements.txt")
    
    if requirements_file.exists():
        return run_command(
            f"{sys.executable} -m pip install -r requirements.txt",
            "Instalando dependências"
        )
    else:
        # Lista de dependências básicas se requirements.txt não existir
        basic_deps = [
            "streamlit>=1.28.0",
            "fastapi>=0.104.0",
            "uvicorn>=0.24.0",
            "pandas>=2.1.0",
            "numpy>=1.24.0",
            "plotly>=5.17.0",
            "cryptography>=41.0.0",
            "qrcode>=7.4.2",
            "pillow>=10.0.0",
            "pydantic>=2.5.0"
        ]
        
        success = True
        for dep in basic_deps:
            if not run_command(f"{sys.executable} -m pip install {dep}", f"Instalando {dep}"):
                success = False
        
        return success

def create_directories():
    """Cria diretórios necessários"""
    directories = [
        "logs",
        "temp",
        "data/exports",
        "data/uploads"
    ]
    
    for dir_path in directories:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
    
    print("✅ Diretórios criados")
    return True

def main():
    """Função principal do setup"""
    print("🚀 AEON SETUP - Configuração do Ambiente")
    print("=" * 50)
    
    # Verificar Python
    if not check_python_version():
        print("\n❌ Setup interrompido - Python inadequado")
        return False
    
    # Atualizar pip
    run_command(f"{sys.executable} -m pip install --upgrade pip", "Atualizando pip")
    
    # Instalar dependências
    if not install_requirements():
        print("\n❌ Setup interrompido - Erro nas dependências")
        return False
    
    # Criar diretórios
    create_directories()
    
    print("\n🎉 SETUP CONCLUÍDO COM SUCESSO!")
    print("\n🚀 Para executar o AEON:")
    print(f"   {sys.executable} -m streamlit run aeon_app.py")
    print("\n🔍 Para verificar a rede:")
    print(f"   {sys.executable} status_checker.py")
    print("\n🌐 Interface disponível em: http://localhost:8501")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
