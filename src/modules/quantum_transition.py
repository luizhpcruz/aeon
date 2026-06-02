import math

class QuantumTransitionModule:
    """
    🌀 Módulo de Transição Quântico-Clássica do AEON.
    Modela a transição de escalas baseada no parâmetro Beta e pontos de bifurcação.
    """
    def __init__(self):
        self.PLANCK_MASS = 2.176434e-8  # kg (m_P)
        self.BIFURCATION_POINT = 7.0    # x ≈ 7
        
    def calcular_regime(self, beta):
        """
        Determina se o sistema está no regime quântico ou clássico.
        β < 0: Quântico
        β > 0: Clássico
        """
        if beta < 0:
            return "QUÂNTICO"
        elif beta > 0:
            return "CLÁSSICO"
        else:
            return "PONTO_DE_TRANSIÇÃO"

    def analisar_fluxo_decisao(self, x, beta):
        """
        Analisa a estabilidade do fluxo no ponto de ruptura x ≈ 7.
        """
        distancia_ruptura = abs(x - self.BIFURCATION_POINT)
        regime = self.calcular_regime(beta)
        
        # O fluxo decide na ruptura
        if distancia_ruptura < 0.1:
            decisao = "RUPTURA_BIFURCAÇÃO_DETECTADA"
            estabilidade = "INSTÁVEL"
        else:
            decisao = "FLUXO_ESTÁVEL"
            estabilidade = "ESTÁVEL"
            
        return {
            "regime": regime,
            "decisao": decisao,
            "estabilidade": estabilidade,
            "distancia_ruptura": distancia_ruptura
        }

    def escala_planck_relativa(self, massa_sistema):
        """
        Calcula a escala do sistema em relação à Massa de Planck.
        """
        return massa_sistema / self.PLANCK_MASS

if __name__ == "__main__":
    transicao = QuantumTransitionModule()
    print("🧪 Testando Transição Quântica...")
    
    # Simulação de travessia do ponto de ruptura
    for x_val in [6.5, 7.0, 7.5]:
        resultado = transicao.analisar_fluxo_decisao(x_val, beta=-1.0)
        print(f"x={x_val} | Regime: {resultado['regime']} | Decisão: {resultado['decisao']} | Estabilidade: {resultado['estabilidade']}")
