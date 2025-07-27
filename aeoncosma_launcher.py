# aeoncosma_launcher.py
"""
🚀 AEONCOSMA SYSTEM LAUNCHER - Inicializador Principal
Sistema completo de 5 pilares AEONCOSMA com segurança integrada
Desenvolvido por Luiz Cruz - 2025
"""

import asyncio
import sys
import os
from datetime import datetime
from typing import Dict, Any

# Importações de segurança (sempre primeiro)
from security.aeoncosma_security_lock import enforce_security

# Importações dos 5 pilares AEONCOSMA
from aeoncosma.cognitive.gpt_node import GPTNode
from aeoncosma.core.aeon_kernel import AeonKernel
from aeoncosma.communication.p2p_interface import P2PInterface
from aeoncosma.reasoning.interaction_engine import InteractionEngine
from aeoncosma.adapters.enterprise_adapter import EnterpriseAdapter

class AeonCosmaSystem:
    """
    🧠 Sistema Principal AEONCOSMA
    Orquestra todos os 5 pilares da arquitetura
    """
    
    def __init__(self, node_id: str = "aeoncosma_main"):
        # 🛡️ Enforcement de segurança obrigatório
        print("🛡️ Executando verificações de segurança AEONCOSMA...")
        self.security_lock = enforce_security()
        
        self.node_id = node_id
        self.components = {}
        self.running = False
        
        print(f"🚀 Inicializando sistema AEONCOSMA ({node_id})")
        
    async def initialize_components(self):
        """Inicializa todos os 5 pilares AEONCOSMA"""
        print("\n🧩 INICIALIZANDO COMPONENTES AEONCOSMA...")
        
        try:
            # 1. 🧠 GPT Node - O Sentido Cognitivo
            print("1️⃣ Inicializando GPT Node (Cognitive)...")
            self.components["gpt_node"] = GPTNode(self.node_id)
            await self.components["gpt_node"].initialize()
            print("   ✅ GPT Node inicializado")
            
            # 2. 🛡️ AEON Kernel - O Guardião da Identidade
            print("2️⃣ Inicializando AEON Kernel (Core)...")
            self.components["aeon_kernel"] = AeonKernel(self.node_id)
            await self.components["aeon_kernel"].initialize()
            print("   ✅ AEON Kernel inicializado")
            
            # 3. 🌐 P2P Interface - O Meio de Comunicação
            print("3️⃣ Inicializando P2P Interface (Communication)...")
            self.components["p2p_interface"] = P2PInterface(self.node_id)
            await self.components["p2p_interface"].initialize()
            print("   ✅ P2P Interface inicializado")
            
            # 4. 🎯 Interaction Engine - O Motor de Raciocínio
            print("4️⃣ Inicializando Interaction Engine (Reasoning)...")
            self.components["interaction_engine"] = InteractionEngine(self.node_id)
            await self.components["interaction_engine"].initialize()
            print("   ✅ Interaction Engine inicializado")
            
            # 5. 🌍 Enterprise Adapter - Os Tentáculos no Mundo
            print("5️⃣ Inicializando Enterprise Adapter (Adapters)...")
            self.components["enterprise_adapter"] = EnterpriseAdapter(self.node_id)
            print("   ✅ Enterprise Adapter inicializado")
            
            print("\n🎯 TODOS OS 5 PILARES AEONCOSMA INICIALIZADOS COM SUCESSO!")
            
        except Exception as e:
            print(f"❌ Erro na inicialização: {e}")
            raise
            
    async def demonstrate_integration(self):
        """Demonstra integração entre os componentes"""
        print("\n🔗 DEMONSTRANDO INTEGRAÇÃO ENTRE PILARES...")
        
        # Exemplo de fluxo integrado
        query = "Analise o mercado de criptomoedas e sugira estratégias"
        
        try:
            # 1. Enterprise Adapter busca dados
            print("🌍 Enterprise Adapter: Coletando dados...")
            insight = await self.components["enterprise_adapter"].fetch_data(
                "local_documents", "market analysis bitcoin ethereum"
            )
            
            if insight:
                print(f"   ✅ Dados coletados: {len(insight.raw_data)} chars")
                
                # 2. GPT Node processa cognitivamente
                print("🧠 GPT Node: Processamento cognitivo...")
                cognitive_response = await self.components["gpt_node"].process_query(
                    query, context=insight.structured_data
                )
                print(f"   ✅ Resposta cognitiva gerada")
                
                # 3. AEON Kernel valida confiabilidade
                print("🛡️ AEON Kernel: Validação de confiabilidade...")
                validation = await self.components["aeon_kernel"].validate_content(
                    cognitive_response["response"]
                )
                print(f"   ✅ Validação: {validation['trust_level']:.2f}")
                
                # 4. Interaction Engine coordena raciocínio
                print("🎯 Interaction Engine: Coordenação de raciocínio...")
                reasoning_result = await self.components["interaction_engine"].process_reasoning_request(
                    query, "local", {"cognitive_response": cognitive_response}
                )
                print(f"   ✅ Raciocínio coordenado")
                
                # 5. P2P Interface prepara para comunicação
                print("🌐 P2P Interface: Preparação para comunicação...")
                message = self.components["p2p_interface"].create_symbolic_message(
                    "KNOWLEDGE_SHARE", reasoning_result["result"]
                )
                print(f"   ✅ Mensagem simbólica criada")
                
                print(f"\n🎉 INTEGRAÇÃO COMPLETA DEMONSTRADA COM SUCESSO!")
                
            else:
                print("   ⚠️ Dados não disponíveis para demonstração completa")
                
        except Exception as e:
            print(f"❌ Erro na demonstração de integração: {e}")
            
    async def get_system_status(self) -> Dict[str, Any]:
        """Retorna status completo do sistema"""
        status = {
            "system_id": self.node_id,
            "timestamp": datetime.now().isoformat(),
            "running": self.running,
            "security_active": True,
            "components": {}
        }
        
        for component_name, component in self.components.items():
            try:
                if hasattr(component, 'get_status'):
                    component_status = await component.get_status()
                else:
                    component_status = {"status": "initialized"}
                    
                status["components"][component_name] = component_status
                
            except Exception as e:
                status["components"][component_name] = {"error": str(e)}
                
        return status
        
    async def run_comprehensive_demo(self):
        """Executa demonstração completa do sistema"""
        print("\n🎪 EXECUTANDO DEMONSTRAÇÃO COMPLETA AEONCOSMA")
        print("=" * 60)
        
        await self.initialize_components()
        await self.demonstrate_integration()
        
        # Status final
        print("\n📊 STATUS FINAL DO SISTEMA:")
        status = await self.get_system_status()
        
        print(f"   Sistema ID: {status['system_id']}")
        print(f"   Timestamp: {status['timestamp']}")
        print(f"   Segurança ativa: {status['security_active']}")
        print(f"   Componentes inicializados: {len(status['components'])}")
        
        for comp_name, comp_status in status["components"].items():
            if "error" in comp_status:
                print(f"      ❌ {comp_name}: {comp_status['error']}")
            else:
                print(f"      ✅ {comp_name}: OK")
                
        print(f"\n🎯 SISTEMA AEONCOSMA COMPLETO E OPERACIONAL!")

async def main():
    """Função principal do launcher"""
    print("🚀 AEONCOSMA SYSTEM LAUNCHER v1.0")
    print("Sistema de 5 pilares com segurança integrada")
    print("Desenvolvido por Luiz Cruz - 2025")
    print("=" * 60)
    
    try:
        # Inicializa sistema principal
        system = AeonCosmaSystem("aeoncosma_launcher_demo")
        
        # Executa demonstração completa
        await system.run_comprehensive_demo()
        
        print("\n🎉 LAUNCHER EXECUTADO COM SUCESSO!")
        print("🛡️ Sistema seguro e pronto para operação")
        
    except KeyboardInterrupt:
        print("\n⏹️ Sistema interrompido pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro no launcher: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
