# 🔧 GUIA COMPLETO DE CONFIGURAÇÃO GIT - PROJETO AEON

## 📋 **CONFIGURAÇÃO BÁSICA GLOBAL**

### 1️⃣ **Identidade do Desenvolvedor:**
```bash
# Configurar nome global (já configurado)
git config --global user.name "lzcz"

# Configurar email global (já configurado)  
git config --global user.email "lzcz@live.com"

# Verificar configuração
git config --list | grep user
```

### 2️⃣ **Configuração Específica do Projeto AEON:**
```bash
# Navegar para o projeto
cd "c:\Users\Luiz\OneDrive\Área de Trabalho\aeon"

# Configurar nome específico para este projeto (opcional)
git config user.name "Luiz Cruz"
git config user.email "luizhpcruz@gmail.com"

# Configurar branch padrão
git config init.defaultBranch main
```

## 🚀 **CONFIGURAÇÕES AVANÇADAS PARA AEON**

### 3️⃣ **Aliases Úteis:**
```bash
# Logs bonitos
git config --global alias.lg "log --oneline --graph --decorate --all"

# Status curto
git config --global alias.st "status -s"

# Push com upstream automático
git config --global alias.pushup "push -u origin HEAD"

# Desfazer último commit (mantendo mudanças)
git config --global alias.undo "reset HEAD~1"
```

### 4️⃣ **Configurações de Performance:**
```bash
# Cache de credenciais (15 minutos)
git config --global credential.helper "cache --timeout=900"

# Otimizar para repositórios grandes
git config --global core.preloadindex true
git config --global core.fscache true

# Configurar diff melhor
git config --global diff.algorithm patience
```

### 5️⃣ **Configurações Específicas para Windows:**
```bash
# Quebras de linha (já configurado)
git config --global core.autocrlf true

# Encoding UTF-8 (já configurado)
git config --global i18n.commitencoding utf-8

# Case insensitive (já configurado)
git config --global core.ignorecase true
```

## 📊 **WORKFLOW RECOMENDADO PARA AEON**

### 6️⃣ **Branches Strategy:**
```bash
# Branch principal para releases
git checkout -b main

# Branch de desenvolvimento (atual)
git checkout develop

# Branches para features
git checkout -b feature/nova-funcionalidade

# Branches para hotfixes
git checkout -b hotfix/correcao-critica
```

### 7️⃣ **Comandos Essenciais para o Projeto:**
```bash
# 1. Atualizar do repositório remoto
git pull origin develop

# 2. Criar nova branch para feature
git checkout -b feature/minha-feature

# 3. Fazer commits frequentes
git add .
git commit -m "🔧 Implementa nova funcionalidade X"

# 4. Sincronizar com origin
git push -u origin feature/minha-feature

# 5. Merge na develop (via GitHub PR é melhor)
git checkout develop
git merge feature/minha-feature
```

## 🛡️ **CONFIGURAÇÕES DE SEGURANÇA**

### 8️⃣ **GPG Signing (Opcional mas Recomendado):**
```bash
# Gerar chave GPG
gpg --full-generate-key

# Listar chaves
gpg --list-secret-keys --keyid-format LONG

# Configurar Git para usar GPG
git config --global user.signingkey [SUA_CHAVE_ID]
git config --global commit.gpgsign true
```

### 9️⃣ **SSH Keys (Alternativa ao HTTPS):**
```bash
# Gerar chave SSH
ssh-keygen -t ed25519 -C "luizhpcruz@gmail.com"

# Iniciar ssh-agent
eval "$(ssh-agent -s)"

# Adicionar chave
ssh-add ~/.ssh/id_ed25519

# Testar conexão
ssh -T git@github.com
```

## 📁 **CONFIGURAÇÃO DO .gitignore OTIMIZADA**

### 🔧 **Já configurado, mas pode adicionar:**
```gitignore
# AEON específico
*.log
temp/
cache/
model_outputs/
simulation_results/
*.tmp

# Python otimizado
__pycache__/
*.pyc
.pytest_cache/
.coverage
.env

# VS Code otimizado
.vscode/settings.json
.vscode/launch.json
```

## 🎯 **COMANDOS ÚTEIS PARA DESENVOLVIMENTO AEON**

### 🔄 **Sincronização:**
```bash
# Verificar mudanças remotas
git fetch

# Ver diferenças
git diff origin/develop

# Merge suave
git pull --rebase origin develop
```

### 📊 **Análise:**
```bash
# Ver histórico gráfico
git log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset'

# Estatísticas do projeto
git shortlog -sn

# Arquivos mais modificados
git log --pretty=format: --name-only | sort | uniq -c | sort -rg | head -10
```

### 🚨 **Recuperação:**
```bash
# Recuperar arquivo deletado
git checkout HEAD -- arquivo.py

# Desfazer merge
git reset --hard HEAD~1

# Limpar working directory
git clean -fd
```

## ✅ **VERIFICAÇÃO DA CONFIGURAÇÃO**

### 📋 **Checklist:**
- [x] User name/email configurado
- [x] Repository remoto conectado
- [x] Branch develop sincronizada
- [x] .gitignore otimizado
- [x] Encoding UTF-8
- [ ] Aliases configurados
- [ ] SSH/GPG (opcional)

### 🔍 **Comandos de Verificação:**
```bash
# Verificar tudo
git config --list

# Testar conexão
git ls-remote origin

# Status completo
git status -v
```

---

## 🎯 **PRÓXIMOS PASSOS:**

1. **Configurar aliases úteis** (5 min)
2. **Testar workflow completo** (10 min)  
3. **Configurar SSH** para maior segurança (15 min)
4. **Implementar commit hooks** para qualidade (20 min)

**Quer que eu configure alguma dessas opções automaticamente?** 🚀
