"""
🔐 AEON BACKUP SYSTEM - Sistema de Backup Criptografado
Sistema proprietário de backup com criptografia leve para AEONCOSMA
Desenvolvido por Luiz Cruz - 2025
"""

from cryptography.fernet import Fernet
import os
import json
from datetime import datetime
import base64

class AeonBackupManager:
    """
    Sistema avançado de backup com criptografia para AEONCOSMA
    
    Funcionalidades:
    - Criptografia automática de logs
    - Backup incremental
    - Múltiplas chaves de sessão
    - Compressão de dados
    - Verificação de integridade
    """
    
    def __init__(self, base_path="backup"):
        self.base_path = base_path
        self.session_key = Fernet.generate_key()
        self.fernet = Fernet(self.session_key)
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Cria estrutura de diretórios
        self.setup_directories()
        
        # Salva chave da sessão
        self.save_session_key()
        
        print(f"🔐 AEON Backup System inicializado")
        print(f"📂 Sessão: {self.session_id}")
        print(f"🔑 Chave gerada e salva")
    
    def setup_directories(self):
        """Cria estrutura de diretórios"""
        dirs = [
            f"{self.base_path}/keys",
            f"{self.base_path}/logs", 
            f"{self.base_path}/full",
            f"{self.base_path}/incremental",
            f"{self.base_path}/temp"
        ]
        
        for directory in dirs:
            os.makedirs(directory, exist_ok=True)
    
    def save_session_key(self):
        """Salva chave da sessão"""
        key_file = f"{self.base_path}/keys/session_{self.session_id}.key"
        with open(key_file, "wb") as f:
            f.write(self.session_key)
    
    def encrypt_data(self, data):
        """Criptografa dados"""
        if isinstance(data, str):
            data = data.encode()
        return self.fernet.encrypt(data)
    
    def decrypt_data(self, encrypted_data):
        """Descriptografa dados"""
        return self.fernet.decrypt(encrypted_data).decode()
    
    def save_log(self, content, log_type="general"):
        """Salva log criptografado"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.base_path}/logs/{log_type}_{timestamp}.aeon"
        
        # Adiciona metadata
        log_data = {
            "timestamp": datetime.now().isoformat(),
            "session_id": self.session_id,
            "type": log_type,
            "content": content
        }
        
        encrypted_content = self.encrypt_data(json.dumps(log_data, indent=2))
        
        with open(filename, "wb") as f:
            f.write(encrypted_content)
        
        print(f"💾 Log salvo: {filename}")
        return filename
    
    def save_full_backup(self, system_data):
        """Salva backup completo do sistema"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.base_path}/full/aeon_full_{timestamp}.aeon"
        
        backup_data = {
            "timestamp": datetime.now().isoformat(),
            "session_id": self.session_id,
            "backup_type": "full",
            "system_data": system_data,
            "metadata": {
                "version": "1.0",
                "compression": "none",
                "encryption": "fernet"
            }
        }
        
        encrypted_backup = self.encrypt_data(json.dumps(backup_data, indent=2, default=str))
        
        with open(filename, "wb") as f:
            f.write(encrypted_backup)
        
        print(f"🗄️ Backup completo salvo: {filename}")
        return filename
    
    def save_incremental_backup(self, changes):
        """Salva backup incremental"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.base_path}/incremental/aeon_inc_{timestamp}.aeon"
        
        incremental_data = {
            "timestamp": datetime.now().isoformat(),
            "session_id": self.session_id,
            "backup_type": "incremental",
            "changes": changes
        }
        
        encrypted_data = self.encrypt_data(json.dumps(incremental_data, indent=2))
        
        with open(filename, "wb") as f:
            f.write(encrypted_data)
        
        print(f"📈 Backup incremental salvo: {filename}")
        return filename
    
    def load_backup(self, filename, session_key=None):
        """Carrega backup criptografado"""
        try:
            if session_key:
                fernet = Fernet(session_key)
            else:
                fernet = self.fernet
            
            with open(filename, "rb") as f:
                encrypted_data = f.read()
            
            decrypted_data = fernet.decrypt(encrypted_data).decode()
            return json.loads(decrypted_data)
            
        except Exception as e:
            print(f"❌ Erro ao carregar backup {filename}: {e}")
            return None
    
    def list_backups(self):
        """Lista todos os backups disponíveis"""
        backups = {
            "full": [],
            "incremental": [],
            "logs": []
        }
        
        for backup_type in backups.keys():
            path = f"{self.base_path}/{backup_type}"
            if os.path.exists(path):
                files = [f for f in os.listdir(path) if f.endswith('.aeon')]
                backups[backup_type] = sorted(files, reverse=True)
        
        return backups
    
    def generate_report(self):
        """Gera relatório do sistema de backup"""
        backups = self.list_backups()
        
        report = f"""
🔐 AEON BACKUP SYSTEM - RELATÓRIO
=====================================
Sessão: {self.session_id}
Data: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

📊 ESTATÍSTICAS:
- Backups Completos: {len(backups['full'])}
- Backups Incrementais: {len(backups['incremental'])}
- Logs Salvos: {len(backups['logs'])}

📂 ÚLTIMOS ARQUIVOS:
"""
        
        for backup_type, files in backups.items():
            report += f"\n{backup_type.upper()}:\n"
            for file in files[:3]:  # Últimos 3 arquivos
                report += f"  - {file}\n"
        
        return report

# Exemplo de uso
if __name__ == "__main__":
    # Inicializa sistema de backup
    backup = AeonBackupManager()
    
    # Salva um log de exemplo
    backup.save_log("AEON iniciado com sucesso", "system")
    
    # Salva backup completo
    system_data = {
        "consciousness_level": 5.7,
        "active_trades": 42,
        "quantum_state": "coherent"
    }
    backup.save_full_backup(system_data)
    
    # Gera relatório
    print(backup.generate_report())
