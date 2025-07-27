# security/aeoncosma_threat_detector.py
"""
🚨 AEONCOSMA THREAT DETECTOR - Sistema de Detecção de Ameaças
Detecta e bloqueia ameaças em tempo real
Desenvolvido por Luiz Cruz - 2025
"""

import os
import sys
import json
import time
import threading
import socket
import psutil
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import subprocess

@dataclass
class ThreatAlert:
    """Alerta de ameaça detectada"""
    alert_id: str
    timestamp: str
    threat_type: str
    severity: str  # low, medium, high, critical
    source: str
    description: str
    mitigation_action: str
    details: Dict[str, Any]

class AeonThreatDetector:
    """
    Detector de ameaças para AEONCOSMA
    Monitora atividades suspeitas e bloqueia ameaças
    """
    
    def __init__(self, node_id: str = "threat_detector"):
        self.node_id = node_id
        self.active_threats: List[ThreatAlert] = []
        self.blocked_ips: List[str] = []
        self.quarantine_processes: List[int] = []
        
        # Configurações de detecção
        self.threat_rules = {
            "network_scanning": {
                "enabled": True,
                "threshold": 20,  # 20 conexões/min
                "action": "block_ip"
            },
            "resource_abuse": {
                "enabled": True,
                "cpu_threshold": 80,  # 80% CPU
                "memory_threshold": 80,  # 80% RAM
                "action": "throttle"
            },
            "port_manipulation": {
                "enabled": True,
                "privileged_ports": list(range(1, 1024)),
                "action": "alert"
            },
            "process_injection": {
                "enabled": True,
                "suspicious_processes": ["cmd.exe", "powershell.exe", "nc.exe", "telnet.exe"],
                "action": "quarantine"
            },
            "file_tampering": {
                "enabled": True,
                "protected_files": ["*.py", "config.*", "security/*"],
                "action": "block"
            }
        }
        
        # Estado do sistema
        self.system_baseline = self.get_system_baseline()
        self.monitoring_active = True
        
        # Thread de monitoramento
        self.monitor_thread = threading.Thread(target=self.threat_monitoring_loop, daemon=True)
        self.monitor_thread.start()
        
        print(f"🚨 AEONCOSMA Threat Detector ativo para [{node_id}]")
    
    def get_system_baseline(self) -> Dict:
        """Estabelece baseline do sistema"""
        try:
            return {
                "cpu_percent": psutil.cpu_percent(interval=1),
                "memory_percent": psutil.virtual_memory().percent,
                "network_connections": len(psutil.net_connections()),
                "running_processes": len(psutil.pids()),
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            print(f"⚠️ Erro ao estabelecer baseline: {e}")
            return {}
    
    def detect_network_scanning(self) -> Optional[ThreatAlert]:
        """Detecta scanning de rede"""
        if not self.threat_rules["network_scanning"]["enabled"]:
            return None
        
        try:
            connections = psutil.net_connections(kind='inet')
            external_connections = [
                c for c in connections 
                if c.raddr and not c.raddr.ip.startswith('127.')
            ]
            
            # Agrupa por IP externo
            ip_counts = {}
            for conn in external_connections:
                ip = conn.raddr.ip
                ip_counts[ip] = ip_counts.get(ip, 0) + 1
            
            # Verifica threshold
            for ip, count in ip_counts.items():
                if count > self.threat_rules["network_scanning"]["threshold"]:
                    return ThreatAlert(
                        alert_id=f"net_scan_{int(time.time())}",
                        timestamp=datetime.now().isoformat(),
                        threat_type="network_scanning",
                        severity="high",
                        source=ip,
                        description=f"Scanning de rede detectado de {ip}: {count} conexões",
                        mitigation_action="block_ip",
                        details={"ip": ip, "connection_count": count}
                    )
        
        except Exception as e:
            print(f"⚠️ Erro na detecção de network scanning: {e}")
        
        return None
    
    def detect_resource_abuse(self) -> Optional[ThreatAlert]:
        """Detecta abuso de recursos do sistema"""
        if not self.threat_rules["resource_abuse"]["enabled"]:
            return None
        
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory_percent = psutil.virtual_memory().percent
            
            if (cpu_percent > self.threat_rules["resource_abuse"]["cpu_threshold"] or 
                memory_percent > self.threat_rules["resource_abuse"]["memory_threshold"]):
                
                # Identifica processos suspeitos
                processes = []
                for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                    try:
                        if proc.info['cpu_percent'] > 20 or proc.info['memory_percent'] > 20:
                            processes.append(proc.info)
                    except:
                        continue
                
                return ThreatAlert(
                    alert_id=f"resource_abuse_{int(time.time())}",
                    timestamp=datetime.now().isoformat(),
                    threat_type="resource_abuse",
                    severity="medium",
                    source="localhost",
                    description=f"Abuso de recursos: CPU {cpu_percent}%, RAM {memory_percent}%",
                    mitigation_action="throttle",
                    details={
                        "cpu_percent": cpu_percent,
                        "memory_percent": memory_percent,
                        "suspicious_processes": processes
                    }
                )
        
        except Exception as e:
            print(f"⚠️ Erro na detecção de abuso de recursos: {e}")
        
        return None
    
    def detect_port_manipulation(self, port: int) -> Optional[ThreatAlert]:
        """Detecta manipulação de portas suspeitas"""
        if not self.threat_rules["port_manipulation"]["enabled"]:
            return None
        
        if port in self.threat_rules["port_manipulation"]["privileged_ports"]:
            return ThreatAlert(
                alert_id=f"port_manip_{port}_{int(time.time())}",
                timestamp=datetime.now().isoformat(),
                threat_type="port_manipulation",
                severity="medium",
                source="localhost",
                description=f"Tentativa de uso de porta privilegiada: {port}",
                mitigation_action="alert",
                details={"port": port, "type": "privileged"}
            )
        
        return None
    
    def detect_process_injection(self) -> Optional[ThreatAlert]:
        """Detecta injeção de processos suspeitos"""
        if not self.threat_rules["process_injection"]["enabled"]:
            return None
        
        try:
            suspicious_found = []
            
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    proc_name = proc.info['name'].lower()
                    
                    for suspicious in self.threat_rules["process_injection"]["suspicious_processes"]:
                        if suspicious.lower() in proc_name:
                            suspicious_found.append({
                                "pid": proc.info['pid'],
                                "name": proc.info['name'],
                                "cmdline": proc.info['cmdline']
                            })
                except:
                    continue
            
            if suspicious_found:
                return ThreatAlert(
                    alert_id=f"proc_inject_{int(time.time())}",
                    timestamp=datetime.now().isoformat(),
                    threat_type="process_injection",
                    severity="high",
                    source="localhost",
                    description=f"Processos suspeitos detectados: {len(suspicious_found)}",
                    mitigation_action="quarantine",
                    details={"suspicious_processes": suspicious_found}
                )
        
        except Exception as e:
            print(f"⚠️ Erro na detecção de injeção de processos: {e}")
        
        return None
    
    def mitigate_threat(self, alert: ThreatAlert):
        """Executa ações de mitigação para ameaças"""
        print(f"🛡️ Executando mitigação: {alert.mitigation_action} para {alert.threat_type}")
        
        try:
            if alert.mitigation_action == "block_ip":
                self.block_ip(alert.details.get("ip"))
            
            elif alert.mitigation_action == "quarantine":
                for proc in alert.details.get("suspicious_processes", []):
                    self.quarantine_process(proc["pid"])
            
            elif alert.mitigation_action == "throttle":
                self.throttle_resources()
            
            elif alert.mitigation_action == "alert":
                self.send_alert_notification(alert)
            
            elif alert.mitigation_action == "block":
                self.block_file_access(alert.details)
        
        except Exception as e:
            print(f"❌ Erro na mitigação: {e}")
    
    def block_ip(self, ip: str):
        """Bloqueia IP suspeito"""
        if ip and ip not in self.blocked_ips:
            self.blocked_ips.append(ip)
            print(f"🚫 IP bloqueado: {ip}")
            
            # No ambiente real, implementaria regras de firewall
            # Por segurança, apenas loga no momento
    
    def quarantine_process(self, pid: int):
        """Coloca processo em quarentena"""
        if pid not in self.quarantine_processes:
            self.quarantine_processes.append(pid)
            print(f"🔒 Processo em quarentena: PID {pid}")
            
            # Em ambiente real, limitaria recursos do processo
            # Por segurança, apenas loga no momento
    
    def throttle_resources(self):
        """Throttle de recursos do sistema"""
        print("⏳ Aplicando throttle de recursos...")
        
        # Em ambiente real, limitaria CPU/memoria
        # Por segurança, apenas loga no momento
    
    def send_alert_notification(self, alert: ThreatAlert):
        """Envia notificação de alerta"""
        print(f"📢 ALERTA CRÍTICO: {alert.description}")
        print(f"   Severidade: {alert.severity}")
        print(f"   Fonte: {alert.source}")
    
    def block_file_access(self, details: Dict):
        """Bloqueia acesso a arquivos"""
        print(f"🔐 Bloqueando acesso a arquivos: {details}")
    
    def threat_monitoring_loop(self):
        """Loop principal de monitoramento de ameaças"""
        while self.monitoring_active:
            try:
                # Executa todas as detecções
                detections = [
                    self.detect_network_scanning(),
                    self.detect_resource_abuse(),
                    self.detect_process_injection()
                ]
                
                # Processa alertas encontrados
                for alert in detections:
                    if alert:
                        self.active_threats.append(alert)
                        print(f"🚨 AMEAÇA DETECTADA: {alert.description}")
                        
                        # Executa mitigação imediata para ameaças críticas
                        if alert.severity in ["high", "critical"]:
                            self.mitigate_threat(alert)
                
                # Limpeza de ameaças antigas (últimas 24h)
                cutoff_time = datetime.now() - timedelta(hours=24)
                self.active_threats = [
                    t for t in self.active_threats 
                    if datetime.fromisoformat(t.timestamp) > cutoff_time
                ]
                
                time.sleep(5)  # Verifica a cada 5 segundos
                
            except Exception as e:
                print(f"❌ Erro no loop de monitoramento: {e}")
                time.sleep(10)
    
    def check_ip_blocked(self, ip: str) -> bool:
        """Verifica se IP está bloqueado"""
        return ip in self.blocked_ips
    
    def check_process_quarantined(self, pid: int) -> bool:
        """Verifica se processo está em quarentena"""
        return pid in self.quarantine_processes
    
    def get_threat_summary(self) -> Dict:
        """Gera resumo de ameaças"""
        now = datetime.now()
        last_24h = now - timedelta(hours=24)
        
        recent_threats = [
            t for t in self.active_threats 
            if datetime.fromisoformat(t.timestamp) > last_24h
        ]
        
        threat_types = {}
        severity_counts = {}
        
        for threat in recent_threats:
            threat_types[threat.threat_type] = threat_types.get(threat.threat_type, 0) + 1
            severity_counts[threat.severity] = severity_counts.get(threat.severity, 0) + 1
        
        return {
            "detector_status": "active" if self.monitoring_active else "stopped",
            "total_threats": len(self.active_threats),
            "threats_last_24h": len(recent_threats),
            "blocked_ips": len(self.blocked_ips),
            "quarantined_processes": len(self.quarantine_processes),
            "threat_types": threat_types,
            "severity_breakdown": severity_counts,
            "system_status": self.get_system_baseline(),
            "timestamp": now.isoformat()
        }
    
    def export_threat_report(self) -> str:
        """Exporta relatório completo de ameaças"""
        report = {
            "report_type": "AEONCOSMA Threat Detection Report",
            "generated_at": datetime.now().isoformat(),
            "node_id": self.node_id,
            "summary": self.get_threat_summary(),
            "active_threats": [
                {
                    "alert_id": t.alert_id,
                    "timestamp": t.timestamp,
                    "type": t.threat_type,
                    "severity": t.severity,
                    "source": t.source,
                    "description": t.description,
                    "mitigation": t.mitigation_action,
                    "details": t.details
                }
                for t in self.active_threats
            ],
            "blocked_ips": self.blocked_ips,
            "quarantined_processes": self.quarantine_processes,
            "threat_rules": self.threat_rules
        }
        
        return json.dumps(report, indent=2, ensure_ascii=False)
    
    def stop_monitoring(self):
        """Para o monitoramento de ameaças"""
        self.monitoring_active = False
        print(f"🛑 AEONCOSMA Threat Detector parado para [{self.node_id}]")

# Detector global para uso em toda a aplicação
global_threat_detector: Optional[AeonThreatDetector] = None

def get_threat_detector(node_id: str = "global") -> AeonThreatDetector:
    """Obtém ou cria detector de ameaças global"""
    global global_threat_detector
    
    if global_threat_detector is None:
        global_threat_detector = AeonThreatDetector(node_id)
    
    return global_threat_detector

if __name__ == "__main__":
    # Teste do sistema de detecção de ameaças
    print("🧪 Testando AEONCOSMA Threat Detector...")
    
    detector = AeonThreatDetector("test_node")
    
    # Simula algumas verificações
    time.sleep(2)
    
    # Testa detecção de porta privilegiada
    port_alert = detector.detect_port_manipulation(80)
    if port_alert:
        print(f"🚨 Alerta de porta: {port_alert.description}")
    
    # Gera relatório
    print("\n📊 Resumo de Ameaças:")
    print(json.dumps(detector.get_threat_summary(), indent=2))
    
    detector.stop_monitoring()
    print("\n🎯 Threat Detector testado com sucesso!")
