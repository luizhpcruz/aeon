"""
🏗️ AEONCOSMA P2P Network - Desenhos Técnicos AutoCAD
Plantas baixas e desenhos técnicos detalhados
Copyright 2025 - Luiz H. P. Cruz
"""

import json
import math
from datetime import datetime
from typing import Dict, List, Tuple, Any

class TechnicalDrawingGenerator:
    """Gerador de desenhos técnicos para AutoCAD"""
    
    def __init__(self, network_data_file: str):
        self.network_data = self.load_network_data(network_data_file)
        
    def load_network_data(self, filename: str) -> Dict[str, Any]:
        """Carregar dados da rede"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data
        except Exception as e:
            print(f"❌ Erro ao carregar dados: {e}")
            return {}
    
    def create_infrastructure_plan(self) -> str:
        """Criar planta baixa da infraestrutura"""
        from aeoncosma_autocad_integration import DXFExporter
        
        print("🏗️ Gerando planta baixa da infraestrutura...")
        
        dxf = DXFExporter()
        
        # Configurar layers específicos
        dxf.add_layer("SERVERS", 1)          # Vermelho - Servidores
        dxf.add_layer("NETWORK_EQUIPMENT", 5) # Azul - Equipamentos de rede
        dxf.add_layer("CABLES", 8)           # Cinza - Cabeamento
        dxf.add_layer("ROOM_OUTLINE", 7)     # Branco - Contorno da sala
        dxf.add_layer("DIMENSIONS", 3)       # Verde - Dimensões
        dxf.add_layer("ANNOTATIONS", 2)      # Amarelo - Anotações
        
        # Sala do data center (30m x 20m)
        room_width = 3000  # 30m em centímetros
        room_height = 2000  # 20m em centímetros
        
        # Contorno da sala
        room_corners = [
            (0, 0), (room_width, 0), (room_width, room_height), (0, room_height), (0, 0)
        ]
        
        for i in range(len(room_corners) - 1):
            dxf.add_line(room_corners[i], room_corners[i+1], "ROOM_OUTLINE")
        
        # Racks de servidores (representando nós hub)
        hub_count = self.network_data.get('network_scale', {}).get('hub_nodes', 10)
        rack_width = 60  # 60cm
        rack_depth = 100  # 100cm
        
        print(f"📡 Posicionando {hub_count} racks de servidores (nós hub)...")
        
        # Disposição dos racks em 2 fileiras
        racks_per_row = hub_count // 2
        row_spacing = 800  # 8m entre fileiras
        rack_spacing = 200  # 2m entre racks
        
        for i in range(hub_count):
            row = i // racks_per_row
            pos_in_row = i % racks_per_row
            
            x = 300 + pos_in_row * (rack_width + rack_spacing)
            y = 300 + row * row_spacing
            
            # Desenhar rack
            rack_corners = [
                (x, y), (x + rack_width, y), 
                (x + rack_width, y + rack_depth), (x, y + rack_depth), (x, y)
            ]
            
            for j in range(len(rack_corners) - 1):
                dxf.add_line(rack_corners[j], rack_corners[j+1], "SERVERS")
            
            # Etiqueta do rack
            dxf.add_text((x + 10, y + rack_depth + 10), f"HUB-{i+1:02d}", 3.0, "ANNOTATIONS")
        
        # Equipamentos de rede (switches, roteadores)
        equipment_positions = [
            (100, 100, "CORE-SW-01"),
            (100, 200, "CORE-SW-02"),
            (2700, 100, "EDGE-RTR-01"),
            (2700, 200, "EDGE-RTR-02"),
            (1400, 1800, "MGMT-SW-01")
        ]
        
        print("🌐 Posicionando equipamentos de rede...")
        
        for x, y, label in equipment_positions:
            # Desenhar equipamento (retângulo)
            eq_width = 45
            eq_height = 30
            
            eq_corners = [
                (x, y), (x + eq_width, y),
                (x + eq_width, y + eq_height), (x, y + eq_height), (x, y)
            ]
            
            for j in range(len(eq_corners) - 1):
                dxf.add_line(eq_corners[j], eq_corners[j+1], "NETWORK_EQUIPMENT")
            
            dxf.add_text((x, y + eq_height + 5), label, 2.5, "ANNOTATIONS")
        
        # Cabeamento principal
        print("🔌 Desenhando cabeamento principal...")
        
        # Calhas de cabos
        cable_tray_routes = [
            [(150, 50), (2750, 50)],   # Calha horizontal inferior
            [(150, 1950), (2750, 1950)], # Calha horizontal superior
            [(150, 50), (150, 1950)],  # Calha vertical esquerda
            [(2750, 50), (2750, 1950)] # Calha vertical direita
        ]
        
        for route in cable_tray_routes:
            for i in range(len(route) - 1):
                dxf.add_line(route[i], route[i+1], "CABLES")
        
        # Conexões dos racks às calhas
        for i in range(hub_count):
            row = i // racks_per_row
            pos_in_row = i % racks_per_row
            
            rack_x = 300 + pos_in_row * (rack_width + rack_spacing) + rack_width // 2
            rack_y = 300 + row * row_spacing
            
            # Conectar à calha mais próxima
            if row == 0:  # Primeira fileira
                dxf.add_line((rack_x, rack_y), (rack_x, 50), "CABLES")
            else:  # Segunda fileira
                dxf.add_line((rack_x, rack_y + rack_depth), (rack_x, 1950), "CABLES")
        
        # Título e informações
        dxf.add_text((50, room_height + 100), "AEONCOSMA P2P NETWORK - PLANTA BAIXA DO DATA CENTER", 8.0, "ANNOTATIONS")
        dxf.add_text((50, room_height + 70), f"Data Center: {hub_count} Racks + Infraestrutura de Rede", 4.0, "ANNOTATIONS")
        dxf.add_text((50, room_height + 50), f"Escala: 1:100 | Data: {datetime.now().strftime('%d/%m/%Y')}", 3.0, "ANNOTATIONS")
        
        # Dimensões
        dxf.add_text((room_width // 2 - 100, -50), f"{room_width/100:.0f}m", 4.0, "DIMENSIONS")
        dxf.add_text((-100, room_height // 2), f"{room_height/100:.0f}m", 4.0, "DIMENSIONS")
        
        # Legenda técnica
        legend_x = room_width + 200
        legend_items = [
            ("SERVERS", "Racks de Servidores (Nós Hub)"),
            ("NETWORK_EQUIPMENT", "Equipamentos de Rede"),
            ("CABLES", "Infraestrutura de Cabeamento"),
            ("ROOM_OUTLINE", "Perímetro do Data Center")
        ]
        
        dxf.add_text((legend_x, room_height), "LEGENDA TÉCNICA", 5.0, "ANNOTATIONS")
        
        for i, (layer, description) in enumerate(legend_items):
            y_pos = room_height - 50 - i * 30
            dxf.add_line((legend_x, y_pos), (legend_x + 30, y_pos), layer)
            dxf.add_text((legend_x + 40, y_pos - 5), description, 3.0, "ANNOTATIONS")
        
        # Salvar arquivo
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'aeoncosma_infrastructure_{timestamp}.dxf'
        dxf.save_dxf(filename)
        
        return filename
    
    def create_network_diagram(self) -> str:
        """Criar diagrama de rede lógica"""
        from aeoncosma_autocad_integration import DXFExporter
        
        print("📊 Gerando diagrama de rede lógica...")
        
        dxf = DXFExporter()
        
        # Layers para diagrama lógico
        dxf.add_layer("CORE_LAYER", 1)        # Vermelho - Core
        dxf.add_layer("DISTRIBUTION_LAYER", 5) # Azul - Distribuição
        dxf.add_layer("ACCESS_LAYER", 3)      # Verde - Acesso
        dxf.add_layer("LOGICAL_CONNECTIONS", 8) # Cinza - Conexões lógicas
        dxf.add_layer("IP_ADDRESSES", 7)      # Branco - Endereços IP
        dxf.add_layer("PROTOCOLS", 2)         # Amarelo - Protocolos
        
        # Core layer (Internet e roteadores principais)
        core_y = 400
        dxf.add_circle((400, core_y), 30, "CORE_LAYER")
        dxf.add_text((350, core_y + 40), "INTERNET", 4.0, "PROTOCOLS")
        dxf.add_text((350, core_y - 60), "Core Layer", 3.0, "IP_ADDRESSES")
        
        # Distribution layer (nós hub)
        dist_y = 250
        hub_count = self.network_data.get('network_scale', {}).get('hub_nodes', 10)
        
        hub_positions = []
        for i in range(hub_count):
            x = 100 + i * 70
            hub_positions.append((x, dist_y))
            
            dxf.add_circle((x, dist_y), 20, "DISTRIBUTION_LAYER")
            dxf.add_text((x - 15, dist_y + 30), f"HUB-{i+1}", 2.5, "IP_ADDRESSES")
            dxf.add_text((x - 20, dist_y - 40), f"10.0.{i+1}.1", 2.0, "IP_ADDRESSES")
            
            # Conexão com core
            dxf.add_line((x, dist_y + 20), (400, core_y - 30), "LOGICAL_CONNECTIONS")
        
        # Access layer (amostra de nós padrão)
        access_y = 100
        standard_sample = 20  # Mostrar apenas 20 nós padrão
        
        for i in range(standard_sample):
            x = 50 + i * 35
            dxf.add_circle((x, access_y), 8, "ACCESS_LAYER")
            
            if i % 5 == 0:  # Mostrar IP apenas para alguns
                dxf.add_text((x - 15, access_y - 25), f"192.168.{i//5+1}.{i%5+10}", 1.5, "IP_ADDRESSES")
            
            # Conectar ao hub mais próximo
            closest_hub_idx = min(i // 2, hub_count - 1)
            if closest_hub_idx < len(hub_positions):
                hub_pos = hub_positions[closest_hub_idx]
                dxf.add_line((x, access_y + 8), (hub_pos[0], hub_pos[1] - 20), "LOGICAL_CONNECTIONS")
        
        # Título e especificações técnicas
        dxf.add_text((50, 500), "AEONCOSMA P2P NETWORK - DIAGRAMA LÓGICO", 8.0, "PROTOCOLS")
        dxf.add_text((50, 480), "Arquitetura de Rede Hierárquica", 4.0, "PROTOCOLS")
        
        # Especificações técnicas
        specs = [
            "ESPECIFICAÇÕES TÉCNICAS:",
            f"• Total de Nós: {self.network_data.get('network_scale', {}).get('total_nodes', 105)}",
            f"• Throughput: {self.network_data.get('traffic_analysis', {}).get('messages_per_second', 72.6):.1f} msg/s",
            f"• Disponibilidade: {self.network_data.get('network_scale', {}).get('availability', '100%')}",
            f"• Protocolo: TCP/IP sobre P2P",
            f"• Segurança: AES-256 + PKI",
            f"• Topologia: Híbrida Star-Mesh"
        ]
        
        for i, spec in enumerate(specs):
            dxf.add_text((500, 450 - i * 20), spec, 3.0, "PROTOCOLS")
        
        # Salvar arquivo
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'aeoncosma_logical_diagram_{timestamp}.dxf'
        dxf.save_dxf(filename)
        
        return filename

def main():
    """Executar geração de desenhos técnicos"""
    print("🏗️ AEONCOSMA P2P NETWORK - DESENHOS TÉCNICOS AUTOCAD")
    print("=" * 70)
    print("👨‍💻 Desenvolvido por: Luiz H. P. Cruz")
    print("📅 Data: Agosto 2025")
    print("🏗️ Desenhos Técnicos Profissionais")
    print("=" * 70)
    
    # Localizar dados da rede
    import glob
    report_files = glob.glob("massive_p2p_report_*.json")
    
    if not report_files:
        print("❌ Nenhum relatório de rede encontrado!")
        return
        
    latest_report = max(report_files)
    print(f"📄 Usando dados: {latest_report}")
    
    # Criar gerador de desenhos técnicos
    tech_drawing = TechnicalDrawingGenerator(latest_report)
    
    # Gerar desenhos
    print(f"\n🏗️ GERANDO DESENHOS TÉCNICOS...")
    
    infrastructure_file = tech_drawing.create_infrastructure_plan()
    logical_diagram_file = tech_drawing.create_network_diagram()
    
    print(f"\n✅ DESENHOS TÉCNICOS CONCLUÍDOS!")
    print(f"📁 Planta Baixa: {infrastructure_file}")
    print(f"📊 Diagrama Lógico: {logical_diagram_file}")
    
    print(f"\n📋 ARQUIVOS AUTOCAD DISPONÍVEIS:")
    print(f"1. 🏗️ aeoncosma_network_*.dxf - Topologia da Rede P2P")
    print(f"2. 🏢 {infrastructure_file} - Planta Baixa do Data Center")
    print(f"3. 📊 {logical_diagram_file} - Diagrama Lógico da Rede")
    
    print(f"\n🎯 COMO USAR NO AUTOCAD:")
    print(f"1. Abra cada arquivo DXF no AutoCAD")
    print(f"2. Use ZOOM EXTENTS (Z + E) para visualizar")
    print(f"3. Controle layers para diferentes visualizações")
    print(f"4. Use PLOT para imprimir em escalas técnicas")
    print(f"5. Combine com XREF para projetos maiores")
    
    print(f"\n🌟 APLICAÇÕES PROFISSIONAIS:")
    print(f"• Documentação técnica de projetos")
    print(f"• Apresentações para clientes")
    print(f"• Planejamento de infraestrutura")
    print(f"• Manutenção e troubleshooting")
    print(f"• Expansão da rede")
    
    print(f"\n🚀 Rede AEONCOSMA agora disponível no AutoCAD!")
    print(f"💎 Desenhos técnicos profissionais por Luiz H. P. Cruz")

if __name__ == "__main__":
    main()
