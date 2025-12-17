#!/bin/bash
# CTO Brain Auto-Backup Script
# Automatically saves brain state to GitHub

TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
LOG_FILE="/workspace/apex-trade/backup.log"

echo "[$TIMESTAMP] Auto-backup triggered" >> "$LOG_FILE"

# Change to repository directory
cd /workspace/apex-trade || exit 1

# Add all changes
git add . 2>/dev/null

# Commit if there are changes
if git diff --staged --quiet; then
    echo "[$TIMESTAMP] No changes to backup" >> "$LOG_FILE"
else
    git commit -m "Auto-backup: $TIMESTAMP" 2>/dev/null
    if [ $? -eq 0 ]; then
        git push origin main 2>/dev/null
        echo "[$TIMESTAMP] Backup completed successfully" >> "$LOG_FILE"
    else
        echo "[$TIMESTAMP] Backup failed - commit error" >> "$LOG_FILE"
    fi
fi

echo "[$TIMESTAMP] Auto-backup process complete" >> "$LOG_FILE"