# security/aeoncosma_audit_monitor.py
"""
🕵️ AEONCOSMA AUDIT MONITOR - Sistema de Auditoria Avançado
Monitora comportamentos suspeitos e atividades maliciosas
Desenvolvido por Luiz Cruz - 2025
"""

import os
import sys
import json
import time
import hashlib
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import logging

@dataclass
class SecurityEvent:
    """Evento de segurança detectado"""
    timestamp: str
    event_type: str
    severity: str  # low, medium, high, critical
    description: str
    node_id: str
    details: Dict[str, Any]
    source_ip: str = "127.0.0.1"

class AeonAuditMonitor:
    """
    Monitor de auditoria para AEONCOSMA
    Detecta padrões suspeitos e atividades maliciosas
    """
    
    def __init__(self, node_id: str = "monitor"):
        self.node_id = node_id
        self.events: List[SecurityEvent] = []
        self.suspicious_patterns = {
            "rapid_connections": {"threshold": 10, "window": 60},  # 10 conexões em 60s
            "failed_validations": {"threshold": 5, "window": 300}, # 5 falhas em 5min
            "unusual_ports": {"ports": list(range(1, 1024))},      # Portas privilegiadas
            "external_ips": {"pattern": r"^(?!127\.|10\.|192\.168\.|172\.16\.)"},
            "suspicious_args": {"args": ["--daemon", "--silent", "--autorun", "--stealth"]},
            "mass_broadcasting": {"threshold": 100, "window": 60}, # 100 broadcasts em 60s
        }
        
        self.connection_history = []
        self.validation_history = []
        self.broadcast_history = []
        
        # Setup logging
        self.setup_logging()
        
        # Thread de monitoramento contínuo
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self.continuous_monitoring, daemon=True)
        self.monitor_thread.start()
        
        print(f"🕵️ AEONCOSMA Audit Monitor iniciado para [{node_id}]")
    
    def setup_logging(self):
        """Configura sistema de logging"""
        log_dir = "security/logs"
        os.makedirs(log_dir, exist_ok=True)
        
        # Logger para eventos de segurança
        self.security_logger = logging.getLogger('aeoncosma_security')
        self.security_logger.setLevel(logging.INFO)
        
        # Handler para arquivo
        log_file = os.path.join(log_dir, f"security_audit_{datetime.now().strftime('%Y%m%d')}.log")
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        
        # Formato do log
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        
        self.security_logger.addHandler(file_handler)
    
    def log_connection_attempt(self, peer_info: Dict, source_ip: str = "127.0.0.1"):
        """Log de tentativa de conexão"""
        self.connection_history.append({
            "timestamp": datetime.now(),
            "peer_info": peer_info,
            "source_ip": source_ip
        })
        
        # Verifica padrões suspeitos
        self.check_rapid_connections(source_ip)
        self.check_unusual_ports(peer_info.get("port", 0))
        self.check_external_ips(source_ip)
    
    def log_validation_result(self, peer_id: str, result: bool, reason: str = ""):
        """Log de resultado de validação"""
        self.validation_history.append({
            "timestamp": datetime.now(),
            "peer_id": peer_id,
            "result": result,
            "reason": reason
        })
        
        if not result:
            self.check_failed_validations(peer_id)
    
    def log_broadcast_event(self, message_type: str, targets: int):
        """Log de evento de broadcast"""
        self.broadcast_history.append({
            "timestamp": datetime.now(),
            "message_type": message_type,
            "targets": targets
        })
        
        self.check_mass_broadcasting()
    
    def check_rapid_connections(self, source_ip: str):
        """Detecta conexões rápidas suspeitas"""
        cutoff_time = datetime.now() - timedelta(seconds=self.suspicious_patterns["rapid_connections"]["window"])
        recent_connections = [
            c for c in self.connection_history 
            if c["timestamp"] > cutoff_time and c["source_ip"] == source_ip
        ]
        
        if len(recent_connections) > self.suspicious_patterns["rapid_connections"]["threshold"]:
            self.create_security_event(
                event_type="rapid_connections",
                severity="high",
                description=f"Conexões rápidas suspeitas detectadas de {source_ip}",
                details={"count": len(recent_connections), "source_ip": source_ip}
            )
    
    def check_failed_validations(self, peer_id: str):
        """Detecta falhas de validação suspeitas"""
        cutoff_time = datetime.now() - timedelta(seconds=self.suspicious_patterns["failed_validations"]["window"])
        recent_failures = [
            v for v in self.validation_history 
            if v["timestamp"] > cutoff_time and v["peer_id"] == peer_id and not v["result"]
        ]
        
        if len(recent_failures) > self.suspicious_patterns["failed_validations"]["threshold"]:
            self.create_security_event(
                event_type="repeated_validation_failures",
                severity="medium",
                description=f"Múltiplas falhas de validação para {peer_id}",
                details={"failures": len(recent_failures), "peer_id": peer_id}
            )
    
    def check_unusual_ports(self, port: int):
        """Detecta uso de portas suspeitas"""
        if port in self.suspicious_patterns["unusual_ports"]["ports"]:
            self.create_security_event(
                event_type="unusual_port_usage",
                severity="medium",
                description=f"Uso de porta privilegiada detectado: {port}",
                details={"port": port}
            )
    
    def check_external_ips(self, ip: str):
        """Detecta tentativas de conexão externa"""
        if not (ip.startswith("127.") or ip.startswith("10.") or 
                ip.startswith("192.168.") or ip.startswith("172.16.")):
            self.create_security_event(
                event_type="external_ip_attempt",
                severity="critical",
                description=f"Tentativa de conexão externa detectada: {ip}",
                details={"external_ip": ip}
            )
    
    def check_mass_broadcasting(self):
        """Detecta broadcasting em massa suspeito"""
        cutoff_time = datetime.now() - timedelta(seconds=self.suspicious_patterns["mass_broadcasting"]["window"])
        recent_broadcasts = [
            b for b in self.broadcast_history 
            if b["timestamp"] > cutoff_time
        ]
        
        total_targets = sum(b["targets"] for b in recent_broadcasts)
        
        if total_targets > self.suspicious_patterns["mass_broadcasting"]["threshold"]:
            self.create_security_event(
                event_type="mass_broadcasting",
                severity="high",
                description=f"Broadcasting em massa detectado: {total_targets} alvos",
                details={"total_targets": total_targets, "broadcasts": len(recent_broadcasts)}
            )
    
    def check_suspicious_arguments(self, args: List[str]):
        """Verifica argumentos suspeitos na linha de comando"""
        suspicious_found = []
        
        for arg in args:
            for suspicious_arg in self.suspicious_patterns["suspicious_args"]["args"]:
                if suspicious_arg.lower() in arg.lower():
                    suspicious_found.append(arg)
        
        if suspicious_found:
            self.create_security_event(
                event_type="suspicious_arguments",
                severity="high",
                description=f"Argumentos suspeitos detectados: {suspicious_found}",
                details={"arguments": suspicious_found}
            )
    
    def create_security_event(self, event_type: str, severity: str, description: str, details: Dict):
        """Cria um evento de segurança"""
        event = SecurityEvent(
            timestamp=datetime.now().isoformat(),
            event_type=event_type,
            severity=severity,
            description=description,
            node_id=self.node_id,
            details=details
        )
        
        self.events.append(event)
        
        # Log do evento
        self.security_logger.warning(f"SECURITY_EVENT | {severity.upper()} | {event_type} | {description} | {json.dumps(details)}")
        
        # Alerta no console para eventos críticos
        if severity == "critical":
            print(f"🚨 ALERTA CRÍTICO DE SEGURANÇA: {description}")
            print(f"   Detalhes: {details}")
        elif severity == "high":
            print(f"⚠️ ALERTA DE SEGURANÇA: {description}")
    
    def continuous_monitoring(self):
        """Monitoramento contínuo em background"""
        while self.monitoring:
            try:
                time.sleep(10)  # Verifica a cada 10 segundos
                
                # Limpeza de histórico antigo (mantém últimas 24h)
                cutoff_time = datetime.now() - timedelta(hours=24)
                
                self.connection_history = [
                    c for c in self.connection_history if c["timestamp"] > cutoff_time
                ]
                
                self.validation_history = [
                    v for v in self.validation_history if v["timestamp"] > cutoff_time
                ]
                
                self.broadcast_history = [
                    b for b in self.broadcast_history if b["timestamp"] > cutoff_time
                ]
                
                # Remove eventos antigos (mantém últimos 7 dias)
                old_cutoff = datetime.now() - timedelta(days=7)
                self.events = [
                    e for e in self.events 
                    if datetime.fromisoformat(e.timestamp) > old_cutoff
                ]
                
            except Exception as e:
                print(f"⚠️ Erro no monitoramento contínuo: {e}")
    
    def get_security_summary(self) -> Dict:
        """Gera resumo de segurança"""
        now = datetime.now()
        last_24h = now - timedelta(hours=24)
        
        recent_events = [
            e for e in self.events 
            if datetime.fromisoformat(e.timestamp) > last_24h
        ]
        
        severity_counts = {}
        for event in recent_events:
            severity_counts[event.severity] = severity_counts.get(event.severity, 0) + 1
        
        return {
            "monitoring_status": "active" if self.monitoring else "stopped",
            "total_events": len(self.events),
            "events_last_24h": len(recent_events),
            "severity_breakdown": severity_counts,
            "recent_connections": len([
                c for c in self.connection_history 
                if c["timestamp"] > last_24h
            ]),
            "recent_validations": len([
                v for v in self.validation_history 
                if v["timestamp"] > last_24h
            ]),
            "recent_broadcasts": len([
                b for b in self.broadcast_history 
                if b["timestamp"] > last_24h
            ]),
            "timestamp": now.isoformat()
        }
    
    def export_security_report(self) -> str:
        """Exporta relatório completo de segurança"""
        report = {
            "report_type": "AEONCOSMA Security Audit Report",
            "generated_at": datetime.now().isoformat(),
            "node_id": self.node_id,
            "summary": self.get_security_summary(),
            "all_events": [
                {
                    "timestamp": e.timestamp,
                    "type": e.event_type,
                    "severity": e.severity,
                    "description": e.description,
                    "details": e.details
                }
                for e in self.events
            ],
            "suspicious_patterns": self.suspicious_patterns
        }
        
        return json.dumps(report, indent=2, ensure_ascii=False)
    
    def stop_monitoring(self):
        """Para o monitoramento"""
        self.monitoring = False
        print(f"🛑 AEONCOSMA Audit Monitor parado para [{self.node_id}]")

# Monitor global para uso em toda a aplicação
global_audit_monitor: Optional[AeonAuditMonitor] = None

def get_audit_monitor(node_id: str = "global") -> AeonAuditMonitor:
    """Obtém ou cria monitor de auditoria global"""
    global global_audit_monitor
    
    if global_audit_monitor is None:
        global_audit_monitor = AeonAuditMonitor(node_id)
    
    return global_audit_monitor

if __name__ == "__main__":
    # Teste do sistema de auditoria
    print("🧪 Testando AEONCOSMA Audit Monitor...")
    
    monitor = AeonAuditMonitor("test_node")
    
    # Simula alguns eventos
    monitor.log_connection_attempt({"node_id": "test", "port": 9000}, "127.0.0.1")
    monitor.log_validation_result("test_peer", True)
    monitor.check_suspicious_arguments(sys.argv)
    
    # Gera relatório
    print("\n📊 Resumo de Segurança:")
    print(json.dumps(monitor.get_security_summary(), indent=2))
    
    monitor.stop_monitoring()
    print("\n🎯 Audit Monitor testado com sucesso!")
