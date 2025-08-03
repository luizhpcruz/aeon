"""
🔐 AEONCOSMA Crypto Engine
Motor de criptografia avançada com AES + SHA-3 + Assinatura Digital
Copyright 2025 - Luiz H. P. Cruz
"""

import hashlib
import secrets
import base64
import asyncio
from datetime import datetime
from typing import Dict, Any, Optional
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend

class CryptoEngine:
    """🔐 Motor de criptografia enterprise do AEONCOSMA"""
    
    def __init__(self):
        self.version = "1.0.0"
        self.author = "Luiz H. P. Cruz"
        self.supported_algorithms = {
            'symmetric': ['AES-256-GCM'],
            'asymmetric': ['RSA-4096'],
            'hash': ['SHA3-256', 'SHA3-512', 'BLAKE2b']
        }
        self.keys = {}
        self._generate_master_keys()
    
    def _generate_master_keys(self):
        """Gerar chaves mestras RSA-4096"""
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=4096,
            backend=default_backend()
        )
        
        self.keys['private'] = private_key
        self.keys['public'] = private_key.public_key()
    
    def compute_hash(self, data: bytes, algorithm: str = 'sha3-256') -> str:
        """Computar hash com algoritmos seguros"""
        if algorithm.lower() == 'sha3-256':
            return hashlib.sha3_256(data).hexdigest()
        elif algorithm.lower() == 'sha3-512':
            return hashlib.sha3_512(data).hexdigest()
        elif algorithm.lower() == 'blake2b':
            return hashlib.blake2b(data).hexdigest()
        else:
            # Fallback para SHA3-256
            return hashlib.sha3_256(data).hexdigest()
    
    def generate_signature(self, data: bytes) -> str:
        """Gerar assinatura digital RSA"""
        signature = self.keys['private'].sign(
            data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return base64.b64encode(signature).decode('utf-8')
    
    def verify_signature(self, data: bytes, signature: str) -> bool:
        """Verificar assinatura digital"""
        try:
            signature_bytes = base64.b64decode(signature)
            self.keys['public'].verify(
                signature_bytes,
                data,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except Exception:
            return False
    
    async def encrypt(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Criptografar dados com AES-256-GCM"""
        plaintext = str(data.get('message', '')).encode('utf-8')
        
        # Gerar chave e IV aleatórios
        key = secrets.token_bytes(32)  # 256 bits
        iv = secrets.token_bytes(12)   # 96 bits para GCM
        
        # Criptografar com AES-256-GCM
        cipher = Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(plaintext) + encryptor.finalize()
        
        # Gerar hash e assinatura
        data_hash = self.compute_hash(plaintext)
        signature = self.generate_signature(plaintext)
        
        # Simulação de processamento assíncrono
        await asyncio.sleep(0.1)
        
        result = {
            "status": "encrypted",
            "algorithm": "AES-256-GCM",
            "ciphertext": base64.b64encode(ciphertext).decode('utf-8'),
            "key": base64.b64encode(key).decode('utf-8'),
            "iv": base64.b64encode(iv).decode('utf-8'),
            "tag": base64.b64encode(encryptor.tag).decode('utf-8'),
            "hash": data_hash,
            "signature": signature,
            "timestamp": datetime.now().isoformat(),
            "engine_version": self.version
        }
        
        return result
    
    async def decrypt(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Descriptografar dados AES-256-GCM"""
        try:
            ciphertext = base64.b64decode(data['ciphertext'])
            key = base64.b64decode(data['key'])
            iv = base64.b64decode(data['iv'])
            tag = base64.b64decode(data['tag'])
            
            # Descriptografar
            cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag), backend=default_backend())
            decryptor = cipher.decryptor()
            plaintext = decryptor.update(ciphertext) + decryptor.finalize()
            
            # Verificar hash
            computed_hash = self.compute_hash(plaintext)
            hash_valid = computed_hash == data.get('hash', '')
            
            # Verificar assinatura
            signature_valid = self.verify_signature(plaintext, data.get('signature', ''))
            
            await asyncio.sleep(0.1)
            
            result = {
                "status": "decrypted",
                "message": plaintext.decode('utf-8'),
                "hash_valid": hash_valid,
                "signature_valid": signature_valid,
                "timestamp": datetime.now().isoformat()
            }
            
            return result
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def get_public_key_pem(self) -> str:
        """Obter chave pública em formato PEM"""
        public_key_pem = self.keys['public'].public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return public_key_pem.decode('utf-8')
    
    def get_engine_info(self) -> Dict[str, Any]:
        """Obter informações do engine"""
        return {
            "version": self.version,
            "author": self.author,
            "supported_algorithms": self.supported_algorithms,
            "public_key": self.get_public_key_pem(),
            "status": "operational"
        }
    
    def shutdown(self):
        """Desligar o crypto engine"""
        # Limpar chaves da memória (securamente)
        self.keys.clear()
        print("🔐 Crypto Engine desligado")
