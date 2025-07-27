# aeoncosma/gpu/stable_diffusion_visualizer.py
"""
🎨 AEONCOSMA Stable Diffusion Network Visualizer
Gera arte simbólica dos estados da rede usando IA generativa
Desenvolvido por Luiz Cruz - 2025
"""

import json
import time
import threading
from datetime import datetime
from typing import Dict, List, Any
import sys
import os

# Adiciona path para importações
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

try:
    from diffusers import StableDiffusionPipeline
    import torch
    from PIL import Image
    import numpy as np
    DIFFUSION_AVAILABLE = True
    GPU_AVAILABLE = torch.cuda.is_available()
except ImportError as e:
    print(f"⚠️ Stable Diffusion não disponível: {e}")
    DIFFUSION_AVAILABLE = False
    GPU_AVAILABLE = False

class NetworkArtGenerator:
    """
    Gerador de arte que transforma estados da rede em imagens
    Usa Stable Diffusion para criar representações visuais simbólicas
    """
    
    def __init__(self, model_id="runwayml/stable-diffusion-v1-5", device=None):
        self.model_id = model_id
        self.device = device or ("cuda" if GPU_AVAILABLE else "cpu")
        self.pipeline = None
        self.generation_history = []
        
        if DIFFUSION_AVAILABLE:
            try:
                print(f"🎨 Carregando Stable Diffusion: {model_id}")
                self.pipeline = StableDiffusionPipeline.from_pretrained(
                    model_id,
                    torch_dtype=torch.float16 if GPU_AVAILABLE else torch.float32,
                    use_safetensors=True
                )
                self.pipeline = self.pipeline.to(self.device)
                
                # Otimizações para economizar memória
                if GPU_AVAILABLE:
                    self.pipeline.enable_attention_slicing()
                    self.pipeline.enable_model_cpu_offload()
                
                print(f"✅ Stable Diffusion carregado no {self.device}")
                
            except Exception as e:
                print(f"❌ Erro ao carregar Stable Diffusion: {e}")
                self.pipeline = None
        else:
            print("⚠️ Stable Diffusion não disponível - usando simulação")

    def network_state_to_prompt(self, network_state: Dict) -> str:
        """
        Converte estado da rede em prompt criativo para Stable Diffusion
        
        Args:
            network_state: Estado atual da rede com métricas
        
        Returns:
            str: Prompt otimizado para geração de arte
        """
        # Extrai métricas principais
        total_nodes = network_state.get("total_nodes", 1000)
        active_nodes = network_state.get("active_nodes", 500)
        consensus_strength = network_state.get("consensus_strength", 0.5)
        ai_confidence = network_state.get("ai_confidence", 0.5)
        connections_density = network_state.get("connections_density", 0.3)
        
        # Calcula atividade da rede (0-1)
        network_activity = active_nodes / total_nodes if total_nodes > 0 else 0
        
        # Base do prompt baseado na atividade
        if network_activity > 0.8:
            base_theme = "a vibrant thriving digital ecosystem with intense neural connections"
        elif network_activity > 0.6:
            base_theme = "a dynamic network of glowing interconnected nodes"
        elif network_activity > 0.4:
            base_theme = "a moderate digital network with pulsing data streams"
        elif network_activity > 0.2:
            base_theme = "a sparse network of distant digital entities"
        else:
            base_theme = "a dormant digital realm with faint connections"
        
        # Adiciona elementos baseados no consenso
        if consensus_strength > 0.8:
            consensus_element = "with perfect harmony and synchronized patterns"
        elif consensus_strength > 0.6:
            consensus_element = "with strong coordination and flowing energy"
        elif consensus_strength > 0.4:
            consensus_element = "with moderate alignment and mixed signals"
        else:
            consensus_element = "with chaotic discord and conflicting energies"
        
        # Adiciona elementos baseados na confiança da IA
        if ai_confidence > 0.8:
            ai_element = "guided by brilliant artificial minds"
        elif ai_confidence > 0.6:
            ai_element = "enhanced by intelligent decision making"
        elif ai_confidence > 0.4:
            ai_element = "assisted by emerging AI consciousness"
        else:
            ai_element = "with primitive artificial reasoning"
        
        # Adiciona elementos visuais baseados na densidade de conexões
        if connections_density > 0.7:
            visual_element = "dense web of light, quantum entanglement patterns"
        elif connections_density > 0.5:
            visual_element = "intricate network topology, holographic data flows"
        elif connections_density > 0.3:
            visual_element = "scattered connection points, digital constellation"
        else:
            visual_element = "isolated nodes, minimalist cyber architecture"
        
        # Combina elementos em prompt final
        prompt = f"{base_theme} {consensus_element}, {ai_element}, {visual_element}, " \
                f"cyberpunk aesthetic, neon colors, 4k digital art, highly detailed, " \
                f"sci-fi concept art, neural network visualization, " \
                f"futuristic technology, glowing particles, data visualization"
        
        # Adiciona parâmetros negativos para melhor qualidade
        negative_prompt = "blurry, low quality, distorted, ugly, bad anatomy, " \
                         "text, watermark, signature, duplicate, mutation"
        
        return {
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "network_metrics": {
                "total_nodes": total_nodes,
                "network_activity": network_activity,
                "consensus_strength": consensus_strength,
                "ai_confidence": ai_confidence,
                "connections_density": connections_density
            }
        }

    def generate_network_art(self, network_state: Dict, 
                           width=512, height=512, 
                           num_inference_steps=20,
                           guidance_scale=7.5) -> Dict:
        """
        Gera arte baseada no estado da rede
        
        Args:
            network_state: Estado atual da rede
            width, height: Dimensões da imagem
            num_inference_steps: Passos de inferência (qualidade vs velocidade)
            guidance_scale: Força do prompt (criatividade vs precisão)
        
        Returns:
            dict: Resultado com imagem e metadados
        """
        if not self.pipeline:
            return self.simulate_art_generation(network_state)
        
        start_time = time.time()
        
        try:
            # Gera prompt criativo
            prompt_data = self.network_state_to_prompt(network_state)
            
            print(f"🎨 Gerando arte: {prompt_data['prompt'][:100]}...")
            
            # Gera imagem com Stable Diffusion
            with torch.autocast(self.device):
                result = self.pipeline(
                    prompt=prompt_data['prompt'],
                    negative_prompt=prompt_data['negative_prompt'],
                    width=width,
                    height=height,
                    num_inference_steps=num_inference_steps,
                    guidance_scale=guidance_scale,
                    generator=torch.manual_seed(int(time.time()) % 2**32)
                )
            
            image = result.images[0]
            generation_time = time.time() - start_time
            
            # Salva imagem
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"network_art_{timestamp}.png"
            image.save(filename)
            
            # Metadados da geração
            generation_data = {
                "timestamp": datetime.now().isoformat(),
                "filename": filename,
                "prompt": prompt_data['prompt'],
                "negative_prompt": prompt_data['negative_prompt'],
                "network_metrics": prompt_data['network_metrics'],
                "generation_params": {
                    "width": width,
                    "height": height,
                    "num_inference_steps": num_inference_steps,
                    "guidance_scale": guidance_scale
                },
                "generation_time": generation_time,
                "device": self.device,
                "model_id": self.model_id
            }
            
            self.generation_history.append(generation_data)
            
            print(f"✅ Arte gerada em {generation_time:.1f}s: {filename}")
            
            return {
                "success": True,
                "image": image,
                "metadata": generation_data
            }
            
        except Exception as e:
            print(f"❌ Erro na geração de arte: {e}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

    def simulate_art_generation(self, network_state: Dict) -> Dict:
        """Simulação de geração de arte quando Stable Diffusion não está disponível"""
        print("🎨 Simulando geração de arte (Stable Diffusion não disponível)")
        
        time.sleep(2)  # Simula tempo de processamento
        
        prompt_data = self.network_state_to_prompt(network_state)
        
        # Cria imagem simulada
        try:
            from PIL import Image, ImageDraw
            
            # Cria imagem simples baseada nas métricas
            img = Image.new('RGB', (512, 512), color='black')
            draw = ImageDraw.Draw(img)
            
            # Desenha representação simples da rede
            activity = prompt_data['network_metrics']['network_activity']
            consensus = prompt_data['network_metrics']['consensus_strength']
            
            # Círculos representando nós
            for i in range(int(50 * activity)):
                x = np.random.randint(50, 462)
                y = np.random.randint(50, 462)
                radius = int(10 * consensus + 5)
                color = (
                    int(255 * activity),
                    int(255 * consensus), 
                    int(255 * prompt_data['network_metrics']['ai_confidence'])
                )
                draw.ellipse([x-radius, y-radius, x+radius, y+radius], fill=color)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"network_art_simulated_{timestamp}.png"
            img.save(filename)
            
            return {
                "success": True,
                "image": img,
                "metadata": {
                    "timestamp": datetime.now().isoformat(),
                    "filename": filename,
                    "prompt": prompt_data['prompt'],
                    "network_metrics": prompt_data['network_metrics'],
                    "simulation": True
                }
            }
            
        except ImportError:
            return {
                "success": False,
                "error": "PIL not available for simulation",
                "metadata": {
                    "prompt": prompt_data['prompt'],
                    "network_metrics": prompt_data['network_metrics']
                }
            }

    def generate_art_sequence(self, network_states: List[Dict], 
                            interval=10, batch_size=5) -> List[Dict]:
        """
        Gera sequência de artes baseada em múltiplos estados da rede
        
        Args:
            network_states: Lista de estados da rede ao longo do tempo
            interval: Intervalo entre gerações (segundos)
            batch_size: Máximo de imagens por batch
        
        Returns:
            list: Lista de resultados de geração
        """
        print(f"🎬 Gerando sequência de {len(network_states)} artes...")
        
        results = []
        
        for i, state in enumerate(network_states[:batch_size]):
            print(f"🎨 Gerando arte {i+1}/{min(len(network_states), batch_size)}")
            
            # Adiciona informação temporal ao estado
            temporal_state = state.copy()
            temporal_state["sequence_position"] = i
            temporal_state["total_sequence"] = len(network_states)
            temporal_state["time_evolution"] = i / len(network_states)
            
            result = self.generate_network_art(temporal_state)
            results.append(result)
            
            if i < len(network_states) - 1:  # Não espera no último item
                time.sleep(interval)
        
        print(f"🎬 Sequência concluída: {len(results)} artes geradas")
        return results

    def create_network_timelapse(self, art_sequence: List[Dict], 
                                output_name="network_evolution.gif") -> str:
        """
        Cria timelapse das artes geradas
        
        Args:
            art_sequence: Sequência de artes geradas
            output_name: Nome do arquivo de saída
        
        Returns:
            str: Caminho do arquivo criado
        """
        try:
            from PIL import Image
            
            images = []
            for art_result in art_sequence:
                if art_result["success"] and "image" in art_result:
                    images.append(art_result["image"])
            
            if images:
                # Cria GIF animado
                images[0].save(
                    output_name,
                    save_all=True,
                    append_images=images[1:],
                    duration=2000,  # 2 segundos por frame
                    loop=0
                )
                
                print(f"🎬 Timelapse criado: {output_name}")
                return output_name
            else:
                print("⚠️ Nenhuma imagem válida para timelapse")
                return None
                
        except Exception as e:
            print(f"❌ Erro ao criar timelapse: {e}")
            return None

    def get_generation_statistics(self) -> Dict:
        """Retorna estatísticas das gerações de arte"""
        if not self.generation_history:
            return {"total_generations": 0}
        
        total_time = sum(g.get("generation_time", 0) for g in self.generation_history)
        avg_time = total_time / len(self.generation_history)
        
        return {
            "total_generations": len(self.generation_history),
            "total_generation_time": total_time,
            "average_generation_time": avg_time,
            "first_generation": self.generation_history[0]["timestamp"],
            "last_generation": self.generation_history[-1]["timestamp"],
            "device_used": self.device,
            "model_id": self.model_id,
            "diffusion_available": DIFFUSION_AVAILABLE
        }

    def export_generation_log(self, filename="art_generation_log.json") -> str:
        """Exporta log de todas as gerações"""
        log_data = {
            "generator_info": {
                "model_id": self.model_id,
                "device": self.device,
                "diffusion_available": DIFFUSION_AVAILABLE
            },
            "statistics": self.get_generation_statistics(),
            "generation_history": self.generation_history
        }
        
        with open(filename, 'w') as f:
            json.dump(log_data, f, indent=2, default=str)
        
        print(f"📁 Log de gerações exportado: {filename}")
        return filename

def test_network_art_generator():
    """Teste do gerador de arte de rede"""
    print("🎨 Testando Network Art Generator...")
    
    # Cria gerador (vai usar simulação se Stable Diffusion não estiver disponível)
    generator = NetworkArtGenerator()
    
    # Estado fictício da rede
    test_network_state = {
        "total_nodes": 10000,
        "active_nodes": 7500,
        "consensus_strength": 0.85,
        "ai_confidence": 0.73,
        "connections_density": 0.6,
        "timestamp": datetime.now().isoformat()
    }
    
    # Gera prompt
    prompt_data = generator.network_state_to_prompt(test_network_state)
    print(f"🎯 Prompt gerado: {prompt_data['prompt'][:150]}...")
    
    # Gera arte
    result = generator.generate_network_art(test_network_state)
    
    if result["success"]:
        print(f"✅ Arte gerada com sucesso!")
        print(f"📁 Arquivo: {result['metadata']['filename']}")
    else:
        print(f"❌ Erro na geração: {result['error']}")
    
    # Estatísticas
    stats = generator.get_generation_statistics()
    print(f"📊 Estatísticas: {stats}")
    
    # Exporta log
    log_file = generator.export_generation_log()
    
    return generator

def main():
    """Execução principal do visualizador"""
    import argparse
    
    parser = argparse.ArgumentParser(description='AEONCOSMA Stable Diffusion Visualizer')
    parser.add_argument('--model', default="runwayml/stable-diffusion-v1-5", help='Modelo Stable Diffusion')
    parser.add_argument('--device', default=None, help='Device (cuda/cpu)')
    parser.add_argument('--test', action='store_true', help='Executa teste')
    parser.add_argument('--nodes', type=int, default=1000, help='Número de nós para teste')
    
    args = parser.parse_args()
    
    if args.test:
        test_network_art_generator()
    else:
        # Uso interativo
        generator = NetworkArtGenerator(model_id=args.model, device=args.device)
        
        # Estado exemplo
        example_state = {
            "total_nodes": args.nodes,
            "active_nodes": int(args.nodes * 0.75),
            "consensus_strength": 0.8,
            "ai_confidence": 0.7,
            "connections_density": 0.5
        }
        
        result = generator.generate_network_art(example_state)
        
        if result["success"]:
            print(f"🎨 Arte da rede gerada: {result['metadata']['filename']}")
        else:
            print(f"❌ Falha na geração: {result['error']}")

if __name__ == "__main__":
    main()
