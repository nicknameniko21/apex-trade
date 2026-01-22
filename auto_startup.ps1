# CTO Autonomous Brain - Automatic Startup Script (PowerShell)
# This script runs automatically to restore and initialize all systems

Write-Host "🚀 CTO Self-Sustaining System - Auto Startup"
Write-Host "=============================================="

# Navigate to workspace
$workspaceDir = "c:\Users\rhuam\Documents\GitHub\apex-trade"
Set-Location $workspaceDir

# Run Python startup if it exists
$pythonScript = Join-Path $workspaceDir "cto_self_sustaining_startup.py"
if (Test-Path $pythonScript) {
    python $pythonScript
} else {
    Write-Host "⚠️  Python startup script not found at: $pythonScript"
    Write-Host "Current directory: $(Get-Location)"
    Write-Host "Files in directory:"
    Get-ChildItem -Path $workspaceDir -File | Select-Object -First 10
}

Write-Host "✅ CTO Systems startup script complete"
