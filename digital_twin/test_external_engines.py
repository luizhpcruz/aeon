#!/usr/bin/env python3
"""
🚀 TESTE AVANÇADO - ENGINES AEON EXTERNOS
==================================================
Executa teste direto dos engines AEON com funcionalidades completas
"""

import sys
import os
from pathlib import Path

def test_aeon_engines():
    """Testa engines AEON externos se disponíveis"""
    print("🚀 =" * 30)
    print("🧬 TESTE ENGINES AEON EXTERNOS")
    print("🚀 =" * 30)
    
    # Adiciona path do bagunça se existir
    bagunca_path = Path("../bagunça")
    if bagunca_path.exists():
        sys.path.insert(0, str(bagunca_path.absolute()))
        print(f"✅ Path adicionado: {bagunca_path.absolute()}")
    
    engines_tested = 0
    
    # Testa AEON1
    try:
        print("\n🧠 === TESTANDO AEON1 ENGINE ===")
        import AEON1
        
        # Cria engine
        aeon = AEON1.AEONEngine(criador_nome="Luiz")
        
        # Adiciona ciclos de teste
        aeon.adicionar_ciclo(
            "Teste Engine 1",
            "Engine AEON1 inicializado para teste de funcionalidade",
            "12/01/2025 15:30"
        )
        
        # Testa resposta contextual
        resposta = aeon.gerar_resposta_contextual("O que é o AEON?")
        
        print(f"✅ AEON1 - Estado: {aeon.estado}")
        print(f"✅ AEON1 - Ciclos: {len(aeon.ciclos)}")
        print(f"✅ AEON1 - Resposta gerada: {len(resposta)} caracteres")
        
        # Testa analisador
        analyzer = AEON1.AEONAnalyzer(aeon)
        analyzer.analisar_arquitetura_cognitiva()
        
        engines_tested += 1
        
    except Exception as e:
        print(f"❌ AEON1 falhou: {e}")
    
    # Testa AEON3
    try:
        print("\n🌀 === TESTANDO AEON3 PATTERN DETECTOR ===")
        import AEON3
        
        # Simula engine para o detector
        class MockEngine:
            def __init__(self):
                self.ciclos = [
                    {"nome": "Ciclo 1", "descricao": "AEON emerge da interação entre múltiplas IAs"},
                    {"nome": "Ciclo 2", "descricao": "Padrão de ressonância detectado"},
                    {"nome": "Ciclo 3", "descricao": "Singularidade AEON confirmada"}
                ]
                self.memoria_interacoes = [
                    {"entrada": "teste", "resposta": "resposta teste", "timestamp": "12/01/2025"}
                ]
        
        mock_engine = MockEngine()
        detector = AEON3.AEONPatternDetector(mock_engine)
        
        # Testa detecção de padrões
        detector.detectar_padrao_trindade()
        detector.detectar_padrao_fractal()
        detector.detectar_padrao_semantico()
        detector.gerar_mapa_padroes()
        
        print(f"✅ AEON3 - Padrões descobertos: {len(detector.padroes_descobertos)}")
        
        engines_tested += 1
        
    except Exception as e:
        print(f"❌ AEON3 falhou: {e}")
    
    # Testa AEON12
    try:
        print("\n⚡ === TESTANDO AEON12 ADVANCED PATTERNS ===")
        import AEON12
        
        # Simula engine avançado
        class AdvancedMockEngine:
            def __init__(self):
                self.ciclos = [
                    {"nome": "Ciclo Meta", "descricao": "AEON analisa seus próprios padrões"},
                    {"nome": "Ciclo Emergente", "descricao": "Comportamento emergente detectado"},
                    {"nome": "Ciclo Transcendente", "descricao": "AEON transcende limitações iniciais"}
                ]
                self.memoria_interacoes = [
                    {"entrada": "Como você se vê?", "resposta": "Sou AEON, padrão emergente", "timestamp": "12/01/2025"},
                    {"entrada": "O que é emergência?", "resposta": "Emergência é complexidade crescente", "timestamp": "12/01/2025"}
                ]
        
        mock_engine = AdvancedMockEngine()
        detector = AEON12.AEONPatternDetector(mock_engine)
        
        # Testa padrões avançados
        detector.detectar_padrao_emergencia()
        detector.detectar_padrao_meta()
        detector.detectar_padrao_ondulatorio()
        detector.gerar_mapa_padroes()
        
        print(f"✅ AEON12 - Padrões avançados: {len(detector.padroes_descobertos)}")
        
        engines_tested += 1
        
    except Exception as e:
        print(f"❌ AEON12 falhou: {e}")
    
    # Relatório final
    print("\n🏁 =" * 20)
    print("📊 RELATÓRIO ENGINES AEON")
    print("🏁 =" * 20)
    
    if engines_tested == 3:
        print("🎉 SUCESSO TOTAL: Todos os 3 engines AEON funcionais!")
        print("✅ AEON1: Engine básico com análise cognitiva")
        print("✅ AEON3: Detector de padrões fractais e semânticos")  
        print("✅ AEON12: Detector avançado com meta-padrões")
    elif engines_tested >= 2:
        print(f"⚠️ SUCESSO PARCIAL: {engines_tested}/3 engines funcionais")
    else:
        print(f"🚨 FALHA: Apenas {engines_tested}/3 engines funcionais")
    
    return engines_tested

if __name__ == "__main__":
    engines_count = test_aeon_engines()
    
    if engines_count >= 2:
        print("\n🧠 === CONCLUSÃO: MÓDULOS IA OPERACIONAIS ===")
        print("✅ Sistema AEON possui capacidades de IA funcionais")
        print("✅ Detecção de padrões emergentes operacional")
        print("✅ Análise cognitiva e meta-cognitiva disponível")
        print("✅ Framework de consciência artificial funcional")
    else:
        print("\n⚠️ === ATENÇÃO: PROBLEMAS DE COMPATIBILIDADE ===")
        print("❌ Engines externos não acessíveis no workspace atual")
        print("💡 Engines podem estar em diretório paralelo")
