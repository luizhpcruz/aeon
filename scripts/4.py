"""
AEON - Análise de Entropia em Sistemas Dinâmicos
===============================================

Este script realiza análise de entropia em sistemas dinâmicos com múltiplas fitas
paralelas, testando diferentes tipos de entrada (aleatória, pulso, ruído).

Autor: Luiz F. + GitHub Copilot
Data: Julho/2025
"""

import numpy as np
import collections
import copy
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os
import sys
from datetime import datetime

# Configurar matplotlib para evitar problemas de display
plt.rcParams['figure.max_open_warning'] = 50

# — Função ciclo não simbólico —
def ciclo_nao_simbolico(mem, est, p_mut=0.1):
    """
    Executa um ciclo de mutação não simbólica na memória.
    
    Args:
        mem: Lista representando a memória/fita
        est: Número de estados possíveis
        p_mut: Probabilidade de mutação (default: 0.1)
    
    Returns:
        Lista com o novo estado da memória
    """
    nova = mem[:]
    for i in range(len(mem)):
        if mem[i] is not None:
            if np.random.rand() < p_mut:
                nova[i] = np.random.randint(est)
    return nova

# — Função entropia —
def calcular_entropia(mem):
    """
    Calcula a entropia de Shannon para uma sequência de memória.
    
    Args:
        mem: Lista representando o estado da memória
    
    Returns:
        Float: Valor da entropia em bits
    """
    ativos = [v for v in mem if v is not None]
    if not ativos:
        return 0.0
    cnt = collections.Counter(ativos)
    freqs = np.array([cnt[k] for k in sorted(cnt)]) / len(ativos)
    return -np.sum(freqs * np.log2(freqs + 1e-12))

# — Geração de entrada —
def gerar_entrada(tipo, tamanho):
    if tipo == "aleatoria":
        return np.random.choice([None,0,1,2,3], tamanho)
    elif tipo == "pulso":
        arr = [None]*tamanho
        meio = tamanho//2
        arr[meio:meio+3] = [3,3,3]
        return arr
    elif tipo == "ruido":
        base = [0,1,2,3,None]
        return np.random.choice(base, tamanho, p=[0.1,0.1,0.1,0.1,0.6])
    else:
        return [None]*tamanho

# — Segmentação por janela —
def segmentar_e_medir(fitas_hist, janela=5):
    n_fitas, n_ciclos = fitas_hist.shape
    n_janelas = n_ciclos // janela
    ent_medias = np.zeros((n_fitas, n_janelas))
    for j in range(n_janelas):
        ent_medias[:, j] = np.mean(fitas_hist[:, j*janela:(j+1)*janela], axis=1)
    return ent_medias

# — Parâmetros —
N_CICLOS_TESTE = 50
N_FITAS = 5
N_CELULAS = 32
N_ESTADOS = 4

# — Simulação —
entradas_testes = ["aleatoria", "pulso", "ruido"]
resultados = {}

for tipo in entradas_testes:
    fitas = [[None]*N_CELULAS for _ in range(N_FITAS)]
    entrada = gerar_entrada(tipo, N_CELULAS)
    print(f"Testando entrada: {tipo}")
    
    hist_ent = np.zeros((N_FITAS, N_CICLOS_TESTE))
    
    for t in range(N_CICLOS_TESTE):
        for i in range(N_FITAS):
            for idx in range(N_CELULAS):
                fitas[i][idx] = entrada[idx]
            fitas[i] = ciclo_nao_simbolico(fitas[i], N_ESTADOS, p_mut=0.1)
        for i in range(N_FITAS):
            hist_ent[i, t] = calcular_entropia(fitas[i])
    
    resultados[tipo] = hist_ent.copy()

# — Gráfico de entropia por fita —
plt.figure(figsize=(15,10))
for idx, tipo in enumerate(entradas_testes):
    plt.subplot(3,1,idx+1)
    for i in range(N_FITAS):
        plt.plot(resultados[tipo][i], label=f"Fita {i}")
    plt.title(f"Entropia - Entrada: {tipo}")
    plt.xlabel("Ciclo")
    plt.ylabel("Entropia (bits)")
    plt.legend()
    plt.grid(True, linestyle=':')
plt.tight_layout()
plt.show()

# — Segmentação temporal —
ent_segmentada = segmentar_e_medir(resultados["aleatoria"], janela=10)
plt.figure(figsize=(8,5))
for i in range(N_FITAS):
    plt.plot(ent_segmentada[i], label=f"Fita {i}")
plt.title("Entropia Média por Janela (entrada aleatória, janela=10 ciclos)")
plt.xlabel("Janela Temporal")
plt.ylabel("Entropia Média")
plt.legend()
plt.grid(True, linestyle=':')
plt.tight_layout()
plt.show()

# — Heatmap visual —
plt.figure(figsize=(10,6))
sns.heatmap(resultados["pulso"], cmap="magma", cbar_kws={'label': 'Entropia (bits)'})
plt.title("Heatmap Entrópico — Entrada: pulso")
plt.xlabel("Ciclo Temporal")
plt.ylabel("Fita")
plt.tight_layout()
plt.show()

# — Entropia por posição genômica —
final_memorias = {tipo: [] for tipo in entradas_testes}
for tipo in entradas_testes:
    fitas_final = [[None]*N_CELULAS for _ in range(N_FITAS)]
    entrada = gerar_entrada(tipo, N_CELULAS)
    for i in range(N_FITAS):
        fitas_final[i] = entrada.copy()
        for _ in range(N_CICLOS_TESTE):
            fitas_final[i] = ciclo_nao_simbolico(fitas_final[i], N_ESTADOS, p_mut=0.1)
    final_memorias[tipo] = fitas_final

plt.figure(figsize=(12, 4))
for idx, tipo in enumerate(entradas_testes):
    matriz = np.array(final_memorias[tipo])
    entropias_por_posicao = []
    for col in matriz.T:
        ativos = [v for v in col if v is not None]
        if not ativos:
            entropias_por_posicao.append(0.0)
        else:
            cnt = collections.Counter(ativos)
            freqs = np.array([cnt[k] for k in sorted(cnt)]) / len(ativos)
            entropias_por_posicao.append(-np.sum(freqs * np.log2(freqs + 1e-12)))
    plt.subplot(1, 3, idx + 1)
    plt.plot(entropias_por_posicao, color='indigo')
    plt.title(f"Entropia por Célula — {tipo}")
    plt.xlabel("Posição Genômica")
    plt.ylabel("Entropia")
    plt.grid(True, linestyle=':')
plt.tight_layout()
plt.show()

# — Exportação e finalização —
def salvar_resultados(resultados, timestamp):
    """Salva os resultados da simulação em arquivos."""
    try:
        # Criar diretórios se não existirem
        os.makedirs("../data", exist_ok=True)
        os.makedirs("../visualizations", exist_ok=True)
        
        # Salvar dados CSV
        for tipo, dados in resultados.items():
            df = pd.DataFrame(dados.T, columns=[f"Fita {i}" for i in range(dados.shape[0])])
            filename = f"../data/entropia_{tipo}_{timestamp}.csv"
            df.to_csv(filename, index=False)
            print(f"✅ Dados salvos: {filename}")
        
        print(f"📊 Simulação concluída em {datetime.now().strftime('%H:%M:%S')}")
        
    except Exception as e:
        print(f"❌ Erro ao salvar resultados: {e}")

if __name__ == "__main__":
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        print(f"🧬 AEON - Iniciando análise de entropia [{timestamp}]")
        print("=" * 50)
        
        # Executar simulação principal (código existente aqui)
        
        # Salvar resultados
        salvar_resultados(resultados, timestamp)
        
    except KeyboardInterrupt:
        print("\n⏹️ Simulação interrompida pelo usuário")
    except Exception as e:
        print(f"❌ Erro durante execução: {e}")
        sys.exit(1)