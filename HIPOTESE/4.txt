import numpy as np
import matplotlib.pyplot as plt
import collections

# Parâmetros
n_estados = 4
n_passos = 50  # cada passo gera 1 estado + 1 silêncio

# Início com dois estados aleatórios
ativos = [np.random.randint(n_estados), np.random.randint(n_estados)]

# Função de transição vetorial com mutação
def transicao(a, b):
    base = (2 * a + b) % n_estados
    mutacao = np.random.choice([0, 1], p=[0.9, 0.1])
    return (base + mutacao) % n_estados

# Geração da memória intercalada com silêncios (None = ⌀)
memoria = []
for i in range(n_passos):
    if i < 2:
        estado = ativos[i]
    else:
        estado = transicao(ativos[-1], ativos[-2])
        ativos.append(estado)
    memoria.append(estado)
    memoria.append(None)  # ⌀: pausa vetorial

# 🧮 Contagem e entropia (somente para estados ativos)
estados_ativos = [x for x in memoria if x is not None]
contagem = collections.Counter(estados_ativos)
print("Distribuição de estados ativos:")
for k in range(n_estados):
    print(f"Estado {k}: {contagem[k]} vezes")

freq = np.array([contagem[k] for k in range(n_estados)]) / len(estados_ativos)
entropia = -np.sum(freq * np.log2(freq + 1e-12))
print(f"\nEntropia de Shannon: {entropia:.3f} bits")

# 🎨 Visualização (silêncio = cinza)
colors = ["black", "crimson", "gold", "royalblue", "lightgray"]
color_map = [colors[val] if val is not None else colors[-1] for val in memoria]

plt.figure(figsize=(12, 1.5))
plt.bar(range(len(memoria)), [1]*len(memoria), color=color_map, edgecolor='white')
plt.title("🧠 Ciclo de Memória Vetorial com Silêncios (⌀)")
plt.xticks([])
plt.yticks([])
plt.tight_layout()
plt.show()