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

    async def continuous_learning_loop(self, interval_seconds: int = 60):
        """Run continuous learning loop"""
        logger.info(f"Starting autonomous learning loop (interval: {interval_seconds}s)")

        while True:
            try:
                # Generate and execute learning tasks
                task_ids = self.generate_learning_tasks()
                logger.info(f"Generated {len(task_ids)} learning tasks")

                results = self.execute_all_tasks()
                logger.info(f"Executed {len(results['executed'])} tasks")

                # Generate adaptive tasks based on learning
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
