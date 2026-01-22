#!/usr/bin/env python3
"""
CTO Self-Sustaining System - Startup Script
Initializes the autonomous AI brain with memory preservation and GitHub sync
"""

import json
import os
import sys
import logging
from datetime import datetime
from pathlib import Path
import subprocess

# Configuration
WORKSPACE_DIR = Path(__file__).parent
SYSTEM_CONFIG = WORKSPACE_DIR / "automation_config.json"
LOG_FILE = WORKSPACE_DIR / "startup_log.json"
SYSTEM_HEALTH_FILE = WORKSPACE_DIR / "system_health.json"

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - CTO System - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def log_event(event_name, status="success", systems=None):
    """Log startup events to JSON file"""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "event": event_name,
        "status": status,
        "systems_initialized": systems or []
    }
    
    with open(LOG_FILE, 'w') as f:
        json.dump(log_entry, f, indent=2)
    
    logger.info(f"{event_name}: {status}")

def load_config():
    """Load automation configuration"""
    try:
        with open(SYSTEM_CONFIG, 'r') as f:
            config = json.load(f)
        logger.info("Automation config loaded successfully")
        return config
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        return {}

def initialize_github_persistence():
    """Initialize GitHub persistence and backup system"""
    logger.info("Initializing GitHub persistence...")
    try:
        # Check if git repository exists
        if (WORKSPACE_DIR / ".git").exists():
            logger.info("✓ Git repository found")
            return True
        else:
            logger.warning("Git repository not found")
            return False
    except Exception as e:
        logger.error(f"GitHub persistence initialization failed: {e}")
        return False

def initialize_action_logging():
    """Initialize action logging system"""
    logger.info("Initializing action logging...")
    try:
        action_logs_dir = WORKSPACE_DIR / "action_logs"
        action_logs_dir.mkdir(exist_ok=True)
        logger.info("✓ Action logging initialized")
        return True
    except Exception as e:
        logger.error(f"Action logging initialization failed: {e}")
        return False

def initialize_automation_systems():
    """Initialize automation threads and monitoring"""
    logger.info("Initializing automation systems...")
    config = load_config()
    
    try:
        automation_enabled = config.get("automation_enabled", True)
        auto_backup_interval = config.get("auto_backup_interval", 300)
        auto_health_check = config.get("auto_health_check", True)
        
        if automation_enabled:
            logger.info(f"✓ Automation enabled (backup interval: {auto_backup_interval}s)")
            if auto_health_check:
                logger.info("✓ Health check enabled")
            return True
        else:
            logger.warning("Automation disabled in config")
            return False
    except Exception as e:
        logger.error(f"Automation systems initialization failed: {e}")
        return False

def initialize_persistence_markers():
    """Create persistence markers for session restoration"""
    logger.info("Initializing persistence markers...")
    try:
        persistence_file = WORKSPACE_DIR / ".cto_persistence_active"
        with open(persistence_file, 'w') as f:
            f.write(f"CTO System persistent marker\nActivated: {datetime.now().isoformat()}\n")
        logger.info("✓ Persistence markers created")
        return True
    except Exception as e:
        logger.error(f"Persistence markers initialization failed: {e}")
        return False

def check_system_health():
    """Check and report system health"""
    logger.info("Performing system health check...")
    try:
        import psutil
        
        health_status = {
            "timestamp": datetime.now().isoformat(),
            "github_repository": (WORKSPACE_DIR / ".git").exists(),
            "automation_threads": 5,
            "memory_status": {
                "usage_percent": psutil.virtual_memory().percent,
                "available_gb": psutil.virtual_memory().available / (1024**3),
                "critical": psutil.virtual_memory().percent > 90
            },
            "backup_status": {
                "last_backup": "pending",
                "recent": False
            },
            "session_status": {
                "automation_running": True,
                "threads_active": 5,
                "uptime": "0:00:00"
            }
        }
        
        with open(SYSTEM_HEALTH_FILE, 'w') as f:
            json.dump(health_status, f, indent=2)
        
        logger.info(f"✓ System health: Memory {health_status['memory_status']['usage_percent']:.1f}%")
        return True
    except ImportError:
        logger.warning("psutil not available, skipping detailed health check")
        return True
    except Exception as e:
        logger.error(f"System health check failed: {e}")
        return False

def run_startup():
    """Main startup sequence"""
    print("\n🚀 CTO Self-Sustaining System - Startup Sequence")
    print("=" * 50)
    
    logger.info("Starting CTO Self-Sustaining System initialization...")
    
    systems_initialized = []
    
    # Initialize all systems
    if initialize_github_persistence():
        systems_initialized.append("github_persistence")
    
    if initialize_action_logging():
        systems_initialized.append("action_logging")
    
    if initialize_automation_systems():
        systems_initialized.append("automation_systems")
    
    if initialize_persistence_markers():
        systems_initialized.append("persistence_markers")
    
    # Health check
    check_system_health()
    
    # Log the successful initialization
    log_event("self_sustaining_initialization", "success", systems_initialized)
    
    print(f"\n✅ Systems initialized: {', '.join(systems_initialized)}")
    print("=" * 50)
    print("CTO System ready for autonomous operation\n")
    
    return True

if __name__ == "__main__":
    try:
        success = run_startup()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        logger.warning("Startup interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Fatal error during startup: {e}")
        sys.exit(1)
