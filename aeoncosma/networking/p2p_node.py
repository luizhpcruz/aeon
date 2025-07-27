# aeoncosma/networking/p2p_node.py
"""
🌐 AEONCOSMA P2P NODE - Nó Descentralizado
Sistema de nós independentes com validação sequencial
Desenvolvido por Luiz Cruz - 2025
"""

import socket
import threading
import json
import time
from datetime import datetime
from typing import Dict, List, Any
import sys
import os

# Adiciona path para importações
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# 🛡️ SISTEMA DE SEGURANÇA AEONCOSMA - SEMPRE PRIMEIRO
try:
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    from security.aeoncosma_security_lock import AeonSecurityLock
    from security.aeoncosma_audit_monitor import get_audit_monitor
    from security.aeoncosma_environment_isolator import (
        EnvironmentIsolator, PortSecurityMonitor, 
        CodeSandbox, FileSystemWatchdog, initialize_advanced_security
    )
    SECURITY_ENABLED = True
    
    # Executa verificações de segurança obrigatórias
    security_lock = AeonSecurityLock()
    security_lock.enforce_all_security_measures()
    
    # Inicializa monitor de auditoria
    audit_monitor = get_audit_monitor("p2p_system")
    audit_monitor.check_suspicious_arguments(sys.argv)
    
    # 🔥 INICIALIZA DEFESAS AVANÇADAS
    print("🛡️ Inicializando defesas avançadas AEONCOSMA...")
    advanced_security = initialize_advanced_security()
    
    # Extrai componentes individuais
    env_isolator = advanced_security["env_isolator"]
    port_monitor = advanced_security["port_monitor"]  
    code_sandbox = advanced_security["code_sandbox"]
    fs_watchdog = advanced_security["fs_watchdog"]
    
    print("🔥 DEFESAS AVANÇADAS ATIVAS - SISTEMA ULTRA BLINDADO!")
    
except ImportError:
    print("⚠️ Sistema de segurança não encontrado - MODO INSEGURO")
    SECURITY_ENABLED = False
    security_lock = None
    audit_monitor = None
    env_isolator = None
    port_monitor = None
    code_sandbox = None
    fs_watchdog = None
except SystemExit as e:
    print(f"🚫 EXECUÇÃO BLOQUEADA PELO SISTEMA DE SEGURANÇA: {e}")
    raise

try:
    from networking.validation_logic import validate_node
    from core.aeon_core_simplified import AeonCoreSimplified
    from core.feedback_module import FeedbackModule
    from networking.network_handler import NetworkHandler
    from networking.peer_discovery import PeerDiscovery
    MODULAR_SYSTEM = True
except ImportError:
    print("⚠️ Sistema modular não encontrado - usando modo básico")
    MODULAR_SYSTEM = False
    def validate_node(*args):
        return True

# Importações GPU opcionais
try:
    from gpu.node_brain import NodeBrain
    from gpu.gpu_utils import GPUManager
    GPU_ENHANCED = True
except ImportError:
    GPU_ENHANCED = False

class P2PNode:
    """
    Nó P2P do AEONCOSMA com validação sequencial e feedback do backend
    """
    
    def __init__(self, host="127.0.0.1", port=9000, node_id="node_001", aeon_address="http://127.0.0.1:8000/validate"):
        # 🛡️ VERIFICAÇÕES DE SEGURANÇA OBRIGATÓRIAS
        if SECURITY_ENABLED:
            # Força localhost apenas
            if host != "127.0.0.1" and host != "localhost":
                raise ValueError(f"🚫 SEGURANÇA: Host '{host}' não permitido. Apenas localhost é aceito.")
            
            # Bloqueia endereços AEON externos
            if not aeon_address.startswith("http://127.0.0.1") and not aeon_address.startswith("http://localhost"):
                raise ValueError(f"🚫 SEGURANÇA: AEON address externo não permitido: {aeon_address}")
            
            # 🔥 VERIFICAÇÕES AVANÇADAS DE SEGURANÇA
            print(f"🔒 [{node_id}] Executando verificações avançadas de segurança...")
            
            # Monitora ambiente por modificações maliciosas
            env_violations = env_isolator.monitor_environment_changes()
            if env_violations:
                print(f"🚨 [{node_id}] {len(env_violations)} violações de ambiente detectadas!")
                for violation in env_violations:
                    print(f"  ⚠️ {violation['variable']}: {violation['description']}")
            
            # Registra processo como autorizado para usar a porta
            port_monitor.register_authorized_process(node_id, [port])
            
            # Escaneia diretório atual por arquivos suspeitos
            fs_scan = fs_watchdog.scan_directory(".")
            if fs_scan["suspicious_files"]:
                print(f"🚨 [{node_id}] {len(fs_scan['suspicious_files'])} arquivos suspeitos detectados!")
                # Move arquivos suspeitos para quarentena
                for file_info in fs_scan["suspicious_files"]:
                    fs_watchdog.quarantine_file(file_info["path"])
            
            # Verifica se porta já está em uso por processo não autorizado
            port_scan = port_monitor.scan_port_usage()
            if port_scan["violations"]:
                print(f"🚨 [{node_id}] Violações de porta detectadas!")
                for violation in port_scan["violations"]:
                    if violation["port"] == port:
                        raise ValueError(f"🚫 SEGURANÇA: Porta {port} está sendo usada por processo não autorizado!")
            
            # Log de inicialização segura
            security_lock.log_execution("p2p_node_init", {
                "node_id": node_id,
                "host": host,
                "port": port,
                "aeon_address": aeon_address,
                "advanced_security_checks": "PASSED"
            })
            
            print(f"🔒 [{node_id}] Inicialização com segurança ULTRA AVANÇADA ativada")
            print(f"🛡️ [{node_id}] Ambiente isolado, portas monitoradas, sandbox ativo, filesystem protegido")
        
        self.host = host
        self.port = port
        self.node_id = node_id
        self.peers = []
        self.aeon_address = aeon_address
        self.running = False
        self.socket = None
        self.connections = []
        
        # Inicializa sistema AEON modular se disponível
        if MODULAR_SYSTEM:
            self.aeon_core = AeonCoreSimplified(self.node_id)
            self.feedback_module = FeedbackModule()
            self.network_handler = NetworkHandler(
                host=self.host,
                port=self.port,
                node_id=self.node_id,
                aeon_core=self.aeon_core,
                feedback_module=self.feedback_module
            )
            self.peer_discovery = PeerDiscovery(
                discovery_port=self.port + 1000,
                node_info={
                    "node_id": self.node_id,
                    "host": self.host,
                    "port": self.port,
                    "capabilities": ["trading", "fractal_analysis", "ai_decisions"],
                    "version": "1.0.0"
                }
            )
            print(f"🧠 [{self.node_id}] Sistema AEON Modular ativado")
        else:
            self.aeon_core = None
            self.feedback_module = None
            self.network_handler = None
            self.peer_discovery = None
            print(f"⚠️ [{self.node_id}] Modo básico - Sistema modular não disponível")
        
        # Inicializa componentes GPU opcionais
        if GPU_ENHANCED:
            try:
                self.node_brain = NodeBrain()
                self.gpu_manager = GPUManager(0)  # GPU 0 por padrão
                print(f"🎮 [{self.node_id}] GPU Enhancement ativado")
            except Exception as e:
                print(f"⚠️ [{self.node_id}] GPU Enhancement falhou: {e}")
                self.node_brain = None
                self.gpu_manager = None
        else:
            self.node_brain = None
            self.gpu_manager = None
        
        # Estatísticas do nó
        self.stats = {
            "start_time": None,
            "peers_validated": 0,
            "peers_rejected": 0,
            "messages_sent": 0,
            "messages_received": 0,
            "blocks_broadcasted": 0,
            "aeon_validations": 0,
            "gpu_operations": 0,
            "neural_decisions": 0
        }
        
        print(f"🌐 [{self.node_id}] Nó P2P AEONCOSMA inicializado")
        print(f"📍 Endereço: {self.host}:{self.port}")
        print(f"🔗 Backend AEON: {self.aeon_address}")

    def start(self):
        """Inicia o nó P2P"""
        self.running = True
        self.stats["start_time"] = datetime.now()
        
        # Thread para escutar conexões
        listen_thread = threading.Thread(target=self.listen, daemon=True)
        listen_thread.start()
        
        # Thread para estatísticas
        stats_thread = threading.Thread(target=self.stats_monitor, daemon=True)
        stats_thread.start()
        
        print(f"✅ [{self.node_id}] Nó iniciado em {self.host}:{self.port}")
        print(f"👂 [{self.node_id}] Aguardando conexões de peers...")

    def listen(self):
        """Escuta conexões de outros nós"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind((self.host, self.port))
            self.socket.listen(5)
            
            while self.running:
                try:
                    conn, addr = self.socket.accept()
                    self.connections.append(conn)
                    
                    # Processa conexão em thread separada
                    peer_thread = threading.Thread(
                        target=self.handle_peer, 
                        args=(conn, addr), 
                        daemon=True
                    )
                    peer_thread.start()
                    
                except socket.error as e:
                    if self.running:
                        print(f"❌ [{self.node_id}] Erro de socket: {e}")
                        
        except Exception as e:
            print(f"❌ [{self.node_id}] Erro crítico ao escutar: {e}")

    def handle_peer(self, conn, addr):
        """Processa conexão de um peer"""
        try:
            print(f"🤝 [{self.node_id}] Nova conexão de {addr}")
            
            # 🕵️ LOG DE AUDITORIA: Conexão recebida
            if SECURITY_ENABLED and audit_monitor:
                audit_monitor.log_connection_attempt(
                    {"source": "incoming", "address": str(addr)}, 
                    str(addr[0])
                )
                
                # 🔥 VERIFICAÇÕES AVANÇADAS EM TEMPO REAL
                # Monitora modificações de ambiente durante conexão
                env_violations = env_isolator.monitor_environment_changes()
                if env_violations:
                    print(f"🚨 [{self.node_id}] Violações de ambiente durante conexão: {len(env_violations)}")
                    audit_monitor.log_security_event("environment_violation", {
                        "violations": env_violations,
                        "connection_source": str(addr)
                    })
                
                # Verifica se houve hijacking de porta durante conexão
                port_violations = port_monitor.block_suspicious_port_activity()
                if port_violations:
                    print(f"🚨 [{self.node_id}] Atividade suspeita de porta bloqueada!")
            
            # Recebe dados do peer
            data = conn.recv(4096).decode('utf-8')
            if not data:
                return
                
            self.stats["messages_received"] += 1
            
            try:
                peer_info = json.loads(data)
                print(f"📨 [{self.node_id}] Dados recebidos: {peer_info}")
                
                # Valida o nó usando sistema modular ou básico
                if MODULAR_SYSTEM and self.aeon_core:
                    # Validação com AEON Core Simplificado
                    print(f"🧠 [{self.node_id}] Usando validação AEON Core modular")
                    
                    # Cria contexto para decisão do AEON
                    context = {
                        "node_id": peer_info["node_id"],
                        "host": peer_info["host"],
                        "port": peer_info["port"],
                        "timestamp": peer_info["timestamp"],
                        "reputation_score": self.feedback_module.get_score(peer_info["node_id"]) if self.feedback_module else 0.5,
                        "context": peer_info.get("context", {})
                    }
                    
                    # AEON decide sobre o nó
                    decision = self.aeon_core.make_decision(context)
                    is_valid = decision["approved"]
                    self.stats["aeon_validations"] += 1
                    
                    # Usa NodeBrain se disponível para segunda opinião
                    if GPU_ENHANCED and self.node_brain:
                        # Converte contexto para features neurais
                        peer_features = self.context_to_neural_features(context)
                        neural_decision = self.node_brain.make_decision(peer_features)
                        
                        # Combina decisões (AEON tem peso 0.7, Neural tem peso 0.3)
                        combined_confidence = (decision.get("final_score", 0.5) * 0.7 + 
                                             neural_decision["confidence"] * 0.3)
                        is_valid = combined_confidence > 0.5
                        self.stats["neural_decisions"] += 1
                        
                        print(f"🎮 [{self.node_id}] Decisão híbrida AEON+Neural: {combined_confidence:.3f}")
                    
                    if is_valid:
                        self.peers.append(peer_info)
                        self.stats["peers_validated"] += 1
                        
                        # 🕵️ LOG DE AUDITORIA: Validação bem-sucedida
                        if SECURITY_ENABLED and audit_monitor:
                            audit_monitor.log_validation_result(
                                peer_info["node_id"], 
                                True, 
                                "AEON Core validation successful"
                            )
                        
                        # Atualiza feedback positivo
                        if self.feedback_module:
                            self.feedback_module.update_score(peer_info["node_id"], "validation", True)
                        
                        response = {
                            "status": "accepted",
                            "node_id": self.node_id,
                            "timestamp": datetime.now().isoformat(),
                            "peer_count": len(self.peers),
                            "validation_type": "aeon_core_modular" + ("_neural" if GPU_ENHANCED and self.node_brain else ""),
                            "aeon_score": decision.get("final_score", 0),
                            "confidence": decision.get("confidence", 0)
                        }
                        
                        print(f"✅ [{self.node_id}] Nó validado pelo AEON Core: {peer_info['node_id']}")
                        
                    else:
                        self.stats["peers_rejected"] += 1
                        
                        # 🕵️ LOG DE AUDITORIA: Validação rejeitada
                        if SECURITY_ENABLED and audit_monitor:
                            audit_monitor.log_validation_result(
                                peer_info["node_id"], 
                                False, 
                                decision.get("reasoning", "AEON Core validation failed")
                            )
                        
                        # Atualiza feedback negativo
                        if self.feedback_module:
                            self.feedback_module.update_score(peer_info["node_id"], "validation", False)
                        
                        response = {
                            "status": "rejected",
                            "node_id": self.node_id,
                            "reason": "AEON Core validation failed",
                            "timestamp": datetime.now().isoformat(),
                            "validation_type": "aeon_core_modular",
                            "reasoning": decision.get("reasoning", "No reasoning provided")
                        }
                        
                        print(f"❌ [{self.node_id}] Nó rejeitado pelo AEON Core: {peer_info['node_id']}")
                        print(f"   Razão: {decision.get('reasoning', 'N/A')}")
                
                elif GPU_ENHANCED and self.node_brain:
                    # Validação apenas neural (fallback quando AEON não disponível)
                    print(f"🎮 [{self.node_id}] Usando validação Neural apenas")
                    
                    context = {
                        "node_id": peer_info["node_id"],
                        "host": peer_info["host"],
                        "port": peer_info["port"],
                        "timestamp": peer_info["timestamp"],
                        "context": peer_info.get("context", {})
                    }
                    
                    peer_features = self.context_to_neural_features(context)
                    neural_decision = self.node_brain.make_decision(peer_features)
                    is_valid = neural_decision["decision"]
                    self.stats["neural_decisions"] += 1
                    
                    if is_valid:
                        self.peers.append(peer_info)
                        self.stats["peers_validated"] += 1
                        
                        response = {
                            "status": "accepted",
                            "node_id": self.node_id,
                            "timestamp": datetime.now().isoformat(),
                            "peer_count": len(self.peers),
                            "validation_type": "neural_only",
                            "neural_confidence": neural_decision["confidence"],
                            "reasoning": neural_decision["reasoning"]
                        }
                        
                        print(f"✅ [{self.node_id}] Nó validado por IA Neural: {peer_info['node_id']}")
                        
                    else:
                        self.stats["peers_rejected"] += 1
                        response = {
                            "status": "rejected",
                            "node_id": self.node_id,
                            "reason": "Neural validation failed",
                            "timestamp": datetime.now().isoformat(),
                            "validation_type": "neural_only",
                            "reasoning": neural_decision["reasoning"]
                        }
                        
                        print(f"❌ [{self.node_id}] Nó rejeitado por IA Neural: {peer_info.get('node_id', 'unknown')}")
                
                else:
                    # Validação básica (fallback)
                    if validate_node(peer_info, self.node_id, self.peers, self.aeon_address):
                        self.peers.append(peer_info)
                        self.stats["peers_validated"] += 1
                        
                        response = {
                            "status": "accepted",
                            "node_id": self.node_id,
                            "timestamp": datetime.now().isoformat(),
                            "peer_count": len(self.peers),
                            "validation_type": "basic"
                        }
                        
                        print(f"✅ [{self.node_id}] Nó validado (modo básico): {peer_info['node_id']}")
                        
                    else:
                        self.stats["peers_rejected"] += 1
                        response = {
                            "status": "rejected",
                            "node_id": self.node_id,
                            "reason": "Basic validation failed",
                            "timestamp": datetime.now().isoformat(),
                            "validation_type": "basic"
                        }
                        
                        print(f"❌ [{self.node_id}] Nó rejeitado (modo básico): {peer_info.get('node_id', 'unknown')}")
                
                # Envia resposta
                conn.send(json.dumps(response).encode('utf-8'))
                self.stats["messages_sent"] += 1
                
            except json.JSONDecodeError as e:
                print(f"⚠️ [{self.node_id}] Erro ao decodificar JSON: {e}")
                error_response = {"status": "error", "reason": "Invalid JSON"}
                conn.send(json.dumps(error_response).encode('utf-8'))
                
        except Exception as e:
            print(f"❌ [{self.node_id}] Erro ao processar peer: {e}")
        finally:
            conn.close()

    def connect_to_peer(self, peer_host, peer_port, my_previous_node=None):
        """Conecta a outro peer"""
        try:
            print(f"🔗 [{self.node_id}] Conectando a {peer_host}:{peer_port}")
            
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            sock.connect((peer_host, peer_port))
            
            # Prepara dados para envio
            my_info = {
                "node_id": self.node_id,
                "host": self.host,
                "port": self.port,
                "previous": my_previous_node,
                "timestamp": datetime.now().isoformat(),
                "context": {
                    "peers_count": len(self.peers),
                    "uptime": self.get_uptime()
                }
            }
            
            # Envia informações
            sock.send(json.dumps(my_info).encode('utf-8'))
            self.stats["messages_sent"] += 1
            
            # Recebe resposta
            response = sock.recv(4096).decode('utf-8')
            if response:
                response_data = json.loads(response)
                self.stats["messages_received"] += 1
                
                print(f"📩 [{self.node_id}] Resposta: {response_data}")
                return response_data
                
        except Exception as e:
            print(f"❌ [{self.node_id}] Erro ao conectar com peer: {e}")
            return None
        finally:
            sock.close()

    def broadcast_message(self, message):
        """Envia mensagem para todos os peers conhecidos"""
        print(f"📢 [{self.node_id}] Broadcasting: {message}")
        
        # Usa network handler se disponível, senão método básico
        if MODULAR_SYSTEM and self.network_handler:
            result = self.network_handler.broadcast(message)
            if result:
                self.stats["blocks_broadcasted"] += 1
                print(f"📊 [{self.node_id}] Broadcast resultado: sucesso")
                return result
            else:
                print(f"⚠️ [{self.node_id}] Nenhum peer válido para broadcast")
                return {"success_rate": 0, "message": "No valid peers"}
        else:
            # Método básico original
            for peer in self.peers:
                try:
                    if peer.get("host") and peer.get("port"):
                        response = self.connect_to_peer(
                            peer["host"], 
                            peer["port"], 
                            self.node_id
                        )
                        if response:
                            print(f"✅ [{self.node_id}] Broadcast enviado para {peer['node_id']}")
                except Exception as e:
                    print(f"⚠️ [{self.node_id}] Erro no broadcast para {peer.get('node_id', 'unknown')}: {e}")

    def broadcast_validation_result(self, validated_node_id: str, validation_result: Dict):
        """Broadcast do resultado de validação para a rede"""
        if MODULAR_SYSTEM and self.network_handler:
            result = self.network_handler.broadcast({
                "type": "validation_result",
                "validated_node": validated_node_id,
                "result": validation_result
            })
            
            if result:
                print(f"📡 [{self.node_id}] Validation broadcast: sucesso")
                return result
        
        return {"success_rate": 0, "message": "Network handler not available"}

    def broadcast_network_state(self):
        """Broadcast do estado atual da rede"""
        if MODULAR_SYSTEM and self.aeon_core:
            network_state = {
                "node_id": self.node_id,
                "peers_count": len(self.peers),
                "uptime": self.get_uptime(),
                "stats": self.stats
            }
            
            if self.network_handler:
                result = self.network_handler.broadcast({
                    "type": "network_state",
                    "state": network_state
                })
                
                if result:
                    print(f"🌐 [{self.node_id}] Network state broadcast: sucesso")
                    return result
        
        return {"success_rate": 0, "message": "Network components not available"}

    def context_to_neural_features(self, context):
        """Converte contexto para features neurais para o NodeBrain"""
        if not GPU_ENHANCED:
            return None
        
        try:
            # Importa torch se disponível
            import torch
            
            features = torch.zeros(7)  # 7 features para o NodeBrain
            
            # Feature 1: Hash do node_id (normalizado)
            features[0] = hash(context.get("node_id", "")) % 1000 / 1000.0
            
            # Feature 2: Porta normalizada
            features[1] = context.get("port", 9000) / 65535.0
            
            # Feature 3: Timestamp recency (últimas 24h)
            timestamp = context.get("timestamp", datetime.now().isoformat())
            try:
                peer_time = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                age_hours = (datetime.now() - peer_time).total_seconds() / 3600
                features[2] = max(0, 1 - age_hours / 24.0)  # Mais recente = valor maior
            except:
                features[2] = 0.5
            
            # Feature 4: Reputation score
            features[3] = context.get("reputation_score", 0.5)
            
            # Feature 5: Network density (peers count)
            features[4] = min(len(self.peers) / 100.0, 1.0)
            
            # Feature 6: Uptime score
            features[5] = min(self.get_uptime() / 3600.0, 1.0)
            
            # Feature 7: Random factor for exploration
            import random
            features[6] = random.random()
            
            return features
            
        except ImportError:
            # Fallback sem torch
            return [
                hash(context.get("node_id", "")) % 1000 / 1000.0,
                context.get("port", 9000) / 65535.0,
                0.5,  # timestamp placeholder
                context.get("reputation_score", 0.5),
                min(len(self.peers) / 100.0, 1.0),
                min(self.get_uptime() / 3600.0, 1.0),
                0.5   # random placeholder
            ]
        except Exception as e:
            print(f"⚠️ [{self.node_id}] Erro ao converter contexto para features neurais: {e}")
            return None

    def get_uptime(self):
        """Retorna tempo de atividade em segundos"""
        if self.stats["start_time"]:
            return int((datetime.now() - self.stats["start_time"]).total_seconds())
        return 0

    def stats_monitor(self):
        """Monitor de estatísticas do nó"""
        while self.running:
            time.sleep(30)  # Atualiza a cada 30 segundos
            if self.running:
                stats_msg = f"📊 [{self.node_id}] Stats - Peers: {len(self.peers)}, Validados: {self.stats['peers_validated']}, Rejeitados: {self.stats['peers_rejected']}, Uptime: {self.get_uptime()}s"
                
                if MODULAR_SYSTEM and self.stats["aeon_validations"] > 0:
                    stats_msg += f", AEON Validations: {self.stats['aeon_validations']}, Broadcasts: {self.stats['blocks_broadcasted']}"
                
                if GPU_ENHANCED and self.stats["neural_decisions"] > 0:
                    stats_msg += f", Neural Decisions: {self.stats['neural_decisions']}, GPU Ops: {self.stats['gpu_operations']}"
                
                print(stats_msg)
                
                # Limpeza periódica se disponível
                if MODULAR_SYSTEM and self.network_handler:
                    pass  # Network handler faz limpeza automática

    def get_network_info(self):
        """Retorna informações da rede"""
        base_info = {
            "node_id": self.node_id,
            "address": f"{self.host}:{self.port}",
            "peers_count": len(self.peers),
            "peers": [{"node_id": p.get("node_id"), "host": p.get("host"), "port": p.get("port")} for p in self.peers],
            "stats": self.stats,
            "uptime": self.get_uptime(),
            "status": "running" if self.running else "stopped",
            "validation_mode": "aeon_core_modular" if MODULAR_SYSTEM else "basic"
        }
        
        # Adiciona informações AEON se disponível
        if MODULAR_SYSTEM:
            if self.aeon_core:
                metrics = self.aeon_core.get_performance_metrics()
                base_info["aeon_metrics"] = metrics
            
            if self.feedback_module:
                base_info["feedback_health"] = self.feedback_module.get_network_health()
            
            if self.network_handler:
                base_info["network_stats"] = self.network_handler.get_stats()
        
        # Adiciona informações GPU se disponível
        if GPU_ENHANCED:
            base_info["gpu_enhanced"] = True
            
            if self.node_brain:
                base_info["node_brain_stats"] = self.node_brain.get_brain_stats()
            
            if self.gpu_manager:
                base_info["gpu_manager_stats"] = self.gpu_manager.get_stats()
        else:
            base_info["gpu_enhanced"] = False
        
        return base_info

    def get_aeon_feedback(self):
        """Retorna feedback do AEON Core para este nó"""
        if MODULAR_SYSTEM and self.aeon_core:
            metrics = self.aeon_core.get_performance_metrics()
            return {"msg": "AEON Core modular ativo", "metrics": metrics, "code": 200}
        else:
            return {"msg": "AEON Core not available", "code": 503}

    def get_advanced_security_report(self):
        """Retorna relatório completo de segurança avançada"""
        if not SECURITY_ENABLED:
            return {"error": "Sistema de segurança não ativo", "code": 503}
        
        try:
            # Coleta relatórios de todos os sistemas de segurança
            security_report = {
                "timestamp": datetime.now().isoformat(),
                "node_id": self.node_id,
                "security_level": "ULTRA_ADVANCED",
                "systems_active": {
                    "security_lock": security_lock is not None,
                    "audit_monitor": audit_monitor is not None,
                    "environment_isolator": env_isolator is not None,
                    "port_monitor": port_monitor is not None,
                    "code_sandbox": code_sandbox is not None,
                    "filesystem_watchdog": fs_watchdog is not None
                }
            }
            
            # Relatório de isolamento de ambiente
            if env_isolator:
                security_report["environment"] = env_isolator.get_isolation_report()
            
            # Relatório de monitoramento de portas
            if port_monitor:
                security_report["ports"] = port_monitor.scan_port_usage()
            
            # Relatório do sandbox
            if code_sandbox:
                security_report["sandbox"] = code_sandbox.get_sandbox_report()
            
            # Relatório do filesystem watchdog
            if fs_watchdog:
                security_report["filesystem"] = fs_watchdog.get_watchdog_report()
            
            # Estatísticas de segurança do nó
            security_report["node_security_stats"] = {
                "total_connections": len(self.connections),
                "peers_validated": self.stats.get("peers_validated", 0),
                "peers_rejected": self.stats.get("peers_rejected", 0),
                "uptime": self.get_uptime(),
                "security_violations_detected": len(security_report.get("environment", {}).get("environment_violations", [])) +
                                               len(security_report.get("ports", {}).get("violations", [])) +
                                               len(security_report.get("sandbox", {}).get("violations", [])) +
                                               len(security_report.get("filesystem", {}).get("file_violations", []))
            }
            
            # Calcula nível de segurança geral
            total_violations = security_report["node_security_stats"]["security_violations_detected"]
            if total_violations == 0:
                security_report["overall_security_level"] = "🛡️ IMPENETRÁVEL"
                security_report["security_score"] = 100.0
            elif total_violations <= 3:
                security_report["overall_security_level"] = "🔒 ALTAMENTE SEGURO"
                security_report["security_score"] = 85.0
            elif total_violations <= 10:
                security_report["overall_security_level"] = "⚠️ MODERADAMENTE SEGURO"
                security_report["security_score"] = 60.0
            else:
                security_report["overall_security_level"] = "🚨 VULNERÁVEL"
                security_report["security_score"] = 30.0
            
            return security_report
            
        except Exception as e:
            return {"error": f"Erro ao gerar relatório de segurança: {e}", "code": 500}

    def export_ledger(self):
        """Exporta conhecimento do AEON Core"""
        if MODULAR_SYSTEM and self.aeon_core:
            return self.aeon_core.export_knowledge()
        else:
            return json.dumps({"error": "AEON Core not available"}, indent=2)

    def stop(self):
        """Para o nó P2P"""
        print(f"🛑 [{self.node_id}] Parando nó...")
        self.running = False
        
        # Fecha todas as conexões
        for conn in self.connections:
            try:
                conn.close()
            except:
                pass
                
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
                
        print(f"✅ [{self.node_id}] Nó parado com sucesso")

def main():
    """Função principal para teste"""
    import argparse
    
    parser = argparse.ArgumentParser(description='AEONCOSMA P2P Node')
    parser.add_argument('--port', type=int, default=9000, help='Porta do nó')
    parser.add_argument('--node-id', default='node_001', help='ID do nó')
    parser.add_argument('--host', default='127.0.0.1', help='Host do nó')
    
    args = parser.parse_args()
    
    # Cria e inicia nó
    node = P2PNode(
        host=args.host,
        port=args.port,
        node_id=args.node_id
    )
    
    try:
        node.start()
        print(f"🚀 [{args.node_id}] Nó em execução. Pressione Ctrl+C para parar.")
        
        # Mantém o programa rodando
        while node.running:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print(f"\n🛑 [{args.node_id}] Interrompido pelo usuário")
    finally:
        node.stop()

if __name__ == "__main__":
    main()
