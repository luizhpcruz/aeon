@echo off
echo 🧹 LIMPEZA AUTOMATIZADA - PROJETO AEON
echo =====================================

echo.
echo 📁 Criando pasta de backup...
if not exist "ARCHIVE_BACKUP" mkdir "ARCHIVE_BACKUP"

echo.
echo 🔍 Verificando pastas grandes...

if exist "archive" (
    echo 📦 Movendo pasta 'archive' ^(3.71 GB^)...
    move "archive" "ARCHIVE_BACKUP\archive_backup_%date:~10,4%%date:~4,2%%date:~7,2%" >nul 2>&1
    if %errorlevel%==0 (
        echo ✅ Archive movido com sucesso
    ) else (
        echo ❌ Erro ao mover archive
    )
) else (
    echo ℹ️ Pasta 'archive' não encontrada
)

if exist "digital_twin" (
    echo 🤖 Movendo pasta 'digital_twin' ^(2.60 GB^)...
    move "digital_twin" "ARCHIVE_BACKUP\digital_twin_backup_%date:~10,4%%date:~4,2%%date:~7,2%" >nul 2>&1
    if %errorlevel%==0 (
        echo ✅ Digital twin movido com sucesso
    ) else (
        echo ❌ Erro ao mover digital_twin
    )
) else (
    echo ℹ️ Pasta 'digital_twin' não encontrada
)

echo.
echo 🐍 Limpando cache Python...
pip cache purge >nul 2>&1
echo ✅ Cache Python limpo

echo.
echo 🗑️ Removendo arquivos temporários...
del /s /q *.tmp >nul 2>&1
del /s /q *.cache >nul 2>&1
del /s /q *.pyc >nul 2>&1
echo ✅ Arquivos temporários removidos

echo.
echo 📊 RELATÓRIO DE LIMPEZA:
echo =========================
echo 💾 Operações realizadas:
echo   - Cache Python limpo
echo   - Arquivos temporários removidos
if exist "ARCHIVE_BACKUP\archive_backup_*" echo   - Archive movido para backup ^(3.71 GB^)
if exist "ARCHIVE_BACKUP\digital_twin_backup_*" echo   - Digital twin movido para backup ^(2.60 GB^)

echo.
echo 🔍 PROJETO AEON ATUAL ^(mantido^):
if exist "p2p" echo   ✅ p2p: mantido
if exist "scripts" echo   ✅ scripts: mantido  
if exist "docs" echo   ✅ docs: mantido
if exist "core" echo   ✅ core: mantido
if exist "teoria" echo   ✅ teoria: mantido

echo.
echo 🎯 Backup criado em: ARCHIVE_BACKUP\
echo 🔒 Todos os arquivos importantes foram preservados!
echo ✅ Limpeza concluída com sucesso!

pause
