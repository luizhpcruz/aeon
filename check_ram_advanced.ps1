# 🖥️ VERIFICAÇÃO RÁPIDA DE RAM - PROJETO AEON
# Script PowerShell para análise instantânea

param(
    [switch]$Detailed,
    [switch]$Monitor,
    [int]$Interval = 5
)

function Get-RAMInfo {
    $os = Get-WmiObject Win32_OperatingSystem
    $cs = Get-WmiObject Win32_ComputerSystem
    
    $totalRAM = [math]::Round($cs.TotalPhysicalMemory / 1GB, 2)
    $freeRAM = [math]::Round($os.FreePhysicalMemory / 1MB / 1024, 2)
    $usedRAM = [math]::Round($totalRAM - $freeRAM, 2)
    $usagePercent = [math]::Round(($usedRAM / $totalRAM) * 100, 1)
    
    return @{
        TotalGB      = $totalRAM
        UsedGB       = $usedRAM
        FreeGB       = $freeRAM
        UsagePercent = $usagePercent
    }
}

function Get-AeonProcesses {
    $processes = @()
    
    # Processos Python relacionados ao AEON
    Get-Process python* -ErrorAction SilentlyContinue | ForEach-Object {
        if ($_.CommandLine -match "(aeon|p2p|entropy|cosma|verna)" -or 
            $_.MainWindowTitle -match "aeon") {
            $processes += [PSCustomObject]@{
                Name     = "🐍 " + $_.ProcessName
                PID      = $_.Id
                MemoryMB = [math]::Round($_.WorkingSet / 1MB, 1)
                Type     = "AEON Script"
            }
        }
    }
    
    # VS Code
    Get-Process *Code* -ErrorAction SilentlyContinue | ForEach-Object {
        $processes += [PSCustomObject]@{
            Name     = "📝 " + $_.ProcessName
            PID      = $_.Id
            MemoryMB = [math]::Round($_.WorkingSet / 1MB, 1)
            Type     = "VS Code"
        }
    }
    
    return $processes | Sort-Object MemoryMB -Descending
}

function Show-RAMStatus {
    param($RAMInfo, $Processes)
    
    Clear-Host
    
    # Header
    Write-Host "🧬 AEON RAM STATUS - $(Get-Date -Format 'HH:mm:ss')" -ForegroundColor Cyan
    Write-Host "=" * 50 -ForegroundColor Gray
    
    # RAM Status
    $statusColor = switch ($RAMInfo.UsagePercent) {
        { $_ -lt 70 } { "Green" }
        { $_ -lt 85 } { "Yellow" }
        default { "Red" }
    }
    
    $statusIcon = switch ($RAMInfo.UsagePercent) {
        { $_ -lt 70 } { "🟢" }
        { $_ -lt 85 } { "🟡" }
        default { "🔴" }
    }
    
    Write-Host "$statusIcon RAM: $($RAMInfo.UsagePercent)%" -ForegroundColor $statusColor
    Write-Host "💾 Total: $($RAMInfo.TotalGB) GB" -ForegroundColor White
    Write-Host "✅ Disponível: $($RAMInfo.FreeGB) GB" -ForegroundColor Green
    Write-Host "🔥 Em uso: $($RAMInfo.UsedGB) GB" -ForegroundColor $statusColor
    Write-Host ""
    
    # AEON Impact
    if ($Processes.Count -gt 0) {
        $totalAeonRAM = ($Processes | Measure-Object MemoryMB -Sum).Sum
        $impactPercent = [math]::Round(($totalAeonRAM / ($RAMInfo.TotalGB * 1024)) * 100, 1)
        
        Write-Host "🧬 IMPACTO AEON: $($Processes.Count) processos" -ForegroundColor Magenta
        Write-Host "📊 Uso total: $([math]::Round($totalAeonRAM, 1)) MB ($impactPercent%)" -ForegroundColor Magenta
        Write-Host "-" * 50 -ForegroundColor Gray
        
        $Processes | ForEach-Object {
            $color = if ($_.MemoryMB -gt 100) { "Yellow" } elseif ($_.MemoryMB -gt 50) { "White" } else { "Gray" }
            Write-Host "$($_.Name) (PID $($_.PID)): $($_.MemoryMB) MB" -ForegroundColor $color
        }
    }
    else {
        Write-Host "🧬 Nenhum processo AEON detectado" -ForegroundColor Gray
    }
    
    Write-Host ""
    
    # Alerts
    if ($RAMInfo.UsagePercent -ge 90) {
        Write-Host "🚨 ALERTA CRÍTICO: RAM acima de 90%!" -ForegroundColor Red -BackgroundColor Black
        Write-Host "💡 Feche aplicações desnecessárias imediatamente" -ForegroundColor Red
    }
    elseif ($RAMInfo.UsagePercent -ge 85) {
        Write-Host "⚠️ ATENÇÃO: RAM acima de 85%" -ForegroundColor Yellow -BackgroundColor Black
        Write-Host "📊 Monitore o uso de memória" -ForegroundColor Yellow
    }
}

function Show-DetailedInfo {
    param($RAMInfo)
    
    Write-Host "`n📋 INFORMAÇÕES DETALHADAS:" -ForegroundColor Cyan
    Write-Host "-" * 30 -ForegroundColor Gray
    
    # Classificação do sistema
    $systemClass = switch ($RAMInfo.TotalGB) {
        { $_ -lt 4 } { "💻 Sistema Básico (Atenção com AEON)" }
        { $_ -lt 8 } { "🖥️ Sistema Padrão (OK para AEON)" }
        { $_ -lt 16 } { "🚀 Sistema Avançado (Ideal para AEON)" }
        default { "🏆 Sistema High-End (Perfeito para AEON)" }
    }
    
    Write-Host $systemClass -ForegroundColor Green
    
    # Impacto AEON estimado
    $estimatedAeonUsage = 0.555 # GB conforme análise
    $impactPercent = [math]::Round(($estimatedAeonUsage / $RAMInfo.TotalGB) * 100, 1)
    
    Write-Host "`n🎯 IMPACTO ESTIMADO AEON:" -ForegroundColor Yellow
    Write-Host "   Uso médio: 555 MB (0.55 GB)" -ForegroundColor White
    Write-Host "   Impacto: $impactPercent% da RAM total" -ForegroundColor White
    
    $recommendation = switch ($impactPercent) {
        { $_ -lt 5 } { "✅ Impacto baixo - Execute sem restrições" }
        { $_ -lt 10 } { "👍 Impacto moderado - Monitore ocasionalmente" }
        { $_ -lt 15 } { "⚠️ Impacto alto - Monitore regularmente" }
        default { "🚨 Impacto crítico - Considere upgrade de RAM" }
    }
    
    Write-Host "   $recommendation" -ForegroundColor Magenta
}

# Main Logic
Write-Host "🚀 Iniciando verificação de RAM..." -ForegroundColor Green

if ($Monitor) {
    Write-Host "📊 Modo monitor ativado (Interval: $Interval segundos)" -ForegroundColor Cyan
    Write-Host "Pressione Ctrl+C para sair" -ForegroundColor Gray
    Write-Host ""
    
    try {
        while ($true) {
            $ramInfo = Get-RAMInfo
            $processes = Get-AeonProcesses
            Show-RAMStatus -RAMInfo $ramInfo -Processes $processes
            
            if ($Detailed) {
                Show-DetailedInfo -RAMInfo $ramInfo
            }
            
            Start-Sleep $Interval
        }
    }
    catch {
        Write-Host "`n👋 Monitor encerrado!" -ForegroundColor Green
    }
}
else {
    # Single check
    $ramInfo = Get-RAMInfo
    $processes = Get-AeonProcesses
    Show-RAMStatus -RAMInfo $ramInfo -Processes $processes
    
    if ($Detailed) {
        Show-DetailedInfo -RAMInfo $ramInfo
    }
    
    Write-Host "`n✅ Verificação concluída!" -ForegroundColor Green
    Write-Host "💡 Use -Monitor para monitoramento contínuo" -ForegroundColor Gray
    Write-Host "💡 Use -Detailed para informações extras" -ForegroundColor Gray
}

# Usage examples at the end
Write-Host "`n📖 EXEMPLOS DE USO:" -ForegroundColor Cyan
Write-Host "   .\check_ram.ps1                    # Verificação única" -ForegroundColor Gray
Write-Host "   .\check_ram.ps1 -Detailed          # Com informações extras" -ForegroundColor Gray
Write-Host "   .\check_ram.ps1 -Monitor           # Monitor contínuo" -ForegroundColor Gray
Write-Host "   .\check_ram.ps1 -Monitor -Interval 10  # Monitor a cada 10s" -ForegroundColor Gray
