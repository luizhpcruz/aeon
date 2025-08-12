#!/usr/bin/env python3
"""
🧬 AEON Dashboard - Módulo de Monitoramento RAM
Sistema integrado de monitoramento de recursos para o projeto AEON
"""

import psutil
import json
import time
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
import threading
import queue
from pathlib import Path

@dataclass
class RAMSnapshot:
    """Snapshot de uso de RAM em um momento específico"""
    timestamp: str
    total_gb: float
    used_gb: float
    available_gb: float
    percent: float
    aeon_processes: List[Dict]
    aeon_total_mb: float
    system_status: str
    alert_level: str

class AeonRAMDashboard:
    """Dashboard de monitoramento RAM para AEON"""
    
    def __init__(self, history_size: int = 100):
        self.history_size = history_size
        self.snapshots: List[RAMSnapshot] = []
        self.monitoring = False
        self.monitor_thread: Optional[threading.Thread] = None
        self.data_queue = queue.Queue()
        
        # Configurações de alertas
        self.alert_thresholds = {
            'normal': 70,      # < 70% = Verde
            'warning': 85,     # 70-85% = Amarelo  
            'critical': 95     # > 85% = Vermelho
        }
        
        # Processos AEON conhecidos
        self.aeon_keywords = [
            'aeon', 'p2p', 'entropy', 'cosma', 'verna', 
            'dashboard', 'cosmologia', 'simulation'
        ]
        
    def get_current_snapshot(self) -> RAMSnapshot:
        """Captura snapshot atual do sistema"""
        # Informações básicas de RAM
        memory = psutil.virtual_memory()
        
        # Detecta processos AEON
        aeon_processes = self._detect_aeon_processes()
        aeon_total_mb = sum(proc['memory_mb'] for proc in aeon_processes)
        
        # Determina status do sistema
        system_status = self._get_system_status(memory.percent)
        alert_level = self._get_alert_level(memory.percent)
        
        return RAMSnapshot(
            timestamp=datetime.now().isoformat(),
            total_gb=round(memory.total / (1024**3), 2),
            used_gb=round(memory.used / (1024**3), 2),
            available_gb=round(memory.available / (1024**3), 2),
            percent=round(memory.percent, 1),
            aeon_processes=aeon_processes,
            aeon_total_mb=round(aeon_total_mb, 1),
            system_status=system_status,
            alert_level=alert_level
        )
    
    def _detect_aeon_processes(self) -> List[Dict]:
        """Detecta processos relacionados ao AEON"""
        aeon_processes = []
        
        for proc in psutil.process_iter(['pid', 'name', 'memory_info', 'cmdline', 'create_time']):
            try:
                # Verifica processos Python com scripts AEON
                if proc.info['name'].lower() in ['python.exe', 'python3.exe', 'pythonw.exe']:
                    cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
                    
                    if any(keyword in cmdline.lower() for keyword in self.aeon_keywords):
                        memory_mb = proc.info['memory_info'].rss / (1024*1024)
                        
                        # Identifica tipo de processo AEON
                        process_type = self._identify_aeon_type(cmdline)
                        
                        aeon_processes.append({
                            'pid': proc.info['pid'],
                            'name': proc.info['name'],
                            'memory_mb': round(memory_mb, 1),
                            'type': process_type,
                            'cmdline': cmdline[:80] + '...' if len(cmdline) > 80 else cmdline,
                            'uptime_minutes': round((time.time() - proc.info['create_time']) / 60, 1)
                        })
                
                # Verifica VS Code (importante para desenvolvimento AEON)
                elif 'code' in proc.info['name'].lower():
                    memory_mb = proc.info['memory_info'].rss / (1024*1024)
                    aeon_processes.append({
                        'pid': proc.info['pid'],
                        'name': proc.info['name'],
                        'memory_mb': round(memory_mb, 1),
                        'type': 'development',
                        'cmdline': 'VS Code IDE',
                        'uptime_minutes': round((time.time() - proc.info['create_time']) / 60, 1)
                    })
                    
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
                
        return sorted(aeon_processes, key=lambda x: x['memory_mb'], reverse=True)
    
    def _identify_aeon_type(self, cmdline: str) -> str:
        """Identifica o tipo de processo AEON baseado na linha de comando"""
        cmdline_lower = cmdline.lower()
        
        if 'p2p' in cmdline_lower or 'cluster' in cmdline_lower:
            return 'p2p_network'
        elif 'entropy' in cmdline_lower:
            return 'entropy_simulation'
        elif 'cosma' in cmdline_lower or 'cosmologia' in cmdline_lower:
            return 'cosmology_model'
        elif 'verna' in cmdline_lower:
            return 'neural_analysis'
        elif 'dashboard' in cmdline_lower:
            return 'dashboard'
        elif 'launcher' in cmdline_lower:
            return 'launcher'
        else:
            return 'aeon_general'
    
    def _get_system_status(self, usage_percent: float) -> str:
        """Determina status textual do sistema"""
        if usage_percent < 50:
            return "Excelente"
        elif usage_percent < 70:
            return "Bom"
        elif usage_percent < 85:
            return "Moderado"
        elif usage_percent < 95:
            return "Alto"
        else:
            return "Crítico"
    
    def _get_alert_level(self, usage_percent: float) -> str:
        """Determina nível de alerta"""
        if usage_percent < self.alert_thresholds['normal']:
            return "normal"
        elif usage_percent < self.alert_thresholds['warning']:
            return "warning"
        else:
            return "critical"
    
    def add_snapshot(self, snapshot: Optional[RAMSnapshot] = None):
        """Adiciona snapshot ao histórico"""
        if snapshot is None:
            snapshot = self.get_current_snapshot()
        
        self.snapshots.append(snapshot)
        
        # Mantém apenas os últimos N snapshots
        if len(self.snapshots) > self.history_size:
            self.snapshots = self.snapshots[-self.history_size:]
    
    def get_statistics(self, minutes: int = 60) -> Dict:
        """Calcula estatísticas dos últimos N minutos"""
        cutoff_time = datetime.now() - timedelta(minutes=minutes)
        
        recent_snapshots = [
            s for s in self.snapshots 
            if datetime.fromisoformat(s.timestamp) > cutoff_time
        ]
        
        if not recent_snapshots:
            return {'error': 'Dados insuficientes'}
        
        percentages = [s.percent for s in recent_snapshots]
        aeon_usage = [s.aeon_total_mb for s in recent_snapshots]
        
        return {
            'period_minutes': minutes,
            'samples': len(recent_snapshots),
            'ram_usage': {
                'average': round(sum(percentages) / len(percentages), 1),
                'maximum': max(percentages),
                'minimum': min(percentages),
                'current': recent_snapshots[-1].percent
            },
            'aeon_impact': {
                'average_mb': round(sum(aeon_usage) / len(aeon_usage), 1),
                'maximum_mb': max(aeon_usage),
                'minimum_mb': min(aeon_usage),
                'current_mb': recent_snapshots[-1].aeon_total_mb
            },
            'alerts_triggered': len([s for s in recent_snapshots if s.alert_level != 'normal'])
        }
    
    def generate_report(self) -> Dict:
        """Gera relatório completo do sistema"""
        current = self.get_current_snapshot()
        stats_1h = self.get_statistics(60)
        stats_24h = self.get_statistics(1440)
        
        # Análise de impacto AEON
        aeon_impact_percent = (current.aeon_total_mb / (current.total_gb * 1024)) * 100
        
        # Recomendações baseadas no uso atual
        recommendations = self._generate_recommendations(current, aeon_impact_percent)
        
        return {
            'timestamp': current.timestamp,
            'current_status': {
                'ram_usage_percent': current.percent,
                'system_status': current.system_status,
                'alert_level': current.alert_level,
                'total_ram_gb': current.total_gb,
                'available_gb': current.available_gb
            },
            'aeon_impact': {
                'total_processes': len(current.aeon_processes),
                'total_memory_mb': current.aeon_total_mb,
                'impact_percent': round(aeon_impact_percent, 2),
                'process_breakdown': self._analyze_process_types(current.aeon_processes)
            },
            'statistics': {
                'last_hour': stats_1h,
                'last_24_hours': stats_24h
            },
            'recommendations': recommendations,
            'process_details': current.aeon_processes[:10]  # Top 10 processos
        }
    
    def _analyze_process_types(self, processes: List[Dict]) -> Dict:
        """Analisa distribuição por tipo de processo"""
        type_stats = {}
        
        for proc in processes:
            proc_type = proc['type']
            if proc_type not in type_stats:
                type_stats[proc_type] = {'count': 0, 'memory_mb': 0}
            
            type_stats[proc_type]['count'] += 1
            type_stats[proc_type]['memory_mb'] += proc['memory_mb']
        
        # Arredonda valores
        for stats in type_stats.values():
            stats['memory_mb'] = round(stats['memory_mb'], 1)
        
        return type_stats
    
    def _generate_recommendations(self, snapshot: RAMSnapshot, aeon_impact: float) -> List[str]:
        """Gera recomendações baseadas no estado atual"""
        recommendations = []
        
        if snapshot.percent > 90:
            recommendations.append("🚨 RAM crítica! Feche aplicações desnecessárias imediatamente")
            recommendations.append("💡 Considere reiniciar o sistema se o problema persistir")
        elif snapshot.percent > 85:
            recommendations.append("⚠️ RAM alta. Monitore processos que consomem mais memória")
            recommendations.append("🔧 Considere fechar abas não utilizadas no VS Code")
        
        if aeon_impact > 15:
            recommendations.append("🧬 Processos AEON usando muita RAM. Execute apenas módulos necessários")
        elif aeon_impact > 10:
            recommendations.append("📊 Considere otimizar scripts AEON para usar menos memória")
        
        if len(snapshot.aeon_processes) > 5:
            recommendations.append("🔄 Muitos processos AEON ativos. Verifique se todos são necessários")
        
        if snapshot.total_gb < 8:
            recommendations.append("💾 Sistema com RAM limitada. Considere upgrade para 8GB+ para melhor performance AEON")
        
        if not recommendations:
            recommendations.append("✅ Sistema operando normalmente. Continue o bom trabalho!")
        
        return recommendations
    
    def start_monitoring(self, interval_seconds: int = 30):
        """Inicia monitoramento contínuo em background"""
        if self.monitoring:
            return False
        
        self.monitoring = True
        self.monitor_thread = threading.Thread(
            target=self._monitor_loop, 
            args=(interval_seconds,),
            daemon=True
        )
        self.monitor_thread.start()
        return True
    
    def stop_monitoring(self):
        """Para o monitoramento contínuo"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
    
    def _monitor_loop(self, interval: int):
        """Loop principal de monitoramento"""
        while self.monitoring:
            try:
                snapshot = self.get_current_snapshot()
                self.add_snapshot(snapshot)
                
                # Envia dados para queue (para interfaces que consomem)
                self.data_queue.put(snapshot)
                
            except Exception as e:
                print(f"Erro no monitoramento: {e}")
            
            time.sleep(interval)
    
    def export_data(self, filepath: str = None) -> str:
        """Exporta dados históricos para JSON"""
        if filepath is None:
            filepath = f"aeon_ram_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        export_data = {
            'export_timestamp': datetime.now().isoformat(),
            'total_snapshots': len(self.snapshots),
            'snapshots': [asdict(snapshot) for snapshot in self.snapshots]
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        return filepath

def create_dashboard_widget() -> str:
    """Cria widget HTML para integração com dashboard web"""
    return """
    <div id="aeon-ram-widget" class="widget">
        <div class="widget-header">
            <h3>🧬 AEON RAM Monitor</h3>
            <span id="ram-status" class="status-badge">Normal</span>
        </div>
        <div class="widget-content">
            <div class="ram-usage">
                <div class="usage-bar">
                    <div id="usage-fill" class="usage-fill" style="width: 0%"></div>
                </div>
                <div class="usage-text">
                    <span id="usage-percent">0%</span> de <span id="total-ram">0 GB</span>
                </div>
            </div>
            <div class="aeon-impact">
                <p>Impacto AEON: <span id="aeon-usage">0 MB</span> (<span id="aeon-percent">0%</span>)</p>
                <p>Processos ativos: <span id="aeon-processes">0</span></p>
            </div>
            <div id="recommendations" class="recommendations"></div>
        </div>
    </div>
    
    <style>
    .widget {
        border: 1px solid #ddd;
        border-radius: 8px;
        margin: 10px;
        background: white;
    }
    .widget-header {
        background: #f5f5f5;
        padding: 10px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid #ddd;
    }
    .status-badge {
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 12px;
        font-weight: bold;
    }
    .status-badge.normal { background: #d4edda; color: #155724; }
    .status-badge.warning { background: #fff3cd; color: #856404; }
    .status-badge.critical { background: #f8d7da; color: #721c24; }
    .widget-content { padding: 15px; }
    .usage-bar {
        width: 100%;
        height: 20px;
        background: #e9ecef;
        border-radius: 10px;
        overflow: hidden;
        margin: 10px 0;
    }
    .usage-fill {
        height: 100%;
        background: linear-gradient(90deg, #28a745, #ffc107, #dc3545);
        transition: width 0.3s ease;
    }
    .usage-text { text-align: center; font-weight: bold; }
    .aeon-impact { margin: 15px 0; font-size: 14px; }
    .recommendations { margin-top: 15px; }
    .recommendations p { margin: 5px 0; padding: 5px; background: #f8f9fa; border-radius: 4px; }
    </style>
    """

# Exemplo de uso
if __name__ == "__main__":
    print("🧬 Iniciando AEON RAM Dashboard...")
    
    dashboard = AeonRAMDashboard()
    
    # Coleta alguns snapshots iniciais
    for i in range(3):
        dashboard.add_snapshot()
        time.sleep(1)
    
    # Gera relatório
    report = dashboard.generate_report()
    
    print(f"📊 Sistema: {report['current_status']['system_status']}")
    print(f"💾 RAM: {report['current_status']['ram_usage_percent']}%")
    print(f"🧬 AEON: {report['aeon_impact']['total_memory_mb']} MB ({report['aeon_impact']['impact_percent']}%)")
    print(f"🔧 Processos: {report['aeon_impact']['total_processes']}")
    
    print("\n📋 Recomendações:")
    for rec in report['recommendations']:
        print(f"  {rec}")
    
    print(f"\n💾 Dados exportados para: {dashboard.export_data()}")
