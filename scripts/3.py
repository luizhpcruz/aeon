import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import random

# ----- CONFIGURAÇÃO -----
BASES = ['A', 'T', 'G', 'C', 'Ω', 'Ψ', 'Λ', 'Z', 'Δ', 'Φ', 'Ξ', 'Σ', 'β', 'κ', 'η', 'ν']
BASE_TO_VEC = {b: np.eye(len(BASES))[i] for i, b in enumerate(BASES)}
L = 91
POP_SIZE = 50
CYCLES = 155
NUM_STRANDS = 7

# ----- FUNÇÕES -----
def encode_genome(genome):
    return np.array([BASE_TO_VEC[sym] for sym in genome])

def compute_entropy(batch_encoded):
    entropies = []
    for i in range(L):
        position_vectors = [g[i] for g in batch_encoded]
        probs = np.mean(position_vectors, axis=0) + 1e-9
        H = -np.sum(probs * np.log2(probs))
        entropies.append(H)
    return np.array(entropies)

def generate_batch(n=POP_SIZE):
    return [[random.choice(BASES) for _ in range(L)] for _ in range(n)]

def crossover(g1, g2):
    cut1, cut2 = L // 3, 2 * L // 3
    return g1[:cut1] + g2[cut1:cut2] + g1[cut2:]

def mutate_genome(genome, mutation_rate):
    new = genome.copy()
    for i in range(L):
        if i % 13 == 0:
            prev = genome[(i - 1) % L]
            next = genome[(i + 1) % L]
            idx = (BASES.index(prev) + BASES.index(next)) % len(BASES)
            new[i] = BASES[idx]
        elif random.random() < mutation_rate:
            new[i] = random.choice(BASES)
    return new

# ----- SIMULAÇÃO MULTIFITA COM ESTÍMULO -----
multi_entropy = []

for strand in range(NUM_STRANDS):
    population = generate_batch()
    strand_entropy = []

    for cycle in range(CYCLES):
        # Estímulo simbólico: redução da taxa de mutação em ciclos 100–130
        if 100 <= cycle <= 130:
            mutation_rate = 0.01  # silêncio simbólico
        else:
            mutation_rate = 0.03  # padrão normal

        mutated = [mutate_genome(g, mutation_rate) for g in population]
        random.shuffle(mutated)
        offspring = [crossover(mutated[i], mutated[i+1]) for i in range(0, POP_SIZE-1, 2)]
        population = (mutated + offspring)[:POP_SIZE]
        encoded = [encode_genome(g) for g in population]
        strand_entropy.append(compute_entropy(encoded))

    multi_entropy.append(np.array(strand_entropy))

# ----- VISUALIZAÇÃO: CURVAS DE ENTROPIA -----
plt.figure(figsize=(12, 6))
for i, entropy_matrix in enumerate(multi_entropy):
    mean_entropy = entropy_matrix.mean(axis=1)
    plt.plot(mean_entropy, label=f'Fita {i+1}')
plt.axvspan(100, 130, color='gray', alpha=0.2, label='Estímulo: Silêncio Cognitivo')
plt.xlabel("Ciclo Evolutivo")
plt.ylabel("Entropia Média (bits)")
plt.title("AEONCOSMA — Resposta Entrópica à Pergunta Simbólica")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# ----- VISUALIZAÇÃO: HEATMAPS INDIVIDUAIS -----
for i, entropy_matrix in enumerate(multi_entropy):
    plt.figure(figsize=(12, 6))
    sns.heatmap(entropy_matrix, cmap="plasma", cbar_kws={'label': 'Entropia (bits)'})
    plt.title(f"Fita {i+1} — Genoma Evolutivo com Estímulo Silencioso (Ciclos 100–130)")
    plt.xlabel("Posição no Genoma (0–90)")
    plt.ylabel("Ciclo Evolutivo (0–154)")
    plt.tight_layout()
    plt.show()