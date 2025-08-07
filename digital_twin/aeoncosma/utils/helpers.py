"""
🛠️ AEONCOSMA Utilities
Funções auxiliares para plataforma AEONCOSMA
Copyright 2025 - Luiz H. P. Cruz
"""

import json
import hashlib
import base64
import logging
import asyncio
from datetime import datetime
from typing import Dict, List, Any, Optional, Union
from pathlib import Path

class Logger:
    """Sistema de logging para AEONCOSMA"""
    
    def __init__(self, name: str, level: str = "INFO"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, level.upper()))
        
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
    
    def info(self, message: str):
        self.logger.info(message)
    
    def error(self, message: str):
        self.logger.error(message)
    
    def warning(self, message: str):
        self.logger.warning(message)
    
    def debug(self, message: str):
        self.logger.debug(message)

class ConfigManager:
    """Gerenciador de configurações"""
    
    def __init__(self, config_file: str = "aeoncosma_config.json"):
        self.config_file = Path(config_file)
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Carregar configurações do arquivo"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        
        # Configurações padrão
        return {
            "system": {
                "version": "1.0.0",
                "author": "Luiz H. P. Cruz",
                "debug": False
            },
            "crypto": {
                "default_algorithm": "AES-GCM",
                "key_size": 256,
                "use_hardware_rng": True
            },
            "p2p": {
                "max_peers": 50,
                "message_timeout": 30,
                "discovery_interval": 60
            },
            "quantum": {
                "noise_level": 0.05,
                "entanglement_fidelity": 0.98,
                "default_protocol": "BB84"
            },
            "cosmos": {
                "default_model": "ΛCDM",
                "mcmc_steps": 1000,
                "confidence_level": 0.68
            }
        }
    
    def save_config(self):
        """Salvar configurações no arquivo"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"Erro ao salvar configuração: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Obter valor de configuração"""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        """Definir valor de configuração"""
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value

class DataValidator:
    """Validador de dados"""
    
    @staticmethod
    def is_valid_json(data: str) -> bool:
        """Verificar se string é JSON válido"""
        try:
            json.loads(data)
            return True
        except:
            return False
    
    @staticmethod
    def is_valid_base64(data: str) -> bool:
        """Verificar se string é Base64 válido"""
        try:
            base64.b64decode(data)
            return True
        except:
            return False
    
    @staticmethod
    def is_valid_hex(data: str) -> bool:
        """Verificar se string é hexadecimal válido"""
        try:
            int(data, 16)
            return True
        except:
            return False
    
    @staticmethod
    def validate_cosmological_params(params: Dict[str, float]) -> bool:
        """Validar parâmetros cosmológicos"""
        required = ['H0', 'Omega_m', 'Omega_L']
        
        # Verificar se todos os parâmetros estão presentes
        if not all(param in params for param in required):
            return False
        
        # Verificar limites físicos
        if params['H0'] < 50 or params['H0'] > 100:  # km/s/Mpc
            return False
        
        if params['Omega_m'] < 0 or params['Omega_m'] > 1:
            return False
        
        if params['Omega_L'] < 0 or params['Omega_L'] > 1:
            return False
        
        # Verificar se soma é aproximadamente 1 (universo plano)
        total = params['Omega_m'] + params['Omega_L']
        if abs(total - 1.0) > 0.1:
            return False
        
        return True

class SecurityUtils:
    """Utilitários de segurança"""
    
    @staticmethod
    def generate_secure_id(length: int = 16) -> str:
        """Gerar ID seguro"""
        import secrets
        return secrets.token_hex(length)
    
    @staticmethod
    def hash_data(data: str, algorithm: str = "sha256") -> str:
        """Hash de dados"""
        hash_obj = hashlib.new(algorithm)
        hash_obj.update(data.encode('utf-8'))
        return hash_obj.hexdigest()
    
    @staticmethod
    def constant_time_compare(a: str, b: str) -> bool:
        """Comparação em tempo constante"""
        import hmac
        return hmac.compare_digest(a, b)
    
    @staticmethod
    def sanitize_input(data: str) -> str:
        """Sanitizar entrada de dados"""
        # Remover caracteres perigosos
        dangerous_chars = ['<', '>', '"', "'", '&', '\x00']
        for char in dangerous_chars:
            data = data.replace(char, '')
        
        # Limitar tamanho
        return data[:1000]

class PerformanceMonitor:
    """Monitor de performance"""
    
    def __init__(self):
        self.metrics = {}
        self.start_times = {}
    
    def start_timer(self, operation: str):
        """Iniciar timer para operação"""
        self.start_times[operation] = datetime.now()
    
    def end_timer(self, operation: str) -> float:
        """Finalizar timer e retornar duração"""
        if operation in self.start_times:
            duration = (datetime.now() - self.start_times[operation]).total_seconds()
            
            if operation not in self.metrics:
                self.metrics[operation] = []
            
            self.metrics[operation].append(duration)
            del self.start_times[operation]
            
            return duration
        return 0.0
    
    def get_average_time(self, operation: str) -> float:
        """Obter tempo médio de operação"""
        if operation in self.metrics and self.metrics[operation]:
            return sum(self.metrics[operation]) / len(self.metrics[operation])
        return 0.0
    
    def get_stats(self) -> Dict[str, Dict[str, float]]:
        """Obter estatísticas completas"""
        stats = {}
        
        for operation, times in self.metrics.items():
            if times:
                stats[operation] = {
                    "count": len(times),
                    "average": sum(times) / len(times),
                    "min": min(times),
                    "max": max(times),
                    "total": sum(times)
                }
        
        return stats

class AsyncQueue:
    """Fila assíncrona para processamento"""
    
    def __init__(self, maxsize: int = 0):
        self.queue = asyncio.Queue(maxsize=maxsize)
        self.processed = 0
        self.errors = 0
    
    async def put(self, item: Any):
        """Adicionar item à fila"""
        await self.queue.put(item)
    
    async def get(self) -> Any:
        """Obter item da fila"""
        return await self.queue.get()
    
    def task_done(self, success: bool = True):
        """Marcar tarefa como concluída"""
        self.queue.task_done()
        if success:
            self.processed += 1
        else:
            self.errors += 1
    
    async def join(self):
        """Aguardar conclusão de todas as tarefas"""
        await self.queue.join()
    
    def get_stats(self) -> Dict[str, int]:
        """Obter estatísticas da fila"""
        return {
            "queue_size": self.queue.qsize(),
            "processed": self.processed,
            "errors": self.errors,
            "success_rate": self.processed / (self.processed + self.errors) if (self.processed + self.errors) > 0 else 0
        }

class FileManager:
    """Gerenciador de arquivos"""
    
    @staticmethod
    def ensure_directory(path: Union[str, Path]):
        """Garantir que diretório existe"""
        Path(path).mkdir(parents=True, exist_ok=True)
    
    @staticmethod
    def save_json(data: Dict[str, Any], filepath: Union[str, Path]):
        """Salvar dados em JSON"""
        path = Path(filepath)
        FileManager.ensure_directory(path.parent)
        
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    @staticmethod
    def load_json(filepath: Union[str, Path]) -> Optional[Dict[str, Any]]:
        """Carregar dados de JSON"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return None
    
    @staticmethod
    def backup_file(filepath: Union[str, Path]) -> Path:
        """Criar backup de arquivo"""
        path = Path(filepath)
        if path.exists():
            backup_path = path.with_suffix(f".backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}{path.suffix}")
            backup_path.write_bytes(path.read_bytes())
            return backup_path
        return path

class EventBus:
    """Sistema de eventos"""
    
    def __init__(self):
        self.listeners = {}
        self.logger = Logger("EventBus")
    
    def subscribe(self, event_type: str, callback):
        """Inscrever-se em evento"""
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        
        self.listeners[event_type].append(callback)
        self.logger.debug(f"Subscribed to event: {event_type}")
    
    async def emit(self, event_type: str, data: Any = None):
        """Emitir evento"""
        if event_type in self.listeners:
            self.logger.debug(f"Emitting event: {event_type}")
            
            for callback in self.listeners[event_type]:
                try:
                    if asyncio.iscoroutinefunction(callback):
                        await callback(data)
                    else:
                        callback(data)
                except Exception as e:
                    self.logger.error(f"Error in event callback: {e}")
    
    def unsubscribe(self, event_type: str, callback):
        """Cancelar inscrição"""
        if event_type in self.listeners:
            try:
                self.listeners[event_type].remove(callback)
                self.logger.debug(f"Unsubscribed from event: {event_type}")
            except ValueError:
                pass

# Instâncias globais dos utilitários
config = ConfigManager()
logger = Logger("AEONCOSMA")
performance = PerformanceMonitor()
event_bus = EventBus()

# Funções de conveniência
def get_config(key: str, default: Any = None) -> Any:
    """Obter configuração"""
    return config.get(key, default)

def set_config(key: str, value: Any):
    """Definir configuração"""
    config.set(key, value)

def log_info(message: str):
    """Log de informação"""
    logger.info(message)

def log_error(message: str):
    """Log de erro"""
    logger.error(message)

def monitor_performance(operation: str):
    """Decorator para monitorar performance"""
    def decorator(func):
        async def async_wrapper(*args, **kwargs):
            performance.start_timer(operation)
            try:
                result = await func(*args, **kwargs)
                return result
            finally:
                duration = performance.end_timer(operation)
                log_info(f"Operation '{operation}' took {duration:.3f}s")
        
        def sync_wrapper(*args, **kwargs):
            performance.start_timer(operation)
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                duration = performance.end_timer(operation)
                log_info(f"Operation '{operation}' took {duration:.3f}s")
        
        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
    
    return decorator
