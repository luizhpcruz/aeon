import numpy as np
import matplotlib.pyplot as plt
import collections

# Parâmetros
n_estados = 4      # Número de estados possíveis (valores simbólicos)
n_passos = 100     # Quantidade de ciclos de memória

# Inicialização com dois estados iniciais aleatórios
memoria = [np.random.randint(n_estados), np.random.randint(n_estados)]

# 🔁 Função de transição vetorial com mutação probabilística
def transicao(a, b):
    base = (2 * a + b) % n_estados
    mutacao = np.random.choice([0, 1], p=[0.9, 0.1])  # 10% chance de perturbação
    return (base + mutacao) % n_estados

# Gerar a sequência completa
for _ in range(n_passos - 2):
    novo_estado = transicao(memoria[-1], memoria[-2])
    memoria.append(novo_estado)

# 📊 Análise de distribuição
contagem = collections.Counter(memoria)
print("Distribuição de estados:")
for k in range(n_estados):
    print(f"Estado {k}: {contagem[k]} vezes")

# Entropia de Shannon
freq = np.array([contagem[k] for k in range(n_estados)]) / len(memoria)
entropia = -np.sum(freq * np.log2(freq + 1e-12))  # Evita log(0) com epsilon
print(f"\nEntropia de Shannon: {entropia:.3f} bits")

# 🎨 Visualização como imagem vetorial 1D
plt.figure(figsize=(10, 1.5))
plt.imshow([memoria], cmap=plt.cm.get_cmap("Set1", n_estados), aspect='auto')
plt.title("Memória Vetorial como Imagem Discreta")
plt.axis('off')
plt.tight_layout()
plt.show()