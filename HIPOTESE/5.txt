import numpy as np
import matplotlib.pyplot as plt
import collections

# 🔧 Parâmetros gerais
n_passos = 100
n_estados_bin = 2
n_estados_vet = 4

# --------------------------
# Sistema binário (clássico)
# --------------------------
mem_bin = [np.random.randint(n_estados_bin), np.random.randint(n_estados_bin)]
def transicao_bin(a, b):
    return (a ^ b)  # XOR simples

for _ in range(n_passos - 2):
    novo = transicao_bin(mem_bin[-1], mem_bin[-2])
    mem_bin.append(novo)

cont_bin = collections.Counter(mem_bin)
freq_bin = np.array([cont_bin[k] for k in range(n_estados_bin)]) / len(mem_bin)
H_bin = -np.sum(freq_bin * np.log2(freq_bin + 1e-12))

# ------------------------------
# Sistema vetorial com silêncios
# ------------------------------
mem_vet = []
ativos = [np.random.randint(n_estados_vet), np.random.randint(n_estados_vet)]
def transicao_vet(a, b):
    base = (2 * a + b) % n_estados_vet
    mut = np.random.choice([0, 1], p=[0.9, 0.1])
    return (base + mut) % n_estados_vet

for i in range(n_passos):
    if i < 2:
        estado = ativos[i]
    else:
        estado = transicao_vet(ativos[-1], ativos[-2])
        ativos.append(estado)
    mem_vet.append(estado)
    mem_vet.append(None)  # ⌀: silêncio vetorial

ativos_finais = [x for x in mem_vet if x is not None]
cont_vet = collections.Counter(ativos_finais)
freq_vet = np.array([cont_vet[k] for k in range(n_estados_vet)]) / len(ativos_finais)
H_vet = -np.sum(freq_vet * np.log2(freq_vet + 1e-12))

# ------------------------------
# 📊 Exibição dos Resultados
# ------------------------------
print("🔵 Sistema Binário:")
print(f"Estados: {dict(cont_bin)}")
print(f"Entropia: {H_bin:.3f} bits\n")

print("🟣 Sistema Vetorial com ⌀:")
print(f"Estados: {dict(cont_vet)}")
print(f"Entropia (ativos): {H_vet:.3f} bits\n")

# 🎨 Visualização
fig, axs = plt.subplots(2, 1, figsize=(12, 3.2))

# Binário
colors_bin = ["black", "deepskyblue"]
axs[0].bar(range(len(mem_bin)), [1]*len(mem_bin),
           color=[colors_bin[val] for val in mem_bin], edgecolor='white')
axs[0].set_title("🔵 Fita Binária Clássica")
axs[0].axis('off')

# Vetorial
colors_vet = ["black", "crimson", "gold", "royalblue", "lightgray"]
bar_colors = [colors_vet[val] if val is not None else colors_vet[-1] for val in mem_vet]
axs[1].bar(range(len(mem_vet)), [1]*len(mem_vet),
           color=bar_colors, edgecolor='white')
axs[1].set_title("🟣 Memória Vetorial com Silêncios (⌀)")
axs[1].axis('off')

plt.tight_layout()
plt.show()