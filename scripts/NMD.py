import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# ----- Parâmetros Cosmológicos -----
H0 = 70.0                      # Hubble em km/s/Mpc
Ωm = 0.3
ΩΛ = 0.7
c = 299792.458                 # velocidade da luz em km/s

# ----- Modelo de H(z) -----
def H(z):
    return H0 * np.sqrt(Ωm * (1 + z)**3 + ΩΛ)

# ----- Trajetória da luz modificada -----
def light_path_deflected(z, χ):
    r0 = 1.5  # pico de deflexão em z ~ 1.5
    deflection = np.exp(-((z - r0) / 0.5)**2)
    return c / H(z) * (1 - 0.2 * deflection)  # distância comóv. dχ/dz

# ----- Integração de χ(z) -----
z_span = (0, 2.3)
z_eval = np.linspace(*z_span, 1000)
sol = solve_ivp(light_path_deflected, z_span, [0], t_eval=z_eval)
z_model = sol.t
chi_model = sol.y[0]

# ----- Carrega dados Pantheon+ (você pode substituir por csv real) -----
# Simulação rápida
z_pantheon = np.linspace(0.01, 2.3, 50)
mu_pantheon = 5 * np.log10(3000 * np.log10(1 + z_pantheon)) + 25
pantheon_data = pd.DataFrame({'z': z_pantheon, 'mu': mu_pantheon})

# ----- Converte χ(z) do modelo em distância modulada μ(z) -----
chi_interp = np.interp(z_pantheon, z_model, chi_model)
mu_model = 5 * np.log10((1 + z_pantheon) * chi_interp) + 25

# ----- CMB marker -----
cmb = {'z': 1100, 'chi': 13800}  # ponto isolado

# ----- Plot -----
plt.figure(figsize=(10, 6))
plt.scatter(pantheon_data['z'], pantheon_data['mu'], label='Pantheon+ (dados simulados)', color='black')
plt.plot(z_pantheon, mu_model, label='Modelo com deflexão vetorial', color='blue')
plt.axvline(cmb['z'], linestyle='--', color='red', label='CMB z ≈ 1100')
plt.xlabel('Redshift z')
plt.ylabel('Distância modulada μ(z) [mag]')
plt.title('Comparação: Modelo AEON com Deflexão vs Pantheon+')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
