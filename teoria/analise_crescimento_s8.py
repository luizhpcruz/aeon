import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# --- DADOS OBSERVACIONAIS DE f*sigma8(z) ---
fs8_data = np.array([
    [0.25, 0.422, 0.052],
    [0.37, 0.460, 0.038],
    [0.51, 0.457, 0.056],
    [0.60, 0.436, 0.034],
    [0.74, 0.447, 0.079],
    [0.86, 0.473, 0.040]
])

# --- PARÂMETROS DOS MODELOS ---
H0_mod, Om_mod, R0_mod, n_mod = 73.00, 0.291, 0.704, -1.001
sigma8_mod_hoje = 0.78 

H0_lcdm, Om_lcdm = 73.00, 0.302
sigma8_lcdm_hoje = 0.81

# --- MOTORES DE FÍSICA ---
def H_modificado(a, H0, Om, R0, n):
    z = (1.0 / a) - 1.0
    termo_de = (1 - Om - R0) + R0 * (1 + z)**n
    return H0 * np.sqrt(np.maximum(0, Om * (1 + z)**3 + termo_de))

def H_LCDM(a, H0, Om):
    z = (1.0 / a) - 1.0
    return H0 * np.sqrt(Om * (1 + z)**3 + (1 - Om))

# --- EQUAÇÃO DO CRESCIMENTO DE ESTRUTURA ---
def growth_equation(a, y, H_func, Om0):
    D, dD_da = y
    H = H_func(a)
    
    epsilon = 1e-6
    dH_da = (H_func(a + epsilon) - H_func(a - epsilon)) / (2 * epsilon)
    dlnH_dlna = (a / H) * dH_da
    
    Omega_m_a = Om0 * (a**-3) * (H_func(1.0)**2 / H**2)
    
    d2D_da2 = - (1/a**2) * ( (3 + dlnH_dlna) * a * dD_da - 1.5 * Omega_m_a * D )
    return [dD_da, d2D_da2]

# --- FUNÇÃO PRINCIPAL PARA CALCULAR f*sigma8 ---
def calculate_fsigma8(model_params, model_type, z_points, s8_today):
    if model_type == 'lcdm':
        H0, Om0 = model_params
        H_func = lambda a: H_LCDM(a, H0, Om0)
    else:
        H0, Om0, R0, n = model_params
        H_func = lambda a: H_modificado(a, H0, Om0, R0, n)

    a_init = 1e-3
    D_init = a_init
    dD_da_init = 1.0
    y_init = [D_init, dD_da_init]

    a_span = [a_init, 1.0]
    
    # CORREÇÃO: Garantir que os pontos de avaliação estejam ordenados crescentemente
    a_eval_descending = 1. / (1. + z_points)
    sort_indices = np.argsort(a_eval_descending)
    a_eval_ascending = a_eval_descending[sort_indices]

    sol = solve_ivp(growth_equation, a_span, y_init, args=(H_func, Om0), dense_output=True, t_eval=a_eval_ascending, rtol=1e-6)
    
    D_a = sol.y[0]
    dD_da = sol.y[1]
    
    # Normalizar o fator de crescimento para D(a=1)=1
    D_a_norm = D_a / sol.sol(1.0)[0]
    dD_da_norm = dD_da / sol.sol(1.0)[0]
    
    f_a = (a_eval_ascending / D_a_norm) * dD_da_norm
    sigma8_a = s8_today * D_a_norm
    
    # "Desfazer" a ordenação para que os resultados correspondam ao z_points original
    unsort_indices = np.argsort(sort_indices)
    
    return (f_a * sigma8_a)[unsort_indices]

# --- CÁLCULO E PLOTAGEM ---
z_plot = np.linspace(0.01, 1.2, 100)

fsigma8_lcdm = calculate_fsigma8([H0_lcdm, Om_lcdm], 'lcdm', z_plot, sigma8_lcdm_hoje)
fsigma8_mod = calculate_fsigma8([H0_mod, Om_mod, R0_mod, n_mod], 'modificado', z_plot, sigma8_mod_hoje)

plt.figure(figsize=(12, 8))
plt.errorbar(fs8_data[:, 0], fs8_data[:, 1], yerr=fs8_data[:, 2], fmt='o', color='black', label=r'Dados Observacionais ($f\sigma_8$)', capsize=5, zorder=10)
plt.plot(z_plot, fsigma8_lcdm, linestyle='--', color='crimson', lw=2.5, label=r'Previsão $\Lambda$CDM')
plt.plot(z_plot, fsigma8_mod, linestyle='-', color='indigo', lw=2.5, label='Previsão do Modelo Vetorial')

plt.xlabel("Redshift (z)", fontsize=14)
plt.ylabel(r"$f\sigma_8(z)$", fontsize=14)
plt.title("Previsões para o Crescimento de Estrutura vs. Dados", fontsize=16)
plt.legend(fontsize=12)
plt.grid(True, linestyle=':', alpha=0.7)
plt.xlim(0, 1.2)
plt.ylim(0.2, 0.6)
plt.tick_params(axis='both', which='major', labelsize=12)
plt.show()