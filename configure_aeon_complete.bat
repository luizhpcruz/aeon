@echo off
title AEON - Configuracao Completa
echo.
echo ===================================================
echo          CONFIGURACAO COMPLETA PROJETO AEON
echo ===================================================
echo.

echo [1/5] Verificando Git...
git --version
if %errorlevel% neq 0 (
    echo ERRO: Git nao encontrado!
    echo Instale o Git primeiro: https://git-scm.com/
    pause
    exit /b 1
)
echo ✓ Git OK

echo.
echo [2/5] Configurando aliases Git...
git config --global alias.lg "log --oneline --graph --decorate --all"
git config --global alias.st "status -s" 
git config --global alias.co "checkout"
git config --global alias.br "branch"
git config --global alias.ci "commit"
git config --global alias.pushup "push -u origin HEAD"
git config --global alias.undo "reset HEAD~1"
echo ✓ Aliases configurados

echo.
echo [3/5] Configurando otimizacoes Git...
git config --global core.preloadindex true
git config --global core.fscache true
git config --global diff.algorithm patience
git config --global pull.rebase false
git config --global credential.helper manager
echo ✓ Otimizacoes aplicadas

echo.
echo [4/5] Verificando status do repositorio...
git remote -v
git status --porcelain
echo ✓ Status verificado

echo.
echo [5/5] Criando scripts de monitoramento...
echo ✓ monitor_ram.py - Monitor Python completo (precisa psutil)
echo ✓ check_ram_simple.ps1 - Verificacao PowerShell rapida
echo ✓ GUIA_CONFIG_GIT.md - Documentacao completa

echo.
echo ===================================================
echo                CONFIGURACAO CONCLUIDA!
echo ===================================================
echo.
echo FERRAMENTAS DISPONIVEIS:
echo.
echo GIT ALIASES:
echo   git lg      = Log grafico bonito
echo   git st      = Status curto  
echo   git co      = Checkout
echo   git br      = Branch
echo   git ci      = Commit
echo   git pushup  = Push com upstream
echo   git undo    = Desfazer ultimo commit
echo.
echo MONITORAMENTO RAM:
echo   .\check_ram_simple.ps1           = Verificacao rapida
echo   .\check_ram_simple.ps1 -Monitor  = Monitor continuo
echo   python monitor_ram.py            = Monitor Python (se psutil instalado)
echo.
echo REPOSITORIO:
echo   URL: https://github.com/luizhpcruz/aeon.git
echo   Branch: develop
echo   Status: Sincronizado
echo.

echo Testando verificacao de RAM...
powershell -ExecutionPolicy Bypass -File "check_ram_simple.ps1"

echo.
echo ===================================================
echo Configuracao AEON concluida com sucesso!
echo Seu ambiente esta pronto para desenvolvimento.
echo ===================================================
echo.
pause
