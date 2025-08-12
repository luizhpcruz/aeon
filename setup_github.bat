@echo off
echo 🧬 CONFIGURAÇÃO DO REPOSITÓRIO AEON NO GITHUB
echo ==============================================
echo.

echo 📋 Passos para configurar o GitHub:
echo.

echo 1️⃣ CRIAR REPOSITÓRIO NO GITHUB:
echo    • Acesse: https://github.com/new
echo    • Nome: aeon
echo    • Descrição: Advanced Evolutionary Organism Network
echo    • Público ou Privado (sua escolha)
echo    • NÃO marque 'Initialize with README'
echo.

echo 2️⃣ CONFIGURAR GIT LOCAL:
echo git config user.name "luizhpcruz"
echo git config user.email "seu-email@example.com"
echo.

echo 3️⃣ ADICIONAR REMOTE:
echo git remote add origin https://github.com/luizhpcruz/aeon.git
echo.

echo 4️⃣ VERIFICAR STATUS:
echo git status
echo.

echo 5️⃣ ADICIONAR ARQUIVOS:
echo git add .
echo.

echo 6️⃣ FAZER COMMIT:
echo git commit -m "🧬 Initial AEON project setup"
echo.

echo 7️⃣ PUSH PARA GITHUB:
echo git push -u origin develop
echo.

echo 📊 VERIFICAÇÕES ATUAIS:
echo • Repositório local: %CD%
git branch --show-current 2>nul && echo • Branch atual: || echo • Branch atual: não detectada
git remote -v 2>nul | findstr "origin" && echo • Remote configurado: || echo • Remote configurado: nenhum
echo.

echo 🔧 COMANDOS ÚTEIS:
echo • Ver status: git status
echo • Ver commits: git log --oneline
echo • Ver remotes: git remote -v
echo • Ver branches: git branch -a
echo.

echo 💡 DICA: Se o repositório 'aeon' já existir no seu GitHub,
echo          você pode usar o mesmo nome ou criar um novo.
echo.

echo ⚡ EXECUTAR AUTOMATICAMENTE? (s/n)
set /p choice="Pressione 's' para executar os comandos automaticamente: "

if /i "%choice%"=="s" (
    echo.
    echo 🚀 Executando configuração...
    
    echo • Configurando usuário Git...
    git config user.name "luizhpcruz"
    git config user.email "luizhpcruz@users.noreply.github.com"
    
    echo • Verificando remote...
    git remote | findstr "origin" >nul || git remote add origin https://github.com/luizhpcruz/aeon.git
    
    echo • Verificando status...
    git status
    
    echo.
    echo ✅ Configuração básica concluída!
    echo 💡 Agora você pode fazer: git add . && git commit && git push
)

pause
