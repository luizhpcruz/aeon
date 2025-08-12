# Security Policy

## Supported Versions

Atualmente suportamos as seguintes versões do AEON com atualizações de segurança:

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

Se você descobrir uma vulnerabilidade de segurança no AEON, por favor nos ajude a manter o projeto seguro seguindo estas diretrizes:

### Como Reportar

1. **NÃO** crie uma issue pública no GitHub
2. Envie um email para: [criar email seguro]
3. Ou use o GitHub Security Advisory: https://github.com/luizhpcruz/aeon1/security/advisories

### Informações a Incluir

- Descrição detalhada da vulnerabilidade
- Passos para reproduzir o problema
- Impacto potencial
- Versões afetadas
- Sugestões de correção (se houver)

### O que Esperamos

- **Responsabilidade**: Não divulgue publicamente até recebermos e analisarmos
- **Tempo**: Tentaremos responder em 48 horas
- **Colaboração**: Trabalharemos juntos para resolver o problema

### O que Você Pode Esperar

1. **Confirmação** em até 48 horas
2. **Análise inicial** em até 7 dias
3. **Correção e teste** em até 30 dias
4. **Divulgação coordenada** após correção

### Recompensas

Atualmente não oferecemos recompensas monetárias, mas:
- Reconhecimento público (se desejado)
- Crédito no CHANGELOG
- Contribuição valorizada para a comunidade

## Práticas de Segurança

### Para Usuários

- Sempre use a versão mais recente
- Mantenha dependências atualizadas
- Use ambientes virtuais isolados
- Não execute código não confiável
- Configure adequadamente permissões de arquivo

### Para Desenvolvedores

- Validate todas as entradas de usuário
- Use HTTPS para comunicação
- Implemente logging de segurança
- Execute análise estática regular
- Mantenha dependências atualizadas

## Configurações Seguras

### Ambiente de Produção

```bash
# Use variáveis de ambiente para configurações sensíveis
export AEON_SECRET_KEY="sua-chave-secreta"
export AEON_DEBUG=false
export AEON_ALLOWED_HOSTS="localhost,127.0.0.1"
```

### Rede P2P

```python
# Configure autenticação adequada
P2P_CONFIG = {
    "use_encryption": True,
    "require_auth": True,
    "max_connections": 10,
    "timeout": 30
}
```

### Arquivos de Configuração

- Nunca commite senhas ou chaves
- Use `.env` files para desenvolvimento
- Configure `.gitignore` adequadamente
- Use gestores de segredos em produção

## Atualizações de Segurança

Atualizações de segurança são publicadas:
- Como releases no GitHub
- No arquivo CHANGELOG.md
- Em avisos de segurança do GitHub

## Contato

Para questões relacionadas à segurança:
- GitHub Security Advisory
- Issues privadas (marque como security)
- Email: [configurar email de segurança]

Obrigado por ajudar a manter o AEON seguro! 🔒
