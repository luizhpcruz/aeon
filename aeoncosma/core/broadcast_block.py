# aeoncosma/core/broadcast_block.py
"""
📡 BROADCAST BLOCK - Sistema de Distribuição de Blocos
Broadcast inteligente de blocos e mensagens para rede P2P
Desenvolvido por Luiz Cruz - 2025
"""

import json
import socket
import threading
import time
from datetime import datetime
from typing import Dict, List, Tuple, Any, Optional

class BroadcastManager:
    """
    Gerenciador de broadcast para rede AEONCOSMA P2P
    """
    
    def __init__(self, max_retries: int = 3, timeout: float = 2.0):
        self.max_retries = max_retries
        self.timeout = timeout
        self.broadcast_history = []
        self.failed_peers = {}
        self.stats = {
            "total_broadcasts": 0,
            "successful_sends": 0,
            "failed_sends": 0,
            "total_peers_reached": 0
        }
        
        print(f"📡 BroadcastManager inicializado")
        print(f"⚙️ Max retries: {max_retries}, Timeout: {timeout}s")

    def broadcast_block(self, peers: List[Tuple[str, int]], block_data: Dict[str, Any], broadcast_type: str = "block") -> Dict[str, Any]:
        """
        Envia um bloco codificado em JSON para todos os peers conectados
        
        Args:
            peers: Lista de tuplas (ip, port) dos peers conectados
            block_data: Bloco ou mensagem a ser enviada
            broadcast_type: Tipo de broadcast (block, validation, message, etc.)
            
        Returns:
            Resultado detalhado do broadcast
        """
        broadcast_id = f"broadcast_{int(time.time())}_{len(self.broadcast_history)}"
        
        print(f"📡 [Broadcast {broadcast_id}] Iniciando {broadcast_type} para {len(peers)} peers...")
        
        broadcast_start = time.time()
        
        # Prepara dados do broadcast
        broadcast_data = {
            "broadcast_id": broadcast_id,
            "type": broadcast_type,
            "timestamp": datetime.now().isoformat(),
            "sender": "AEONCOSMA_Core",
            "data": block_data
        }
        
        message = json.dumps(broadcast_data).encode('utf-8')
        
        results = {
            "broadcast_id": broadcast_id,
            "type": broadcast_type,
            "total_peers": len(peers),
            "successful_peers": [],
            "failed_peers": [],
            "peer_responses": {},
            "broadcast_time": 0,
            "success_rate": 0
        }
        
        # Broadcast paralelo usando threads
        def send_to_peer(peer_address: Tuple[str, int]):
            ip, port = peer_address
            peer_key = f"{ip}:{port}"
            
            try:
                # Verifica se peer está na lista de falhas recentes
                if peer_key in self.failed_peers:
                    last_fail_time = self.failed_peers[peer_key]
                    if time.time() - last_fail_time < 60:  # Espera 1 minuto antes de tentar novamente
                        print(f"⏭️ [Broadcast] Pulando {peer_key} (falha recente)")
                        results["failed_peers"].append({
                            "address": peer_key,
                            "reason": "Recent failure - skipped"
                        })
                        return
                
                # Tenta enviar com retries
                success = False
                last_error = None
                
                for attempt in range(self.max_retries):
                    try:
                        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                            sock.settimeout(self.timeout)
                            sock.connect((ip, port))
                            
                            # Envia dados
                            sock.sendall(message)
                            
                            # Tenta receber resposta (opcional)
                            try:
                                sock.settimeout(1.0)  # Timeout menor para resposta
                                response = sock.recv(1024).decode('utf-8')
                                
                                if response:
                                    try:
                                        response_data = json.loads(response)
                                        results["peer_responses"][peer_key] = response_data
                                        print(f"📨 [Broadcast] Resposta de {peer_key}: {response_data.get('status', 'OK')}")
                                    except json.JSONDecodeError:
                                        results["peer_responses"][peer_key] = {"raw_response": response}
                                        
                            except socket.timeout:
                                # Timeout na resposta não é erro crítico
                                results["peer_responses"][peer_key] = {"status": "sent_no_response"}
                            
                            success = True
                            break
                            
                    except Exception as e:
                        last_error = str(e)
                        if attempt < self.max_retries - 1:
                            time.sleep(0.5 * (attempt + 1))  # Backoff exponencial
                
                if success:
                    results["successful_peers"].append(peer_key)
                    self.stats["successful_sends"] += 1
                    
                    # Remove da lista de falhas se existir
                    if peer_key in self.failed_peers:
                        del self.failed_peers[peer_key]
                        
                    print(f"✅ [Broadcast] Enviado para {peer_key}")
                else:
                    results["failed_peers"].append({
                        "address": peer_key,
                        "reason": last_error or "Unknown error"
                    })
                    self.stats["failed_sends"] += 1
                    
                    # Adiciona à lista de falhas
                    self.failed_peers[peer_key] = time.time()
                    
                    print(f"❌ [Broadcast] Falha ao enviar para {peer_key}: {last_error}")
                    
            except Exception as e:
                results["failed_peers"].append({
                    "address": f"{ip}:{port}",
                    "reason": f"Critical error: {str(e)}"
                })
                self.stats["failed_sends"] += 1
                print(f"💥 [Broadcast] Erro crítico para {ip}:{port}: {e}")
        
        # Executa broadcast em paralelo
        threads = []
        for peer in peers:
            thread = threading.Thread(target=send_to_peer, args=(peer,), daemon=True)
            thread.start()
            threads.append(thread)
        
        # Aguarda todos os threads terminarem
        for thread in threads:
            thread.join(timeout=self.timeout + 5)  # Timeout extra para safety
        
        # Calcula resultados finais
        broadcast_time = time.time() - broadcast_start
        results["broadcast_time"] = broadcast_time
        results["success_rate"] = (len(results["successful_peers"]) / len(peers) * 100) if peers else 0
        
        # Atualiza estatísticas globais
        self.stats["total_broadcasts"] += 1
        self.stats["total_peers_reached"] += len(results["successful_peers"])
        
        # Registra no histórico
        self.broadcast_history.append({
            "broadcast_id": broadcast_id,
            "timestamp": datetime.now().isoformat(),
            "type": broadcast_type,
            "peers_targeted": len(peers),
            "peers_reached": len(results["successful_peers"]),
            "success_rate": results["success_rate"],
            "broadcast_time": broadcast_time
        })
        
        # Limita histórico a últimos 100 broadcasts
        if len(self.broadcast_history) > 100:
            self.broadcast_history = self.broadcast_history[-100:]
        
        print(f"📊 [Broadcast {broadcast_id}] Concluído: {len(results['successful_peers'])}/{len(peers)} peers ({results['success_rate']:.1f}%) em {broadcast_time:.2f}s")
        
        return results

    def broadcast_validation_result(self, peers: List[Tuple[str, int]], node_id: str, validation_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Broadcast específico para resultados de validação
        """
        validation_broadcast = {
            "validation_type": "node_validation",
            "target_node": node_id,
            "result": validation_result,
            "validator": "AEONCOSMA_Validator",
            "network_consensus": True
        }
        
        return self.broadcast_block(peers, validation_broadcast, "validation")

    def broadcast_network_state(self, peers: List[Tuple[str, int]], network_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Broadcast do estado atual da rede
        """
        state_broadcast = {
            "state_type": "network_update",
            "network_state": network_state,
            "ledger_summary": network_state.get("ledger_summary", {}),
            "active_nodes": network_state.get("total_nodes", 0)
        }
        
        return self.broadcast_block(peers, state_broadcast, "network_state")

    def broadcast_message(self, peers: List[Tuple[str, int]], message: str, sender_id: str = "AEONCOSMA") -> Dict[str, Any]:
        """
        Broadcast de mensagem simples
        """
        message_broadcast = {
            "message_type": "general",
            "content": message,
            "sender": sender_id,
            "priority": "normal"
        }
        
        return self.broadcast_block(peers, message_broadcast, "message")

    def get_reliable_peers(self, peers: List[Tuple[str, int]]) -> List[Tuple[str, int]]:
        """
        Filtra peers confiáveis (sem falhas recentes)
        """
        reliable_peers = []
        current_time = time.time()
        
        for ip, port in peers:
            peer_key = f"{ip}:{port}"
            
            # Peer não está na lista de falhas ou falha foi há mais de 5 minutos
            if peer_key not in self.failed_peers or (current_time - self.failed_peers[peer_key]) > 300:
                reliable_peers.append((ip, port))
        
        return reliable_peers

    def cleanup_failed_peers(self, max_age_minutes: int = 10):
        """
        Remove peers da lista de falhas após tempo especificado
        """
        current_time = time.time()
        max_age_seconds = max_age_minutes * 60
        
        peers_to_remove = [
            peer_key for peer_key, fail_time in self.failed_peers.items()
            if (current_time - fail_time) > max_age_seconds
        ]
        
        for peer_key in peers_to_remove:
            del self.failed_peers[peer_key]
            
        if peers_to_remove:
            print(f"🧹 [Broadcast] Limpeza: {len(peers_to_remove)} peers removidos da lista de falhas")

    def get_broadcast_stats(self) -> Dict[str, Any]:
        """
        Retorna estatísticas detalhadas de broadcast
        """
        total_attempts = self.stats["successful_sends"] + self.stats["failed_sends"]
        overall_success_rate = (self.stats["successful_sends"] / total_attempts * 100) if total_attempts > 0 else 0
        
        return {
            "total_broadcasts": self.stats["total_broadcasts"],
            "total_send_attempts": total_attempts,
            "successful_sends": self.stats["successful_sends"],
            "failed_sends": self.stats["failed_sends"],
            "overall_success_rate": overall_success_rate,
            "total_peers_reached": self.stats["total_peers_reached"],
            "average_peers_per_broadcast": self.stats["total_peers_reached"] / self.stats["total_broadcasts"] if self.stats["total_broadcasts"] > 0 else 0,
            "failed_peers_count": len(self.failed_peers),
            "recent_broadcasts": self.broadcast_history[-10:] if self.broadcast_history else []
        }

def broadcast_block(peers: List[Tuple[str, int]], block_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Função standalone para backward compatibility
    Envia um bloco codificado em JSON para todos os peers conectados
    """
    manager = BroadcastManager()
    return manager.broadcast_block(peers, block_data)

def main():
    """Função de teste para o sistema de broadcast"""
    print("🧪 Testando sistema de broadcast...")
    
    # Peers de teste (provavelmente não vão responder, mas testa a lógica)
    test_peers = [
        ("127.0.0.1", 9001),
        ("127.0.0.1", 9002),
        ("127.0.0.1", 9003)
    ]
    
    # Cria manager
    manager = BroadcastManager(max_retries=2, timeout=1.0)
    
    # Teste 1: Broadcast de bloco
    print("\n--- Teste 1: Broadcast de Bloco ---")
    test_block = {
        "type": "validation",
        "data": {
            "node": "test_node_001",
            "score": 85,
            "status": "validated"
        }
    }
    
    result1 = manager.broadcast_block(test_peers, test_block, "test_block")
    print(f"Resultado: {result1['success_rate']:.1f}% de sucesso")
    
    # Teste 2: Broadcast de mensagem
    print("\n--- Teste 2: Broadcast de Mensagem ---")
    result2 = manager.broadcast_message(test_peers, "Hello AEONCOSMA Network!", "test_sender")
    print(f"Resultado: {result2['success_rate']:.1f}% de sucesso")
    
    # Teste 3: Estatísticas
    print("\n--- Teste 3: Estatísticas ---")
    stats = manager.get_broadcast_stats()
    print(f"Total broadcasts: {stats['total_broadcasts']}")
    print(f"Success rate geral: {stats['overall_success_rate']:.1f}%")
    print(f"Peers falhando: {stats['failed_peers_count']}")

if __name__ == "__main__":
    main()
