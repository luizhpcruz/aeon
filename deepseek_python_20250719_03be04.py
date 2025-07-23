import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp, trapz
from scipy.optimize import curve_fit
import pandas as pd

# =================================================
# PARTE 1: DADOS OBSERVACIONAIS REAIS
# =================================================

# --- Carregar dados do Pantheon+ (Supernovas) ---
pantheon = pd.read_csv('https://github.com/PantheonPlusSH0ES/DataRelease/raw/main/Pantheon%2B_Data/4_DISTANCES_AND_COVAR/Pantheon%2BSH0ES.dat', 
                       delim_whitespace=True)
z_sn = pantheon['zHD'].values
mu_obs = pantheon['MU_SH0ES'].values
mu_err = pantheon['MU_DIFF'].values

# --- Carregar dados fσ8 (Crescimento de Estruturas) ---
fs8_data = pd.read_csv('https://raw.githubusercontent.com/armando-cn/fsigma8/master/data/fsigma8.dat', 
                       delim_whitespace=True, comment='#')
z_fs8 = fs8_data['z'].values
fs8_obs = fs8_data['f_sigma8'].values
fs8_err = fs8_data['err'].values

# --- Carregar dados H(z) (Chronometers) ---
hz_data = pd.read_csv('https://gitlab.com/mmoresco/CCcov/-/raw/master/Hz_all.dat', 
                      delim_whitespace=True, comment='#')
z_hz = hz_data['z'].values
hz_obs = hz_data['Hz'].values
hz_err = hz_data['err'].values

# =================================================
# PARTE 2: MODELOS COSMOLÓGICOS
# =================================================

# --- Constantes Fundamentais ---
c = 299792.458  # km/s

# *** Modelo ΛCDM ***
def H_LCDM(z, H0, Om):
    return H0 * np.sqrt(Om * (1+z)**3 + (1 - Om))

def mu_integrand(z, H0, Om):
    return c / H_LCDM(z, H0, Om)

def mu_LCDM(z, H0, Om):
    D_L = (1+z) * np.array([trapz(mu_integrand(np.linspace(0, zi, 500), H0, Om), 
                           dx=zi/500) for zi in z])
    return 5*np.log10(D_L) - 5 + 25  # μ = 5log₁₀(D_L/pc) - 5

# *** Modelo com Ω_ond ***
def H_ond(z, H0, Om, Oond, n):
    Ol = 1 - Om - Oond  # Força planura
    return H0 * np.sqrt(Om*(1+z)**3 + Ol + Oond*(1+z)**n)

def fs8_growth(a, H_func, Om0, s8_0):
    # Resolver equação de crescimento
    def growth_eq(a, y):
        D, dD_da = y
        H = H_func(a)
        dH_da = (H_func(a+1e-6) - H_func(a-1e-6)) / 2e-6
        Om_a = Om0 * (H_func(1)**2 / H**2) * a**(-3)
        d2D_da2 = -(3/a + dH_da/H)*dD_da + 1.5*Om_a*D/a**2
        return [dD_da, d2D_da2]
    
    sol = solve_ivp(growth_eq, [1e-3, 1.0], [1e-3, 1], 
                    t_eval=[a], args=(), rtol=1e-6)
    D = sol.y[0][-1]
    dD_da = sol.y[1][-1]
    f = a * dD_da / D
    return f * s8_0 * D

# =================================================
# PARTE 3: AJUSTE AOS DADOS REAIS
# =================================================

# --- Funções χ² para otimização ---
def chi2_LCDM(params):
    H0, Om, s8 = params
    # Ajuste a H(z)
    model_hz = H_LCDM(z_hz, H0, Om)
    chi2_hz = np.sum(((model_hz - hz_obs)/hz_err)**2)
    
    # Ajuste a Supernovas
    model_mu = mu_LCDM(z_sn, H0, Om)
    chi2_sn = np.sum(((model_mu - mu_obs)/mu_err)**2)
    
    # Ajuste a fσ8
    model_fs8 = [fs8_growth(1/(1+z), lambda a: H_LCDM(1/a-1, H0, Om), Om, s8) 
                for z in z_fs8]
    chi2_fs8 = np.sum(((model_fs8 - fs8_obs)/fs8_err)**2)
    
    return chi2_hz + chi2_sn + chi2_fs8

def chi2_ond(params):
    H0, Om, Oond, n, s8 = params
    # Ajuste a H(z)
    model_hz = H_ond(z_hz, H0, Om, Oond, n)
    chi2_hz = np.sum(((model_hz - hz_obs)/hz_err)**2)
    
    # Ajuste a Supernovas
    def H_func(a): 
        return H_ond(1/a-1, H0, Om, Oond, n)
    D_L = (1+z_sn)*np.array([trapz(c/H_func(np.linspace(1,1/(1+zi),500)), 
                               dx=np.log(1/(1+zi))/500) for zi in z_sn])
    model_mu = 5*np.log10(D_L) - 5 + 25
    chi2_sn = np.sum(((model_mu - mu_obs)/mu_err)**2)
    
    # Ajuste a fσ8
    model_fs8 = [fs8_growth(1/(1+z), H_func, Om, s8) for z in z_fs8]
    chi2_fs8 = np.sum(((model_fs8 - fs8_obs)/fs8_err)**2)
    
    return chi2_hz + chi2_sn + chi2_fs8

# --- Otimização com MCMC (exemplo simplificado) ---
from scipy.optimize import differential_evolution

# ΛCDM
bounds_LCDM = [(65, 75), (0.2, 0.4), (0.7, 0.9)]
result_LCDM = differential_evolution(chi2_LCDM, bounds_LCDM, strategy='best1bin', popsize=15)
H0_LCDM, Om_LCDM, s8_LCDM = result_LCDM.x

# Modelo com Ω_ond
bounds_ond = [(65, 75), (0.2, 0.4), (0.0, 0.2), (-5, 5), (0.7, 0.9)]
result_ond = differential_evolution(chi2_ond, bounds_ond, strategy='best1bin', popsize=20)
H0_ond, Om_ond, Oond_ond, n_ond, s8_ond = result_ond.x

# =================================================
# PARTE 4: COMPARAÇÃO ESTATÍSTICA
# =================================================

# Calcular χ² total
chi2_LCDM_val = chi2_LCDM([H0_LCDM, Om_LCDM, s8_LCDM])
chi2_ond_val = chi2_ond([H0_ond, Om_ond, Oond_ond, n_ond, s8_ond])

# Critérios de informação
k_LCDM = 3
k_ond = 5
N_data = len(z_sn) + len(z_fs8) + len(z_hz)

AIC_LCDM = chi2_LCDM_val + 2*k_LCDM
AIC_ond = chi2_ond_val + 2*k_ond

BIC_LCDM = chi2_LCDM_val + k_LCDM*np.log(N_data)
BIC_ond = chi2_ond_val + k_ond*np.log(N_data)

print("ΛCDM:")
print(f"  H0 = {H0_LCDM:.1f}, Ωm = {Om_LCDM:.3f}, σ8 = {s8_LCDM:.3f}")
print(f"  χ² = {chi2_LCDM_val:.1f}, AIC = {AIC_LCDM:.1f}, BIC = {BIC_LCDM:.1f}")

print("\nModelo com Ω_ond:")
print(f"  H0 = {H0_ond:.1f}, Ωm = {Om_ond:.3f}, Ω_ond = {Oond_ond:.4f}, n = {n_ond:.2f}, σ8 = {s8_ond:.3f}")
print(f"  χ² = {chi2_ond_val:.1f}, AIC = {AIC_ond:.1f}, BIC = {BIC_ond:.1f}")

# =================================================
# PARTE 5: VISUALIZAÇÃO DOS RESULTADOS
# =================================================

# Configurar plots
fig, axs = plt.subplots(3, 1, figsize=(10, 15), sharex=True)

# Painel 1: H(z)
z_range = np.linspace(0, 2, 100)
axs[0].errorbar(z_hz, hz_obs, yerr=hz_err, fmt='o', label='Dados H(z)')
axs[0].plot(z_range, H_LCDM(z_range, H0_LCDM, Om_LCDM), 'r--', label='ΛCDM')
axs[0].plot(z_range, H_ond(z_range, H0_ond, Om_ond, Oond_ond, n_ond), 'b-', label='Modelo Ω_ond')
axs[0].set_ylabel('H(z) [km/s/Mpc]')

# Painel 2: Supernovas
axs[1].errorbar(z_sn, mu_obs, yerr=mu_err, fmt='o', alpha=0.5, label='Pantheon+')
axs[1].plot(z_range, mu_LCDM(z_range, H0_LCDM, Om_LCDM), 'r--')
axs[1].plot(z_range, [mu_ond(zi, H0_ond, Om_ond, Oond_ond, n_ond) for zi in z_range], 'b-')
axs[1].set_ylabel('μ(z)')

# Painel 3: fσ8(z)
axs[2].errorbar(z_fs8, fs8_obs, yerr=fs8_err, fmt='o', label='Dados fσ8')
axs[2].plot(z_range, [fs8_growth(1/(1+zi), lambda a: H_LCDM(1/a-1, H0_LCDM, Om_LCDM), Om_LCDM, s8_LCDM) 
                for zi in z_range], 'r--')
axs[2].plot(z_range, [fs8_growth(1/(1+zi), lambda a: H_ond(1/a-1, H0_ond, Om_ond, Oond_ond, n_ond), Om_ond, s8_ond) 
                for zi in z_range], 'b-')
axs[2].set_xlabel('Redshift z')
axs[2].set_ylabel('fσ₈(z)')

for ax in axs:
    ax.legend()
    ax.grid(True)

plt.tight_layout()
plt.savefig('comparacao_dados_reais.png', dpi=300)
plt.show()