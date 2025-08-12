@echo off
echo 🚀 Enviando projeto AEON para GitHub...
echo.

cd /d "c:\Users\Luiz\OneDrive\Área de Trabalho\aeon"

echo ✅ Configurando repositório...
git remote set-url origin https://github.com/luizhpcruz/aeon1.git

echo ✅ Adicionando arquivos...
git add .

echo ✅ Criando commit...
git commit -m "🚀 AEON - Sistema Completo de Simulação Evolutiva

- Sistema P2P distribuído para simulações cosmológicas
- Motor de entropia quântica multi-dimensional  
- Análise de padrões fractais e evolução temporal
- Interface dashboard interativa
- Documentação completa e CI/CD configurado
- Arquitetura modular com 12+ componentes especializados"

echo ✅ Configurando branch principal...
git branch -M main

echo ✅ Enviando para GitHub...
git push -u origin main --force

echo.
echo 🎉 Projeto enviado com sucesso para:
echo https://github.com/luizhpcruz/aeon1
echo.
pause
