import numpy as np
import matplotlib.pyplot as plt
import time

# --- MÓDULO 1: O DNA SIMBÓLICO (A "Constituição") ---
class SymbolicDNA:
    """
    Define as leis fundamentais do nosso universo-brinquedo.
    """
    def __init__(self, nome, regra_mutacao, taxa_acoplamento_vida):
        self.nome = nome
        # A regra de mutação define a "física" da rede
        self.regra_mutacao = regra_mutacao 
        # O acoplamento define a "biofísica"
        self.taxa_acoplamento_vida = taxa_acoplamento_vida

# --- MÓDULO 2: A REDE VETORIAL (O "Espaço-Tempo Quântico") ---
class QuantumFoam:
    """
    Representa a rede de "bolhas interligadas" ou o campo vetorial.
    """
    def __init__(self, tamanho, dna):
        self.tamanho = tamanho
        self.dna = dna
        # O estado é uma fita de valores (ex: spin, energia)
        self.estados = np.random.rand(tamanho)
        self.entropia = 0

    def evoluir(self):
        # A evolução segue a "lei" definida no DNA
        # Exemplo: um autômato celular simples como regra
        novos_estados = np.copy(self.estados)
        for i in range(self.tamanho):
            vizinho_esq = self.estados[i-1]
            vizinho_dir = self.estados[(i+1) % self.tamanho]
            # A física está aqui:
            novos_estados[i] = self.dna.regra_mutacao(vizinho_esq, self.estados[i], vizinho_dir)
        self.estados = novos_estados

    def calcular_entropia(self):
        # Calcula a entropia de Shannon da distribuição de estados
        hist, _ = np.histogram(self.estados, bins=10, range=(0,1))
        probs = hist / self.tamanho
        probs = probs[probs > 0] # Evita log(0)
        self.entropia = -np.sum(probs * np.log2(probs))

# --- MÓDULO 3: O SISTEMA BIOLÓGICO (O "Ressonador") ---
class BioSystem:
    """
    Representa um sistema vivo simples que ressoa com a rede quântica.
    """
    def __init__(self, dna):
        self.dna = dna
        self.vitalidade = 0.5 # Saúde inicial
        self.hist_vitalidade = []

    def ressoar(self, entropia_da_rede):
        # A "Ressonância Fóton-Vida": a vitalidade do sistema é afetada pela entropia do seu ambiente
        # Um ambiente com entropia média (nem caos, nem ordem total) é o ideal
        caos = entropia_da_rede / np.log2(10) # Normaliza a entropia
        sintonia = 1.0 - abs(caos - 0.5) * 2 # Pico em 0.5
        
        # O acoplamento do DNA define quão forte é essa ressonância
        mudanca_vitalidade = (sintonia - 0.5) * self.dna.taxa_acoplamento_vida
        self.vitalidade += mudanca_vitalidade
        self.vitalidade = max(0, min(1, self.vitalidade)) # Limita entre 0 e 1
        self.hist_vitalidade.append(self.vitalidade)

# --- CONFIGURAÇÃO E EXECUÇÃO DA SIMULAÇÃO ---

# Vamos definir duas "físicas" diferentes através do DNA
regra_caotica = lambda l, c, r: (l + c + r + 0.1) % 1.0
regra_ordenada = lambda l, c, r: (l + r) / 2
dna_caotico = SymbolicDNA(nome="Universo Caótico", regra_mutacao=regra_caotica, taxa_acoplamento_vida=0.05)
dna_ordenado = SymbolicDNA(nome="Universo Ordenado", regra_mutacao=regra_ordenada, taxa_acoplamento_vida=0.05)

# Inicializar os dois universos
universo_caotico = QuantumFoam(tamanho=100, dna=dna_caotico)
biosistema_caotico = BioSystem(dna=dna_caotico)

universo_ordenado = QuantumFoam(tamanho=100, dna=dna_ordenado)
biosistema_ordenado = BioSystem(dna=dna_ordenado)

# Loop da simulação
num_ciclos = 200
for i in range(num_ciclos):
    # Universo 1
    universo_caotico.evoluir()
    universo_caotico.calcular_entropia()
    biosistema_caotico.ressoar(universo_caotico.entropia)
    
    # Universo 2
    universo_ordenado.evoluir()
    universo_ordenado.calcular_entropia()
    biosistema_ordenado.ressoar(universo_ordenado.entropia)

# --- VISUALIZAÇÃO DOS RESULTADOS ---
fig, axs = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

# Gráfico para o Universo Caótico
axs[0].plot(biosistema_caotico.hist_vitalidade, label="Vitalidade do Bio-Sistema", color='crimson')
ax0_twin = axs[0].twinx()
ax0_twin.plot([h.entropia for h in [universo_caotico]*num_ciclos], label="Entropia da Rede", color='royalblue', linestyle=':')
axs[0].set_title(f"Simulação: {universo_caotico.dna.nome}")
axs[0].set_ylabel("Vitalidade", color='crimson')
ax0_twin.set_ylabel("Entropia (bits)", color='royalblue')
axs[0].grid(True)
axs[0].legend(loc='upper left')
ax0_twin.legend(loc='upper right')

# Gráfico para o Universo Ordenado
axs[1].plot(biosistema_ordenado.hist_vitalidade, label="Vitalidade do Bio-Sistema", color='crimson')
ax1_twin = axs[1].twinx()
ax1_twin.plot([h.entropia for h in [universo_ordenado]*num_ciclos], label="Entropia da Rede", color='royalblue', linestyle=':')
axs[1].set_title(f"Simulação: {universo_ordenado.dna.nome}")
axs[1].set_xlabel("Ciclo de Evolução")
axs[1].set_ylabel("Vitalidade", color='crimson')
ax1_twin.set_ylabel("Entropia (bits)", color='royalblue')
axs[1].grid(True)
axs[1].legend(loc='upper left')
ax1_twin.legend(loc='upper right')

plt.tight_layout()
plt.show()