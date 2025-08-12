# Contribuindo para o AEON

Obrigado por considerar contribuir para o projeto AEON! 🙏

## 🚀 Como Contribuir

### 1. **Fork e Clone**
```bash
# Fork no GitHub e clone localmente
git clone https://github.com/SEU_USUARIO/aeon1.git
cd aeon1
git remote add upstream https://github.com/luizhpcruz/aeon1.git
```

### 2. **Configurar Ambiente**
```bash
# Instalar dependências
pip install -r requirements.txt

# Instalar dependências de desenvolvimento
pip install -r requirements-dev.txt
```

### 3. **Criar Branch**
```bash
# Criar branch para sua feature
git checkout -b feature/nova-funcionalidade
# ou
git checkout -b bugfix/corrigir-problema
```

### 4. **Desenvolver**
- Siga os padrões de código Python (PEP 8)
- Adicione testes para novas funcionalidades
- Documente seu código
- Execute os testes localmente

### 5. **Testar**
```bash
# Executar testes
python -m pytest

# Executar linting
flake8 .

# Testar sistema P2P
python -m p2p.cluster
```

### 6. **Commit e Push**
```bash
# Commit com mensagem descritiva
git commit -m "feat: adiciona nova funcionalidade X"

# Push para seu fork
git push origin feature/nova-funcionalidade
```

### 7. **Pull Request**
1. Abra PR no GitHub
2. Descreva as mudanças claramente
3. Referencie issues relacionadas
4. Aguarde review

## 📋 Diretrizes

### **Padrões de Código**
- Use PEP 8 para Python
- Documente funções e classes
- Mantenha funções pequenas e focadas
- Use nomes descritivos para variáveis

### **Commits**
Use o padrão [Conventional Commits](https://conventionalcommits.org/):
- `feat:` para novas funcionalidades
- `fix:` para correções de bugs
- `docs:` para documentação
- `test:` para testes
- `refactor:` para refatorações

### **Testes**
- Escreva testes para novas funcionalidades
- Mantenha coverage acima de 80%
- Use pytest para testes
- Teste em múltiplas versões Python (3.11, 3.12, 3.13)

### **Documentação**
- Atualize README.md se necessário
- Documente APIs e interfaces
- Adicione exemplos de uso
- Mantenha CHANGELOG.md atualizado

## 🐛 Reportando Bugs

Use o template de issue no GitHub incluindo:
- Descrição clara do problema
- Passos para reproduzir
- Ambiente (OS, Python version)
- Logs relevantes

## 💡 Sugerindo Features

Use o template de feature request incluindo:
- Descrição da funcionalidade
- Justificativa/motivação
- Exemplos de uso
- Implementação sugerida

## 📞 Contato

- **Issues**: Para bugs e features
- **Discussions**: Para perguntas gerais
- **Email**: Através do GitHub

## 🙏 Reconhecimento

Todos os contribuidores serão listados no README.md e CONTRIBUTORS.md.

Obrigado por ajudar a tornar o AEON melhor! 🚀
