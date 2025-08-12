# Análise de RAM - Projeto AEON
Write-Host "=== ANÁLISE DE RAM - PROJETO AEON ===" -ForegroundColor Cyan
Write-Host ""

# Informações gerais do sistema
$memory = Get-WmiObject -Class Win32_OperatingSystem
$totalGB = [math]::Round($memory.TotalVisibleMemorySize / 1024 / 1024, 2)
$freeGB = [math]::Round($memory.FreePhysicalMemory / 1024 / 1024, 2)
$usedGB = [math]::Round($totalGB - $freeGB, 2)
$usedPercent = [math]::Round(($usedGB / $totalGB) * 100, 1)

Write-Host "💾 MEMÓRIA DO SISTEMA:" -ForegroundColor Green
Write-Host "   Total RAM: $totalGB GB"
Write-Host "   RAM Usada: $usedGB GB ($usedPercent%)"
Write-Host "   RAM Livre: $freeGB GB"
Write-Host ""

# Processos Python
Write-Host "🐍 PROCESSOS PYTHON:" -ForegroundColor Yellow
$pythonProcesses = Get-Process | Where-Object { $_.ProcessName -like "*python*" }
if ($pythonProcesses) {
    $pythonProcesses | Sort-Object WorkingSet -Descending | ForEach-Object {
        $memoryMB = [math]::Round($_.WorkingSet / 1MB, 1)
        Write-Host "   PID $($_.Id): $memoryMB MB - $($_.ProcessName)"
    }
    $totalPythonMB = ($pythonProcesses | Measure-Object WorkingSet -Sum).Sum / 1MB
    Write-Host "   Total Python: $([math]::Round($totalPythonMB, 1)) MB"
}
else {
    Write-Host "   Nenhum processo Python ativo"
}
Write-Host ""

# Processos VS Code
Write-Host "💻 PROCESSOS VS CODE:" -ForegroundColor Magenta
$codeProcesses = Get-Process | Where-Object { $_.ProcessName -like "*Code*" -or $_.ProcessName -like "*electron*" }
if ($codeProcesses) {
    $totalCodeMB = ($codeProcesses | Measure-Object WorkingSet -Sum).Sum / 1MB
    Write-Host "   Processos encontrados: $($codeProcesses.Count)"
    Write-Host "   Total VS Code: $([math]::Round($totalCodeMB, 1)) MB"
    
    # Top 5 processos VS Code
    $codeProcesses | Sort-Object WorkingSet -Descending | Select-Object -First 5 | ForEach-Object {
        $memoryMB = [math]::Round($_.WorkingSet / 1MB, 1)
        Write-Host "   PID $($_.Id): $memoryMB MB - $($_.ProcessName)"
    }
}
else {
    Write-Host "   Nenhum processo VS Code ativo"
}
Write-Host ""

# Impacto estimado do projeto AEON
Write-Host "🧬 IMPACTO ESTIMADO PROJETO AEON:" -ForegroundColor Red
$estimatedAeonMB = 350  # Estimativa conservadora
$impactPercent = [math]::Round(($estimatedAeonMB / ($totalGB * 1024)) * 100, 2)
Write-Host "   Estimativa: ~$estimatedAeonMB MB"
Write-Host "   Impacto no sistema: ~$impactPercent%"

if ($impactPercent -lt 2) {
    Write-Host "   ✅ IMPACTO BAIXO - Sistema saudável" -ForegroundColor Green
}
elseif ($impactPercent -lt 5) {
    Write-Host "   ⚠️ IMPACTO MODERADO - Monitorar uso" -ForegroundColor Yellow
}
else {
    Write-Host "   ❌ IMPACTO ALTO - Considerar otimização" -ForegroundColor Red
}

Write-Host ""
Write-Host "=== ANÁLISE CONCLUÍDA ===" -ForegroundColor Cyan
