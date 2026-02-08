#!/usr/bin/env python3
"""
Task Generator for Swarm Learning
Automatically creates and executes tasks to drive autonomous learning
"""

import asyncio
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AutonomousTaskGenerator:
    """Generates tasks to drive swarm learning and evolution"""

    def __init__(self, swarm, workspace_dir: str = None):
        self.swarm = swarm
        self.workspace_dir = Path(workspace_dir) if workspace_dir else Path.cwd()
        self.task_log = self.workspace_dir / "action_logs" / "autonomous_tasks.log"
        self.task_log.parent.mkdir(parents=True, exist_ok=True)
        self.generated_tasks = []

    def generate_learning_tasks(self) -> List[str]:
        """Generate tasks to trigger agent learning"""
        tasks = [
            {
                "id": "learn_analyze_code",
                "desc": "analyze codebase for patterns and improvements",
                "type": "analysis",
                "priority": 1
            },
            {
                "id": "learn_generate_docs",
                "desc": "generate documentation from code comments",
                "type": "documentation",
                "priority": 2
            },
            {
                "id": "learn_optimize_performance",
                "desc": "identify and suggest performance optimizations",
                "type": "optimization",
                "priority": 1
            },
            {
                "id": "learn_test_coverage",
                "desc": "analyze test coverage and suggest improvements",
                "type": "testing",
                "priority": 2
            },
            {
                "id": "learn_refactor_code",
                "desc": "suggest code refactoring for maintainability",
                "type": "refactoring",
                "priority": 3
            },
            {
                "id": "learn_security_audit",
                "desc": "audit code for potential security issues",
                "type": "security",
                "priority": 1
            },
            {
                "id": "learn_fix_errors",
                "desc": "find and fix code syntax errors in pine scripts",
                "type": "error_fixing",
                "priority": 1
            },
            {
                "id": "learn_architecture_review",
                "desc": "review system architecture for improvements",
                "type": "architecture",
                "priority": 2
            },
            {
                "id": "learn_integration_testing",
                "desc": "test integration between system components",
                "type": "integration",
                "priority": 2
            },
            {
                "id": "learn_dependency_analysis",
                "desc": "analyze dependencies and suggest updates",
                "type": "dependencies",
                "priority": 3
            }
        ]

        created_ids = []
        for task_spec in tasks:
            try:
                task = self.swarm.create_task(
                    task_id=task_spec["id"],
                    description=task_spec["desc"],
                    priority=task_spec["priority"]
                )
                created_ids.append(task.task_id)
                self.generated_tasks.append(task_spec)
                logger.info(f"Created learning task: {task_spec['id']}")
            except Exception as e:
                logger.error(f"Failed to create task {task_spec['id']}: {e}")

        return created_ids

    def execute_all_tasks(self) -> Dict[str, Any]:
        """Execute all created tasks and collect results"""
        results = {
            "timestamp": datetime.now().isoformat(),
            "total_tasks": len(self.swarm.tasks),
            "executed": [],
            "failed": []
        }

        for task_id, task in self.swarm.tasks.items():
            if task.status in ["pending", "assigned"]:
                try:
                    # Assign to first available agent
                    if not task.assigned_to and self.swarm.agents:
                        agent_id = list(self.swarm.agents.keys())[0]
                        self.swarm.assign_task(task_id, agent_id)

                    # Execute task
                    result = self.swarm.execute_task(task_id)
                    if result.get("success"):
                        results["executed"].append({
                            "task_id": task_id,
                            "agent": result.get("agent_name"),
                            "timestamp": result.get("executed_at")
                        })
                        logger.info(f"Executed task: {task_id}")
                    else:
                        results["failed"].append(task_id)
                except Exception as e:
                    logger.error(f"Task execution failed {task_id}: {e}")
                    results["failed"].append(task_id)

        self._log_execution(results)
        return results

    def get_agent_learning_status(self) -> Dict[str, Any]:
        """Get learning progress across all agents"""
        status = {
            "timestamp": datetime.now().isoformat(),
            "agents": {}
        }

        # Note: Agents are stored in autonomous_agents dict, not swarm.agents
        # This gets the metrics from swarm agents
        for agent_id, agent in self.swarm.agents.items():
            status["agents"][agent_id] = {
                "name": agent.name,
                "role": agent.role.value,
                "tasks_completed": agent.tasks_completed,
                "status": agent.status
            }

        return status

    def generate_adaptive_tasks(self) -> List[str]:
        """Generate tasks based on current learning patterns"""
        adaptive_tasks = []

        # Check which task types have low success rates
        # and create more focused tasks for learning

        for agent_id, agent in self.swarm.agents.items():
            if hasattr(agent, 'learned_patterns'):
                for task_type, pattern in agent.learned_patterns.items():
                    success_rate = pattern.get('successes', 0) / (
                        pattern.get('successes', 0) + pattern.get('failures', 1)
                    )

                    # If success rate is low, create more tasks to improve
                    if success_rate < 0.7:
                        adaptive_task = {
                            "id": f"adaptive_{task_type}_{len(adaptive_tasks)}",
                            "desc": f"Practice and improve {task_type} capability",
                            "type": task_type,
                            "priority": 1,
                            "reason": f"Low success rate: {success_rate:.1%}"
                        }

                        try:
                            task = self.swarm.create_task(
                                adaptive_task["id"],
                                adaptive_task["desc"],
                                adaptive_task["priority"]
                            )
                            adaptive_tasks.append(task.task_id)
                            logger.info(f"Created adaptive task: {adaptive_task['id']}")
                        except Exception as e:
                            logger.error(f"Failed to create adaptive task: {e}")

        return adaptive_tasks

    def detect_code_issues(self) -> List[Dict[str, Any]]:
        """Scan codebase for issues and create learning tasks"""
        issues = []
        
        try:
            # Check Pine Scripts for syntax errors
            pine_dir = self.workspace_dir / "pine_scripts"
            if pine_dir.exists():
                for pine_file in pine_dir.glob("*.pine"):
                    try:
                        content = pine_file.read_text()
                        # Look for common issues
                        if "end of line without line continuation" in content or \
                           content.count("or") > content.count(" or ") or \
                           content.count("and") > content.count(" and "):
                            issues.append({
                                "file": str(pine_file.name),
                                "type": "syntax_error",
                                "priority": 1
                            })
                    except Exception as e:
                        logger.warning(f"Error checking {pine_file}: {e}")
            
            # Create learning tasks for each issue found
            for issue in issues:
                task_id = f"fix_{issue['type']}_{issue['file'].replace('.', '_')}"
                try:
                    task = self.swarm.create_task(
                        task_id=task_id,
                        description=f"Fix {issue['type']} in {issue['file']}",
                        priority=issue['priority']
                    )
                    logger.info(f"Created error-fixing task: {task_id}")
                except Exception as e:
                    logger.error(f"Failed to create fix task: {e}")
        
        except Exception as e:
            logger.warning(f"Error during code issue detection: {e}")
        
        return issues

    def learn_from_failures(self) -> Dict[str, Any]:
        """Analyze failed tasks and create targeted learning tasks"""
        learning_focus = {
            "timestamp": datetime.now().isoformat(),
            "created_tasks": []
        }

        try:
            # Look for agents with low success rates
            for agent_id, agent in self.swarm.agents.items():
                if hasattr(agent, 'learned_patterns'):
                    for task_type, pattern in agent.learned_patterns.items():
                        total = pattern.get('successes', 0) + pattern.get('failures', 0)
                        if total > 0:
                            success_rate = pattern['successes'] / total
                            if success_rate < 0.7:  # Less than 70% success
                                # Create focused learning task
                                task_id = f"practice_{task_type}_{agent_id}"
                                try:
                                    task = self.swarm.create_task(
                                        task_id=task_id,
                                        description=f"Practice {task_type} (success rate: {success_rate:.1%})",
                                        priority=1
                                    )
                                    learning_focus["created_tasks"].append(task_id)
                                    logger.info(f"Created practice task for {agent_id}: {task_type}")
                                except Exception as e:
                                    logger.error(f"Failed to create practice task: {e}")
        
        except Exception as e:
            logger.warning(f"Error analyzing failures: {e}")
        
        return learning_focus

    async def continuous_learning_loop(self, interval_seconds: int = 60):
        """Run continuous learning loop"""
        logger.info(f"Starting autonomous learning loop (interval: {interval_seconds}s)")

        while True:
            try:
                # 1. Detect code issues and create fix tasks
                issues = self.detect_code_issues()
                if issues:
                    logger.info(f"Detected {len(issues)} code issues to fix")
                
                # 2. Generate standard learning tasks
                task_ids = self.generate_learning_tasks()
                logger.info(f"Generated {len(task_ids)} learning tasks")

                # 3. Execute all tasks
                results = self.execute_all_tasks()
                logger.info(f"Executed {len(results['executed'])} tasks, {len(results['failed'])} failed")

                # 4. Analyze failures and create practice tasks
                focus = self.learn_from_failures()
                if focus["created_tasks"]:
                    logger.info(f"Created {len(focus['created_tasks'])} focused learning tasks")

                # 5. Generate adaptive tasks based on learning
                adaptive_ids = self.generate_adaptive_tasks()
                if adaptive_ids:
                    logger.info(f"Generated {len(adaptive_ids)} adaptive tasks")

                # Get current learning status
                status = self.get_agent_learning_status()
                logger.info(f"Learning status: {len(status['agents'])} agents active")

                # Wait before next cycle
                await asyncio.sleep(interval_seconds)

            except Exception as e:
                logger.error(f"Learning loop error: {e}")
                await asyncio.sleep(10)  # Short wait on error

    def _log_execution(self, data: Dict[str, Any]):
        """Log task execution"""
        with open(self.task_log, 'a') as f:
            f.write(json.dumps(data) + "\n")
