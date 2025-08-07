"""
AEON Equipment Simulator - Simulador de Equipamentos Industriais
Demonstração de integração com diferentes tipos de equipamentos
"""

import random
import time
from datetime import datetime, timedelta

class AEONEquipmentSimulator:
    """Simulador de equipamentos industriais para rede AEON"""
    
    def __init__(self):
        self.equipment_database = {
            "desktop_pc": {
                "type": "💻 Desktop PC",
                "specs": {"cpu": "Intel i5-10400", "ram": "8GB DDR4", "network": "Gigabit Ethernet"},
                "os": ["Windows 11", "Ubuntu 20.04", "CentOS 8"],
                "power": "65W",
                "protocols": ["HTTP", "WebSocket", "MQTT"],
                "price_range": "R$ 2.500 - R$ 8.000",
                "compatibility": "100%"
            },
            "laptop": {
                "type": "💻 Laptop",
                "specs": {"cpu": "Intel i7-11800H", "ram": "16GB DDR4", "network": "Wi-Fi 6 + Ethernet"},
                "os": ["Windows 11", "macOS Big Sur", "Linux"],
                "power": "45W",
                "protocols": ["HTTP", "WebSocket", "VPN"],
                "price_range": "R$ 3.000 - R$ 12.000",
                "compatibility": "100%"
            },
            "industrial_workstation": {
                "type": "🖥️ Workstation Industrial",
                "specs": {"cpu": "Intel Xeon W-1290P", "ram": "32GB ECC", "network": "Dual Gigabit"},
                "os": ["Windows Server", "Red Hat Enterprise"],
                "power": "125W",
                "protocols": ["OPC UA", "Modbus TCP", "HTTP"],
                "price_range": "R$ 15.000 - R$ 40.000",
                "compatibility": "100%"
            },
            "smartphone": {
                "type": "📱 Smartphone",
                "specs": {"cpu": "Snapdragon 888", "ram": "8GB", "network": "5G + Wi-Fi 6"},
                "os": ["Android 12", "iOS 15"],
                "power": "15W",
                "protocols": ["HTTP", "WebSocket", "MQTT"],
                "price_range": "R$ 800 - R$ 4.000",
                "compatibility": "95%"
            },
            "industrial_tablet": {
                "type": "📲 Tablet Industrial",
                "specs": {"cpu": "Intel Atom x7", "ram": "8GB", "network": "4G + Wi-Fi + Ethernet"},
                "os": ["Windows 10 IoT", "Android Industrial"],
                "power": "20W",
                "protocols": ["Modbus", "OPC UA", "HTTP"],
                "price_range": "R$ 5.000 - R$ 15.000",
                "compatibility": "100%"
            },
            "ihm_siemens": {
                "type": "🎛️ IHM Siemens TP1200",
                "specs": {"display": "12' TFT", "ram": "1GB", "network": "Profinet + Ethernet"},
                "os": ["WinCC RT"],
                "power": "24V DC",
                "protocols": ["Profinet", "Modbus TCP", "S7"],
                "price_range": "R$ 8.000 - R$ 20.000",
                "compatibility": "90%"
            },
            "clp_siemens": {
                "type": "🔧 CLP Siemens S7-1500",
                "specs": {"cpu": "1515-2 PN", "memory": "1MB", "network": "Profinet"},
                "os": ["Step 7"],
                "power": "24V DC",
                "protocols": ["Profinet", "Modbus TCP", "OPC UA"],
                "price_range": "R$ 12.000 - R$ 35.000",
                "compatibility": "85%"
            },
            "protection_relay": {
                "type": "⚡ Relé ABB REF630",
                "specs": {"cpu": "ARM Cortex", "memory": "128MB", "network": "Ethernet"},
                "os": ["REF630 Firmware"],
                "power": "220V AC",
                "protocols": ["IEC 61850", "Modbus", "DNP3"],
                "price_range": "R$ 25.000 - R$ 80.000",
                "compatibility": "80%"
            },
            "energy_meter": {
                "type": "📊 Medidor Schneider PM8000",
                "specs": {"accuracy": "0.2S", "memory": "64MB", "network": "Ethernet"},
                "os": ["PowerLogic OS"],
                "power": "230V AC",
                "protocols": ["Modbus TCP", "DNP3", "IEC 61850"],
                "price_range": "R$ 8.000 - R$ 25.000",
                "compatibility": "85%"
            },
            "temp_sensor": {
                "type": "🌡️ Sensor Honeywell T7350",
                "specs": {"range": "-40°C to +85°C", "accuracy": "±0.5°C", "network": "Modbus RTU"},
                "os": ["Embedded Firmware"],
                "power": "24V DC",
                "protocols": ["Modbus RTU", "BACnet"],
                "price_range": "R$ 500 - R$ 2.000",
                "compatibility": "75%"
            },
            "iot_gateway": {
                "type": "📡 Gateway Moxa UC-8100",
                "specs": {"cpu": "ARM Cortex-A8", "ram": "1GB", "network": "Ethernet + Wi-Fi + 4G"},
                "os": ["Debian Linux"],
                "power": "12-48V DC",
                "protocols": ["Modbus", "MQTT", "OPC UA", "HTTP"],
                "price_range": "R$ 3.000 - R$ 8.000",
                "compatibility": "95%"
            },
            "solar_inverter": {
                "type": "⚡ Inversor SMA Central",
                "specs": {"power": "1000kW", "efficiency": "98.5%", "network": "Ethernet"},
                "os": ["SMA OS"],
                "power": "Grid Connected",
                "protocols": ["Modbus TCP", "SNMP", "SunSpec"],
                "price_range": "R$ 200.000 - R$ 800.000",
                "compatibility": "70%"
            },
            "ups": {
                "type": "🔋 UPS Schneider Galaxy",
                "specs": {"power": "50kVA", "efficiency": "96%", "network": "Ethernet + USB"},
                "os": ["PowerChute OS"],
                "power": "380V AC",
                "protocols": ["SNMP", "HTTP", "Modbus"],
                "price_range": "R$ 50.000 - R$ 200.000",
                "compatibility": "80%"
            },
            "industrial_switch": {
                "type": "🌐 Switch Cisco IE-3400",
                "specs": {"ports": "24x Gigabit", "poe": "740W", "network": "Layer 3"},
                "os": ["Cisco IOS"],
                "power": "PoE+ 30W/port",
                "protocols": ["SNMP", "HTTP", "SSH", "Telnet"],
                "price_range": "R$ 15.000 - R$ 40.000",
                "compatibility": "90%"
            },
            "4g_router": {
                "type": "📡 Roteador Teltonika RUT955",
                "specs": {"connectivity": "4G LTE Cat 4", "wifi": "802.11n", "network": "Ethernet"},
                "os": ["OpenWrt Linux"],
                "power": "12V DC",
                "protocols": ["HTTP", "SNMP", "MQTT", "VPN"],
                "price_range": "R$ 1.500 - R$ 4.000",
                "compatibility": "95%"
            },
            "industrial_drone": {
                "type": "🚁 Drone DJI Matrice 300",
                "specs": {"flight_time": "55min", "payload": "2.7kg", "network": "4G + Wi-Fi"},
                "os": ["DJI Flight OS"],
                "power": "Battery 5935mAh",
                "protocols": ["HTTP", "MQTT", "DJI SDK"],
                "price_range": "R$ 40.000 - R$ 120.000",
                "compatibility": "60%"
            },
            "edge_server": {
                "type": "🖥️ Servidor HPE Edgeline",
                "specs": {"cpu": "Intel Xeon D", "ram": "64GB", "network": "25GbE"},
                "os": ["Windows Server", "Ubuntu Server", "VMware"],
                "power": "600W",
                "protocols": ["HTTP", "OPC UA", "MQTT", "REST"],
                "price_range": "R$ 80.000 - R$ 300.000",
                "compatibility": "100%"
            }
        }
    
    def get_equipment_by_category(self, category: str) -> dict:
        """Retorna equipamentos por categoria"""
        category_mapping = {
            "ti": ["desktop_pc", "laptop", "industrial_workstation"],
            "mobile": ["smartphone", "industrial_tablet"],
            "industrial": ["ihm_siemens", "clp_siemens", "protection_relay", "energy_meter"],
            "iot": ["temp_sensor", "iot_gateway"],
            "energy": ["solar_inverter", "ups"],
            "network": ["industrial_switch", "4g_router"],
            "special": ["industrial_drone"],
            "infrastructure": ["edge_server"]
        }
        
        equipment_ids = category_mapping.get(category, [])
        return {k: v for k, v in self.equipment_database.items() if k in equipment_ids}
    
    def simulate_equipment_connection(self, equipment_id: str) -> dict:
        """Simula conexão de equipamento à rede AEON"""
        if equipment_id not in self.equipment_database:
            return {"success": False, "error": "Equipamento não encontrado"}
        
        equipment = self.equipment_database[equipment_id]
        
        # Simular processo de conexão
        connection_steps = [
            "🔍 Descobrindo equipamento na rede...",
            "🤝 Estabelecendo handshake inicial...",
            "🔒 Verificando certificados de segurança...",
            "⚙️ Configurando protocolos de comunicação...",
            "📊 Testando troca de dados...",
            "✅ Conexão estabelecida com sucesso!"
        ]
        
        # Calcular tempo de conexão baseado na compatibilidade
        compatibility = int(equipment["compatibility"].replace("%", ""))
        connection_time = round(6.0 - (compatibility / 100) * 4, 1)  # 2-6 segundos
        
        # Simular problemas de conexão para equipamentos menos compatíveis
        success_rate = compatibility / 100
        connection_success = random.random() < success_rate
        
        if not connection_success:
            return {
                "success": False,
                "equipment": equipment,
                "error": "Falha na conexão - verifique compatibilidade de protocolos",
                "retry_suggestion": "Instalar AEON Bridge Adapter"
            }
        
        # Dados de conexão simulados
        connection_data = {
            "success": True,
            "equipment": equipment,
            "connection_time": connection_time,
            "ip_address": f"192.168.1.{random.randint(10, 254)}",
            "port": random.randint(8000, 9999),
            "protocol_used": random.choice(equipment["protocols"]),
            "data_rate": f"{random.randint(100, 1000)} Kbps",
            "latency": f"{random.randint(5, 50)} ms",
            "signal_strength": f"{random.randint(70, 100)}%",
            "connection_steps": connection_steps,
            "timestamp": datetime.now().isoformat()
        }
        
        return connection_data
    
    def get_compatibility_matrix(self) -> dict:
        """Retorna matriz de compatibilidade por protocolo"""
        protocols = ["HTTP", "WebSocket", "MQTT", "Modbus TCP", "OPC UA", "IEC 61850", "DNP3", "SNMP"]
        
        matrix = {}
        for equipment_id, equipment in self.equipment_database.items():
            matrix[equipment_id] = {
                "name": equipment["type"],
                "protocols": equipment["protocols"],
                "compatibility": equipment["compatibility"],
                "supported_protocols": {protocol: protocol in equipment["protocols"] for protocol in protocols}
            }
        
        return matrix
    
    def generate_integration_report(self) -> dict:
        """Gera relatório de integração completo"""
        total_equipment = len(self.equipment_database)
        
        # Calcular estatísticas
        compatibilities = [int(eq["compatibility"].replace("%", "")) for eq in self.equipment_database.values()]
        avg_compatibility = sum(compatibilities) / len(compatibilities)
        
        protocol_support = {}
        for equipment in self.equipment_database.values():
            for protocol in equipment["protocols"]:
                protocol_support[protocol] = protocol_support.get(protocol, 0) + 1
        
        # Categorizar por nível de compatibilidade
        high_compat = len([c for c in compatibilities if c >= 90])
        medium_compat = len([c for c in compatibilities if 70 <= c < 90])
        low_compat = len([c for c in compatibilities if c < 70])
        
        return {
            "total_equipment_types": total_equipment,
            "average_compatibility": round(avg_compatibility, 1),
            "compatibility_distribution": {
                "high": {"count": high_compat, "percentage": round(high_compat/total_equipment*100, 1)},
                "medium": {"count": medium_compat, "percentage": round(medium_compat/total_equipment*100, 1)},
                "low": {"count": low_compat, "percentage": round(low_compat/total_equipment*100, 1)}
            },
            "most_supported_protocols": dict(sorted(protocol_support.items(), key=lambda x: x[1], reverse=True)[:5]),
            "recommended_bridges": {
                "Modbus to AEON": "Para CLPs e medidores industriais",
                "OPC UA to AEON": "Para sistemas SCADA modernos",
                "IEC 61850 to AEON": "Para proteção elétrica",
                "Serial to Ethernet": "Para equipamentos legados"
            }
        }

# Função de teste rápido
def test_equipment_connection(equipment_type: str):
    """Teste rápido de conexão de equipamento"""
    simulator = AEONEquipmentSimulator()
    return simulator.simulate_equipment_connection(equipment_type)
