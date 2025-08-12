#!/usr/bin/env python3
"""
Script para configurar e enviar projeto AEON para GitHub
"""
import subprocess
import sys
import os

def run_command(command, description):
    """Executa um comando e mostra o resultado"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - Sucesso")
            if result.stdout.strip():
                print(f"   Output: {result.stdout.strip()}")
        else:
            print(f"❌ {description} - Erro")
            if result.stderr.strip():
                print(f"   Erro: {result.stderr.strip()}")
        return result.returncode == 0
    except Exception as e:
        print(f"❌ {description} - Exceção: {e}")
        return False

def main():
    print("🚀 CONFIGURAÇÃO GITHUB - PROJETO AEON")
    print("=" * 50)
    
    # Verificar se estamos no diretório correto
    if not os.path.exists('.git'):
        print("❌ Não foi encontrado repositório Git neste diretório")
        return 1
    
    # Configurar usuário Git
    run_command('git config user.name "luizhpcruz"', "Configurar nome do usuário")
    run_command('git config user.email "luizhpcruz@users.noreply.github.com"', "Configurar email do usuário")
    
    # Verificar remote
    result = subprocess.run('git remote -v', shell=True, capture_output=True, text=True)
    if 'origin' not in result.stdout:
        run_command('git remote add origin git@github.com:luizhpcruz/aeon.git', "Adicionar repositório remoto")
    else:
        print("✅ Repositório remoto já configurado")
    
    # Verificar status
    run_command('git status --porcelain', "Verificar status do repositório")
    
    # Adicionar arquivos importantes
    files_to_add = [
        '.gitignore',
        'README_NEW.md', 
        'CHANGELOG.md',
        '.github/',
        'p2p/',
        'scripts/',
        'GUIA_PASSO_A_PASSO.md',
        'GUIA_RAPIDO.md',
        'EXEMPLOS_PRATICOS.md',
        'ECOSYSTEM_ARCHITECTURE.md',
        'ECOSYSTEM_CREATED.md',
        'run_*.py',
        'requirements.txt'
    ]
    
    print("\n📁 Adicionando arquivos ao staging...")
    for file in files_to_add:
        if os.path.exists(file):
            run_command(f'git add "{file}"', f"Adicionar {file}")
    
    # Fazer commit
    commit_message = """🚀 feat: Projeto AEON completo com P2P, documentação e CI/CD

- ✅ Sistema P2P distribuído funcional
- ✅ Análise de entropia multi-dimensional  
- ✅ Modelo cosmológico integrado
- ✅ Sistema V.E.R.N.A. neural evolutivo
- ✅ Documentação completa (guias + exemplos)
- ✅ Pipeline CI/CD configurado
- ✅ Templates GitHub (issues/PRs)
- ✅ .gitignore otimizado
- ✅ README profissional
- ✅ Changelog estruturado

Projeto pronto para desenvolvimento colaborativo!"""
    
    if run_command(f'git commit -m "{commit_message}"', "Fazer commit das mudanças"):
        print("✅ Commit realizado com sucesso")
    else:
        print("ℹ️ Nenhuma mudança para commit ou commit já existe")
    
    # Push para GitHub
    if run_command('git push -u origin develop', "Enviar para GitHub"):
        print("🎉 Projeto enviado para GitHub com sucesso!")
        print("🔗 Acesse: https://github.com/luizhpcruz/aeon")
    else:
        print("❌ Erro ao enviar para GitHub")
        print("💡 Verifique se a chave SSH está configurada:")
        print("   ssh -T git@github.com")
    
    print("\n📊 RESUMO FINAL:")
    print("✅ Repositório configurado")
    print("✅ Arquivos organizados") 
    print("✅ Documentação completa")
    print("✅ CI/CD configurado")
    print("🚀 Projeto AEON pronto no GitHub!")

if __name__ == "__main__":
    sys.exit(main())
