import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize_scalar

# -------------------------------------------------
# 1. Constantes Cosmológicas
# -------------------------------------------------
H0 = 70  # km/s/Mpc
Omega_m = 0.295
Omega_r = 9e-5

# -------------------------------------------------
# 2. Parâmetros do HIDEM (fixos, com bons resultados anteriores)
# -------------------------------------------------
Omega_seed = 0.672
m = -0.822
a_c = 1.312

def Omega_halo(a):
    """
    Termo HIDEM: representa a contribuição dinâmica derivada do colapso de estruturas.
    """
    return Omega_seed * a**(-m) * np.exp(-a_c / a)

# -------------------------------------------------
# 3. Dinâmica dos SMBHs: perfil da densidade (função gaussiana)
# -------------------------------------------------
def rho_BH_z(z):
    """
    Perfil gaussiano com pico em z ~ 1.5 e largura 0.6:
    """
    return np.exp(-0.5 * ((z - 1.5) / 0.6)**2)

def Omega_BH_new(a, alpha):
    """
    Contribuição dinâmica dos SMBHs, com parâmetro de acoplamento alpha.
    Normaliza pela densidade no presente (z=0).
    """
    z = 1 / a - 1
    return alpha * rho_BH_z(z) / rho_BH_z(0)

# -------------------------------------------------
# 4. Modelo Combinado: HIDEM + nova dinâmica de SMBHs
# -------------------------------------------------
def H2_combined(a, alpha):
    """
    H^2(a)/H0^2 para o modelo combinado, sem constante Λ.
    """
    return Omega_m * a**(-3) + Omega_r * a**(-4) + (Omega_halo(a) + Omega_BH_new(a, alpha))

# -------------------------------------------------
# 5. Dados Observacionais de H(z)
# -------------------------------------------------
# Dados de cronômetros cósmicos (exemplo)
z_obs = np.array([0.07, 0.12, 0.17, 0.27, 0.4, 0.48, 0.9, 1.3, 1.43, 1.75])
Hz_obs = np.array([69, 68.6, 83, 77, 95, 97, 117, 168, 177, 202])
Hz_err = np.array([19.6, 26.2, 8.0, 14, 17, 60, 23, 17, 18, 40])
a_obs = 1 / (1 + z_obs)

def chi2_combined(alpha):
    """
    Calcula o total de chi² para os dados de H(z) usando o modelo combinado.
    """
    Hz_model = H0 * np.sqrt(H2_combined(a_obs, alpha))
    return np.sum( ((Hz_obs - Hz_model)/Hz_err)**2 )

# -------------------------------------------------
# 6. Otimização do Parâmetro α do Modelo Combinado
# -------------------------------------------------
res_combined = minimize_scalar(chi2_combined, bounds=(0.001, 5.0), method='bounded')
alpha_opt_combined = res_combined.x
chi2_value_combined = chi2_combined(alpha_opt_combined)

# Número de dados e número de parâmetros livres (apenas α é livre)
n_data = len(z_obs)
k_combined = 1

AIC_combined = 2 * k_combined + chi2_value_combined
BIC_combined = k_combined * np.log(n_data) + chi2_value_combined

# -------------------------------------------------
# 7. Modelo ΛCDM para Comparação
# -------------------------------------------------
def H2_LCDM(a):
    """
    H^2(a)/H0^2 para ΛCDM: com Ω_Λ = 1 - Ω_m - Ω_r.
    """
    Omega_L = 1 - Omega_m - Omega_r
    return Omega_m * a**(-3) + Omega_r * a**(-4) + Omega_L

Hz_LCDM_obs = H0 * np.sqrt(H2_LCDM(a_obs))
chi2_LCDM = np.sum( ((Hz_obs - Hz_LCDM_obs)/Hz_err)**2 )
# Se tratarmos as variáveis de ΛCDM como fixas, k_LCDM = 0.
k_LCDM = 0  
AIC_LCDM = 2 * k_LCDM + chi2_LCDM
BIC_LCDM = k_LCDM * np.log(n_data) + chi2_LCDM

# -------------------------------------------------
# 8. Plot das Curvas de H(z)
# -------------------------------------------------
z_grid = np.linspace(0, 4, 400)
a_grid = 1 / (1 + z_grid)
Hz_combined = H0 * np.sqrt(H2_combined(a_grid, alpha_opt_combined))
Hz_LCDM_grid = H0 * np.sqrt(H2_LCDM(a_grid))

plt.figure(figsize=(8.5, 5.5))
plt.errorbar(z_obs, Hz_obs, yerr=Hz_err, fmt='o',
             label='Dados Reais', color='k', capsize=3)
plt.plot(z_grid, Hz_combined, lw=2,
         label=f'Combined (α = {alpha_opt_combined:.3f})', color='C1')
plt.plot(z_grid, Hz_LCDM_grid, '--', lw=2,
         label='ΛCDM', color='gray')
plt.xlabel('Redshift z')
plt.ylabel('H(z) [km/s/Mpc]')
plt.title('Comparação: Modelo Combinado HIDEM + SMBH vs ΛCDM')
plt.legend()
plt.gca().invert_xaxis()
plt.grid(True)
plt.tight_layout()
plt.show()

# -------------------------------------------------
# 9. Impressão dos Resultados
# -------------------------------------------------
print("Modelo Combinado (HIDEM + nova dinâmica de SMBHs):")
print(f"  α otimizado: {alpha_opt_combined:.4f}")
print(f"  χ² total: {chi2_value_combined:.2f}")
print(f"  AIC: {AIC_combined:.2f}")
print(f"  BIC: {BIC_combined:.2f}\n")

print("Modelo ΛCDM:")
print(f"  χ² total: {chi2_LCDM:.2f}")
print(f"  AIC: {AIC_LCDM:.2f}")
print(f"  BIC: {BIC_LCDM:.2f}")