# CTO Brain Auto-Backup Script (PowerShell)
# Automatically saves brain state to GitHub

param(
    [switch]$Force = $false
)

# Get current timestamp
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$logFile = "c:\Users\rhuam\Documents\GitHub\apex-trade\backup.log"
$workspaceDir = "c:\Users\rhuam\Documents\GitHub\apex-trade"

# Function to log messages
function Log-Message {
    param([string]$message)
    $logEntry = "[$timestamp] $message"
    Add-Content -Path $logFile -Value $logEntry
    Write-Host $logEntry
}

# Main backup sequence
Write-Host "🔄 CTO Auto-Backup System - Initiated"
Write-Host "========================================"

Log-Message "Auto-backup triggered"

try {
    # Change to repository directory
    Push-Location $workspaceDir
    
    # Check if git is available
    $gitVersion = git --version 2>&1
    if ($LASTEXITCODE -ne 0) {
        Log-Message "ERROR: Git not found or not installed"
        exit 1
    }
    
    Log-Message "Git version: $gitVersion"
    
    # Add all changes
    Log-Message "Adding changes to git..."
    git add . 2>&1 | Out-Null
    
    # Check if there are staged changes
    $gitStatus = git diff --cached --name-only 2>&1
    
    if ([string]::IsNullOrWhiteSpace($gitStatus) -and -not $Force) {
        Log-Message "No changes to backup"
    } else {
        # Commit changes
        Log-Message "Committing changes..."
        git commit -m "Auto-backup: $timestamp" 2>&1 | Out-Null
        
        if ($LASTEXITCODE -eq 0) {
            # Push to remote
            Log-Message "Pushing to remote repository..."
            git push origin main 2>&1 | Out-Null
            
            if ($LASTEXITCODE -eq 0) {
                Log-Message "Backup completed successfully"
            } else {
                Log-Message "WARNING: Push failed"
            }
        } else {
            Log-Message "ERROR: Commit failed"
        }
    }
    
    # Get backup status
    $lastCommit = git log -1 --format="%ai" 2>&1
    if ($LASTEXITCODE -eq 0) {
        Log-Message "Last commit: $lastCommit"
    }
    
} catch {
    Log-Message "EXCEPTION: $_"
} finally {
    Pop-Location
    Log-Message "Auto-backup process complete"
}

Write-Host "========================================="
Write-Host "✅ Backup completed`n"
