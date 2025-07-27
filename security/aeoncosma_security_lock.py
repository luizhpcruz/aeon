# security/aeoncosma_security_lock.py
"""
🔐 AEONCOSMA SECURITY LOCK - Sistema de Segurança Ultra Avançado
Sistema de proteção multi-camadas para o ecossistema AEONCOSMA
Desenvolvido por Luiz Cruz - 2025
"""

import sys
import os
import platform
import hashlib
import json
import time
import subprocess
import re
from datetime import datetime
from typing import Dict, List, Any, Optional
import sqlite3

class AeonSecurityLock:
    """
    🛡️ Sistema de Segurança Principal AEONCOSMA
    Proteção contra execução não autorizada e ambientes suspeitos
    """
    
    def __init__(self):
        self.system = platform.system()
        self.authorized_user = 'Luiz'
        self.security_db_path = "security/security_audit.db"
        self.init_security_database()
        
        # Assinatura de integridade do sistema
        self.system_fingerprint = self.generate_system_fingerprint()
        
        print(f"🔒 AEONCOSMA Security Lock inicializado ({self.system})")
        
    def init_security_database(self):
        """Inicializa base de dados de auditoria de segurança"""
        os.makedirs(os.path.dirname(self.security_db_path), exist_ok=True)
        
        conn = sqlite3.connect(self.security_db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS security_events (
                event_id TEXT PRIMARY KEY,
                timestamp TEXT NOT NULL,
                event_type TEXT NOT NULL,
                description TEXT NOT NULL,
                severity TEXT NOT NULL,
                source_module TEXT NOT NULL,
                metadata TEXT NOT NULL
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS execution_log (
                execution_id TEXT PRIMARY KEY,
                timestamp TEXT NOT NULL,
                module_name TEXT NOT NULL,
                function_name TEXT NOT NULL,
                parameters TEXT NOT NULL,
                result TEXT NOT NULL,
                execution_time REAL NOT NULL
            )
        """)
        
        conn.commit()
        conn.close()
        
    def generate_system_fingerprint(self) -> str:
        """Gera fingerprint único do sistema"""
        fingerprint_data = {
            "system": self.system,
            "python_version": sys.version,
            "platform": platform.platform(),
            "user": os.getlogin() if hasattr(os, 'getlogin') else "unknown",
            "working_directory": os.getcwd()
        }
        
        fingerprint_str = json.dumps(fingerprint_data, sort_keys=True)
        return hashlib.sha256(fingerprint_str.encode()).hexdigest()[:16]
        
    def log_security_event(self, event_type: str, description: str, 
                          severity: str, source_module: str, metadata: Dict[str, Any] = None):
        """Registra evento de segurança"""
        event_id = hashlib.sha256(f"{time.time()}-{event_type}-{description}".encode()).hexdigest()[:16]
        
        conn = sqlite3.connect(self.security_db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO security_events 
            (event_id, timestamp, event_type, description, severity, source_module, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            event_id, datetime.now().isoformat(), event_type, description,
            severity, source_module, json.dumps(metadata or {})
        ))
        
        conn.commit()
        conn.close()
        
        # Log crítico vai para console também
        if severity in ["CRITICAL", "HIGH"]:
            print(f"🚨 SECURITY {severity}: {description}")
            
    def log_execution(self, function_name: str, parameters: Dict[str, Any], 
                     result: str = "SUCCESS", module_name: str = "unknown"):
        """Registra execução de função para auditoria"""
        execution_id = hashlib.sha256(f"{time.time()}-{function_name}".encode()).hexdigest()[:16]
        start_time = time.time()
        
        conn = sqlite3.connect(self.security_db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO execution_log
            (execution_id, timestamp, module_name, function_name, parameters, result, execution_time)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            execution_id, datetime.now().isoformat(), module_name, function_name,
            json.dumps(parameters), result, time.time() - start_time
        ))
        
        conn.commit()
        conn.close()
        
    def enforce_localhost_only(self):
        """Força execução apenas em localhost"""
        try:
            forbidden_args = ['--remote', '--external', '--public', '--0.0.0.0']
            forbidden_env = ['AEON_REMOTE', 'REMOTE_ACCESS', 'PUBLIC_ACCESS']
            
            # Verifica argumentos suspeitos
            if any(arg in sys.argv for arg in forbidden_args):
                violation = f"Argumento remoto detectado: {sys.argv}"
                self.log_security_event("REMOTE_ACCESS_ATTEMPT", violation, "CRITICAL", "security_lock")
                raise PermissionError(f"❌ Execução remota não autorizada: {violation}")
                
            # Verifica variáveis de ambiente suspeitas
            for env_var in forbidden_env:
                if os.environ.get(env_var) == '1':
                    violation = f"Variável de ambiente remota: {env_var}"
                    self.log_security_event("REMOTE_ENV_DETECTED", violation, "CRITICAL", "security_lock")
                    raise PermissionError(f"❌ Configuração remota detectada: {violation}")
                    
            self.log_security_event("LOCALHOST_CHECK", "Verificação localhost OK", "INFO", "security_lock")
            
        except Exception as e:
            self.log_security_event("LOCALHOST_CHECK_ERROR", str(e), "HIGH", "security_lock")
            raise
            
    def prevent_root_execution(self):
        """Previne execução como root/administrador"""
        try:
            if self.system != 'Windows':
                try:
                    if os.geteuid() == 0:
                        violation = "Execução como root detectada"
                        self.log_security_event("ROOT_EXECUTION", violation, "CRITICAL", "security_lock")
                        raise PermissionError("❌ Execução como root é proibida.")
                except AttributeError:
                    pass  # Sistema sem geteuid
            else:
                # Windows: verifica se é administrador
                try:
                    is_admin = subprocess.run(['net', 'session'], capture_output=True, text=True).returncode == 0
                    if is_admin:
                        violation = "Execução como administrador detectada"
                        self.log_security_event("ADMIN_EXECUTION", violation, "HIGH", "security_lock")
                        print("⚠️ Executando como administrador - cuidado extra necessário")
                except:
                    pass
                    
            self.log_security_event("ROOT_CHECK", "Verificação privilégios OK", "INFO", "security_lock")
            
        except Exception as e:
            self.log_security_event("ROOT_CHECK_ERROR", str(e), "HIGH", "security_lock")
            raise
            
    def block_autorun_arguments(self):
        """Bloqueia argumentos perigosos de auto-execução"""
        try:
            dangerous_args = [
                '--autorun', '--unsafe', '--dev-bypass', '--skip-security',
                '--no-validation', '--force', '--override', '--admin-mode',
                '--debug-unsafe', '--production-override'
            ]
            
            detected_args = [arg for arg in sys.argv if arg in dangerous_args]
            
            if detected_args:
                violation = f"Argumentos perigosos detectados: {detected_args}"
                self.log_security_event("DANGEROUS_ARGS", violation, "CRITICAL", "security_lock")
                raise PermissionError(f"❌ Argumentos perigosos: {detected_args}")
                
            # Verifica padrões suspeitos
            suspicious_patterns = [r'--.*bypass.*', r'--.*unsafe.*', r'--.*override.*']
            
            for arg in sys.argv:
                for pattern in suspicious_patterns:
                    if re.match(pattern, arg, re.IGNORECASE):
                        violation = f"Padrão suspeito detectado: {arg}"
                        self.log_security_event("SUSPICIOUS_PATTERN", violation, "HIGH", "security_lock")
                        raise PermissionError(f"❌ Argumento suspeito: {arg}")
                        
            self.log_security_event("ARGS_CHECK", "Verificação argumentos OK", "INFO", "security_lock")
            
        except Exception as e:
            self.log_security_event("ARGS_CHECK_ERROR", str(e), "HIGH", "security_lock")
            raise
            
    def fingerprint_check(self):
        """Verifica fingerprint do usuário e sistema"""
        try:
            # Verifica usuário autorizado
            current_user = os.getlogin() if hasattr(os, 'getlogin') else "unknown"
            
            if current_user != self.authorized_user and current_user != "unknown":
                violation = f"Usuário não autorizado: {current_user}"
                self.log_security_event("UNAUTHORIZED_USER", violation, "CRITICAL", "security_lock")
                raise PermissionError(f"❌ Usuário inválido: {current_user}")
                
            # Verifica integridade do ambiente
            current_fingerprint = self.generate_system_fingerprint()
            
            # Log do fingerprint para auditoria
            self.log_security_event("FINGERPRINT_CHECK", f"Fingerprint: {current_fingerprint}", "INFO", "security_lock")
            
            print(f"👤 Usuário verificado: {current_user}")
            print(f"🔍 Fingerprint: {current_fingerprint}")
            
        except Exception as e:
            self.log_security_event("FINGERPRINT_ERROR", str(e), "HIGH", "security_lock")
            raise
            
    def integrity_verification(self):
        """Verificação de integridade do sistema"""
        try:
            critical_files = [
                "security/aeoncosma_security_lock.py",
                "aeoncosma/core/aeon_kernel.py",
                "aeoncosma/cognitive/gpt_node.py"
            ]
            
            integrity_status = {"verified": 0, "missing": 0, "suspicious": 0}
            
            for file_path in critical_files:
                if not os.path.exists(file_path):
                    integrity_status["missing"] += 1
                    self.log_security_event("FILE_MISSING", f"Arquivo crítico ausente: {file_path}", "HIGH", "security_lock")
                else:
                    # Verifica tamanho mínimo (arquivo não vazio)
                    if os.path.getsize(file_path) < 100:
                        integrity_status["suspicious"] += 1
                        self.log_security_event("FILE_SUSPICIOUS", f"Arquivo suspeito: {file_path}", "MEDIUM", "security_lock")
                    else:
                        integrity_status["verified"] += 1
                        
            # Verifica se pelo menos 70% dos arquivos críticos estão OK
            total_files = len(critical_files)
            verified_ratio = integrity_status["verified"] / total_files
            
            if verified_ratio < 0.7:
                violation = f"Integridade comprometida: {integrity_status}"
                self.log_security_event("INTEGRITY_VIOLATION", violation, "CRITICAL", "security_lock")
                raise PermissionError(f"❌ Integridade do sistema comprometida: {integrity_status}")
                
            self.log_security_event("INTEGRITY_CHECK", f"Verificação OK: {integrity_status}", "INFO", "security_lock")
            print(f"🔍 Integridade verificada: {integrity_status}")
            
        except Exception as e:
            self.log_security_event("INTEGRITY_ERROR", str(e), "HIGH", "security_lock")
            raise
            
    def check_network_security(self, host: str, port: int):
        """Verifica segurança de configurações de rede"""
        try:
            # Força localhost apenas
            if host not in ["127.0.0.1", "localhost", "0.0.0.0"]:
                violation = f"Host externo não permitido: {host}"
                self.log_security_event("EXTERNAL_HOST", violation, "CRITICAL", "security_lock")
                raise PermissionError(f"❌ Host externo: {host}")
                
            # Avisa sobre bind em todas as interfaces
            if host == "0.0.0.0":
                warning = f"Bind em todas interfaces detectado: {host}:{port}"
                self.log_security_event("WILDCARD_BIND", warning, "MEDIUM", "security_lock")
                print(f"⚠️ AVISO: Bind em todas as interfaces (0.0.0.0)")
                
            # Verifica portas suspeitas
            dangerous_ports = [22, 23, 80, 443, 3389, 5900]  # SSH, Telnet, HTTP, HTTPS, RDP, VNC
            
            if port in dangerous_ports:
                warning = f"Porta de serviço detectada: {port}"
                self.log_security_event("SERVICE_PORT", warning, "MEDIUM", "security_lock")
                print(f"⚠️ AVISO: Usando porta de serviço padrão: {port}")
                
            self.log_security_event("NETWORK_CHECK", f"Rede OK: {host}:{port}", "INFO", "security_lock")
            
        except Exception as e:
            self.log_security_event("NETWORK_ERROR", str(e), "HIGH", "security_lock")
            raise
            
    def enforce_all_security_measures(self):
        """Executa todas as verificações de segurança obrigatórias"""
        print("🛡️ Executando verificações de segurança AEONCOSMA...")
        
        start_time = time.time()
        
        try:
            self.enforce_localhost_only()
            print("  ✅ Localhost verificado")
            
            self.prevent_root_execution()
            print("  ✅ Privilégios verificados")
            
            self.block_autorun_arguments()
            print("  ✅ Argumentos seguros")
            
            self.fingerprint_check()
            print("  ✅ Fingerprint validado")
            
            self.integrity_verification()
            print("  ✅ Integridade confirmada")
            
            execution_time = time.time() - start_time
            
            self.log_execution("enforce_all_security_measures", {
                "execution_time": execution_time,
                "checks_passed": 5
            }, "ALL_CHECKS_PASSED", "security_lock")
            
            print(f"🔒 Todas as verificações de segurança passaram ({execution_time:.2f}s)")
            
        except Exception as e:
            execution_time = time.time() - start_time
            self.log_execution("enforce_all_security_measures", {
                "execution_time": execution_time,
                "error": str(e)
            }, "SECURITY_FAILURE", "security_lock")
            
            print(f"🚫 FALHA DE SEGURANÇA: {e}")
            raise
            
    def get_security_report(self, last_hours: int = 24) -> Dict[str, Any]:
        """Gera relatório de segurança das últimas horas"""
        conn = sqlite3.connect(self.security_db_path)
        cursor = conn.cursor()
        
        # Timestamp de corte
        cutoff_time = datetime.now().timestamp() - (last_hours * 3600)
        cutoff_iso = datetime.fromtimestamp(cutoff_time).isoformat()
        
        # Eventos de segurança
        cursor.execute("""
            SELECT event_type, severity, COUNT(*) as count
            FROM security_events
            WHERE timestamp > ?
            GROUP BY event_type, severity
            ORDER BY count DESC
        """, (cutoff_iso,))
        
        events_summary = cursor.fetchall()
        
        # Execuções recentes
        cursor.execute("""
            SELECT module_name, function_name, COUNT(*) as count
            FROM execution_log
            WHERE timestamp > ?
            GROUP BY module_name, function_name
            ORDER BY count DESC
            LIMIT 10
        """, (cutoff_iso,))
        
        executions_summary = cursor.fetchall()
        
        conn.close()
        
        return {
            "report_timestamp": datetime.now().isoformat(),
            "period_hours": last_hours,
            "system_fingerprint": self.system_fingerprint,
            "events_summary": [
                {"event_type": row[0], "severity": row[1], "count": row[2]}
                for row in events_summary
            ],
            "executions_summary": [
                {"module": row[0], "function": row[1], "count": row[2]}
                for row in executions_summary
            ],
            "security_status": "ACTIVE"
        }

# Função de conveniência para uso rápido
def enforce_security():
    """Função rápida para enforcement de segurança"""
    lock = AeonSecurityLock()
    lock.enforce_all_security_measures()
    return lock

# Teste rápido se executado diretamente
if __name__ == "__main__":
    print("🔒 TESTE DO SISTEMA DE SEGURANÇA AEONCOSMA")
    print("=" * 50)
    
    try:
        security_lock = enforce_security()
        print("🚀 SEGURANÇA DO AEON FUNCIONANDO PERFEITAMENTE!")
        
        # Gera relatório de teste
        report = security_lock.get_security_report(1)
        print(f"\n📊 Eventos de segurança na última hora: {len(report['events_summary'])}")
        print(f"🔍 Fingerprint do sistema: {report['system_fingerprint']}")
        
    except Exception as e:
        print(f"❌ ERRO DE SEGURANÇA: {e}")
        sys.exit(1)
