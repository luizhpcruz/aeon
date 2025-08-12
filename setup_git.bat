@echo off
echo 🔧 CONFIGURAÇÃO AUTOMATIZADA DO GIT PARA PROJETO AEON
echo ====================================================
echo.

echo ✅ Verificando configuração atual...
git config --global user.name
git config --global user.email
echo.

echo 🎯 Configurando aliases úteis...
git config --global alias.lg "log --oneline --graph --decorate --all"
git config --global alias.st "status -s" 
git config --global alias.co "checkout"
git config --global alias.br "branch"
git config --global alias.ci "commit"
git config --global alias.pushup "push -u origin HEAD"
git config --global alias.undo "reset HEAD~1"
git config --global alias.unstage "reset HEAD --"
echo ✅ Aliases configurados!
echo.

echo 📊 Configurando otimizações...
git config --global core.preloadindex true
git config --global core.fscache true
git config --global diff.algorithm patience
git config --global pull.rebase false
echo ✅ Otimizações aplicadas!
echo.

echo 🛡️ Configurando segurança...
git config --global credential.helper manager
git config --global core.autocrlf true
git config --global i18n.commitencoding utf-8
echo ✅ Configurações de segurança aplicadas!
echo.

echo 📋 RESUMO DA CONFIGURAÇÃO:
echo ========================
echo Aliases disponíveis:
echo   git lg      = Log gráfico bonito
echo   git st      = Status curto
echo   git co      = Checkout
echo   git br      = Branch
echo   git ci      = Commit
echo   git pushup  = Push com upstream
echo   git undo    = Desfazer último commit
echo   git unstage = Remover do staging
echo.

echo 🎯 Testando configuração...
git lg -3
echo.

echo ✅ Configuração Git concluída para projeto AEON!
echo 📍 Repositório: https://github.com/luizhpcruz/aeon.git
echo 🌟 Branch atual: develop
echo.
pause
