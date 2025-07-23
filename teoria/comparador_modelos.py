import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import pandas as pd

# Dados de exemplo - Pantheon+ simplificado
z_data = np.linspace(0.01, 2, 30)
mu_obs = 5 * np.log10(3000 * (1 + z_data)) + 25 + np.random.normal(0, 0.2, size=z_data.shape)
mu_err = np.full_like(z_data, 0.2)

# Modelo padrão ΛCDM
def H_LCDM(z, H0=70, Om=0.3, Ol=0.7):
    return H0 * np.sqrt(Om * (1 + z)**3 + Ol)

def mu_LCDM(z, H0=70, Om=0.3, Ol=0.7):
    c = 299792.458
    Ez = lambda zp: 1 / np.sqrt(Om * (1 + zp)**3 + Ol)
    D_C = [c * np.trapz([Ez(zz) for zz in np.linspace(0, zi, 100)], np.linspace(0, zi, 100)) / H0 for zi in z]
    return 5 * np.log10((1 + z) * np.array(D_C)) + 25

# Modelo modificado com Ω_ond
def H_ond(z, H0=70, Om=0.3, Ol=0.65, Oond=0.05, n=4):
    return H0 * np.sqrt(Om * (1 + z)**3 + Ol + Oond * (1 + z)**n)

def mu_ond(z, H0=70, Om=0.3, Ol=0.65, Oond=0.05, n=4):
    c = 299792.458
    Ez = lambda zp: 1 / np.sqrt(Om * (1 + zp)**3 + Ol + Oond * (1 + zp)**n)
    D_C = [c * np.trapz([Ez(zz) for zz in np.linspace(0, zi, 100)], np.linspace(0, zi, 100)) / H0 for zi in z]
    return 5 * np.log10((1 + z) * np.array(D_C)) + 25

# Função χ²
def chi2(model_mu, mu_obs, mu_err):
    return np.sum(((model_mu - mu_obs) / mu_err) ** 2)

# Executa comparação
mu_model1 = mu_LCDM(z_data)
mu_model2 = mu_ond(z_data)

chi2_1 = chi2(mu_model1, mu_obs, mu_err)
chi2_2 = chi2(mu_model2, mu_obs, mu_err)

k1, k2 = 2, 4
N = len(z_data)
AIC1, AIC2 = chi2_1 + 2*k1, chi2_2 + 2*k2
BIC1, BIC2 = chi2_1 + k1*np.log(N), chi2_2 + k2*np.log(N)

# Mostrar comparação
print(f"ΛCDM:     χ² = {chi2_1:.2f}, AIC = {AIC1:.2f}, BIC = {BIC1:.2f}")
print(f"Modificado: χ² = {chi2_2:.2f}, AIC = {AIC2:.2f}, BIC = {BIC2:.2f}")

# Plot
plt.figure(figsize=(10,6))
plt.errorbar(z_data, mu_obs, yerr=mu_err, fmt='o', label='Dados observacionais')
plt.plot(z_data, mu_model1, label='ΛCDM', color='blue')
plt.plot(z_data, mu_model2, label='Modelo com Ω_ond', color='red')
plt.xlabel("Redshift z")
plt.ylabel("Magnitude aparente")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("comparacao_modelos.png", dpi=300)
plt.show()
