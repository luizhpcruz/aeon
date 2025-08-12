# RAM Check for AEON Project
# PowerShell script for quick RAM analysis

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
        TotalGB = $totalRAM
        UsedGB = $usedRAM
        FreeGB = $freeRAM
        UsagePercent = $usagePercent
    }
}

function Get-AeonProcesses {
    $processes = @()
    
    # Python processes related to AEON
    Get-Process python* -ErrorAction SilentlyContinue | ForEach-Object {
        $processes += [PSCustomObject]@{
            Name = "Python: " + $_.ProcessName
            PID = $_.Id
            MemoryMB = [math]::Round($_.WorkingSet / 1MB, 1)
            Type = "AEON Script"
        }
    }
    
    # VS Code
    Get-Process *Code* -ErrorAction SilentlyContinue | ForEach-Object {
        $processes += [PSCustomObject]@{
            Name = "VSCode: " + $_.ProcessName
            PID = $_.Id
            MemoryMB = [math]::Round($_.WorkingSet / 1MB, 1)
            Type = "VS Code"
        }
    }
    
    return $processes | Sort-Object MemoryMB -Descending
}

function Show-RAMStatus {
    param($RAMInfo, $Processes)
    
    Clear-Host
    
    # Header
    Write-Host "AEON RAM STATUS - $(Get-Date -Format 'HH:mm:ss')" -ForegroundColor Cyan
    Write-Host "=" * 50 -ForegroundColor Gray
    
    # RAM Status
    $statusColor = switch ($RAMInfo.UsagePercent) {
        {$_ -lt 70} { "Green" }
        {$_ -lt 85} { "Yellow" }
        default { "Red" }
    }
    
    Write-Host "RAM Usage: $($RAMInfo.UsagePercent)%" -ForegroundColor $statusColor
    Write-Host "Total: $($RAMInfo.TotalGB) GB" -ForegroundColor White
    Write-Host "Available: $($RAMInfo.FreeGB) GB" -ForegroundColor Green
    Write-Host "Used: $($RAMInfo.UsedGB) GB" -ForegroundColor $statusColor
    Write-Host ""
    
    # AEON Impact
    if ($Processes.Count -gt 0) {
        $totalAeonRAM = ($Processes | Measure-Object MemoryMB -Sum).Sum
        $impactPercent = [math]::Round(($totalAeonRAM / ($RAMInfo.TotalGB * 1024)) * 100, 1)
        
        Write-Host "AEON IMPACT: $($Processes.Count) processes" -ForegroundColor Magenta
        Write-Host "Total usage: $([math]::Round($totalAeonRAM, 1)) MB ($impactPercent%)" -ForegroundColor Magenta
        Write-Host "-" * 50 -ForegroundColor Gray
        
        $Processes | ForEach-Object {
            $color = if ($_.MemoryMB -gt 100) { "Yellow" } elseif ($_.MemoryMB -gt 50) { "White" } else { "Gray" }
            Write-Host "$($_.Name) (PID $($_.PID)): $($_.MemoryMB) MB" -ForegroundColor $color
        }
    } else {
        Write-Host "No AEON processes detected" -ForegroundColor Gray
    }
    
    Write-Host ""
    
    # Alerts
    if ($RAMInfo.UsagePercent -ge 90) {
        Write-Host "CRITICAL ALERT: RAM above 90%!" -ForegroundColor Red -BackgroundColor Black
        Write-Host "Close unnecessary applications immediately" -ForegroundColor Red
    } elseif ($RAMInfo.UsagePercent -ge 85) {
        Write-Host "WARNING: RAM above 85%" -ForegroundColor Yellow -BackgroundColor Black
        Write-Host "Monitor memory usage" -ForegroundColor Yellow
    }
}

function Show-DetailedInfo {
    param($RAMInfo)
    
    Write-Host "`nDETAILED INFORMATION:" -ForegroundColor Cyan
    Write-Host "-" * 30 -ForegroundColor Gray
    
    # System classification
    $systemClass = switch ($RAMInfo.TotalGB) {
        {$_ -lt 4} { "Basic System (Monitor AEON usage)" }
        {$_ -lt 8} { "Standard System (OK for AEON)" }
        {$_ -lt 16} { "Advanced System (Ideal for AEON)" }
        default { "High-End System (Perfect for AEON)" }
    }
    
    Write-Host $systemClass -ForegroundColor Green
    
    # Estimated AEON impact
    $estimatedAeonUsage = 0.555 # GB based on analysis
    $impactPercent = [math]::Round(($estimatedAeonUsage / $RAMInfo.TotalGB) * 100, 1)
    
    Write-Host "`nESTIMATED AEON IMPACT:" -ForegroundColor Yellow
    Write-Host "   Average usage: 555 MB (0.55 GB)" -ForegroundColor White
    Write-Host "   Impact: $impactPercent% of total RAM" -ForegroundColor White
    
    $recommendation = switch ($impactPercent) {
        {$_ -lt 5} { "Low impact - Run without restrictions" }
        {$_ -lt 10} { "Moderate impact - Monitor occasionally" }
        {$_ -lt 15} { "High impact - Monitor regularly" }
        default { "Critical impact - Consider RAM upgrade" }
    }
    
    Write-Host "   $recommendation" -ForegroundColor Magenta
}

# Main Logic
Write-Host "Starting RAM check..." -ForegroundColor Green

if ($Monitor) {
    Write-Host "Monitor mode activated (Interval: $Interval seconds)" -ForegroundColor Cyan
    Write-Host "Press Ctrl+C to exit" -ForegroundColor Gray
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
        Write-Host "`nMonitor stopped!" -ForegroundColor Green
    }
} else {
    # Single check
    $ramInfo = Get-RAMInfo
    $processes = Get-AeonProcesses
    Show-RAMStatus -RAMInfo $ramInfo -Processes $processes
    
    if ($Detailed) {
        Show-DetailedInfo -RAMInfo $ramInfo
    }
    
    Write-Host "`nCheck completed!" -ForegroundColor Green
    Write-Host "Use -Monitor for continuous monitoring" -ForegroundColor Gray
    Write-Host "Use -Detailed for extra information" -ForegroundColor Gray
}

# Usage examples
Write-Host "`nUSAGE EXAMPLES:" -ForegroundColor Cyan
Write-Host "   .\check_ram_simple.ps1                    # Single check" -ForegroundColor Gray
Write-Host "   .\check_ram_simple.ps1 -Detailed          # With extra info" -ForegroundColor Gray
Write-Host "   .\check_ram_simple.ps1 -Monitor           # Continuous monitor" -ForegroundColor Gray
Write-Host "   .\check_ram_simple.ps1 -Monitor -Interval 10  # Monitor every 10s" -ForegroundColor Gray
