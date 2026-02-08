#!/usr/bin/env python3
"""
Pine Scripts Auto-Sync
Automatically syncs Pine Scripts from external source and integrates with swarm
"""

import json
import logging
import asyncio
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PineScriptsAutoSync:
    """Automatic synchronization and integration of Pine Scripts"""

    def __init__(self, workspace_dir: str = None):
        self.workspace_dir = Path(workspace_dir) if workspace_dir else Path.cwd()
        self.pine_scripts_dir = self.workspace_dir / "pine_scripts"
        self.sync_log = self.workspace_dir / "action_logs" / "pine_sync.log"
        self.sync_log.parent.mkdir(parents=True, exist_ok=True)

    def sync_from_external(self, source_path: str) -> Dict[str, Any]:
        """Sync Pine Scripts from external repository"""
        try:
            source = Path(source_path)
            if not source.exists():
                logger.error(f"Source path not found: {source_path}")
                return {"success": False, "error": f"Source not found: {source_path}"}

            # Copy new/updated scripts
            import shutil
            stats = {"copied": 0, "updated": 0, "skipped": 0}

            for script_file in source.rglob("*.pine"):
                relative_path = script_file.relative_to(source)
                dest_file = self.pine_scripts_dir / relative_path

                dest_file.parent.mkdir(parents=True, exist_ok=True)

                if dest_file.exists():
                    # Check if source is newer
                    if script_file.stat().st_mtime > dest_file.stat().st_mtime:
                        shutil.copy2(script_file, dest_file)
                        stats["updated"] += 1
                    else:
                        stats["skipped"] += 1
                else:
                    shutil.copy2(script_file, dest_file)
                    stats["copied"] += 1

            self._log_sync(stats)
            logger.info(f"Sync complete: {stats}")
            return {"success": True, "stats": stats}

        except Exception as e:
            logger.error(f"Sync failed: {e}")
            return {"success": False, "error": str(e)}

    def _log_sync(self, stats: Dict[str, int]):
        """Log sync operation"""
        with open(self.sync_log, 'a') as f:
            f.write(json.dumps({
                "timestamp": datetime.now().isoformat(),
                "action": "pine_sync",
                "stats": stats
            }) + "\n")

    async def auto_sync_interval(self, interval_seconds: int = 3600):
        """Periodically sync Pine Scripts"""
        external_source = Path("C:/Users/rhuam/Documents/GitHub/Pines")
        
        while True:
            try:
                result = self.sync_from_external(str(external_source))
                if result["success"]:
                    logger.info("Auto-sync completed successfully")
                else:
                    logger.warning(f"Auto-sync failed: {result.get('error')}")
            except Exception as e:
                logger.error(f"Auto-sync error: {e}")

            await asyncio.sleep(interval_seconds)
