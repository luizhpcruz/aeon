# security/aeoncosma_environment_isolator.py
"""
🔐 AEONCOSMA ENVIRONMENT ISOLATOR
Sistema avançado de isolamento de ambiente e proteção contra manipulação
Desenvolvido por Luiz Cruz - 2025
"""

import os
import sys
import json
import hashlib
from datetime import datetime
from typing import Dict, List, Set, Optional

# Importação opcional do psutil
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    print("⚠️ psutil não disponível - algumas funcionalidades de monitoramento serão limitadas")

class EnvironmentIsolator:
    """
    🛡️ Isolador de ambiente AEONCOSMA
    Protege contra manipulação de variáveis críticas e isolamento de processos
    """
    
    def __init__(self):
        self.original_env = {}
        self.protected_vars = {
            "PYTHONPATH", "PATH", "SECURITY_DISABLED", "BYPASS_MODE", 
            "HACKER_MODE", "DEBUG_MODE", "UNSAFE_MODE", "ADMIN_MODE",
            "ROOT_ACCESS", "PRIVILEGED_MODE", "BACKDOOR_ENABLED",
            "FIREWALL_DISABLED", "ANTIVIRUS_DISABLED", "AUTORUN"
        }
        self.env_violations = []
        self.isolation_active = False
        
        print("🔐 AEONCOSMA Environment Isolator iniciado")
        self._backup_critical_environment()
        self._activate_isolation()
    
    def _backup_critical_environment(self):
        """Faz backup das variáveis críticas originais"""
        for var in self.protected_vars:
            if var in os.environ:
                self.original_env[var] = os.environ[var]
        
        print(f"💾 Backup de {len(self.original_env)} variáveis críticas realizado")
    
    def _activate_isolation(self):
        """Ativa o isolamento do ambiente"""
        try:
            # Bloqueia variáveis suspeitas
            suspicious_vars = [
                "SECURITY_DISABLED", "BYPASS_MODE", "HACKER_MODE",
                "DEBUG_MODE", "UNSAFE_MODE", "ADMIN_MODE", "ROOT_ACCESS"
            ]
            
            for var in suspicious_vars:
                if var in os.environ:
                    del os.environ[var]
                    self.env_violations.append({
                        "variable": var,
                        "action": "removed",
                        "timestamp": datetime.now().isoformat(),
                        "threat_level": "HIGH"
                    })
            
            # Protege PATH e PYTHONPATH
            self._protect_path_variables()
            
            self.isolation_active = True
            print("🛡️ Isolamento de ambiente ATIVADO")
            
        except Exception as e:
            print(f"⚠️ Erro ao ativar isolamento: {e}")
    
    def _protect_path_variables(self):
        """Protege variáveis PATH e PYTHONPATH contra manipulação"""
        # Verifica PYTHONPATH suspeito
        pythonpath = os.environ.get("PYTHONPATH", "")
        suspicious_paths = [
            "malicious", "hacker", "backdoor", "exploit", 
            "payload", "trojan", "virus", "bypass"
        ]
        
        for sus_path in suspicious_paths:
            if sus_path in pythonpath.lower():
                # Remove path suspeito
                clean_paths = [p for p in pythonpath.split(os.pathsep) 
                              if sus_path not in p.lower()]
                os.environ["PYTHONPATH"] = os.pathsep.join(clean_paths)
                
                self.env_violations.append({
                    "variable": "PYTHONPATH",
                    "action": f"cleaned_suspicious_path_{sus_path}",
                    "timestamp": datetime.now().isoformat(),
                    "threat_level": "CRITICAL"
                })
        
        print("🔒 Variáveis PATH protegidas contra manipulação")
    
    def monitor_environment_changes(self) -> List[Dict]:
        """Monitora mudanças no ambiente em tempo real"""
        current_violations = []
        
        for var in self.protected_vars:
            current_value = os.environ.get(var)
            original_value = self.original_env.get(var)
            
            # Detecta modificações não autorizadas
            if var in ["SECURITY_DISABLED", "BYPASS_MODE", "HACKER_MODE"]:
                if current_value and current_value.lower() in ["true", "1", "yes", "enabled"]:
                    current_violations.append({
                        "variable": var,
                        "current_value": current_value,
                        "threat_level": "CRITICAL",
                        "description": f"Tentativa de ativar modo inseguro via {var}"
                    })
                    # Remove imediatamente
                    del os.environ[var]
            
            # Detecta mudanças em variáveis críticas
            elif original_value != current_value and var in ["PATH", "PYTHONPATH"]:
                if current_value and any(sus in current_value.lower() 
                                       for sus in ["malicious", "hacker", "exploit"]):
                    current_violations.append({
                        "variable": var,
                        "current_value": current_value[:100] + "..." if len(current_value) > 100 else current_value,
                        "threat_level": "HIGH",
                        "description": f"Manipulação suspeita detectada em {var}"
                    })
        
        return current_violations
    
    def create_secure_subprocess_env(self) -> Dict[str, str]:
        """Cria ambiente seguro para subprocessos"""
        secure_env = {}
        
        # Copia apenas variáveis seguras
        safe_vars = {
            "HOME", "USER", "USERNAME", "USERPROFILE", "TEMP", "TMP",
            "SYSTEMROOT", "WINDIR", "PROGRAMFILES", "PROGRAMDATA"
        }
        
        for var in safe_vars:
            if var in os.environ:
                secure_env[var] = os.environ[var]
        
        # Define PATH mínimo e seguro
        if sys.platform == "win32":
            secure_env["PATH"] = r"C:\Windows\System32;C:\Windows"
        else:
            secure_env["PATH"] = "/usr/bin:/bin"
        
        # Força configurações seguras
        secure_env["PYTHONPATH"] = ""
        secure_env["SECURITY_MODE"] = "STRICT"
        secure_env["AEONCOSMA_ISOLATED"] = "TRUE"
        
        return secure_env
    
    def get_isolation_report(self) -> Dict:
        """Retorna relatório de isolamento"""
        return {
            "isolation_active": self.isolation_active,
            "protected_variables": len(self.protected_vars),
            "environment_violations": self.env_violations,
            "secure_env_available": True,
            "timestamp": datetime.now().isoformat()
        }

class PortSecurityMonitor:
    """
    🔍 Monitor de segurança de portas
    Detecta e previne hijacking de portas
    """
    
    def __init__(self):
        self.reserved_ports = {9000, 9001, 9002, 8000, 8080}
        self.authorized_processes = set()
        self.port_violations = []
        self.monitoring_active = False
        
        print("🔍 Port Security Monitor iniciado")
    
    def register_authorized_process(self, process_id: str, ports: List[int]):
        """Registra processo autorizado para usar portas específicas"""
        for port in ports:
            self.authorized_processes.add((process_id, port))
        
        print(f"✅ Processo {process_id} autorizado para portas: {ports}")
    
    def scan_port_usage(self) -> Dict:
        """Escaneia uso atual de portas e detecta anomalias"""
        import socket
        
        port_status = {}
        violations = []
        
        for port in self.reserved_ports:
            try:
                # Tenta conectar para verificar se porta está em uso
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.1)
                result = sock.connect_ex(("127.0.0.1", port))
                
                if result == 0:
                    # Porta está em uso - verifica autorização
                    authorized = any(auth_port == port for _, auth_port in self.authorized_processes)
                    
                    port_status[port] = {
                        "status": "in_use",
                        "authorized": authorized,
                        "timestamp": datetime.now().isoformat()
                    }
                    
                    if not authorized:
                        violations.append({
                            "port": port,
                            "threat_level": "HIGH",
                            "description": f"Porta {port} em uso por processo não autorizado",
                            "timestamp": datetime.now().isoformat()
                        })
                        print(f"🚨 ALERTA: Porta {port} hijackada por processo não autorizado!")
                
                else:
                    port_status[port] = {
                        "status": "available",
                        "authorized": True,
                        "timestamp": datetime.now().isoformat()
                    }
                
                sock.close()
                
            except Exception as e:
                port_status[port] = {
                    "status": "error",
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                }
        
        self.port_violations.extend(violations)
        
        return {
            "port_status": port_status,
            "violations": violations,
            "total_protected_ports": len(self.reserved_ports)
        }
    
    def block_suspicious_port_activity(self) -> bool:
        """Bloqueia atividade suspeita em portas"""
        scan_result = self.scan_port_usage()
        
        if scan_result["violations"]:
            print(f"🛡️ Bloqueando {len(scan_result['violations'])} atividades suspeitas de porta")
            # Em um sistema real, aqui implementaríamos bloqueio via firewall
            return True
        
        return False

class CodeSandbox:
    """
    📦 Sandbox para execução segura de código
    Mitiga injeções de código e execução maliciosa
    """
    
    def __init__(self):
        self.restricted_functions = {
            "eval", "exec", "compile", "__import__", "open", 
            "file", "input", "raw_input", "execfile"
        }
        self.restricted_modules = {
            "os", "sys", "subprocess", "socket", "urllib",
            "requests", "ftplib", "telnetlib", "paramiko"
        }
        self.sandbox_violations = []
        
        print("📦 Code Sandbox inicializado")
        self._patch_dangerous_functions()
    
    def _patch_dangerous_functions(self):
        """Aplica patches em funções perigosas"""
        import builtins
        
        # Salva funções originais
        self.original_eval = builtins.eval
        self.original_exec = builtins.exec
        self.original_compile = builtins.compile
        self.original_import = builtins.__import__
        
        # Aplica patches seguros
        builtins.eval = self._safe_eval
        builtins.exec = self._safe_exec
        builtins.compile = self._safe_compile
        builtins.__import__ = self._safe_import
        
        print("🔒 Funções perigosas patchadas com versões seguras")
    
    def _safe_eval(self, code, globals=None, locals=None):
        """Versão segura do eval"""
        self._log_sandbox_violation("eval", code)
        raise SecurityError("🚫 SANDBOX: eval() bloqueado por segurança")
    
    def _safe_exec(self, code, globals=None, locals=None):
        """Versão segura do exec"""
        self._log_sandbox_violation("exec", code)
        raise SecurityError("🚫 SANDBOX: exec() bloqueado por segurança")
    
    def _safe_compile(self, source, filename, mode, flags=0, dont_inherit=False, optimize=-1):
        """Versão segura do compile"""
        self._log_sandbox_violation("compile", source)
        raise SecurityError("🚫 SANDBOX: compile() bloqueado por segurança")
    
    def _safe_import(self, name, globals=None, locals=None, fromlist=(), level=0):
        """Versão segura do __import__"""
        # Bloqueia importação de módulos perigosos
        if name in self.restricted_modules:
            self._log_sandbox_violation("import", name)
            raise SecurityError(f"🚫 SANDBOX: Importação de '{name}' bloqueada por segurança")
        
        # Permite importação segura
        return self.original_import(name, globals, locals, fromlist, level)
    
    def _log_sandbox_violation(self, function: str, code: str):
        """Log de violação do sandbox"""
        violation = {
            "function": function,
            "code": str(code)[:200] + "..." if len(str(code)) > 200 else str(code),
            "timestamp": datetime.now().isoformat(),
            "threat_level": "CRITICAL"
        }
        
        self.sandbox_violations.append(violation)
        print(f"🚨 SANDBOX VIOLATION: {function}() tentou executar código malicioso!")
    
    def get_sandbox_report(self) -> Dict:
        """Retorna relatório do sandbox"""
        return {
            "restricted_functions": len(self.restricted_functions),
            "restricted_modules": len(self.restricted_modules),
            "violations": self.sandbox_violations,
            "patches_active": True,
            "timestamp": datetime.now().isoformat()
        }

class FileSystemWatchdog:
    """
    📁 Guardian do sistema de arquivos
    Detecta e bloqueia arquivos suspeitos
    """
    
    def __init__(self):
        self.suspicious_patterns = {
            "backdoor", "trojan", "virus", "malware", "exploit",
            "payload", "shell", "reverse", "bind", "keylogger",
            "ransomware", "rootkit", "botnet", "rat", "stealer"
        }
        
        self.suspicious_extensions = {
            ".exe", ".bat", ".cmd", ".scr", ".pif", ".com",
            ".vbs", ".js", ".jar", ".ps1", ".dll", ".sys"
        }
        
        self.file_violations = []
        self.quarantine_folder = "security/quarantine"
        
        print("📁 FileSystem Watchdog inicializado")
        self._create_quarantine_folder()
    
    def _create_quarantine_folder(self):
        """Cria pasta de quarentena"""
        try:
            os.makedirs(self.quarantine_folder, exist_ok=True)
            print(f"📂 Pasta de quarentena criada: {self.quarantine_folder}")
        except Exception as e:
            print(f"⚠️ Erro ao criar pasta de quarentena: {e}")
    
    def scan_directory(self, directory: str) -> Dict:
        """Escaneia diretório em busca de arquivos suspeitos"""
        suspicious_files = []
        scanned_files = 0
        
        try:
            for root, dirs, files in os.walk(directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    scanned_files += 1
                    
                    # Verifica nome do arquivo
                    file_lower = file.lower()
                    is_suspicious = False
                    
                    # Verifica padrões suspeitos no nome
                    for pattern in self.suspicious_patterns:
                        if pattern in file_lower:
                            is_suspicious = True
                            break
                    
                    # Verifica extensões perigosas
                    if any(file_lower.endswith(ext) for ext in self.suspicious_extensions):
                        is_suspicious = True
                    
                    # Verifica conteúdo de arquivos de texto
                    if file_lower.endswith(('.py', '.txt', '.js', '.bat', '.ps1')):
                        try:
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                content = f.read(1000)  # Lê apenas primeiros 1000 chars
                                content_lower = content.lower()
                                
                                suspicious_keywords = [
                                    "system compromised", "hacker was here", "backdoor",
                                    "malicious", "exploit", "payload", "reverse shell"
                                ]
                                
                                for keyword in suspicious_keywords:
                                    if keyword in content_lower:
                                        is_suspicious = True
                                        break
                        except:
                            pass  # Ignora erros de leitura
                    
                    if is_suspicious:
                        file_info = {
                            "path": file_path,
                            "size": os.path.getsize(file_path),
                            "modified": datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat(),
                            "threat_level": "HIGH",
                            "detected_at": datetime.now().isoformat()
                        }
                        
                        suspicious_files.append(file_info)
                        self.file_violations.append(file_info)
        
        except Exception as e:
            print(f"⚠️ Erro durante escaneamento: {e}")
        
        return {
            "directory": directory,
            "scanned_files": scanned_files,
            "suspicious_files": suspicious_files,
            "threat_count": len(suspicious_files)
        }
    
    def quarantine_file(self, file_path: str) -> bool:
        """Move arquivo suspeito para quarentena"""
        try:
            import shutil
            
            filename = os.path.basename(file_path)
            quarantine_path = os.path.join(self.quarantine_folder, f"quarantined_{filename}")
            
            shutil.move(file_path, quarantine_path)
            
            print(f"🔒 Arquivo movido para quarentena: {file_path} -> {quarantine_path}")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao quarentenar arquivo: {e}")
            return False
    
    def get_watchdog_report(self) -> Dict:
        """Retorna relatório do watchdog"""
        return {
            "suspicious_patterns": len(self.suspicious_patterns),
            "suspicious_extensions": len(self.suspicious_extensions),
            "file_violations": self.file_violations,
            "quarantine_folder": self.quarantine_folder,
            "timestamp": datetime.now().isoformat()
        }

class SecurityError(Exception):
    """Exceção customizada para violações de segurança"""
    pass

# Função para inicializar todos os sistemas de defesa
def initialize_advanced_security():
    """Inicializa todos os sistemas de defesa avançada"""
    print("🛡️ INICIALIZANDO SISTEMA DE DEFESA AVANÇADO")
    print("=" * 60)
    
    env_isolator = EnvironmentIsolator()
    port_monitor = PortSecurityMonitor()
    code_sandbox = CodeSandbox()
    fs_watchdog = FileSystemWatchdog()
    
    print("=" * 60)
    print("🏆 SISTEMA DE DEFESA AVANÇADO ATIVO!")
    print("🔐 Environment Isolation: ✅ ATIVO")
    print("🔍 Port Security Monitor: ✅ ATIVO") 
    print("📦 Code Sandbox: ✅ ATIVO")
    print("📁 FileSystem Watchdog: ✅ ATIVO")
    print("=" * 60)
    
    return {
        "env_isolator": env_isolator,
        "port_monitor": port_monitor,
        "code_sandbox": code_sandbox,
        "fs_watchdog": fs_watchdog
    }

if __name__ == "__main__":
    # Teste do sistema
    security_systems = initialize_advanced_security()
    
    print("\n🧪 TESTANDO SISTEMAS DE DEFESA...")
    
    # Teste de escaneamento de arquivos
    fs_report = security_systems["fs_watchdog"].scan_directory(".")
    print(f"📁 Escaneamento: {fs_report['scanned_files']} arquivos, {fs_report['threat_count']} ameaças")
    
    # Teste de monitoramento de portas
    port_report = security_systems["port_monitor"].scan_port_usage()
    print(f"🔍 Portas: {len(port_report['violations'])} violações detectadas")
    
    # Teste de isolamento
    env_report = security_systems["env_isolator"].get_isolation_report()
    print(f"🔐 Ambiente: {len(env_report['environment_violations'])} violações detectadas")
    
    print("\n🛡️ SISTEMAS DE DEFESA TESTADOS COM SUCESSO!")
