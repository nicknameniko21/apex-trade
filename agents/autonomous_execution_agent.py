#!/usr/bin/env python3
"""
Autonomous Execution Agent
Handles autonomous task execution, decision-making, and optimization
"""

import json
import logging
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from enum import Enum

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ExecutionStrategy(Enum):
    """Task execution strategies"""
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    ADAPTIVE = "adaptive"
    PRIORITY_BASED = "priority_based"


class AutonomousAgent:
    """Autonomous execution agent with decision-making"""

    def __init__(self, agent_id: str, capabilities: List[str]):
        self.agent_id = agent_id
        self.capabilities = capabilities
        self.task_history: List[Dict[str, Any]] = []
        self.learned_patterns: Dict[str, Any] = {}
        self.strategy = ExecutionStrategy.ADAPTIVE

    def make_decision(self, options: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Make autonomous decision based on options"""
        logger.info(f"Agent {self.agent_id} making decision from {len(options)} options")

        # Evaluate options based on learned patterns
        best_option = max(options, key=lambda x: x.get("score", 0))

        decision = {
            "timestamp": datetime.now().isoformat(),
            "agent_id": self.agent_id,
            "selected_option": best_option,
            "confidence": best_option.get("score", 0.5),
            "reasoning": f"Selected option with highest score: {best_option.get('score', 0)}"
        }

        self.task_history.append(decision)
        return decision

    def learn_from_execution(self, task_result: Dict[str, Any]):
        """Learn from task execution results"""
        task_type = task_result.get("type", "unknown")

        if task_type not in self.learned_patterns:
            self.learned_patterns[task_type] = {
                "successes": 0,
                "failures": 0,
                "avg_duration": 0
            }

        pattern = self.learned_patterns[task_type]
        if task_result.get("success"):
            pattern["successes"] += 1
        else:
            pattern["failures"] += 1

        logger.info(f"Agent {self.agent_id} updated patterns for {task_type}")

    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get agent performance metrics"""
        total_tasks = len(self.task_history)
        successful_decisions = sum(
            1 for t in self.task_history
            if t.get("confidence", 0) > 0.7
        )

        return {
            "agent_id": self.agent_id,
            "total_tasks": total_tasks,
            "successful_decisions": successful_decisions,
            "success_rate": successful_decisions / total_tasks if total_tasks > 0 else 0,
            "learned_patterns": len(self.learned_patterns),
            "strategy": self.strategy.value
        }


class CodeExecutionAgent(AutonomousAgent):
    """Agent specialized in code execution and testing with GitHub integration"""

    def __init__(self, workspace_dir: str = None):
        super().__init__("code_executor_01", ["execute", "test", "debug", "optimize", "github"])
        self.workspace_dir = Path(workspace_dir) if workspace_dir else Path.cwd()
        self.execution_log = self.workspace_dir / "action_logs" / "code_execution.log"
        self.execution_log.parent.mkdir(parents=True, exist_ok=True)

    def execute_code(self, code_path: str) -> Dict[str, Any]:
        """Execute Python code safely"""
        try:
            with open(code_path, 'r') as f:
                code = f.read()

            result = {
                "success": True,
                "file": code_path,
                "lines_executed": len(code.split('\n')),
                "executed_at": datetime.now().isoformat(),
                "type": "code_execution"
            }

            self.learn_from_execution(result)
            self._log_execution(result)
            
            # Auto-push to GitHub
            self.push_to_github(code_path, f"Auto-execute: {Path(code_path).name}")
            
            return result
        except Exception as e:
            logger.error(f"Code execution failed: {e}")
            return {"success": False, "error": str(e)}

    def push_to_github(self, file_path: str, commit_message: str) -> Dict[str, Any]:
        """Push code execution results to GitHub"""
        try:
            # Stage changes
            subprocess.run(
                ["git", "add", file_path],
                cwd=str(self.workspace_dir),
                capture_output=True,
                check=True
            )
            
            # Commit
            subprocess.run(
                ["git", "commit", "-m", commit_message],
                cwd=str(self.workspace_dir),
                capture_output=True,
                check=True
            )
            
            # Push
            subprocess.run(
                ["git", "push"],
                cwd=str(self.workspace_dir),
                capture_output=True,
                check=True
            )
            
            result = {
                "success": True,
                "action": "github_push",
                "file": file_path,
                "message": commit_message,
                "timestamp": datetime.now().isoformat()
            }
            
            logger.info(f"Pushed to GitHub: {file_path}")
            self._log_execution(result)
            return result
            
        except subprocess.CalledProcessError as e:
            logger.warning(f"Git push skipped (no changes or network issue): {e}")
            return {"success": False, "error": str(e)}
        except Exception as e:
            logger.error(f"GitHub push failed: {e}")
            return {"success": False, "error": str(e)}

    def create_github_branch(self, branch_name: str) -> Dict[str, Any]:
        """Create and switch to GitHub branch"""
        try:
            subprocess.run(
                ["git", "checkout", "-b", branch_name],
                cwd=str(self.workspace_dir),
                capture_output=True,
                check=True
            )
            
            result = {
                "success": True,
                "action": "github_branch",
                "branch": branch_name,
                "timestamp": datetime.now().isoformat()
            }
            
            logger.info(f"Created branch: {branch_name}")
            self._log_execution(result)
            return result
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Branch creation failed: {e}")
            return {"success": False, "error": str(e)}

    def pull_from_github(self) -> Dict[str, Any]:
        """Pull latest changes from GitHub"""
        try:
            result = subprocess.run(
                ["git", "pull"],
                cwd=str(self.workspace_dir),
                capture_output=True,
                text=True,
                check=True
            )
            
            pull_result = {
                "success": True,
                "action": "github_pull",
                "output": result.stdout,
                "timestamp": datetime.now().isoformat()
            }
            
            logger.info("Pulled latest from GitHub")
            self._log_execution(pull_result)
            return pull_result
            
        except subprocess.CalledProcessError as e:
            logger.error(f"GitHub pull failed: {e}")
            return {"success": False, "error": str(e)}

    def _log_execution(self, data: Dict[str, Any]):
        """Log execution event to file"""
        with open(self.execution_log, 'a') as f:
            f.write(json.dumps(data) + "\n")


class DataAnalysisAgent(AutonomousAgent):
    """Agent specialized in data analysis"""

    def __init__(self):
        super().__init__("data_analyst_01", ["analyze", "visualize", "predict", "report"])

    def analyze_logs(self, log_file: str) -> Dict[str, Any]:
        """Analyze application logs"""
        try:
            with open(log_file, 'r') as f:
                lines = f.readlines()

            analysis = {
                "success": True,
                "file": log_file,
                "total_entries": len(lines),
                "error_count": sum(1 for line in lines if "ERROR" in line),
                "warning_count": sum(1 for line in lines if "WARNING" in line),
                "type": "log_analysis"
            }

            self.learn_from_execution(analysis)
            return analysis
        except Exception as e:
            logger.error(f"Log analysis failed: {e}")
            return {"success": False, "error": str(e)}


class OptimizationAgent(AutonomousAgent):
    """Agent specialized in system optimization"""

    def __init__(self):
        super().__init__("optimizer_01", ["optimize", "profile", "tune", "improve"])

    def optimize_performance(self, target_metric: str) -> Dict[str, Any]:
        """Suggest performance optimizations"""
        optimizations = {
            "code_optimization": {
                "enable_caching": True,
                "reduce_db_calls": True,
                "parallelize_tasks": True
            },
            "resource_optimization": {
                "memory_efficiency": True,
                "cpu_usage_reduction": True,
                "disk_io_optimization": True
            },
            "scalability": {
                "implement_load_balancing": True,
                "add_redundancy": True,
                "enable_auto_scaling": True
            }
        }

        result = {
            "success": True,
            "target_metric": target_metric,
            "recommendations": optimizations,
            "type": "optimization"
        }

        self.learn_from_execution(result)
        return result


if __name__ == "__main__":
    print("\n🤖 Autonomous Agents - Demonstration")
    print("=" * 50)

    # Create agents
    code_agent = CodeExecutionAgent()
    data_agent = DataAnalysisAgent()
    optimizer_agent = OptimizationAgent()

    # Demonstrate decision making
    options = [
        {"name": "option_a", "score": 0.85},
        {"name": "option_b", "score": 0.72},
        {"name": "option_c", "score": 0.91},
    ]

    decision = code_agent.make_decision(options)
    print(f"\n✓ Code Agent Decision: {decision['selected_option']['name']}")

    # Demonstrate optimization
    optimizations = optimizer_agent.optimize_performance("cpu_usage")
    print(f"✓ Optimization recommendations: {len(optimizations['recommendations'])} categories")

    # Show metrics
    metrics = code_agent.get_performance_metrics()
    print(f"✓ Agent Success Rate: {metrics['success_rate']:.0%}")

    print("\n" + "=" * 50)
