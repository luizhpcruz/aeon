# aeoncosma/main.py
"""
🚀 AEONCOSMA MAIN - Orquestrador Principal
Sistema integrado P2P com IA autônoma e análise fractal
Desenvolvido por Luiz Cruz - 2025
"""

import asyncio
import threading
import time
import signal
import sys
import os
from datetime import datetime
from typing import Dict, List, Any, Optional

# Importações dos módulos do sistema
sys.path.append(os.path.dirname(__file__))

try:
    from networking.network_handler import NetworkHandler
    from networking.peer_discovery import PeerDiscovery
    from core.feedback_module import FeedbackModule
    from core.aeon_core_simplified import AeonCoreSimplified
    print("✅ Todos os módulos principais carregados")
except ImportError as e:
    print(f"❌ Erro ao importar módulos: {e}")
    sys.exit(1)

class AeonCosmaOrchestrator:
    """
    Orquestrador principal do sistema AEONCOSMA
    Gerencia todos os componentes de forma integrada
    """
    
    def __init__(self, node_id: str = "aeon_main", host: str = "127.0.0.1", port: int = 9000):
        self.node_id = node_id
        self.host = host
        self.port = port
        self.running = False
        
        # Componentes principais
        self.network_handler = None
        self.peer_discovery = None
        self.feedback_module = None
        self.aeon_core = None
        
        # Threads de execução
        self.threads = []
        
        # Configuração do sistema
        self.config = {
            "discovery_port": port + 1000,  # Porta para descoberta UDP
            "heartbeat_interval": 30,       # Intervalo de heartbeat
            "stats_interval": 60,           # Intervalo de estatísticas
            "auto_connect": True,           # Conexão automática a peers
            "max_peers": 50,               # Máximo de peers
            "ai_decision_interval": 10      # Intervalo de decisões IA
        }
        
        # Estatísticas globais
        self.stats = {
            "start_time": None,
            "total_connections": 0,
            "total_decisions": 0,
            "total_discoveries": 0,
            "network_health": 0.0,
            "last_update": None
        }
        
        print(f"🚀 [AEONCOSMA] Orquestrador inicializado: {node_id}@{host}:{port}")

    async def initialize(self):
        """Inicializa todos os componentes"""
        print(f"🔧 [AEONCOSMA] Inicializando componentes...")
        
        try:
            # 1. AEON Core (Motor de IA)
            self.aeon_core = AeonCoreSimplified(self.node_id)
            print("✅ AEON Core inicializado")
            
            # 2. Feedback Module (Sistema de Reputação)
            self.feedback_module = FeedbackModule()
            print("✅ Feedback Module inicializado")
            
            # 3. Network Handler (Gerenciador de Rede)
            def network_message_callback(message):
                """Callback para mensagens de rede"""
                try:
                    # Processa mensagem via AEON Core
                    context = {
                        "message": message,
                        "timestamp": datetime.now().isoformat(),
                        "node_id": self.node_id
                    }
                    
                    decision = self.aeon_core.make_decision(context)
                    return {"status": "processed", "approved": decision["approved"]}
                except Exception as e:
                    print(f"⚠️ [AEONCOSMA] Erro no callback de rede: {e}")
                    return {"status": "error", "message": str(e)}
            
            self.network_handler = NetworkHandler(
                node_id=self.node_id,
                port=self.port,
                message_callback=network_message_callback
            )
            print("✅ Network Handler inicializado")
            
            # 4. Peer Discovery (Descoberta Automática)
            self.peer_discovery = PeerDiscovery(
                node_id=self.node_id,
                port=self.port,
                broadcast_port=self.config["discovery_port"]
            )
            print("✅ Peer Discovery inicializado")
            
            # 5. Configurar callbacks
            self._setup_callbacks()
            print("✅ Callbacks configurados")
            
            print(f"🎯 [AEONCOSMA] Todos os componentes inicializados com sucesso!")
            return True
            
        except Exception as e:
            print(f"❌ [AEONCOSMA] Erro na inicialização: {e}")
            return False

    def _setup_callbacks(self):
        """Configura callbacks entre componentes"""
        
        # Callback: Peer descoberto -> Conectar automaticamente
        def on_peer_discovered(peer_info):
            if self.config["auto_connect"] and self.network_handler:
                try:
                    print(f"🔗 [AEONCOSMA] Auto-conectando ao peer descoberto: {peer_info['node_id']}")
                    
                    # Cria contexto para decisão do AEON
                    context = {
                        "node_id": peer_info["node_id"],
                        "host": peer_info["host"],
                        "port": peer_info["port"],
                        "timestamp": datetime.now().isoformat(),
                        "reputation_score": self.feedback_module.get_score(peer_info["node_id"]),
                        "discovery_method": "auto_discovery"
                    }
                    
                    # AEON decide se deve conectar
                    decision = self.aeon_core.make_decision(context)
                    
                    if decision["approved"]:
                        # Conecta via Network Handler
                        response = self.network_handler.connect_to_peer(
                            peer_info["host"], 
                            peer_info["port"]
                        )
                        
                        if response and response.get("status") == "success":
                            print(f"✅ [AEONCOSMA] Conectado com sucesso: {peer_info['node_id']}")
                            self.stats["total_connections"] += 1
                            
                            # Atualiza feedback positivo
                            self.feedback_module.update_score(
                                peer_info["node_id"], 
                                "connection", 
                                True
                            )
                        else:
                            print(f"❌ [AEONCOSMA] Falha na conexão: {peer_info['node_id']}")
                            
                            # Atualiza feedback negativo
                            self.feedback_module.update_score(
                                peer_info["node_id"], 
                                "connection", 
                                False
                            )
                    else:
                        print(f"🚫 [AEONCOSMA] AEON rejeitou conexão: {peer_info['node_id']}")
                        print(f"   Razão: {decision['reasoning']}")
                        
                except Exception as e:
                    print(f"⚠️ [AEONCOSMA] Erro no callback de descoberta: {e}")
        
        # Registra callback no peer discovery
        self.peer_discovery.on_peer_discovered = on_peer_discovered

    async def start(self):
        """Inicia o sistema completo"""
        if self.running:
            print("⚠️ [AEONCOSMA] Sistema já está em execução")
            return
        
        print(f"🚀 [AEONCOSMA] Iniciando sistema completo...")
        self.running = True
        self.stats["start_time"] = datetime.now()
        
        try:
            # 1. Inicia Network Handler
            print("🌐 Iniciando Network Handler...")
            self.network_handler.start_server()
            await asyncio.sleep(1)  # Aguarda inicialização
            
            # 2. Inicia Peer Discovery
            print("🔍 Iniciando Peer Discovery...")
            self.peer_discovery.start_auto_announce(interval_seconds=30)
            await asyncio.sleep(1)
            
            # 3. Inicia monitoramento
            print("📊 Iniciando monitoramento...")
            self._start_monitoring()
            
            # 4. Inicia loop de IA
            print("🧠 Iniciando loop de IA...")
            self._start_ai_loop()
            
            print(f"✅ [AEONCOSMA] Sistema iniciado com sucesso!")
            print(f"🌐 Rede: {self.host}:{self.port}")
            print(f"🔍 Discovery: UDP {self.config['discovery_port']}")
            print(f"🧠 IA: Decisões a cada {self.config['ai_decision_interval']}s")
            
            return True
            
        except Exception as e:
            print(f"❌ [AEONCOSMA] Erro ao iniciar sistema: {e}")
            await self.stop()
            return False

    def _start_monitoring(self):
        """Inicia thread de monitoramento"""
        def monitoring_loop():
            while self.running:
                try:
                    time.sleep(self.config["stats_interval"])
                    if self.running:
                        self._update_network_health()
                        self._print_status_report()
                        
                except Exception as e:
                    print(f"⚠️ [AEONCOSMA] Erro no monitoramento: {e}")
        
        monitor_thread = threading.Thread(target=monitoring_loop, daemon=True)
        monitor_thread.start()
        self.threads.append(monitor_thread)

    def _start_ai_loop(self):
        """Inicia loop de decisões da IA"""
        def ai_decision_loop():
            while self.running:
                try:
                    time.sleep(self.config["ai_decision_interval"])
                    if self.running:
                        self._make_autonomous_decision()
                        
                except Exception as e:
                    print(f"⚠️ [AEONCOSMA] Erro no loop de IA: {e}")
        
        ai_thread = threading.Thread(target=ai_decision_loop, daemon=True)
        ai_thread.start()
        self.threads.append(ai_thread)

    def _make_autonomous_decision(self):
        """Faz decisão autônoma da IA"""
        try:
            # Coleta contexto atual do sistema
            context = {
                "node_id": self.node_id,
                "timestamp": datetime.now().isoformat(),
                "peers_count": len(self.network_handler.peers) if self.network_handler else 0,
                "network_health": self.stats["network_health"],
                "uptime": self._get_uptime(),
                "reputation_score": self.feedback_module.get_score(self.node_id) if self.feedback_module else 0.5,
                "decision_type": "autonomous_health_check"
            }
            
            # AEON toma decisão sobre o estado da rede
            decision = self.aeon_core.make_decision(context)
            self.stats["total_decisions"] += 1
            
            # Age baseado na decisão
            if not decision["approved"] and decision["final_score"] < 0.3:
                print(f"🚨 [AEONCOSMA] IA detectou problema na rede (Score: {decision['final_score']:.3f})")
                print(f"   Ação: Iniciando limpeza e reconexão")
                self._emergency_network_cleanup()
            
        except Exception as e:
            print(f"⚠️ [AEONCOSMA] Erro na decisão autônoma: {e}")

    def _emergency_network_cleanup(self):
        """Limpeza de emergência da rede"""
        try:
            print("🧹 [AEONCOSMA] Executando limpeza de emergência...")
            
            # Limpa peers com baixa reputação
            if self.feedback_module and self.network_handler:
                low_reputation_peers = []
                for peer_id in list(self.network_handler.peers.keys()):
                    score = self.feedback_module.get_score(peer_id)
                    if score < 0.3:
                        low_reputation_peers.append(peer_id)
                
                for peer_id in low_reputation_peers:
                    print(f"🗑️ [AEONCOSMA] Removendo peer com baixa reputação: {peer_id}")
                    if peer_id in self.network_handler.peers:
                        del self.network_handler.peers[peer_id]
            
            # Força nova descoberta
            if self.peer_discovery:
                self.peer_discovery.force_announce()
                
            print("✅ [AEONCOSMA] Limpeza de emergência concluída")
            
        except Exception as e:
            print(f"❌ [AEONCOSMA] Erro na limpeza de emergência: {e}")

    def _update_network_health(self):
        """Atualiza métricas de saúde da rede"""
        try:
            health_factors = []
            
            # Fator 1: Conectividade (quantidade de peers)
            peer_count = len(self.network_handler.peers) if self.network_handler else 0
            connectivity_score = min(1.0, peer_count / 10.0)  # Ideal: 10+ peers
            health_factors.append(connectivity_score)
            
            # Fator 2: Reputação média da rede
            if self.feedback_module:
                network_health = self.feedback_module.get_network_health()
                reputation_score = network_health.get("network_health_score", 50) / 100.0
                health_factors.append(reputation_score)
            
            # Fator 3: Eficiência das decisões IA
            if self.aeon_core:
                metrics = self.aeon_core.get_performance_metrics()
                ai_score = metrics["stats"]["accuracy_rate"]
                health_factors.append(ai_score)
            
            # Calcula saúde geral
            if health_factors:
                self.stats["network_health"] = sum(health_factors) / len(health_factors)
            else:
                self.stats["network_health"] = 0.5
                
        except Exception as e:
            print(f"⚠️ [AEONCOSMA] Erro ao calcular saúde da rede: {e}")

    def _print_status_report(self):
        """Imprime relatório de status"""
        try:
            uptime = self._get_uptime()
            peer_count = len(self.network_handler.peers) if self.network_handler else 0
            
            print(f"\n📊 [AEONCOSMA] RELATÓRIO DE STATUS")
            print(f"⏱️  Uptime: {uptime}s")
            print(f"🌐 Peers conectados: {peer_count}")
            print(f"🔗 Total conexões: {self.stats['total_connections']}")
            print(f"🧠 Decisões IA: {self.stats['total_decisions']}")
            print(f"💚 Saúde da rede: {self.stats['network_health']:.1%}")
            
            if self.feedback_module:
                network_health = self.feedback_module.get_network_health()
                print(f"⭐ Score médio: {network_health.get('average_score', 0):.3f}")
            
            print(f"📈 Status: {'🟢 SAUDÁVEL' if self.stats['network_health'] > 0.7 else '🟡 ATENÇÃO' if self.stats['network_health'] > 0.4 else '🔴 CRÍTICO'}")
            print("-" * 50)
            
        except Exception as e:
            print(f"⚠️ [AEONCOSMA] Erro no relatório de status: {e}")

    def _get_uptime(self) -> int:
        """Retorna tempo de atividade em segundos"""
        if self.stats["start_time"]:
            return int((datetime.now() - self.stats["start_time"]).total_seconds())
        return 0

    async def stop(self):
        """Para o sistema completo"""
        print(f"🛑 [AEONCOSMA] Parando sistema...")
        self.running = False
        
        try:
            # Para componentes em ordem
            if self.peer_discovery:
                self.peer_discovery.stop()
                print("✅ Peer Discovery parado")
            
            if self.network_handler:
                self.network_handler.stop_server()
                print("✅ Network Handler parado")
            
            # Aguarda threads terminarem
            for thread in self.threads:
                if thread.is_alive():
                    thread.join(timeout=2)
            
            print(f"✅ [AEONCOSMA] Sistema parado com sucesso")
            
        except Exception as e:
            print(f"❌ [AEONCOSMA] Erro ao parar sistema: {e}")

    def get_system_status(self) -> Dict[str, Any]:
        """Retorna status completo do sistema"""
        status = {
            "node_id": self.node_id,
            "address": f"{self.host}:{self.port}",
            "running": self.running,
            "uptime": self._get_uptime(),
            "stats": self.stats,
            "config": self.config
        }
        
        if self.network_handler:
            status["network"] = self.network_handler.get_stats()
        
        if self.peer_discovery:
            status["discovery"] = self.peer_discovery.get_stats()
        
        if self.feedback_module:
            status["feedback"] = self.feedback_module.get_network_health()
        
        if self.aeon_core:
            status["aeon"] = self.aeon_core.get_performance_metrics()
        
        return status

async def main():
    """Função principal"""
    print("🚀 INICIANDO AEONCOSMA - SISTEMA P2P COM IA AUTÔNOMA")
    print("=" * 60)
    
    # Cria orquestrador
    orchestrator = AeonCosmaOrchestrator(
        node_id="aeon_main",
        host="127.0.0.1",
        port=9000
    )
    
    # Configura signal handlers
    def signal_handler(signum, frame):
        print(f"\n🛑 Recebido sinal {signum}, parando sistema...")
        asyncio.create_task(orchestrator.stop())
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        # Inicializa e inicia
        if await orchestrator.initialize():
            if await orchestrator.start():
                print("\n🎯 AEONCOSMA EXECUTANDO - Pressione Ctrl+C para parar")
                
                # Mantém sistema rodando
                while orchestrator.running:
                    await asyncio.sleep(1)
            else:
                print("❌ Falha ao iniciar sistema")
                return 1
        else:
            print("❌ Falha ao inicializar sistema")
            return 1
            
    except KeyboardInterrupt:
        print("\n🛑 Interrompido pelo usuário")
    except Exception as e:
        print(f"❌ Erro crítico: {e}")
    finally:
        await orchestrator.stop()
    
    return 0

if __name__ == "__main__":
    asyncio.run(main())
else:
    print("Erro: A função 'loop_for' não foi carregada corretamente.")
