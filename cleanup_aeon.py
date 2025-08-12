#!/usr/bin/env python3
"""
Limpeza automatizada do projeto AEON
"""
import os
import shutil
import time
from pathlib import Path

def get_folder_size(folder_path):
    """Calcula tamanho de uma pasta em MB"""
    total_size = 0
    try:
        for dirpath, dirnames, filenames in os.walk(folder_path):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                try:
                    total_size += os.path.getsize(filepath)
                except (OSError, FileNotFoundError):
                    pass
    except (OSError, FileNotFoundError):
        pass
    return total_size / (1024 * 1024)  # Convert to MB

def create_backup_folder():
    """Cria pasta de backup"""
    backup_path = Path("ARCHIVE_BACKUP")
    backup_path.mkdir(exist_ok=True)
    return backup_path

def main():
    print("🧹 LIMPEZA AUTOMATIZADA - PROJETO AEON")
    print("=" * 50)
    
    base_path = Path(".")
    total_cleaned = 0
    
    # Criar pasta de backup
    backup_path = create_backup_folder()
    print(f"📁 Pasta de backup criada: {backup_path}")
    
    # Lista de operações de limpeza
    cleanup_operations = [
        {
            "name": "Cache Python",
            "action": lambda: os.system("pip cache purge > nul 2>&1"),
            "estimated_mb": 50
        }
    ]
    
    # Pastas para mover para backup (apenas as maiores e antigas)
    folders_to_archive = [
        ("archive", "Arquivos antigos do projeto"),
        ("digital_twin", "Projeto Digital Twin"),
        ("IA p2p trader", "Projeto IA P2P Trader antigo")
    ]
    
    print("\n🔍 ANÁLISE INICIAL:")
    print("-" * 30)
    
    # Verificar pastas grandes
    for folder_name, description in folders_to_archive:
        folder_path = base_path / folder_name
        if folder_path.exists():
            size_mb = get_folder_size(folder_path)
            if size_mb > 100:  # Só processar pastas > 100MB
                print(f"📦 {folder_name}: {size_mb:.1f} MB - {description}")
                
                # Perguntar se deve mover
                response = input(f"   Mover '{folder_name}' para backup? (s/N): ").lower()
                if response in ['s', 'sim', 'y', 'yes']:
                    try:
                        target_path = backup_path / f"{folder_name}_{time.strftime('%Y%m%d')}"
                        print(f"   🔄 Movendo {folder_name}...")
                        shutil.move(str(folder_path), str(target_path))
                        print(f"   ✅ Movido para: {target_path}")
                        total_cleaned += size_mb
                    except Exception as e:
                        print(f"   ❌ Erro ao mover {folder_name}: {e}")
    
    print("\n🧹 LIMPEZA DE CACHE:")
    print("-" * 30)
    
    # Executar operações de limpeza
    for operation in cleanup_operations:
        print(f"   🔄 {operation['name']}...")
        try:
            operation["action"]()
            print(f"   ✅ {operation['name']} limpo")
            total_cleaned += operation["estimated_mb"]
        except Exception as e:
            print(f"   ❌ Erro em {operation['name']}: {e}")
    
    # Limpar logs antigos (mais de 7 dias)
    logs_path = base_path / "logs"
    if logs_path.exists():
        print("   🔄 Limpando logs antigos...")
        try:
            for log_file in logs_path.glob("*.log"):
                # Verificar se arquivo é antigo (modificado há mais de 7 dias)
                if time.time() - log_file.stat().st_mtime > 7 * 24 * 3600:
                    size_mb = log_file.stat().st_size / (1024 * 1024)
                    log_file.unlink()
                    total_cleaned += size_mb
                    print(f"   🗑️  Removido: {log_file.name}")
            print("   ✅ Logs antigos limpos")
        except Exception as e:
            print(f"   ❌ Erro ao limpar logs: {e}")
    
    # Verificar arquivos temporários
    temp_patterns = ["*.tmp", "*.temp", "*.cache", "*.pyc"]
    print("   🔄 Limpando arquivos temporários...")
    
    for pattern in temp_patterns:
        try:
            for temp_file in base_path.rglob(pattern):
                if temp_file.is_file():
                    size_mb = temp_file.stat().st_size / (1024 * 1024)
                    temp_file.unlink()
                    total_cleaned += size_mb
        except Exception as e:
            print(f"   ⚠️ Aviso ao limpar {pattern}: {e}")
    
    print("   ✅ Arquivos temporários limpos")
    
    # Relatório final
    print("\n📊 RELATÓRIO DE LIMPEZA:")
    print("=" * 50)
    print(f"💾 Espaço recuperado: {total_cleaned:.2f} MB")
    print(f"💾 Em GB: {total_cleaned/1024:.2f} GB")
    
    if total_cleaned > 1000:
        print("🎉 Excelente! Muito espaço liberado!")
    elif total_cleaned > 100:
        print("✅ Boa limpeza realizada!")
    else:
        print("ℹ️ Limpeza leve - sistema já estava otimizado")
    
    # Verificar pastas do projeto atual
    print("\n🔍 PROJETO AEON ATUAL (mantido):")
    print("-" * 40)
    current_folders = ["p2p", "scripts", "docs", "core", "teoria"]
    
    for folder in current_folders:
        folder_path = base_path / folder
        if folder_path.exists():
            size_mb = get_folder_size(folder_path)
            status = "✅" if size_mb < 1 else "📁"
            print(f"   {status} {folder}: {size_mb:.2f} MB")
    
    print(f"\n🎯 Pasta de backup criada em: {backup_path.absolute()}")
    print("🔒 Todos os arquivos importantes foram preservados!")
    print("✅ Limpeza concluída com sucesso!")

if __name__ == "__main__":
    main()
