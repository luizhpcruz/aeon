"""
🏗️ AEONCOSMA P2P Network to AutoCAD Integration
Exportar resultados da rede P2P para AutoCAD (DXF)
Copyright 2025 - Luiz H. P. Cruz
"""

import json
import math
import random
from datetime import datetime
from typing import Dict, List, Tuple, Any
import numpy as np

class DXFExporter:
    """Exportador DXF para AutoCAD"""
    
    def __init__(self):
        self.entities = []
        self.layers = {}
        self.colors = {
            'hub_nodes': 1,      # Vermelho
            'standard_nodes': 5, # Azul
            'connections': 8,    # Cinza escuro
            'text': 7,          # Branco/Preto
            'title': 2,         # Amarelo
            'stats': 3          # Verde
        }
        
    def add_layer(self, name: str, color: int = 7):
        """Adicionar camada (layer)"""
        self.layers[name] = color
        
    def add_circle(self, center: Tuple[float, float], radius: float, layer: str = "0", color: int = None):
        """Adicionar círculo"""
        entity = {
            'type': 'CIRCLE',
            'center': center,
            'radius': radius,
            'layer': layer,
            'color': color or self.colors.get(layer, 7)
        }
        self.entities.append(entity)
        
    def add_line(self, start: Tuple[float, float], end: Tuple[float, float], layer: str = "0", color: int = None):
        """Adicionar linha"""
        entity = {
            'type': 'LINE',
            'start': start,
            'end': end,
            'layer': layer,
            'color': color or self.colors.get(layer, 7)
        }
        self.entities.append(entity)
        
    def add_text(self, position: Tuple[float, float], text: str, height: float = 2.0, layer: str = "0", color: int = None):
        """Adicionar texto"""
        entity = {
            'type': 'TEXT',
            'position': position,
            'text': str(text),
            'height': height,
            'layer': layer,
            'color': color or self.colors.get(layer, 7)
        }
        self.entities.append(entity)
        
    def write_dxf_header(self, f):
        """Escrever cabeçalho DXF"""
        f.write("0\nSECTION\n")
        f.write("2\nHEADER\n")
        f.write("9\n$ACADVER\n")
        f.write("1\nAC1015\n")  # AutoCAD 2000
        f.write("9\n$INSBASE\n")
        f.write("10\n0.0\n")
        f.write("20\n0.0\n")
        f.write("30\n0.0\n")
        f.write("0\nENDSEC\n")
        
    def write_dxf_tables(self, f):
        """Escrever tabelas DXF (layers)"""
        f.write("0\nSECTION\n")
        f.write("2\nTABLES\n")
        
        # Tabela de layers
        f.write("0\nTABLE\n")
        f.write("2\nLAYER\n")
        f.write("5\n2\n")
        f.write("100\nAcDbSymbolTable\n")
        f.write(f"70\n{len(self.layers) + 1}\n")
        
        # Layer padrão
        f.write("0\nLAYER\n")
        f.write("5\n10\n")
        f.write("100\nAcDbSymbolTableRecord\n")
        f.write("100\nAcDbLayerTableRecord\n")
        f.write("2\n0\n")
        f.write("70\n0\n")
        f.write("6\nCONTINUOUS\n")
        
        # Layers personalizados
        for layer_name, color in self.layers.items():
            f.write("0\nLAYER\n")
            f.write("5\n11\n")
            f.write("100\nAcDbSymbolTableRecord\n")
            f.write("100\nAcDbLayerTableRecord\n")
            f.write(f"2\n{layer_name}\n")
            f.write("70\n0\n")
            f.write(f"62\n{color}\n")
            f.write("6\nCONTINUOUS\n")
            
        f.write("0\nENDTAB\n")
        f.write("0\nENDSEC\n")
        
    def write_dxf_entities(self, f):
        """Escrever entidades DXF"""
        f.write("0\nSECTION\n")
        f.write("2\nENTITIES\n")
        
        for entity in self.entities:
            if entity['type'] == 'CIRCLE':
                f.write("0\nCIRCLE\n")
                f.write("5\nA0\n")
                f.write("100\nAcDbEntity\n")
                f.write(f"8\n{entity['layer']}\n")
                f.write(f"62\n{entity['color']}\n")
                f.write("100\nAcDbCircle\n")
                f.write(f"10\n{entity['center'][0]}\n")
                f.write(f"20\n{entity['center'][1]}\n")
                f.write("30\n0.0\n")
                f.write(f"40\n{entity['radius']}\n")
                
            elif entity['type'] == 'LINE':
                f.write("0\nLINE\n")
                f.write("5\nA1\n")
                f.write("100\nAcDbEntity\n")
                f.write(f"8\n{entity['layer']}\n")
                f.write(f"62\n{entity['color']}\n")
                f.write("100\nAcDbLine\n")
                f.write(f"10\n{entity['start'][0]}\n")
                f.write(f"20\n{entity['start'][1]}\n")
                f.write("30\n0.0\n")
                f.write(f"11\n{entity['end'][0]}\n")
                f.write(f"21\n{entity['end'][1]}\n")
                f.write("31\n0.0\n")
                
            elif entity['type'] == 'TEXT':
                f.write("0\nTEXT\n")
                f.write("5\nA2\n")
                f.write("100\nAcDbEntity\n")
                f.write(f"8\n{entity['layer']}\n")
                f.write(f"62\n{entity['color']}\n")
                f.write("100\nAcDbText\n")
                f.write(f"10\n{entity['position'][0]}\n")
                f.write(f"20\n{entity['position'][1]}\n")
                f.write("30\n0.0\n")
                f.write(f"40\n{entity['height']}\n")
                f.write(f"1\n{entity['text']}\n")
                f.write("50\n0.0\n")
                
        f.write("0\nENDSEC\n")
        
    def save_dxf(self, filename: str):
        """Salvar arquivo DXF"""
        with open(filename, 'w') as f:
            self.write_dxf_header(f)
            self.write_dxf_tables(f)
            self.write_dxf_entities(f)
            f.write("0\nEOF\n")
        print(f"✅ Arquivo DXF salvo: {filename}")

class AEONCOSMACADIntegration:
    """Integração AEONCOSMA com AutoCAD"""
    
    def __init__(self, network_data_file: str):
        self.network_data = self.load_network_data(network_data_file)
        self.dxf = DXFExporter()
        self.setup_layers()
        
    def load_network_data(self, filename: str) -> Dict[str, Any]:
        """Carregar dados da rede"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            print(f"✅ Dados da rede carregados: {filename}")
            return data
        except Exception as e:
            print(f"❌ Erro ao carregar dados: {e}")
            return {}
            
    def setup_layers(self):
        """Configurar layers do AutoCAD"""
        self.dxf.add_layer("HUB_NODES", 1)        # Vermelho - Nós Hub
        self.dxf.add_layer("STANDARD_NODES", 5)   # Azul - Nós Padrão
        self.dxf.add_layer("CONNECTIONS", 8)      # Cinza - Conexões
        self.dxf.add_layer("LABELS", 7)           # Branco - Rótulos
        self.dxf.add_layer("TITLE", 2)            # Amarelo - Título
        self.dxf.add_layer("STATS", 3)            # Verde - Estatísticas
        self.dxf.add_layer("BORDER", 6)           # Magenta - Borda
        
    def generate_network_layout(self) -> Dict[str, Tuple[float, float]]:
        """Gerar layout da rede para visualização CAD"""
        print("🎨 Gerando layout da rede para AutoCAD...")
        
        node_positions = {}
        
        # Configurar seed para reprodutibilidade
        np.random.seed(42)
        random.seed(42)
        
        # Posições dos nós hub (disposição circular central)
        hub_count = self.network_data.get('network_scale', {}).get('hub_nodes', 10)
        hub_radius = 50  # Raio do círculo central
        
        for i in range(hub_count):
            angle = (2 * math.pi * i) / hub_count
            x = hub_radius * math.cos(angle)
            y = hub_radius * math.sin(angle)
            node_positions[f"hub_{i:03d}"] = (x, y)
            
        # Posições dos nós padrão (disposição em anéis externos)
        standard_count = self.network_data.get('network_scale', {}).get('standard_nodes', 95)
        
        # Distribuir em 3 anéis concêntricos
        nodes_per_ring = [30, 35, 30]  # Distribuição aproximada
        radii = [100, 150, 200]  # Raios dos anéis
        
        node_idx = 0
        for ring_idx, (count, radius) in enumerate(zip(nodes_per_ring, radii)):
            for i in range(count):
                if node_idx >= standard_count:
                    break
                    
                # Adicionar variação aleatória para tornar menos regular
                angle = (2 * math.pi * i) / count + random.uniform(-0.2, 0.2)
                r = radius + random.uniform(-15, 15)
                x = r * math.cos(angle)
                y = r * math.sin(angle)
                
                node_positions[f"node_{node_idx:03d}"] = (x, y)
                node_idx += 1
                
        print(f"✅ Layout gerado para {len(node_positions)} nós")
        return node_positions
        
    def draw_network_topology(self, node_positions: Dict[str, Tuple[float, float]]):
        """Desenhar topologia da rede"""
        print("🏗️ Desenhando topologia da rede...")
        
        # Desenhar conexões (sample para não sobrecarregar)
        hub_nodes = [pos for node, pos in node_positions.items() if node.startswith('hub_')]
        standard_nodes = [pos for node, pos in node_positions.items() if node.startswith('node_')]
        
        # Conexões entre hubs (mesh topology)
        print("🔗 Desenhando conexões entre hubs...")
        for i, pos1 in enumerate(hub_nodes):
            for j, pos2 in enumerate(hub_nodes[i+1:], i+1):
                self.dxf.add_line(pos1, pos2, "CONNECTIONS")
                
        # Conexões hub-nó (sample - apenas algumas para visualização)
        print("⭐ Desenhando conexões hub-nó...")
        connection_sample = min(200, len(standard_nodes))  # Limitar conexões
        
        for i in range(connection_sample):
            if i < len(standard_nodes):
                standard_pos = standard_nodes[i]
                # Conectar ao hub mais próximo
                closest_hub = min(hub_nodes, key=lambda h: 
                    math.sqrt((h[0] - standard_pos[0])**2 + (h[1] - standard_pos[1])**2))
                self.dxf.add_line(standard_pos, closest_hub, "CONNECTIONS")
                
        # Algumas conexões entre nós padrão
        print("🌐 Desenhando conexões entre nós padrão...")
        for i in range(0, min(50, len(standard_nodes)), 5):
            if i + 1 < len(standard_nodes):
                self.dxf.add_line(standard_nodes[i], standard_nodes[i+1], "CONNECTIONS")
                
    def draw_nodes(self, node_positions: Dict[str, Tuple[float, float]]):
        """Desenhar nós da rede"""
        print("🔵 Desenhando nós da rede...")
        
        # Desenhar nós hub
        hub_count = 0
        for node_id, pos in node_positions.items():
            if node_id.startswith('hub_'):
                self.dxf.add_circle(pos, 5.0, "HUB_NODES")  # Círculo maior para hubs
                self.dxf.add_text((pos[0] + 6, pos[1] + 2), f"H{hub_count}", 2.0, "LABELS")
                hub_count += 1
                
        # Desenhar nós padrão
        node_count = 0
        for node_id, pos in node_positions.items():
            if node_id.startswith('node_'):
                if node_count % 5 == 0:  # Desenhar apenas alguns para não sobrecarregar
                    self.dxf.add_circle(pos, 2.0, "STANDARD_NODES")  # Círculo menor
                    if node_count % 20 == 0:  # Rótulos apenas alguns
                        self.dxf.add_text((pos[0] + 3, pos[1] + 1), f"N{node_count}", 1.5, "LABELS")
                node_count += 1
                
    def add_title_and_info(self):
        """Adicionar título e informações"""
        print("📝 Adicionando título e informações...")
        
        # Título principal
        self.dxf.add_text((-100, 250), "AEONCOSMA P2P NETWORK", 8.0, "TITLE")
        self.dxf.add_text((-100, 240), "Rede P2P Massiva - 105 Nós Ativos", 4.0, "TITLE")
        self.dxf.add_text((-100, 230), f"Desenvolvido por: Luiz H. P. Cruz", 3.0, "TITLE")
        self.dxf.add_text((-100, 220), f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}", 2.5, "TITLE")
        
        # Estatísticas
        stats_y = 200
        stats = [
            f"Total de Nós: {self.network_data.get('network_scale', {}).get('total_nodes', 105)}",
            f"Nós Hub: {self.network_data.get('network_scale', {}).get('hub_nodes', 10)}",
            f"Nós Padrão: {self.network_data.get('network_scale', {}).get('standard_nodes', 95)}",
            f"Conexões: {self.network_data.get('connectivity', {}).get('total_connections', 1131)}",
            f"Disponibilidade: {self.network_data.get('network_scale', {}).get('availability', '100%')}",
            f"Throughput: {self.network_data.get('traffic_analysis', {}).get('messages_per_second', 72.6):.1f} msg/s",
            f"Performance: {self.network_data.get('performance_metrics', {}).get('throughput_rating', 'EXCEPCIONAL')}"
        ]
        
        for i, stat in enumerate(stats):
            self.dxf.add_text((-100, stats_y - i*8), stat, 2.5, "STATS")
            
    def add_legend(self):
        """Adicionar legenda"""
        print("🏷️ Adicionando legenda...")
        
        legend_x = 150
        legend_y = 200
        
        # Título da legenda
        self.dxf.add_text((legend_x, legend_y), "LEGENDA", 4.0, "TITLE")
        
        # Elementos da legenda
        self.dxf.add_circle((legend_x, legend_y - 15), 5.0, "HUB_NODES")
        self.dxf.add_text((legend_x + 10, legend_y - 17), "Nós Hub (10 unidades)", 2.5, "LABELS")
        
        self.dxf.add_circle((legend_x, legend_y - 30), 2.0, "STANDARD_NODES")
        self.dxf.add_text((legend_x + 10, legend_y - 32), "Nós Padrão (95 unidades)", 2.5, "LABELS")
        
        self.dxf.add_line((legend_x, legend_y - 45), (legend_x + 15, legend_y - 45), "CONNECTIONS")
        self.dxf.add_text((legend_x + 20, legend_y - 47), "Conexões P2P", 2.5, "LABELS")
        
    def add_border(self):
        """Adicionar borda do desenho"""
        border_points = [
            (-120, -250), (220, -250), (220, 270), (-120, 270), (-120, -250)
        ]
        
        for i in range(len(border_points) - 1):
            self.dxf.add_line(border_points[i], border_points[i+1], "BORDER")
            
    def generate_autocad_drawing(self) -> str:
        """Gerar desenho completo para AutoCAD"""
        print("🏗️ GERANDO DESENHO PARA AUTOCAD...")
        print("=" * 60)
        
        # Gerar layout da rede
        node_positions = self.generate_network_layout()
        
        # Desenhar elementos
        self.draw_network_topology(node_positions)
        self.draw_nodes(node_positions)
        self.add_title_and_info()
        self.add_legend()
        self.add_border()
        
        # Salvar arquivo DXF
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        dxf_filename = f'aeoncosma_network_{timestamp}.dxf'
        self.dxf.save_dxf(dxf_filename)
        
        print(f"✅ Desenho AutoCAD gerado: {dxf_filename}")
        return dxf_filename

def main():
    """Executar integração com AutoCAD"""
    print("🏗️ AEONCOSMA P2P NETWORK - INTEGRAÇÃO AUTOCAD")
    print("=" * 60)
    print("👨‍💻 Desenvolvido por: Luiz H. P. Cruz")
    print("📅 Data: Agosto 2025")
    print("🇧🇷 Tecnologia 100% Brasileira")
    print("=" * 60)
    
    # Localizar dados da rede
    import glob
    report_files = glob.glob("massive_p2p_report_*.json")
    
    if not report_files:
        print("❌ Nenhum relatório de rede encontrado!")
        print("💡 Execute primeiro: python massive_p2p_network.py")
        return
        
    latest_report = max(report_files)
    print(f"📄 Usando dados: {latest_report}")
    
    # Criar integração
    cad_integration = AEONCOSMACADIntegration(latest_report)
    
    # Gerar desenho
    dxf_file = cad_integration.generate_autocad_drawing()
    
    print(f"\n🎉 INTEGRAÇÃO AUTOCAD CONCLUÍDA!")
    print(f"📁 Arquivo DXF: {dxf_file}")
    print(f"\n📋 INSTRUÇÕES PARA AUTOCAD:")
    print(f"1. Abra o AutoCAD")
    print(f"2. Use o comando OPEN ou Ctrl+O")
    print(f"3. Selecione o arquivo: {dxf_file}")
    print(f"4. Use ZOOM EXTENTS (comando Z + E) para ver toda a rede")
    print(f"5. Use LAYER para controlar a visibilidade das camadas")
    print(f"\n🌟 LAYERS DISPONÍVEIS:")
    print(f"   • HUB_NODES (Vermelho) - Nós Hub")
    print(f"   • STANDARD_NODES (Azul) - Nós Padrão")
    print(f"   • CONNECTIONS (Cinza) - Conexões P2P")
    print(f"   • LABELS (Branco) - Rótulos")
    print(f"   • TITLE (Amarelo) - Título")
    print(f"   • STATS (Verde) - Estatísticas")
    print(f"   • BORDER (Magenta) - Borda")
    
    print(f"\n🚀 Rede AEONCOSMA com 105 nós agora visualizada no AutoCAD!")
    print(f"💎 Tecnologia de ponta desenvolvida por Luiz H. P. Cruz")
    
    return dxf_file

if __name__ == "__main__":
    main()
