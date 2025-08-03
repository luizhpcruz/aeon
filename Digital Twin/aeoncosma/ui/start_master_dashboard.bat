@echo off
echo Iniciando AEONCOSMA Master Dashboard...
cd /d "C:\Users\Luiz\OneDrive\Área de Trabalho\aeon\Digital Twin\aeoncosma\ui"
"C:\Users\Luiz\OneDrive\Área de Trabalho\aeon\Digital Twin\.venv\Scripts\python.exe" -m streamlit run master_dashboard.py --server.port 8508
pause
