import streamlit as st
import requests
import pandas as pd
import time
import random
import plotly.express as px
import json
import hashlib
import os
from datetime import datetime, timedelta
import logging

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configuração global
CONFIG = {
    "max_latency_ms": 100,
    "min_packet_ratio": 0.8,
    "historical_window_hours": 24,
    "alert_threshold": 3,
    "data_dir": "integrity_data",
    "benchmark_file": "network_benchmarks.json"
}

# Garantir que diretório de dados existe
os.makedirs(CONFIG["data_dir"], exist_ok=True)

class AEONCOSMAIntegrityValidator:
    def __init__(self):
        self.alerts = []
        self.historical_data = []
        self.benchmarks = self.load_benchmarks()
        
    def load_benchmarks(self):
        """Carrega benchmarks históricos do sistema"""
        benchmark_path = os.path.join(CONFIG["data_dir"], CONFIG["benchmark_file"])
        if os.path.exists(benchmark_path):
            with open(benchmark_path, 'r') as f:
                return json.load(f)
        return {
            "avg_latency_ms": 45.0,
            "avg_packet_ratio": 0.95,
            "uptime_percentage": 98.5,
            "last_updated": datetime.now().isoformat()
        }
    
    def save_benchmarks(self):
        """Salva benchmarks atualizados"""
        benchmark_path = os.path.join(CONFIG["data_dir"], CONFIG["benchmark_file"])
        self.benchmarks["last_updated"] = datetime.now().isoformat()
        with open(benchmark_path, 'w') as f:
            json.dump(self.benchmarks, f, indent=2)
    
    def generate_data_hash(self, data):
        """Gera hash SHA-256 para integridade dos dados"""
        data_str = json.dumps(data, sort_keys=True)
        return hashlib.sha256(data_str.encode()).hexdigest()
    
    def get_node_status(self):
        """Simulador de status dos nós com mais parâmetros"""
        # Diferentes tipos de nós com características específicas
        node_types = ["master", "energy", "ai", "crypto", "quantum", "cosmos", "validator"]
        node_type = random.choice(node_types)
        
        # Modificadores por tipo de nó
        type_modifiers = {
            "master": {"uptime": 0.95, "latency_factor": 0.8, "cpu_factor": 1.2},
            "energy": {"uptime": 0.90, "latency_factor": 1.0, "cpu_factor": 0.9},
            "ai": {"uptime": 0.85, "latency_factor": 1.2, "cpu_factor": 1.5},
            "crypto": {"uptime": 0.88, "latency_factor": 0.9, "cpu_factor": 1.3},
            "quantum": {"uptime": 0.82, "latency_factor": 1.5, "cpu_factor": 1.1},
            "cosmos": {"uptime": 0.80, "latency_factor": 1.3, "cpu_factor": 1.4},
            "validator": {"uptime": 0.92, "latency_factor": 0.7, "cpu_factor": 0.8}
        }
        
        modifiers = type_modifiers.get(node_type, {"uptime": 0.85, "latency_factor": 1.0, "cpu_factor": 1.0})
        
        status = {
            "node_id": f"aeon-{random.randint(1000,9999)}",
            "node_type": node_type,
            "online": random.random() < modifiers["uptime"],
            "latency_ms": round(random.uniform(10, 120) * modifiers["latency_factor"], 2),
            "packets_sent": random.randint(1000, 5000),
            "packets_received": random.randint(800, 4800),
            "cpu_usage": round(random.uniform(5, 85) * modifiers["cpu_factor"], 1),
            "memory_usage": round(random.uniform(15, 90), 1),
            "consensus_participation": random.choice([True, False]),
            "blockchain_sync": random.choice([True, True, False]),
            "timestamp": datetime.now().isoformat(),
        }
        
        # Calcular métricas derivadas
        if status["packets_sent"] > 0:
            status["packet_loss_ratio"] = max(0, 1 - (status["packets_received"] / status["packets_sent"]))
        else:
            status["packet_loss_ratio"] = 0
            
        status["is_healthy"] = self.validate_node_health(status)
        status["can_participate_consensus"] = (
            status["online"] and 
            status["is_healthy"] and 
            status["consensus_participation"] and
            status["blockchain_sync"]
        )
        status["data_hash"] = self.generate_data_hash(status)
        
        return status
    
    def validate_node_health(self, status):
        """Validação interna de integridade do nó"""
        health_checks = []
        
        # Check 1: Latência
        if status["latency_ms"] <= CONFIG["max_latency_ms"]:
            health_checks.append(True)
        else:
            self.alerts.append(f"⚠️ ALERTA: Latência alta ({status['latency_ms']}ms) no nó {status['node_id']}")
            health_checks.append(False)
            
        # Check 2: Perda de pacotes
        if status["packet_loss_ratio"] <= (1 - CONFIG["min_packet_ratio"]):
            health_checks.append(True)
        else:
            self.alerts.append(f"⚠️ ALERTA: Alta perda de pacotes ({status['packet_loss_ratio']:.2%}) no nó {status['node_id']}")
            health_checks.append(False)
            
        # Check 3: Status online
        if status["online"]:
            health_checks.append(True)
        else:
            self.alerts.append(f"🔴 ALERTA CRÍTICO: Nó {status['node_id']} offline")
            health_checks.append(False)
            
        # Check 4: Participação no consenso
        if status["consensus_participation"]:
            health_checks.append(True)
        else:
            self.alerts.append(f"⚠️ ALERTA: Nó {status['node_id']} não participa do consenso")
            health_checks.append(False)
            
        return all(health_checks)
    
    def compare_with_benchmarks(self, status):
        """Comparação externa com benchmarks históricos"""
        anomalies = []
        
        # Comparar latência com benchmark
        if status["latency_ms"] > self.benchmarks["avg_latency_ms"] * 1.5:
            anomalies.append("Latência 50% acima do benchmark")
            
        # Comparar perda de pacotes
        expected_ratio = 1 - status["packet_loss_ratio"]
        if expected_ratio < self.benchmarks["avg_packet_ratio"] * 0.8:
            anomalies.append("Perda de pacotes 20% acima do benchmark")
            
        return anomalies
    
    def detect_attack_patterns(self, cycle_data):
        """Detecta padrões de ataques e anomalias de segurança"""
        attacks = []
        nodes = cycle_data["nodes"]
        
        if len(nodes) == 0:
            return attacks
        
        # 1. Detecção de Ataque DDoS - Alta latência coordenada
        high_latency_nodes = [n for n in nodes if n["latency_ms"] > 150]
        if len(high_latency_nodes) > len(nodes) * 0.4:  # 40% dos nós com alta latência
            attacks.append({
                "type": "DDoS_ATTACK",
                "severity": "HIGH",
                "description": f"Possível ataque DDoS detectado - {len(high_latency_nodes)} nós com latência > 150ms",
                "affected_nodes": [n["node_id"] for n in high_latency_nodes],
                "recommendation": "Investigar tráfego de rede e implementar rate limiting"
            })
        
        # 2. Detecção de Sabotagem - Nós deliberadamente offline
        offline_nodes = [n for n in nodes if not n["online"]]
        if len(offline_nodes) > len(nodes) * 0.3:  # 30% dos nós offline
            attacks.append({
                "type": "SABOTAGE_ATTACK",
                "severity": "CRITICAL",
                "description": f"Possível sabotagem detectada - {len(offline_nodes)} nós offline simultaneamente",
                "affected_nodes": [n["node_id"] for n in offline_nodes],
                "recommendation": "Verificar segurança física e acesso aos nós"
            })
        
        # 3. Detecção de Falhas de Hardware - CPU/Memória em sobrecarga
        overloaded_nodes = [n for n in nodes if n["cpu_usage"] > 90 or n["memory_usage"] > 95]
        if len(overloaded_nodes) > len(nodes) * 0.25:  # 25% dos nós sobrecarregados
            attacks.append({
                "type": "HARDWARE_FAILURE",
                "severity": "MEDIUM",
                "description": f"Falhas de hardware detectadas - {len(overloaded_nodes)} nós sobrecarregados",
                "affected_nodes": [n["node_id"] for n in overloaded_nodes],
                "recommendation": "Verificar recursos de hardware e distribuir carga"
            })
        
        # 4. Detecção de Problemas de Rede - Perda excessiva de pacotes
        packet_loss_nodes = [n for n in nodes if n["packet_loss_ratio"] > 0.3]
        if len(packet_loss_nodes) > len(nodes) * 0.2:  # 20% dos nós com perda alta
            attacks.append({
                "type": "NETWORK_ISSUE",
                "severity": "MEDIUM",
                "description": f"Problemas de rede detectados - {len(packet_loss_nodes)} nós com perda > 30%",
                "affected_nodes": [n["node_id"] for n in packet_loss_nodes],
                "recommendation": "Verificar infraestrutura de rede e conexões"
            })
        
        # 5. Detecção de Dessincronização - Nós fora da blockchain
        desync_nodes = [n for n in nodes if n["online"] and not n["blockchain_sync"]]
        if len(desync_nodes) > len(nodes) * 0.15:  # 15% dos nós dessincronizados
            attacks.append({
                "type": "BLOCKCHAIN_DESYNC",
                "severity": "HIGH",
                "description": f"Dessincronização detectada - {len(desync_nodes)} nós fora da blockchain",
                "affected_nodes": [n["node_id"] for n in desync_nodes],
                "recommendation": "Forçar ressincronização e verificar integridade da blockchain"
            })
        
        # 6. Detecção de Ataque de Consenso - Nós maliciosos
        non_consensus_nodes = [n for n in nodes if n["online"] and not n["consensus_participation"]]
        if len(non_consensus_nodes) > len(nodes) * 0.35:  # 35% não participam do consenso
            attacks.append({
                "type": "CONSENSUS_ATTACK",
                "severity": "CRITICAL",
                "description": f"Possível ataque ao consenso - {len(non_consensus_nodes)} nós não participam",
                "affected_nodes": [n["node_id"] for n in non_consensus_nodes],
                "recommendation": "Investigar nós suspeitos e implementar validação adicional"
            })
        
        return attacks
    
    def calculate_security_metrics(self, cycle_data):
        """Calcula métricas avançadas de segurança"""
        nodes = cycle_data["nodes"]
        if len(nodes) == 0:
            return {}
        
        # Integridade da Rede
        healthy_nodes = sum(1 for n in nodes if n["is_healthy"])
        network_integrity = (healthy_nodes / len(nodes)) * 100
        
        # Score de Consenso
        consensus_nodes = sum(1 for n in nodes if n["can_participate_consensus"])
        consensus_score = (consensus_nodes / len(nodes)) * 100
        
        # Performance da Rede
        avg_latency = sum(n["latency_ms"] for n in nodes) / len(nodes)
        avg_cpu = sum(n["cpu_usage"] for n in nodes) / len(nodes)
        avg_memory = sum(n["memory_usage"] for n in nodes) / len(nodes)
        
        # Distribuição de Tipos
        node_types = {}
        for node in nodes:
            node_type = node.get("node_type", "unknown")
            node_types[node_type] = node_types.get(node_type, 0) + 1
        
        # Calcular balanceamento (ideal seria distribuição uniforme)
        if len(node_types) > 0:
            expected_per_type = len(nodes) / len(node_types)
            balance_variance = sum(abs(count - expected_per_type) for count in node_types.values())
            balance_score = max(0, 100 - (balance_variance / len(nodes)) * 100)
        else:
            balance_score = 0
        
        # Resilência da Rede (capacidade de manter consenso mesmo com falhas)
        min_nodes_for_consensus = max(1, int(len(nodes) * 0.67))
        current_consensus_nodes = consensus_nodes
        resilience_score = min(100, (current_consensus_nodes / min_nodes_for_consensus) * 100)
        
        # Score Geral de Segurança (média ponderada)
        security_score = (
            network_integrity * 0.3 +
            consensus_score * 0.25 +
            resilience_score * 0.2 +
            balance_score * 0.15 +
            max(0, 100 - avg_latency) * 0.1  # Latência baixa = boa performance
        )
        
        return {
            "network_integrity": round(network_integrity, 2),
            "consensus_score": round(consensus_score, 2),
            "avg_latency_ms": round(avg_latency, 2),
            "avg_cpu_usage": round(avg_cpu, 2),
            "avg_memory_usage": round(avg_memory, 2),
            "node_distribution": node_types,
            "balance_score": round(balance_score, 2),
            "resilience_score": round(resilience_score, 2),
            "overall_security_score": round(security_score, 2),
            "total_nodes": len(nodes),
            "healthy_nodes": healthy_nodes,
            "consensus_capable_nodes": consensus_nodes
        }
    
    def save_cycle_data(self, cycle_data):
        """Salva dados do ciclo para análise futura"""
        filename = f"integrity_cycle_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = os.path.join(CONFIG["data_dir"], filename)
        
        with open(filepath, 'w') as f:
            json.dump(cycle_data, f, indent=2)
            
        logger.info(f"Dados do ciclo salvos em: {filepath}")
    
    def run_integrity_check(self):
        """Executa um ciclo completo de verificação de integridade"""
        cycle_start = datetime.now()
        cycle_data = {
            "cycle_id": self.generate_data_hash({"timestamp": cycle_start.isoformat()}),
            "start_time": cycle_start.isoformat(),
            "nodes": [],
            "alerts": [],
            "summary": {},
            "attacks": [],
            "security_metrics": {}
        }
        
        # Simular múltiplos nós na rede
        node_count = random.randint(15, 25)  # Simula rede dinâmica
        healthy_nodes = 0
        total_latency = 0
        
        for _ in range(node_count):
            status = self.get_node_status()
            cycle_data["nodes"].append(status)
            
            if status["is_healthy"]:
                healthy_nodes += 1
            
            total_latency += status["latency_ms"]
            
            # Comparar com benchmarks
            anomalies = self.compare_with_benchmarks(status)
            if anomalies:
                for anomaly in anomalies:
                    alert = f"🔍 ANOMALIA: {anomaly} - Nó {status['node_id']}"
                    self.alerts.append(alert)
                    cycle_data["alerts"].append(alert)
        
        # Detectar padrões de ataque
        cycle_data["attacks"] = self.detect_attack_patterns(cycle_data)
        
        # Calcular métricas de segurança
        cycle_data["security_metrics"] = self.calculate_security_metrics(cycle_data)
        
        # Calcular métricas do ciclo
        avg_latency = total_latency / node_count
        health_percentage = (healthy_nodes / node_count) * 100
        
        cycle_data["summary"] = {
            "total_nodes": node_count,
            "healthy_nodes": healthy_nodes,
            "health_percentage": round(health_percentage, 2),
            "avg_latency_ms": round(avg_latency, 2),
            "quorum_reached": healthy_nodes >= (node_count * 0.67),  # 67% quorum
            "network_stable": health_percentage >= 80,
            "attacks_detected": len(cycle_data["attacks"]),
            "security_level": self.get_security_level(cycle_data["security_metrics"]["overall_security_score"])
        }
        
        cycle_data["end_time"] = datetime.now().isoformat()
        cycle_data["duration_seconds"] = (datetime.now() - cycle_start).total_seconds()
        
        # Salvar dados do ciclo
        self.save_cycle_data(cycle_data)
        
        return cycle_data
    
    def get_security_level(self, score):
        """Determina o nível de segurança baseado no score"""
        if score >= 90:
            return "MAXIMUM"
        elif score >= 75:
            return "HIGH"
        elif score >= 60:
            return "MEDIUM"
        elif score >= 40:
            return "LOW"
        else:
            return "CRITICAL"

# Instância global do validador
validator = AEONCOSMAIntegrityValidator()

# Interface Streamlit (mantida para compatibilidade)
st.set_page_config(page_title="AEONCOSMA Integrity Validator", layout="wide")

st.title("🔐 AEONCOSMA Engine - Validador de Integridade")

# Sidebar de controle
st.sidebar.header("🔧 Configurações")
refresh_rate = st.sidebar.slider("⏱️ Intervalo de atualização (segundos)", 1, 30, 5)
backend_mode = st.sidebar.checkbox("🖥️ Modo Backend (sem interface)", value=False)

# Função legada para compatibilidade
def get_node_status():
    return validator.get_node_status()

# Simulador de dados para gráfico
def generate_latency_data():
    return pd.DataFrame({
        "timestamp": pd.date_range(end=pd.Timestamp.now(), periods=20, freq="S"),
        "latency_ms": [round(random.uniform(20, 120), 2) for _ in range(20)]
    })

# Modo Backend (execução sem interface)
if backend_mode or not hasattr(st, 'session_state'):
    st.info("🖥️ Executando em modo backend...")
    
    # Executar verificação de integridade
    cycle_result = validator.run_integrity_check()
    
    # Exibir resultados no terminal/log
    logger.info("="*60)
    logger.info(f"🔐 AEONCOSMA INTEGRITY CHECK - Ciclo {cycle_result['cycle_id'][:8]}")
    logger.info("="*60)
    logger.info(f"📊 Nós totais: {cycle_result['summary']['total_nodes']}")
    logger.info(f"✅ Nós saudáveis: {cycle_result['summary']['healthy_nodes']}")
    logger.info(f"📈 Saúde da rede: {cycle_result['summary']['health_percentage']}%")
    logger.info(f"⏱️ Latência média: {cycle_result['summary']['avg_latency_ms']} ms")
    logger.info(f"🗳️ Quorum atingido: {'✅' if cycle_result['summary']['quorum_reached'] else '❌'}")
    logger.info(f"🌐 Rede estável: {'✅' if cycle_result['summary']['network_stable'] else '❌'}")
    
    if validator.alerts:
        logger.warning("⚠️ ALERTAS DETECTADOS:")
        for alert in validator.alerts[-5:]:  # Últimos 5 alertas
            logger.warning(f"  {alert}")
    else:
        logger.info("✅ Nenhum alerta crítico detectado")
    
    logger.info("="*60)
    
    st.success("✅ Verificação de integridade concluída - Ver logs no terminal")

# Seções do dashboard (modo interface)
if not backend_mode:
    # Métricas principais em destaque
    col1, col2, col3, col4 = st.columns(4)
    
    # Executar uma verificação rápida para obter métricas atuais
    quick_check = validator.run_integrity_check()
    security_metrics = quick_check["security_metrics"]
    
    with col1:
        st.metric(
            "🔐 Segurança Geral", 
            f"{security_metrics['overall_security_score']:.1f}%",
            delta=f"{quick_check['summary']['security_level']}"
        )
    
    with col2:
        st.metric(
            "🌐 Integridade da Rede", 
            f"{security_metrics['network_integrity']:.1f}%",
            delta=f"{security_metrics['healthy_nodes']}/{security_metrics['total_nodes']} nós"
        )
    
    with col3:
        st.metric(
            "🗳️ Capacidade de Consenso", 
            f"{security_metrics['consensus_score']:.1f}%",
            delta="✅ Ativo" if quick_check['summary']['quorum_reached'] else "❌ Inativo"
        )
    
    with col4:
        st.metric(
            "🚨 Ataques Detectados", 
            quick_check['summary']['attacks_detected'],
            delta="🔴 CRÍTICO" if quick_check['summary']['attacks_detected'] > 0 else "✅ SEGURO"
        )

    # Alertas de segurança críticos
    if quick_check["attacks"]:
        st.error("🚨 **ALERTAS DE SEGURANÇA CRÍTICOS DETECTADOS**")
        for attack in quick_check["attacks"]:
            severity_color = {
                "CRITICAL": "🔴",
                "HIGH": "🟠", 
                "MEDIUM": "🟡",
                "LOW": "🟢"
            }
            
            with st.expander(f"{severity_color.get(attack['severity'], '⚪')} {attack['type']} - {attack['severity']}"):
                st.write(f"**Description:** {attack['description']}")
                st.write(f"**Affected Nodes:** {', '.join(attack['affected_nodes'][:5])}")
                if len(attack['affected_nodes']) > 5:
                    st.write(f"**... and {len(attack['affected_nodes']) - 5} more nodes**")
                st.write(f"**Recommendation:** {attack['recommendation']}")

    # Tabs para organizar informações
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Status Geral", 
        "🔍 Análise de Nós", 
        "📈 Métricas de Performance", 
        "🛡️ Segurança Avançada",
        "⚡ Verificação Completa"
    ])
    
    with tab1:
        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader("🧠 Status do Nó Individual")
            status = get_node_status()
            st.metric("ID do Nó", status["node_id"])
            st.metric("Tipo", status["node_type"].upper())
            st.metric("Status", "Online ✅" if status["online"] else "Offline ❌")
            st.metric("Saúde", "Saudável ✅" if status["is_healthy"] else "Instável ⚠️")

        with col2:
            st.subheader("📡 Métricas de Rede")
            st.metric("Latência", f"{status['latency_ms']} ms")
            st.metric("Pacotes Enviados", status["packets_sent"])
            st.metric("Pacotes Recebidos", status["packets_received"])
            st.metric("Taxa de Perda", f"{status['packet_loss_ratio']:.2%}")

        with col3:
            st.subheader("🔐 Status de Consenso")
            st.metric("Consenso", "Ativo ✅" if status["consensus_participation"] else "Inativo ❌")
            st.metric("Blockchain", "Sincronizado ✅" if status["blockchain_sync"] else "Dessincronizado ❌")
            st.metric("CPU", f"{status['cpu_usage']}%")
            st.metric("Memória", f"{status['memory_usage']}%")

    with tab2:
        st.subheader("🔍 Análise Detalhada dos Nós da Rede")
        
        # Tabela com todos os nós
        if quick_check["nodes"]:
            nodes_df = pd.DataFrame(quick_check["nodes"])
            
            # Selecionar colunas importantes para exibição
            display_columns = [
                "node_id", "node_type", "online", "latency_ms", 
                "packet_loss_ratio", "cpu_usage", "memory_usage", 
                "is_healthy", "can_participate_consensus"
            ]
            
            display_df = nodes_df[display_columns].copy()
            display_df["packet_loss_ratio"] = display_df["packet_loss_ratio"].apply(lambda x: f"{x:.2%}")
            display_df["latency_ms"] = display_df["latency_ms"].apply(lambda x: f"{x:.1f}ms")
            display_df["cpu_usage"] = display_df["cpu_usage"].apply(lambda x: f"{x:.1f}%")
            display_df["memory_usage"] = display_df["memory_usage"].apply(lambda x: f"{x:.1f}%")
            
            st.dataframe(
                display_df,
                use_container_width=True,
                column_config={
                    "node_id": st.column_config.TextColumn("ID do Nó"),
                    "node_type": st.column_config.TextColumn("Tipo"),
                    "online": st.column_config.CheckboxColumn("Online"),
                    "latency_ms": st.column_config.TextColumn("Latência"),
                    "packet_loss_ratio": st.column_config.TextColumn("Perda Pacotes"),
                    "cpu_usage": st.column_config.TextColumn("CPU"),
                    "memory_usage": st.column_config.TextColumn("Memória"),
                    "is_healthy": st.column_config.CheckboxColumn("Saudável"),
                    "can_participate_consensus": st.column_config.CheckboxColumn("Consenso")
                }
            )

    with tab3:
        st.subheader("📈 Métricas de Performance da Rede")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Gráfico de latência ao longo do tempo
            st.subheader("⏱️ Latência ao Longo do Tempo")
            latency_df = generate_latency_data()
            fig_latency = px.line(
                latency_df, 
                x="timestamp", 
                y="latency_ms", 
                title="Variação da Latência",
                markers=True
            )
            
            # Adicionar linhas de referência
            fig_latency.add_hline(
                y=validator.benchmarks["avg_latency_ms"], 
                line_dash="dash", 
                line_color="green",
                annotation_text=f"Benchmark: {validator.benchmarks['avg_latency_ms']} ms"
            )
            
            fig_latency.add_hline(
                y=CONFIG["max_latency_ms"], 
                line_dash="dash", 
                line_color="red",
                annotation_text=f"Limite: {CONFIG['max_latency_ms']} ms"
            )
            
            st.plotly_chart(fig_latency, use_container_width=True)
        
        with col2:
            # Gráfico de distribuição de tipos de nós
            st.subheader("🔧 Distribuição de Tipos de Nós")
            node_dist = security_metrics["node_distribution"]
            
            if node_dist:
                fig_dist = px.pie(
                    values=list(node_dist.values()),
                    names=list(node_dist.keys()),
                    title="Distribuição por Tipo de Nó"
                )
                st.plotly_chart(fig_dist, use_container_width=True)
            
            # Métricas de balanceamento
            st.metric("⚖️ Score de Balanceamento", f"{security_metrics['balance_score']:.1f}%")
            st.metric("🛡️ Score de Resilência", f"{security_metrics['resilience_score']:.1f}%")

    with tab4:
        st.subheader("�️ Análise Avançada de Segurança")
        
        # Dashboard de segurança
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("🔐 Score Geral de Segurança", f"{security_metrics['overall_security_score']:.1f}%")
            st.metric("🌐 Integridade da Rede", f"{security_metrics['network_integrity']:.1f}%")
            st.metric("🗳️ Capacidade de Consenso", f"{security_metrics['consensus_score']:.1f}%")
        
        with col2:
            st.metric("⏱️ Latência Média", f"{security_metrics['avg_latency_ms']:.1f}ms")
            st.metric("💻 CPU Médio", f"{security_metrics['avg_cpu_usage']:.1f}%")
            st.metric("🧠 Memória Média", f"{security_metrics['avg_memory_usage']:.1f}%")
        
        with col3:
            st.metric("📊 Nós Totais", security_metrics['total_nodes'])
            st.metric("✅ Nós Saudáveis", security_metrics['healthy_nodes'])
            st.metric("🗳️ Capazes de Consenso", security_metrics['consensus_capable_nodes'])
        
        # Gráfico de radar para métricas de segurança
        st.subheader("📊 Radar de Segurança")
        
        radar_data = {
            "Métrica": [
                "Integridade", "Consenso", "Resilência", 
                "Balanceamento", "Performance"
            ],
            "Score": [
                security_metrics['network_integrity'],
                security_metrics['consensus_score'],
                security_metrics['resilience_score'],
                security_metrics['balance_score'],
                max(0, 100 - security_metrics['avg_latency_ms'])  # Performance inversa da latência
            ]
        }
        
        fig_radar = px.line_polar(
            pd.DataFrame(radar_data),
            r="Score",
            theta="Métrica",
            line_close=True,
            title="Radar de Métricas de Segurança"
        )
        fig_radar.update_traces(fill='toself')
        st.plotly_chart(fig_radar, use_container_width=True)

    with tab5:
        # Verificação de integridade completa
        if st.button("🔍 Executar Verificação Completa de Integridade", type="primary"):
            with st.spinner("Executando verificação completa..."):
                cycle_result = validator.run_integrity_check()
                
            # Resultados da verificação
            st.success("✅ Verificação concluída!")
            
            col_summary1, col_summary2, col_summary3 = st.columns(3)
            
            with col_summary1:
                st.metric("🔍 Nós Analisados", cycle_result['summary']['total_nodes'])
                st.metric("💚 Nós Saudáveis", cycle_result['summary']['healthy_nodes'])
                st.metric("📈 Saúde da Rede", f"{cycle_result['summary']['health_percentage']}%")
                
            with col_summary2:
                st.metric("⏱️ Latência Média", f"{cycle_result['summary']['avg_latency_ms']} ms")
                st.metric("🗳️ Quorum", "✅ Atingido" if cycle_result['summary']['quorum_reached'] else "❌ Não Atingido")
                st.metric("🌐 Rede Estável", "✅ Sim" if cycle_result['summary']['network_stable'] else "❌ Não")
            
            with col_summary3:
                st.metric("🚨 Ataques Detectados", cycle_result['summary']['attacks_detected'])
                st.metric("🔐 Nível de Segurança", cycle_result['summary']['security_level'])
                st.metric("⏱️ Duração", f"{cycle_result['duration_seconds']:.2f}s")
            
            # Mostrar ataques detectados
            if cycle_result["attacks"]:
                st.error("🚨 **ATAQUES/ANOMALIAS DETECTADOS**")
                for attack in cycle_result["attacks"]:
                    with st.expander(f"⚠️ {attack['type']} - Severidade: {attack['severity']}"):
                        st.write(attack['description'])
                        st.write(f"**Recomendação:** {attack['recommendation']}")
                        st.write(f"**Nós Afetados:** {len(attack['affected_nodes'])}")

    # Alertas em tempo real (sempre visível)
    if validator.alerts:
        st.subheader("🚨 Alertas Recentes do Sistema")
        for alert in validator.alerts[-5:]:  # Últimos 5 alertas
            st.warning(alert)

    # Mensagens da rede (simuladas)
    st.subheader("💬 Log de Mensagens da Rede")
    with st.expander("Ver mensagens recentes"):
        for i in range(8):
            timestamp = pd.Timestamp.now().strftime('%H:%M:%S')
            node_id = f"aeon-{random.randint(1000,9999)}"
            message_types = [
                "consensus_vote", "block_validation", "heartbeat", 
                "data_sync", "peer_discovery", "blockchain_sync",
                "security_check", "integrity_validation"
            ]
            message_type = random.choice(message_types)
            status_icon = random.choice(["✅", "✅", "✅", "⚠️"])
            st.text(f"[{timestamp}] {node_id}: {message_type.upper()} {status_icon}")

    # Informações do sistema
    with st.expander("📊 Benchmarks e Configurações do Sistema"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Benchmarks Atuais")
            st.json(validator.benchmarks)
        
        with col2:
            st.subheader("⚙️ Configurações")
            st.json(CONFIG)

    st.success(f"🔄 Painel atualizado. Próxima verificação em {refresh_rate} segundos...")

# Execução automática
if backend_mode:
    time.sleep(refresh_rate)
    st.experimental_rerun()
else:
    # Auto refresh normal
    time.sleep(refresh_rate)
    st.experimental_rerun()
