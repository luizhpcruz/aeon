# Simulação de OAuth.gov.br — usar real depois da homologação
def simulate_login_govbr(govbr_token: str) -> dict:
    # Em produção, troca token por ID e nome do usuário
    return {
        "govbr_id": "30988877766",  # CPF do supervisor ou funcionário
        "name": "Supervisor Auren"
    }
