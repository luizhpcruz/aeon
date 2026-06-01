"""
📡 AEONCOSMA Quantum Communication Channel
Simulação de comunicação quântica com proteção criptográfica
Copyright 2025 - Luiz H. P. Cruz
"""

import asyncio
import random
import cmath
import numpy as np
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass

@dataclass
class QuantumState:
    """Estado quântico simulado"""
    amplitude_0: complex
    amplitude_1: complex
    measurement_probability: float
    entangled: bool = False
    
    def measure(self) -> int:
        """Simular medição quântica"""
        prob_0 = abs(self.amplitude_0) ** 2
        return 0 if random.random() < prob_0 else 1
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "amplitude_0": [self.amplitude_0.real, self.amplitude_0.imag],
            "amplitude_1": [self.amplitude_1.real, self.amplitude_1.imag],
            "measurement_probability": self.measurement_probability,
            "entangled": self.entangled
        }

@dataclass
class QuantumMessage:
    """Mensagem quântica"""
    id: str
    sender: str
    receiver: str
    qubits: List[QuantumState]
    classical_bits: List[int]
    timestamp: float
    protocol: str = "BB84"  # Protocolo de distribuição de chaves quânticas
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "sender": self.sender,
            "receiver": self.receiver,
            "qubits": [q.to_dict() for q in self.qubits],
            "classical_bits": self.classical_bits,
            "timestamp": self.timestamp,
            "protocol": self.protocol
        }

class QuantumChannel:
    """📡 Canal de comunicação quântica simulado"""
    
    def __init__(self):
        self.version = "1.0.0"
        self.author = "Luiz H. P. Cruz"
        self.channel_id = f"quantum_ch_{random.randint(1000, 9999)}"
        self.noise_level = 0.05  # 5% de ruído
        self.entanglement_fidelity = 0.98  # 98% de fidelidade
        
        # Estado do canal
        self.is_open = False
        self.message_queue: List[QuantumMessage] = []
        self.entangled_pairs: List[Tuple[QuantumState, QuantumState]] = []
        
        # Estatísticas
        self.stats = {
            "messages_sent": 0,
            "messages_received": 0,
            "entangled_pairs_created": 0,
            "quantum_errors": 0,
            "channel_opened": datetime.now()
        }
    
    def _create_qubit(self, bit_value: int, basis: str = "Z") -> QuantumState:
        """Criar um qubit em uma base específica"""
        if basis == "Z":  # Base computacional
            if bit_value == 0:
                return QuantumState(amplitude_0=1+0j, amplitude_1=0+0j, measurement_probability=1.0)
            else:
                return QuantumState(amplitude_0=0+0j, amplitude_1=1+0j, measurement_probability=1.0)
        elif basis == "X":  # Base de Hadamard
            if bit_value == 0:
                # |+⟩ = (|0⟩ + |1⟩)/√2
                return QuantumState(
                    amplitude_0=1/np.sqrt(2), 
                    amplitude_1=1/np.sqrt(2), 
                    measurement_probability=0.5
                )
            else:
                # |-⟩ = (|0⟩ - |1⟩)/√2
                return QuantumState(
                    amplitude_0=1/np.sqrt(2), 
                    amplitude_1=-1/np.sqrt(2), 
                    measurement_probability=0.5
                )
    
    def _apply_noise(self, qubit: QuantumState) -> QuantumState:
        """Aplicar ruído quântico no canal"""
        if random.random() < self.noise_level:
            # Simular erro de bit flip
            qubit.amplitude_0, qubit.amplitude_1 = qubit.amplitude_1, qubit.amplitude_0
            self.stats["quantum_errors"] += 1
        return qubit
    
    def _create_entangled_pair(self) -> Tuple[QuantumState, QuantumState]:
        """Criar par de qubits emaranhados (estado de Bell)"""
        # |Φ+⟩ = (|00⟩ + |11⟩)/√2
        qubit_a = QuantumState(
            amplitude_0=1/np.sqrt(2),
            amplitude_1=0+0j,
            measurement_probability=0.5,
            entangled=True
        )
        qubit_b = QuantumState(
            amplitude_0=0+0j,
            amplitude_1=1/np.sqrt(2),
            measurement_probability=0.5,
            entangled=True
        )
        
        self.stats["entangled_pairs_created"] += 1
        return (qubit_a, qubit_b)
    
    async def open_channel(self) -> Dict[str, Any]:
        """Abrir canal quântico"""
        self.is_open = True
        
        # Criar alguns pares emaranhados iniciais
        for _ in range(5):
            pair = self._create_entangled_pair()
            self.entangled_pairs.append(pair)
        
        await asyncio.sleep(0.1)  # Simular tempo de estabelecimento
        
        result = {
            "status": "channel_opened",
            "channel_id": self.channel_id,
            "noise_level": self.noise_level,
            "entanglement_fidelity": self.entanglement_fidelity,
            "initial_entangled_pairs": len(self.entangled_pairs),
            "timestamp": datetime.now().isoformat()
        }
        
        print(f"📡 Canal quântico {self.channel_id} aberto")
        return result
    
    async def send_message(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Enviar mensagem via canal quântico"""
        if not self.is_open:
            await self.open_channel()
        
        message_text = data.get('message', '')
        sender = data.get('sender', 'unknown')
        receiver = data.get('receiver', 'unknown')
        protocol = data.get('protocol', 'BB84')
        
        # Converter mensagem para bits
        message_bits = [int(bit) for bit in ''.join(format(ord(c), '08b') for c in message_text)]
        
        # Preparar qubits usando protocolo BB84 (simulado)
        qubits = []
        classical_bits = []
        
        for bit in message_bits:
            # Escolher base aleatória
            basis = random.choice(['Z', 'X'])
            qubit = self._create_qubit(bit, basis)
            
            # Aplicar ruído do canal
            qubit = self._apply_noise(qubit)
            
            qubits.append(qubit)
            classical_bits.append(1 if basis == 'X' else 0)  # Informação da base
        
        # Criar mensagem quântica
        message_id = f"qmsg_{random.randint(10000, 99999)}"
        quantum_msg = QuantumMessage(
            id=message_id,
            sender=sender,
            receiver=receiver,
            qubits=qubits,
            classical_bits=classical_bits,
            timestamp=datetime.now().timestamp(),
            protocol=protocol
        )
        
        # Adicionar à fila
        self.message_queue.append(quantum_msg)
        self.stats["messages_sent"] += 1
        
        # Simular tempo de transmissão quântica
        await asyncio.sleep(0.2)
        
        result = {
            "status": "quantum_message_sent",
            "message_id": message_id,
            "sender": sender,
            "receiver": receiver,
            "qubits_sent": len(qubits),
            "protocol": protocol,
            "channel_noise": self.noise_level,
            "quantum_errors": self.stats["quantum_errors"],
            "timestamp": datetime.now().isoformat()
        }
        
        print(f"📡 Mensagem quântica {message_id} enviada ({len(qubits)} qubits)")
        return result
    
    async def receive_message(self, message_id: str) -> Dict[str, Any]:
        """Receber e decodificar mensagem quântica"""
        # Procurar mensagem na fila
        message = None
        for msg in self.message_queue:
            if msg.id == message_id:
                message = msg
                break
        
        if not message:
            return {
                "status": "error",
                "error": "Mensagem não encontrada",
                "timestamp": datetime.now().isoformat()
            }
        
        # Simular medição dos qubits
        measured_bits = []
        for qubit in message.qubits:
            measured_bit = qubit.measure()
            measured_bits.append(measured_bit)
        
        # Reconstruir mensagem (simplificado)
        # Em um protocolo real BB84, haveria reconciliação de bases
        try:
            # Converter bits para caracteres
            chars = []
            for i in range(0, len(measured_bits), 8):
                if i + 8 <= len(measured_bits):
                    byte_bits = measured_bits[i:i+8]
                    char_code = int(''.join(map(str, byte_bits)), 2)
                    if 32 <= char_code <= 126:  # Caracteres imprimíveis
                        chars.append(chr(char_code))
            
            decoded_message = ''.join(chars)
        except:
            decoded_message = "[Erro na decodificação quântica]"
        
        self.stats["messages_received"] += 1
        
        # Simular tempo de decodificação
        await asyncio.sleep(0.1)
        
        result = {
            "status": "quantum_message_received",
            "message_id": message_id,
            "sender": message.sender,
            "receiver": message.receiver,
            "decoded_message": decoded_message,
            "qubits_measured": len(message.qubits),
            "protocol": message.protocol,
            "transmission_time": datetime.now().timestamp() - message.timestamp,
            "timestamp": datetime.now().isoformat()
        }
        
        print(f"📡 Mensagem quântica {message_id} recebida e decodificada")
        return result
    
    def generate_quantum_key(self, key_length: int = 256) -> Dict[str, Any]:
        """Gerar chave criptográfica usando distribuição quântica (QKD)"""
        if not self.entangled_pairs:
            # Criar mais pares emaranhados se necessário
            for _ in range(key_length // 2):
                pair = self._create_entangled_pair()
                self.entangled_pairs.append(pair)
        
        # Simular protocolo QKD
        key_bits = []
        for i in range(min(key_length, len(self.entangled_pairs))):
            pair = self.entangled_pairs[i]
            # Medir o primeiro qubit do par
            bit = pair[0].measure()
            key_bits.append(bit)
        
        # Converter para string hexadecimal
        key_bytes = []
        for i in range(0, len(key_bits), 8):
            if i + 8 <= len(key_bits):
                byte_bits = key_bits[i:i+8]
                byte_value = int(''.join(map(str, byte_bits)), 2)
                key_bytes.append(byte_value)
        
        quantum_key = ''.join(format(b, '02x') for b in key_bytes)
        
        return {
            "status": "quantum_key_generated",
            "key_length": len(quantum_key) * 4,  # bits
            "key": quantum_key,
            "entanglement_fidelity": self.entanglement_fidelity,
            "timestamp": datetime.now().isoformat()
        }
    
    def get_channel_status(self) -> Dict[str, Any]:
        """Obter status do canal quântico"""
        uptime = (datetime.now() - self.stats["channel_opened"]).total_seconds()
        
        return {
            "channel_id": self.channel_id,
            "version": self.version,
            "author": self.author,
            "is_open": self.is_open,
            "noise_level": self.noise_level,
            "entanglement_fidelity": self.entanglement_fidelity,
            "messages_in_queue": len(self.message_queue),
            "entangled_pairs_available": len(self.entangled_pairs),
            "uptime_seconds": uptime,
            "statistics": self.stats
        }
    
    def shutdown(self):
        """Fechar canal quântico"""
        self.is_open = False
        self.message_queue.clear()
        self.entangled_pairs.clear()
        print(f"📡 Canal quântico {self.channel_id} fechado")
