#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 Script simples para gerar visualizações da UHE
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import webbrowser
import os
from datetime import datetime

def criar_visualizacao_simples():
    """Criar uma visualização simples da UHE Itaipu"""
    print("🎨 Criando visualização da UHE Itaipu...")
    
    # Configurar figura
    fig, ax = plt.subplots(1, 1, figsize=(16, 10), dpi=100)
    fig.patch.set_facecolor('white')
    
    # Configurar limites
    ax.set_xlim(0, 1200)
    ax.set_ylim(0, 700)
    ax.set_aspect('equal')
    
    # Título
    ax.text(600, 650, '🏗️ UHE ITAIPU - PLANTA BAIXA', 
            fontsize=20, fontweight='bold', ha='center',
            bbox=dict(boxstyle="round,pad=0.5", facecolor='#4CAF50', alpha=0.8))
    
    # Subtítulo
    ax.text(600, 620, '🚀 Sistema AEON Digital Twin - Luiz H. P. Cruz', 
            fontsize=12, ha='center', style='italic')
    
    # Cores
    cores = {
        'barragem': '#8B4513',
        'casa_forcas': '#2E7D32', 
        'turbinas': '#1976D2',
        'vertedouro': '#00BCD4',
        'agua': '#64B5F6'
    }
    
    # RESERVATÓRIO
    reservatorio = patches.Ellipse((400, 500), 500, 150, 
                                 facecolor=cores['agua'], 
                                 edgecolor='#2196F3',
                                 linewidth=3, alpha=0.6)
    ax.add_patch(reservatorio)
    ax.text(400, 500, '💧 RESERVATÓRIO\n29.0 km³', 
            fontsize=12, ha='center', va='center', fontweight='bold',
            bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.9))
    
    # BARRAGEM
    barragem = patches.Rectangle((200, 350), 600, 15, 
                               facecolor=cores['barragem'], 
                               edgecolor='black', linewidth=2)
    ax.add_patch(barragem)
    ax.text(500, 380, '🏔️ BARRAGEM\n196m × 7,919m', 
            fontsize=11, ha='center', fontweight='bold',
            bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.9))
    
    # CASA DE FORÇAS
    casa_forcas = patches.Rectangle((850, 300), 200, 100, 
                                  facecolor=cores['casa_forcas'], 
                                  edgecolor='black', linewidth=2)
    ax.add_patch(casa_forcas)
    ax.text(950, 350, '🏭 CASA DE FORÇAS\n20 Turbinas\n14,000 MW', 
            fontsize=10, ha='center', va='center', fontweight='bold', color='white')
    
    # TURBINAS (pontos representando cada uma)
    for i in range(20):
        if i < 10:
            x = 870 + (i * 16)
            y = 330
        else:
            x = 870 + ((i-10) * 16)
            y = 370
        
        turbina = patches.Circle((x, y), 6, 
                               facecolor=cores['turbinas'], 
                               edgecolor='white', linewidth=1)
        ax.add_patch(turbina)
        ax.text(x, y, str(i+1), fontsize=6, ha='center', va='center', 
               color='white', fontweight='bold')
    
    # VERTEDOURO
    vertedouro = patches.Rectangle((400, 330), 150, 40, 
                                 facecolor=cores['vertedouro'], 
                                 edgecolor='black', linewidth=2)
    ax.add_patch(vertedouro)
    ax.text(475, 350, '🌊 VERTEDOURO', 
            fontsize=10, ha='center', va='center', fontweight='bold')
    
    # ESPECIFICAÇÕES TÉCNICAS
    specs_text = """
⚡ ESPECIFICAÇÕES TÉCNICAS:
• Potência: 14,000 MW
• Turbinas: 20 Francis
• Geração: 103.1 TWh/ano
• Altura: 196 metros  
• Comprimento: 7,919 metros
• Volume: 29.0 km³
• Área: 1,350 km²
• Construção: 1984
• Investimento: US$ 27 bilhões
    """
    
    ax.text(50, 550, specs_text, fontsize=9, fontweight='bold',
            bbox=dict(boxstyle="round,pad=0.5", facecolor='lightblue', alpha=0.8),
            verticalalignment='top')
    
    # COORDENADAS
    ax.text(50, 250, '📍 Coordenadas:\n-25.4084°, -54.5882°\n🧭 Rio Paraná', 
            fontsize=10, fontweight='bold',
            bbox=dict(boxstyle="round,pad=0.3", facecolor='orange', alpha=0.8))
    
    # DIMENSÕES
    ax.annotate('', xy=(200, 400), xytext=(800, 400),
               arrowprops=dict(arrowstyle='<->', color='red', lw=2))
    ax.text(500, 410, '7,919 m', fontsize=11, ha='center', 
            color='red', fontweight='bold',
            bbox=dict(boxstyle="round,pad=0.2", facecolor='white', alpha=0.9))
    
    # LEGENDA
    legend_elements = [
        patches.Patch(color=cores['barragem'], label='🏔️ Barragem'),
        patches.Patch(color=cores['casa_forcas'], label='🏭 Casa de Forças'),
        patches.Patch(color=cores['turbinas'], label='🔧 Turbinas'),
        patches.Patch(color=cores['vertedouro'], label='🌊 Vertedouro'),
        patches.Patch(color=cores['agua'], label='💧 Reservatório')
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=10)
    
    # FOOTER
    ax.text(600, 50, f'📅 Gerado em: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")} | '
                     '🔬 Sistema AEON Digital Twin', 
            fontsize=12, ha='center', fontweight='bold',
            bbox=dict(boxstyle="round,pad=0.3", facecolor='#4CAF50', alpha=0.9))
    
    # Remover eixos
    ax.set_xticks([])
    ax.set_yticks([])
    ax.grid(True, alpha=0.3)
    
    # Salvar
    filename = 'UHE_ITAIPU_VISUALIZACAO_AEON.png'
    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches='tight', facecolor='white')
    
    print(f"✅ Visualização salva como: {filename}")
    
    # Mostrar
    plt.show()
    
    return filename

def abrir_html():
    """Abrir a visualização HTML no navegador"""
    html_file = 'UHE_ITAIPU_PLANTA_INTERATIVA.html'
    
    if os.path.exists(html_file):
        try:
            webbrowser.open(f'file://{os.path.abspath(html_file)}')
            print(f"🌐 Visualização HTML aberta: {html_file}")
        except Exception as e:
            print(f"❌ Erro: {e}")
            print(f"📁 Abra manualmente: {os.path.abspath(html_file)}")
    else:
        print(f"❌ Arquivo não encontrado: {html_file}")

if __name__ == "__main__":
    print("🚀 VISUALIZADOR UHE ITAIPU - AEON")
    print("👨‍💻 Luiz H. P. Cruz")
    print("="*50)
    
    # Gerar visualização
    arquivo = criar_visualizacao_simples()
    
    # Abrir HTML
    print("\n🌐 Abrindo visualização interativa...")
    abrir_html()
    
    print("\n✅ Visualizações geradas com sucesso!")
    print(f"📁 Arquivo PNG: {arquivo}")
    print("📁 Arquivo HTML: UHE_ITAIPU_PLANTA_INTERATIVA.html")
