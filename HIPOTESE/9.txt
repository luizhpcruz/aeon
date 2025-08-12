import os
os.environ["OMP_NUM_THREADS"] = "1"  # Resolve warning de KMeans no Windows

import numpy as np
import collections
import matplotlib.pyplot as plt
import seaborn as sns
import copy
from sklearn.cluster import KMeans

# — Parâmetros Globais —
N_CELULAS  = 32
N_ESTADOS  = 4
N_CICLOS   = 50
P_ALEATORIA = 0.3
N_FITAS    = 5
TOPOLOGIA  = "aleatoria"

# — Base —
def inicializar_memoria(n, est):
    mem = [None] * n
    for i in range(0, n, 2):
        mem[i] = np.random.randint(est)
    return mem

def colapsar(mem):
    out = []
    i = 0
    while i < len(mem):
        a = mem[i]
        b = mem[i+1] if i+1 < len(mem) else None
        if a == 0 and b == 1:
            out.extend([None, None]); i += 2
        else:
            out.append(a); i += 1
    return out

def mutacao_estado(a, b, est):
    if a is None or b is None: return None
    base = (2*a + b) % est
    mut  = np.random.choice([0,1], p=[0.9,0.1])
    return (base + mut) % est

def ciclo_simbolico(mem, est):
    nova = mem[:]
    for i in range(2, len(mem)):
        if mem[i-2] is not None and mem[i-1] is not None:
            nova[i] = mutacao_estado(mem[i-1], mem[i-2], est)
    return colapsar(nova)

def calcular_entropia(mem):
    ativos = [v for v in mem if v is not None]
    if not ativos: return 0.0
    cnt = collections.Counter(ativos)
    freqs = np.array([cnt[k] for k in sorted(cnt)]) / len(ativos)
    return -np.sum(freqs * np.log2(freqs + 1e-12))

# — Acoplamento adaptativo —
def p_acop_dyn(H_src, H_dst):
    delta = H_src - H_dst
    return 1 / (1 + np.exp(-5 * delta))

def acoplar_silencios(mem_origem, mem_destino, prob, max_estado):
    for idx, val in enumerate(mem_origem):
        if val is None and np.random.rand() < prob:
            if mem_destino[idx] is None:
                mem_destino[idx] = max_estado
    return mem_destino

# — Topologia dinâmica —
def construir_topologia(n, tipo="anel", p_ale=0.3):
    adj = {i: [] for i in range(n)}
    if tipo == "anel":
        for i in range(n):
            adj[i].append((i+1)%n)
            adj[i].append((i-1)%n)
    elif tipo == "aleatoria":
        for i in range(n):
            for j in range(n):
                if i != j and np.random.rand() < p_ale:
                    adj[i].append(j)
    return adj

# — Entrada e Resposta —
def injetar_entrada(fita, entrada):
    for i in range(min(len(fita), len(entrada))):
        fita[i] = entrada[i]
    return fita

def gerar_resposta(fita):
    ativos = [v for v in fita if v is not None]
    if not ativos:
        return "Silêncio"
    freq = collections.Counter(ativos)
    estado_mais_comum = freq.most_common(1)[0][0]
    return f"Estado dominante: {estado_mais_comum}"

# — Execução —
fitas = [inicializar_memoria(N_CELULAS, N_ESTADOS) for _ in range(N_FITAS)]
vizinhos = construir_topologia(N_FITAS, TOPOLOGIA, P_ALEATORIA)
hist_ent = np.zeros((N_FITAS, N_CICLOS))
colapsos = np.zeros((N_FITAS, N_CICLOS))
graus = np.array([len(vizinhos[i]) for i in range(N_FITAS)])

entrada_externa = [1, 0, 2, None, 1, 0, None, 2, 1, 0, None, None, 1, 2, 0, None,
                  1, 0, 2, 1, None, 0, 2, None, 1, 0, 1, None, 2, None, 0, 1]

for t in range(N_CICLOS):
    for i in range(N_FITAS):
        fitas[i] = injetar_entrada(fitas[i], entrada_externa)
        fitas[i] = ciclo_simbolico(fitas[i], N_ESTADOS)
    
    novas = copy.deepcopy(fitas)
    for i in range(N_FITAS):
        Hi = calcular_entropia(fitas[i])
        for j in vizinhos[i]:
            Hj = calcular_entropia(fitas[j])
            p_dyn = p_acop_dyn(Hi, Hj)
            novas[j] = acoplar_silencios(fitas[i], novas[j], p_dyn, N_ESTADOS-1)
    fitas = novas

    if TOPOLOGIA == "aleatoria" and t % 10 == 0:
        vizinhos = construir_topologia(N_FITAS, "aleatoria", P_ALEATORIA)
        graus = np.array([len(vizinhos[i]) for i in range(N_FITAS)])

    for i in range(N_FITAS):
        hist_ent[i, t] = calcular_entropia(fitas[i])
        colapsos[i, t] = fitas[i].count(None)

    print(f"Ciclo {t+1} respostas:")
    for i in range(N_FITAS):
        print(f"  Fita {i}: {gerar_resposta(fitas[i])}")
    print("-" * 30)

# — Visualizações —
plt.figure(figsize=(8,5))
for i in range(N_FITAS):
    plt.plot(range(1, N_CICLOS+1), hist_ent[i], label=f"Fita {i}")
plt.title(f"Entropia — Topologia: {TOPOLOGIA}")
plt.xlabel("Ciclo")
plt.ylabel("Entropia (bits)")
plt.legend()
plt.grid(True, linestyle=':')
plt.tight_layout()
plt.show()

plt.figure(figsize=(10,5))
sns.heatmap(hist_ent, cmap="magma", cbar_kws={'label': 'Entropia'})
plt.title("Mapa de Calor — Rede de Fitas")
plt.xlabel("Ciclo")
plt.ylabel("Fita")
plt.tight_layout()
plt.show()

plt.figure(figsize=(6,4))
plt.scatter(graus, hist_ent.mean(axis=1), c='teal')
plt.xlabel("Grau na Rede")
plt.ylabel("Entropia Média")
plt.title("Correlação Grau vs Entropia Média")
plt.grid(True, linestyle=':')
plt.tight_layout()
plt.show()

kmeans = KMeans(n_clusters=3, random_state=0).fit(hist_ent)
labels = kmeans.labels_

plt.figure(figsize=(8,5))
for i in range(N_FITAS):
    plt.plot(hist_ent[i], label=f"Fita {i} — Cluster {labels[i]}")
plt.title("Clustering de Entropia Temporal")
plt.xlabel("Ciclo")
plt.ylabel("Entropia")
plt.legend()
plt.tight_layout()
plt.show()

plt.figure(figsize=(10,5))
sns.heatmap(colapsos, cmap="Blues", cbar_kws={'label': 'Nº de colapsos'})
plt.title("Mapa de Calor — Colapsos por Fita")
plt.xlabel("Ciclo")
plt.ylabel("Fita")
plt.tight_layout()
plt.show()
