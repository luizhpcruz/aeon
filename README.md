# AEON - Sistema de IA Simbólica e Gêmeo Digital

O projeto **AEON** é uma plataforma avançada que integra conceitos de IA simbólica, gêmeos digitais, redes P2P e computação quântica para criar sistemas adaptativos e resilientes.

## 🚀 Estrutura do Projeto

O repositório foi organizado para seguir as melhores práticas de desenvolvimento, focando na clareza e modularidade:

*   **`src/`**: Código-fonte principal do sistema.
    *   **`core/`**: Motores centrais e lógica de evolução (`AEONKernel`, `AeonCosmaEngine`).
    *   **`modules/`**: Módulos especializados (Criptografia, P2P, Quântico, Cosmologia, Blockchain/Atomic Swap e o `AEONCoreAnalyst`).
    *   **`api/`**: Endpoints e lógica de backend para integração.
    *   **`ui/`**: Interfaces de usuário e dashboards (Streamlit).
*   **`config/`**: Arquivos de configuração e dependências.
*   **`docs/`**: Documentação técnica, relatórios e fundamentos teóricos.
*   **`tests/`**: Suíte de testes para garantir a integridade do sistema.
*   **`docker-compose.yml`**: Orquestração da infraestrutura (API, Prometheus, Grafana).

## 🧠 Componentes Principais

### AEONCoreAnalyst
Um neurônio adaptativo local que utiliza a proporção áurea (PHI) para detectar desvios em fluxos de dados e ajustar a sensibilidade do sistema em tempo real.

### AEONKernel
O coração da evolução simbólica, processando informações e caos para refinar a rede de símbolos do sistema.

### AeonCosmaEngine
O orquestrador modular que integra comunicações P2P, segurança quântica e modelos cosmológicos.

### AEONBlockchain
Módulo de persistência criptográfica que permite a criação de correntes de blocos locais e a execução de Atomic Swaps cross-chain.

## 🛠️ Como Começar

1.  **Instalação**: As dependências estão listadas em `config/requirements.txt`.
2.  **Execução**: O motor principal pode ser iniciado através do `src/core/engine.py` ou via Docker com `docker-compose up`.
3.  **Monitoramento**: Utilize os dashboards em `src/ui/` para visualizar o estado do sistema.

## 📄 Licença

Este projeto está sob a licença [LICENSE](LICENSE).

---
Organizado por **Manus AI** em Junho de 2026.
