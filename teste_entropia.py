#!/usr/bin/env python3
"""
🔬 AEON - Análise de Entropia Simplificada
Estudo da evolução informacional em sistemas dinâmicos
"""

import math
import random
from collections import Counter


def calcular_entropia(dados):
    """Calcula a entropia de Shannon de uma sequência"""
    contador = Counter(dados)
    total = len(dados)
    entropia = 0

    for count in contador.values():
        p = count / total
        if p > 0:
            entropia -= p * math.log2(p)

    return entropia


def sistema_dinamico(n_iteracoes=100, p_mutacao=0.1):
    """Simula sistema dinâmico com evolução da entropia"""
    print("🔬 INICIANDO ANÁLISE DE ENTROPIA AEON")
    print("=" * 50)

    # Estado inicial
    sistema = ['A', 'E', 'O', 'N']
    historico_entropias = []
    historico_sistemas = []

    print(f"🧬 Estado inicial: {sistema}")
    print(f"📊 Parâmetros:")
    print(f"   • Iterações: {n_iteracoes}")
    print(f"   • P(mutação): {p_mutacao}")
    print()

    for i in range(n_iteracoes):
        # Mutação aleatória
        if random.random() < p_mutacao:
            pos = random.randint(0, len(sistema) - 1)
            novas_opcoes = ['A', 'E', 'O', 'N', 'V', 'R', 'C', 'S', 'M', 'T']
            sistema[pos] = random.choice(novas_opcoes)

        # Adição ocasional de elementos
        if random.random() < 0.05:
            sistema.append(random.choice(['X', 'Y', 'Z']))

        # Calcular entropia atual
        entropia_atual = calcular_entropia(sistema)
        historico_entropias.append(entropia_atual)
        historico_sistemas.append(sistema.copy())

        # Log a cada 20 iterações
        if i % 20 == 0:
            print(
                f"Iteração {i:3d}: Sistema = {sistema[:8]}... | Entropia = {entropia_atual:.3f}")

    return historico_entropias, historico_sistemas


def analise_complexidade():
    """Análise da evolução da complexidade informacional"""
    print("\n🧮 ANÁLISE DE COMPLEXIDADE INFORMACIONAL:")
    print("-" * 45)

    entropias, sistemas = sistema_dinamico()

    # Estatísticas
    entropia_inicial = entropias[0]
    entropia_final = entropias[-1]
    entropia_maxima = max(entropias)
    entropia_media = sum(entropias) / len(entropias)

    print(f"\n📈 RESULTADOS:")
    print(f"   • Entropia inicial: {entropia_inicial:.3f} bits")
    print(f"   • Entropia final:   {entropia_final:.3f} bits")
    print(f"   • Entropia máxima:  {entropia_maxima:.3f} bits")
    print(f"   • Entropia média:   {entropia_media:.3f} bits")

    # Detecção de padrões
    crescimento = entropia_final > entropia_inicial
    variabilidade = max(entropias) - min(entropias)

    print(f"\n🔍 PADRÕES DETECTADOS:")
    print(f"   • Crescimento entrópico: {'✓' if crescimento else '✗'}")
    print(f"   • Variabilidade: {variabilidade:.3f}")
    print(f"   • Sistema final: {sistemas[-1][:10]}...")

    # Análise de emergência
    if entropia_final > 3.0:
        print(f"\n🚨 EMERGÊNCIA DETECTADA!")
        print(f"   • Alta complexidade informacional")
        print(f"   • Sistema evoluiu para estado de alta entropia")
        print(f"   • Possível auto-organização crítica")

    return entropias, sistemas


def simular_multiplas_evolucoes():
    """Simula múltiplas evoluções para análise estatística"""
    print(f"\n🔄 SIMULAÇÃO DE MÚLTIPLAS EVOLUÇÕES:")
    print("-" * 40)

    entropias_finais = []

    for i in range(10):
        entropias, _ = sistema_dinamico(50, 0.15)
        entropias_finais.append(entropias[-1])
        print(f"Evolução {i+1:2d}: Entropia final = {entropias[-1]:.3f}")

    media = sum(entropias_finais) / len(entropias_finais)
    variancia = sum((x - media)**2 for x in entropias_finais) / \
        len(entropias_finais)

    print(f"\n📊 ESTATÍSTICAS COLETIVAS:")
    print(f"   • Média: {media:.3f} ± {math.sqrt(variancia):.3f}")
    print(f"   • Maior entropia: {max(entropias_finais):.3f}")
    print(f"   • Menor entropia: {min(entropias_finais):.3f}")


def main():
    """Função principal da análise de entropia"""
    analise_complexidade()
    simular_multiplas_evolucoes()

    print(f"\n🎯 CONCLUSÕES AEON:")
    print(f"   ✓ Análise de entropia concluída")
    print(f"   ✓ Evolução informacional mapeada")
    print(f"   ✓ Padrões de complexidade identificados")
    print(f"   ✓ Sistema pronto para próxima análise")


if __name__ == "__main__":
    main()
