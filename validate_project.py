#!/usr/bin/env python3
"""
🔍 VALIDADOR DE PROJETO AEON COSMOS
==================================

Script para validar se todos os componentes do projeto estão funcionando.
Desenvolvido por Luiz Cruz
"""

import os
import sys
import importlib.util
from pathlib import Path

def validate_file_structure():
    """Valida a estrutura de arquivos do projeto."""
    print("📁 Validando estrutura de arquivos...")
    
    required_files = [
        "requirements.txt",
        "start.py",
        "README.md",
        "LICENSE",
        "docker-compose.yml",
        "aeoncosma/main.py",
        "aeoncosma/core/aeon_entity.py",
        "aeoncosma/core/aeon_tutor.py",
        "aeoncosma/core/aeon_hive_core.py",
        "backend/main.py",
        "ai-core/trading_ai.py",
        "frontend/package.json"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Arquivos faltando:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    else:
        print("✅ Estrutura de arquivos OK")
        return True

def validate_python_imports():
    """Valida se os imports Python estão funcionando."""
    print("\n🐍 Validando imports Python...")
    
    test_modules = [
        ("aeoncosma.core.aeon_entity", "aeoncosma/core/aeon_entity.py"),
        ("aeoncosma.core.aeon_tutor", "aeoncosma/core/aeon_tutor.py"),
        ("aeoncosma.core.aeon_hive_core", "aeoncosma/core/aeon_hive_core.py")
    ]
    
    failed_imports = []
    
    for module_name, file_path in test_modules:
        try:
            if Path(file_path).exists():
                spec = importlib.util.spec_from_file_location(module_name, file_path)
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    print(f"✅ {module_name}")
                else:
                    print(f"❌ {module_name} - Spec inválido")
                    failed_imports.append(module_name)
            else:
                print(f"❌ {module_name} - Arquivo não encontrado")
                failed_imports.append(module_name)
        except Exception as e:
            print(f"❌ {module_name} - Erro: {str(e)}")
            failed_imports.append(module_name)
    
    return len(failed_imports) == 0

def validate_syntax():
    """Valida a sintaxe dos arquivos Python principais."""
    print("\n🔧 Validando sintaxe Python...")
    
    python_files = [
        "aeoncosma/main.py",
        "aeoncosma/core/aeon_entity.py",
        "aeoncosma/core/aeon_tutor.py",
        "start.py"
    ]
    
    syntax_errors = []
    
    for file_path in python_files:
        if Path(file_path).exists():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    code = f.read()
                compile(code, file_path, 'exec')
                print(f"✅ {file_path}")
            except SyntaxError as e:
                print(f"❌ {file_path} - Erro de sintaxe: {e}")
                syntax_errors.append(file_path)
            except Exception as e:
                print(f"⚠️  {file_path} - Aviso: {e}")
        else:
            print(f"❌ {file_path} - Arquivo não encontrado")
            syntax_errors.append(file_path)
    
    return len(syntax_errors) == 0

def validate_dependencies():
    """Valida se as dependências estão listadas."""
    print("\n📦 Validando dependências...")
    
    if not Path("requirements.txt").exists():
        print("❌ requirements.txt não encontrado")
        return False
    
    with open("requirements.txt", 'r') as f:
        requirements = f.read()
    
    required_deps = [
        "numpy", "pandas", "matplotlib", "scikit-learn",
        "fastapi", "uvicorn", "pydantic", "websockets"
    ]
    
    missing_deps = []
    for dep in required_deps:
        if dep not in requirements:
            missing_deps.append(dep)
    
    if missing_deps:
        print("❌ Dependências faltando:")
        for dep in missing_deps:
            print(f"   - {dep}")
        return False
    else:
        print("✅ Dependências OK")
        return True

def validate_docker():
    """Valida configurações Docker."""
    print("\n🐳 Validando configurações Docker...")
    
    docker_files = [
        "docker-compose.yml",
        "Dockerfile.backend",
        "Dockerfile.frontend",
        "Dockerfile.simulation"
    ]
    
    missing_docker = []
    for file_path in docker_files:
        if not Path(file_path).exists():
            missing_docker.append(file_path)
    
    if missing_docker:
        print("❌ Arquivos Docker faltando:")
        for file in missing_docker:
            print(f"   - {file}")
        return False
    else:
        print("✅ Configurações Docker OK")
        return True

def main():
    """Função principal de validação."""
    print("🚀 INICIANDO VALIDAÇÃO DO PROJETO AEON COSMOS")
    print("=" * 50)
    
    results = []
    
    # Executar validações
    results.append(validate_file_structure())
    results.append(validate_python_imports())
    results.append(validate_syntax())
    results.append(validate_dependencies())
    results.append(validate_docker())
    
    # Resumo final
    print("\n" + "=" * 50)
    print("📊 RESUMO DA VALIDAÇÃO")
    
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print("🎉 PROJETO VALIDADO COM SUCESSO!")
        print("✅ Todos os testes passaram")
        return True
    else:
        print(f"⚠️  PROJETO COM PROBLEMAS: {passed}/{total} testes passaram")
        print("🔧 Verifique os erros acima e corrija antes de continuar")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
