from modules.quantum_transition import QuantumTransitionModule


def test_regime_is_selected_from_beta():
    module = QuantumTransitionModule()

    assert module.calcular_regime(-1) == "QUÂNTICO"
    assert module.calcular_regime(0) == "PONTO_DE_TRANSIÇÃO"
    assert module.calcular_regime(1) == "CLÁSSICO"


def test_bifurcation_is_detected_only_near_point():
    module = QuantumTransitionModule()

    near = module.analisar_fluxo_decisao(7.05, -1)
    far = module.analisar_fluxo_decisao(6.5, -1)

    assert near["decisao"] == "RUPTURA_BIFURCAÇÃO_DETECTADA"
    assert near["estabilidade"] == "INSTÁVEL"
    assert far["decisao"] == "FLUXO_ESTÁVEL"
    assert far["estabilidade"] == "ESTÁVEL"


def test_planck_scale_is_relative_to_constant():
    module = QuantumTransitionModule()

    assert module.escala_planck_relativa(module.PLANCK_MASS) == 1
