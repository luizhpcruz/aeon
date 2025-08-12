@echo off
title AEON - Commit e Push para GitHub
echo 🧬 AEON - Commit e Push para GitHub
echo ==================================
echo.

cd /d "c:\Users\Luiz\OneDrive\Área de Trabalho\aeon"

echo 📍 Diretório atual:
cd

echo.
echo 🔧 Configurando repositório remoto:
git remote set-url origin git@github.com:luizhpcruz/aeon.git
git remote -v

echo.
echo 📊 Status do repositório:
git status --short

echo.
echo ➕ Adicionando arquivos:
git add .

echo.
echo 💾 Criando commit:
git commit -m "🧬 AEON - Sistema Completo de Simulação Evolutiva

✨ Características Principais:
- Sistema P2P distribuído para simulações cosmológicas  
- Motor de entropia quântica multi-dimensional
- Análise de padrões fractais e evolução temporal
- Interface dashboard interativa
- Documentação técnica completa

🚀 Componentes:
- AEON Cosma: Simulações cosmológicas
- V.E.R.N.A: Sistema de análise neural  
- P2P Cluster: Rede distribuída
- Dashboard: Interface web
- Scripts de automação

📊 Arquitetura modular e escalável com CI/CD configurado"

echo.
echo 🚀 Enviando para GitHub:
git push -u origin main

echo.
echo ✅ Commit realizado com sucesso!
echo 📍 Repositório: git@github.com:luizhpcruz/aeon.git
echo.
pause
