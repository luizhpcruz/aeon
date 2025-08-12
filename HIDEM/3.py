import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize_scalar

# --- 1. Constantes cosmológicas ---
H0 = 70  # km/s/Mpc
c = 299792.458
Omega_m = 0.295
Omega_r = 9e-5

# --- 2. Densidade relativa de SMBH observada (normalizada) ---
def rho_BH_z(z):
    return np.exp(-0.5*((z - 1.5)/0.6)**2)

# --- 3. Ω_DE(a) derivado dos SMBHs ---
def Omega_DE_BH(a, alpha):
    z = 1/a - 1
    return alpha * rho_BH_z(z) / rho_BH_z(0)

# --- 4. H²(a) sem Λ, apenas matéria, radiação, DE_BH ---
def H2_BH_only(a, alpha):
    return Omega_m * a**(-3) + Omega_r * a**(-4) + Omega_DE_BH(a, alpha)

# --- 5. Dados reais de H(z) ---
z_obs = np.array([0.07, 0.12, 0.17, 0.27, 0.4, 0.48, 0.9, 1.3, 1.43, 1.75])
Hz_obs = np.array([69, 68.6, 83, 77, 95, 97, 117, 168, 177, 202])
Hz_err = np.array([19.6, 26.2, 8.0, 14, 17, 60, 23, 17, 18, 40])
a_obs = 1 / (1 + z_obs)

# --- 6. Função objetivo para ajustar α ---
def chi2(alpha):
    Hz_model = H0 * np.sqrt(H2_BH_only(a_obs, alpha))
    return np.sum(((Hz_obs - Hz_model) / Hz_err) ** 2)

# --- 7. Otimização de α ---
res = minimize_scalar(chi2, bounds=(0.001, 5.0), method='bounded')
alpha_opt = res.x

# --- 8. Grid para exibir curvas ---
z_grid = np.linspace(0, 4, 400)
a_grid = 1 / (1 + z_grid)
Hz_BH = H0 * np.sqrt(H2_BH_only(a_grid, alpha_opt))

Hz_LCDM = H0 * np.sqrt(Omega_m * (1 + z_grid)**3 + 1 - Omega_m - Omega_r)

# --- 9. Plot com dados ---
plt.figure(figsize=(8.5,5.5))
plt.errorbar(z_obs, Hz_obs, yerr=Hz_err, fmt='o', label='Dados reais', color='k', capsize=3)
plt.plot(z_grid, Hz_BH, lw=2, label=f'Só SMBH (α = {alpha_opt:.2f})', color='C1')
plt.plot(z_grid, Hz_LCDM, '--', label='ΛCDM', color='gray')
plt.xlabel('Redshift z')
plt.ylabel('H(z) [km/s/Mpc]')
plt.title('Expansão cósmica com energia escura gerada por SMBHs')
plt.legend()
plt.grid(True)
plt.gca().invert_xaxis()
plt.tight_layout()
plt.show()