# -*- coding: utf-8 -*-
"""
Módulo para Análise Bayesiana Real do Projeto AEON.

Este script utiliza PyMC para realizar a amostragem MCMC (Markov Chain Monte Carlo)
sobre os dados de entropia gerados pelo sistema core, substituindo a simulação
anterior por um modelo probabilístico robusto.

PRIORIDADE: CRÍTICA
"""

# 1. Importação de Bibliotecas
import pymc as pm
import numpy as np
import pandas as pd
import arviz as az
import logging
import matplotlib.pyplot as plt
from pathlib import Path
import sys

# Adicionar path do projeto para importar módulos AEON
current_dir = Path(__file__).parent.parent.parent
sys.path.append(str(current_dir))

# Configuração básica de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class BayesianEntropyAnalyzer:
    """
    Encapsula a lógica da análise Bayesiana para os dados de entropia do AEON.
    """
    def __init__(self, data_path: str):
        """
        Inicializa o analisador.

        Args:
            data_path (str): Caminho para o arquivo de dados (ex: .csv) 
                             contendo as métricas de entropia.
        """
        self.data_path = data_path
        self.data = self._load_data()
        self.model = None
        self.trace = None

    def _load_data(self) -> pd.DataFrame:
        """
        Carrega os dados de entropia do caminho especificado.
        
        TODO: Adaptar esta função para carregar os dados reais do banco de dados
              ou do arquivo gerado pelo sistema core do AEON.
        """
        logging.info(f"Carregando dados de {self.data_path}...")
        try:
            # Exemplo de carregamento de um CSV.
            # O arquivo deve conter uma coluna, por exemplo, 'entropy_values'
            df = pd.read_csv(self.data_path)
            if 'entropy_values' not in df.columns:
                raise ValueError("O arquivo CSV deve conter a coluna 'entropy_values'.")
            logging.info("Dados carregados com sucesso.")
            return df
        except FileNotFoundError:
            logging.warning(f"Arquivo não encontrado em: {self.data_path}. Gerando dados simulados para demonstração.")
            # Gerar dados simulados se o arquivo não existir, para fins de teste.
            # Simular dados de entropia Shannon realistas (0 a ~8 bits)
            np.random.seed(42)
            n_samples = 500
            
            # Simular entropia com duas componentes: base + variação temporal
            base_entropy = np.random.normal(loc=4.5, scale=0.8, size=n_samples)
            temporal_variation = 0.5 * np.sin(np.linspace(0, 4*np.pi, n_samples))
            noise = np.random.normal(0, 0.2, size=n_samples)
            
            simulated_entropy = base_entropy + temporal_variation + noise
            # Garantir que entropia seja positiva
            simulated_entropy = np.clip(simulated_entropy, 0.1, 8.0)
            
            return pd.DataFrame({
                'entropy_values': simulated_entropy,
                'timestamp': pd.date_range(start='2025-01-01', periods=n_samples, freq='H')
            })

    def define_model(self):
        """
        Define o modelo estatístico Bayesiano usando PyMC.

        Este é um modelo de exemplo que assume que os dados de entropia seguem
        uma distribuição Normal. O objetivo é estimar a média (mu) e o desvio
        padrão (sigma) dessa distribuição.
        """
        logging.info("Definindo o modelo Bayesiano...")
        coords = {"observation": self.data.index.values}
        
        with pm.Model(coords=coords) as self.model:
            # --- Priors (Nossas crenças iniciais sobre os parâmetros) ---
            # Prior para a média (mu) da entropia. Assumimos que a média
            # deve estar em torno de 4.5 bits (valor típico para entropia Shannon)
            mu = pm.Normal('mu', mu=4.5, sigma=2.0)
            
            # Prior para o desvio padrão (sigma). Deve ser positivo.
            # Usamos uma Meia-Normal (HalfNormal).
            sigma = pm.HalfNormal('sigma', sigma=1.0)

            # --- Likelihood (Como os dados são gerados) ---
            # A probabilidade dos dados observados ('entropy_values') dado os parâmetros.
            # Assumimos que os dados seguem uma distribuição Normal com a média mu e o desvio sigma.
            y_obs = pm.Normal(
                'y_obs', 
                mu=mu, 
                sigma=sigma, 
                observed=self.data['entropy_values'],
                dims="observation"
            )
        
        logging.info("Modelo definido com sucesso.")
        # Opcional: Visualizar a estrutura do modelo
        # pm.model_to_graphviz(self.model)

    def run_mcmc(self, draws: int = 2000, tune: int = 1000, chains: int = 4):
        """
        Executa a amostragem MCMC para inferir os parâmetros do modelo.

        Args:
            draws (int): O número de amostras a serem geradas para cada cadeia.
            tune (int): O número de iterações de "aquecimento" a serem descartadas.
            chains (int): O número de cadeias a serem executadas em paralelo.
        """
        if self.model is None:
            raise ValueError("O modelo deve ser definido antes de executar a amostragem. Chame define_model().")
            
        logging.info(f"Iniciando amostragem MCMC com {chains} cadeias, {draws} draws e {tune} tune steps...")
        with self.model:
            # Configurar sampler para melhor performance
            self.trace = pm.sample(
                draws=draws, 
                tune=tune, 
                chains=chains, 
                target_accept=0.95,
                random_seed=42,
                return_inferencedata=True
            )
        logging.info("Amostragem MCMC concluída.")

    def analyze_results(self):
        """
        Analisa e exibe os resultados da inferência.
        """
        if self.trace is None:
            raise ValueError("A amostragem MCMC deve ser executada primeiro. Chame run_mcmc().")

        logging.info("Gerando resumo dos resultados...")
        # az.summary() fornece estatísticas dos parâmetros (média, desvio padrão, etc.)
        summary = az.summary(self.trace, round_to=4)
        print("\n" + "="*60)
        print("🧠 ANÁLISE BAYESIANA - RESULTADOS FINAIS")
        print("="*60)
        print(summary)

        # Calcular intervalos de credibilidade
        hdi = az.hdi(self.trace, hdi_prob=0.95)
        print(f"\n📊 Intervalos de Credibilidade (95%):")
        for var in ['mu', 'sigma']:
            if var in hdi:
                lower, upper = hdi[var].values
                print(f"  {var}: [{lower:.4f}, {upper:.4f}]")

        # Diagnósticos de convergência
        print(f"\n🔍 Diagnósticos de Convergência:")
        rhat = az.rhat(self.trace)
        print(f"  R-hat (mu): {rhat['mu'].values:.4f}")
        print(f"  R-hat (sigma): {rhat['sigma'].values:.4f}")
        print("  📝 R-hat < 1.01 indica boa convergência")

        # Tamanho efetivo da amostra
        ess = az.ess(self.trace)
        print(f"\n📈 Tamanho Efetivo da Amostra:")
        print(f"  ESS (mu): {ess['mu'].values:.0f}")
        print(f"  ESS (sigma): {ess['sigma'].values:.0f}")

        logging.info("Gerando gráficos de diagnóstico (trace plots)...")
        try:
            # az.plot_trace() ajuda a diagnosticar a convergência das cadeias MCMC
            az.plot_trace(self.trace, var_names=['mu', 'sigma'])
            
            # Salva a figura em um arquivo PNG em vez de tentar exibi-la
            output_path = "bayesian_trace_plot.png"
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            plt.close()  # Fecha a figura para liberar memória
            logging.info(f"Gráfico de diagnóstico salvo em: {output_path}")
            
            # Posterior plots
            fig2, ax2 = plt.subplots(1, 2, figsize=(10, 4))
            az.plot_posterior(self.trace, var_names=['mu'], ax=ax2[0])
            az.plot_posterior(self.trace, var_names=['sigma'], ax=ax2[1])
            plt.tight_layout()
            plt.savefig('bayesian_posterior.png', dpi=300, bbox_inches='tight')
            plt.close()  # Fecha a figura para liberar memória
            logging.info("Posteriores salvos em 'bayesian_posterior.png'")
            
        except Exception as e:
            logging.warning(f"Erro ao gerar gráficos: {e}")

    def get_posterior_samples(self) -> dict:
        """
        Retorna amostras da distribuição posterior para uso em outros módulos.
        
        Returns:
            dict: Dicionário com amostras dos parâmetros
        """
        if self.trace is None:
            raise ValueError("A amostragem MCMC deve ser executada primeiro.")
        
        return {
            'mu_samples': az.extract(self.trace, var_names=['mu'])['mu'].values,
            'sigma_samples': az.extract(self.trace, var_names=['sigma'])['sigma'].values,
            'summary': az.summary(self.trace)
        }

    def save_results(self, output_path: str = "bayesian_results.nc"):
        """
        Salva os resultados da análise em formato NetCDF.
        
        Args:
            output_path (str): Caminho para salvar os resultados
        """
        if self.trace is None:
            raise ValueError("A amostragem MCMC deve ser executada primeiro.")
        
        self.trace.to_netcdf(output_path)
        logging.info(f"Resultados salvos em: {output_path}")

class BayesianCosmologyAnalyzer:
    """
    Análise Bayesiana específica para dados cosmológicos do AEON.
    Integra com o cosmos_fitter.py existente.
    """
    
    def __init__(self, supernovas_data=None):
        """
        Inicializa analisador cosmológico.
        
        Args:
            supernovas_data: Dados de supernovas (z, mu, sigma)
        """
        self.data = supernovas_data
        self.model = None
        self.trace = None
    
    def define_cosmology_model(self):
        """
        Define modelo Bayesiano para parâmetros cosmológicos.
        """
        logging.info("Definindo modelo cosmológico Bayesiano...")
        
        if self.data is None:
            # Gerar dados sintéticos de supernovas
            logging.warning("Usando dados sintéticos de supernovas")
            z = np.linspace(0.01, 2.0, 100)
            mu_theory = 5 * np.log10(self._luminosity_distance(z, 67.4, 0.315)) + 25
            mu_obs = mu_theory + np.random.normal(0, 0.15, len(z))
            sigma = np.full(len(z), 0.15)
            
            self.data = {
                'redshift': z,
                'distance_modulus': mu_obs,
                'error': sigma
            }
        
        with pm.Model() as self.model:
            # Priors baseados no Planck 2018
            H0 = pm.Normal('H0', mu=67.4, sigma=1.0)
            Omega_m = pm.Normal('Omega_m', mu=0.315, sigma=0.007)
            
            # Modelo físico: módulo de distância
            z = self.data['redshift']
            mu_theory = pm.Deterministic(
                'mu_theory',
                5 * pm.math.log10(self._luminosity_distance_pm(z, H0, Omega_m)) + 25
            )
            
            # Likelihood
            pm.Normal(
                'obs',
                mu=mu_theory,
                sigma=self.data['error'],
                observed=self.data['distance_modulus']
            )
        
        logging.info("Modelo cosmológico definido.")
    
    def _luminosity_distance(self, z, H0, Omega_m):
        """Distância luminosa (versão NumPy)"""
        c = 299792.458  # km/s
        Omega_L = 1 - Omega_m
        
        # Integração numérica simplificada
        dz = 0.01
        z_array = np.arange(0, np.max(z) + dz, dz)
        E_z = np.sqrt(Omega_m * (1 + z_array)**3 + Omega_L)
        
        d_c = (c / H0) * np.trapz(1/E_z, z_array)
        d_L = d_c * (1 + z)
        
        return d_L
    
    def _luminosity_distance_pm(self, z, H0, Omega_m):
        """Distância luminosa (versão PyMC)"""
        c = 299792.458
        Omega_L = 1 - Omega_m
        
        # Aproximação analítica para PyMC
        # Para z pequeno: d_L ≈ (c/H0) * z * [1 + z(1-q0)/2]
        # onde q0 = Omega_m/2 - Omega_L
        q0 = Omega_m/2 - Omega_L
        d_L = (c/H0) * z * (1 + z * (1 - q0)/2)
        
        return d_L

# --- Bloco de Execução Principal ---
if __name__ == '__main__':
    logging.info("--- Iniciando Pipeline de Análise Bayesiana do AEON ---")
    
    # Caminho para os dados. Altere para o caminho real do seu arquivo.
    # Se o arquivo não existir, o script usará dados simulados.
    DATA_FILE_PATH = 'data/entropy_metrics.csv'
    
    try:
        print("🚀 AEON - Análise Bayesiana Real com PyMC")
        print("=" * 50)
        
        # 1. Análise de Entropia
        print("\n🧠 1. ANÁLISE BAYESIANA DE ENTROPIA")
        analyzer = BayesianEntropyAnalyzer(data_path=DATA_FILE_PATH)
        analyzer.define_model()
        # Executar a inferência MCMC com parâmetros mais robustos
        # Aumente os draws, tune e chains para garantir a convergência.
        analyzer.run_mcmc(draws=2000, tune=1000, chains=4)
        analyzer.analyze_results()
        
        # Salvar resultados
        analyzer.save_results("aeon_entropy_bayesian.nc")
        
        # 2. Análise Cosmológica (bonus)
        print("\n🌌 2. ANÁLISE COSMOLÓGICA BAYESIANA")
        cosmo_analyzer = BayesianCosmologyAnalyzer()
        cosmo_analyzer.define_cosmology_model()
        
        with cosmo_analyzer.model:
            cosmo_trace = pm.sample(2000, tune=1000, chains=4, random_seed=42)
        
        print("\n📊 Resultados Cosmológicos:")
        cosmo_summary = az.summary(cosmo_trace, round_to=4)
        print(cosmo_summary)
        
        print("\n✅ Pipeline de Análise Bayesiana concluído com sucesso!")
        print("📁 Arquivos gerados:")
        print("  • aeon_entropy_bayesian.nc")
        print("  • bayesian_trace_plots.png")
        print("  • bayesian_posterior.png")
        
    except ImportError as e:
        print(f"❌ Erro de importação: {e}")
        print("💻 Execute: pip install pymc arviz matplotlib")
    except Exception as e:
        logging.error(f"Erro durante execução: {e}")
        print(f"❌ Erro: {e}")
    
    logging.info("--- Pipeline de Análise Bayesiana finalizado ---")
