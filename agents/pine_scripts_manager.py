#!/usr/bin/env python3
"""
Pine Scripts Manager
Handles loading, caching, and managing Pine Script strategies
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class PineScript:
    """Pine Script metadata and content"""
    name: str
    path: str
    version: str
    status: str = "active"  # active, broken, deprecated
    last_updated: str = None
    content: Optional[str] = None

    def __post_init__(self):
        if self.last_updated is None:
            self.last_updated = datetime.now().isoformat()


class PineScriptsManager:
    """Manages Pine Script loading and integration"""

    def __init__(self, workspace_dir: str = None):
        self.workspace_dir = Path(workspace_dir) if workspace_dir else Path.cwd()
        self.pine_scripts_dir = self.workspace_dir / "pine_scripts"
        self.cache_file = self.workspace_dir / "action_logs" / "pine_scripts_cache.json"
        self.scripts: Dict[str, PineScript] = {}
        self.cache_file.parent.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Pine Scripts Manager initialized at {self.pine_scripts_dir}")

    def discover_scripts(self) -> List[PineScript]:
        """Discover all Pine Script files in repository"""
        if not self.pine_scripts_dir.exists():
            logger.warning(f"Pine scripts directory not found: {self.pine_scripts_dir}")
            return []

        scripts = []
        for script_file in self.pine_scripts_dir.rglob("*.pine"):
            try:
                with open(script_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    script = PineScript(
                        name=script_file.stem,
                        path=str(script_file),
                        version=self._extract_version(content),
                        content=content
                    )
                    scripts.append(script)
                    self.scripts[script_file.stem] = script
                    logger.info(f"Discovered script: {script.name}")
            except Exception as e:
                logger.error(f"Error reading {script_file}: {e}")

        return scripts

    def validate_script(self, script: PineScript) -> Dict[str, Any]:
        """Validate Pine Script syntax and structure"""
        issues = []
        
        # Check for required Pine Script components
        if not script.content:
            issues.append("Empty script content")
            return {"valid": False, "issues": issues}

        if "@version" not in script.content:
            issues.append("Missing @version directive")
        
        if "strategy(" not in script.content and "study(" not in script.content:
            issues.append("Must define strategy() or study()")

        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "script": script.name
        }

    def fix_broken_script(self, script_name: str) -> bool:
        """Attempt to fix broken scripts"""
        if script_name not in self.scripts:
            logger.warning(f"Script not found: {script_name}")
            return False

        script = self.scripts[script_name]
        content = script.content
        fixes_applied = []

        # Fix 1: Add missing @version if needed
        if "@version" not in content:
            content = '@version = 5\n' + content
            fixes_applied.append("Added @version directive")

        # Fix 2: Fix common Pine Script v5 compatibility issues
        content = content.replace("study(", "indicator(")
        if "indicator(" in content and "study(" not in content:
            fixes_applied.append("Updated study() to indicator()")

        # Fix 3: Fix line continuation issues (operators at end of line)
        import re
        original_content = content
        
        # Find lines ending with 'or' or 'and' followed by newline and indented content
        # Pattern: ) or\n -> or\n)
        content = re.sub(r'\)\s+or\n', '\nor\n', content)
        content = re.sub(r'\)\s+and\n', '\nand\n', content)
        
        # Alternative: move operator to beginning of next line with proper indentation
        lines = content.split('\n')
        fixed_lines = []
        i = 0
        while i < len(lines):
            line = lines[i]
            if i < len(lines) - 1 and (line.rstrip().endswith(' or') or line.rstrip().endswith(' and')):
                # Line ends with operator - remove it and add to next line
                operator = 'or' if line.rstrip().endswith(' or') else 'and'
                line_without_op = line.rstrip()[:-len(operator)-1]
                fixed_lines.append(line_without_op)
                next_line = lines[i + 1]
                next_indent = len(next_line) - len(next_line.lstrip())
                fixed_lines.append(' ' * next_indent + operator + ' ' + next_line.lstrip())
                i += 2
            else:
                fixed_lines.append(line)
                i += 1
        
        new_content = '\n'.join(fixed_lines)
        if new_content != original_content:
            content = new_content
            fixes_applied.append("Fixed line continuation (operators at EOL)")

        # Save fixed script
        if fixes_applied:
            script.content = content
            script.status = "fixed"
            logger.info(f"Fixed {script_name}: {', '.join(fixes_applied)}")
            return True

        return False

    def cache_scripts(self):
        """Cache script metadata to disk"""
        cache_data = {
            "timestamp": datetime.now().isoformat(),
            "scripts": {name: asdict(script) for name, script in self.scripts.items()}
        }
        with open(self.cache_file, 'w') as f:
            json.dump(cache_data, f, indent=2)
        logger.info(f"Cached {len(self.scripts)} scripts")

    def _extract_version(self, content: str) -> str:
        """Extract Pine Script version from content"""
        import re
        match = re.search(r'@version\s*=\s*(\d+)', content)
        return match.group(1) if match else "unknown"

    def get_all_scripts(self) -> List[PineScript]:
        """Return all cached scripts"""
        return list(self.scripts.values())

    def get_script(self, name: str) -> Optional[PineScript]:
        """Get specific script by name"""
        return self.scripts.get(name)
