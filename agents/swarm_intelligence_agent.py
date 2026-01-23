#!/usr/bin/env python3
"""
Swarm Intelligence Agent
Core multi-agent coordination system for autonomous task execution
"""

import json
import logging
import asyncio
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Callable
from dataclasses import dataclass, asdict, field
from enum import Enum

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AgentRole(Enum):
    """Agent role classification"""
    COORDINATOR = "coordinator"
    ANALYZER = "analyzer"
    EXECUTOR = "executor"
    MONITOR = "monitor"
    COMMUNICATOR = "communicator"


@dataclass
class Task:
    """Task definition for agent execution"""
    task_id: str
    description: str
    priority: int
    assigned_to: Optional[str] = None
    status: str = "pending"
    created_at: str = None
    completed_at: Optional[str] = None
    result: Optional[Dict[str, Any]] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()


@dataclass
class Agent:
    """Agent definition"""
    agent_id: str
    name: str
    role: AgentRole
    capabilities: List[str]
    status: str = "idle"
    tasks_completed: int = 0
    created_at: str = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()


@dataclass
class ModelProfile:
    """LLM model profile for routing and coordination"""
    model_id: str
    name: str
    provider: str
    strengths: List[str]
    status: str = "available"
    endpoint: Optional[str] = None
    created_at: str = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()


@dataclass
class WorkflowStep:
    """Workflow step definition"""
    step_id: str
    description: str
    priority: int = 5
    assigned_to: Optional[str] = None
    status: str = "pending"
    result: Optional[Dict[str, Any]] = None


@dataclass
class Workflow:
    """Workflow definition for multi-step execution"""
    workflow_id: str
    name: str
    description: str
    steps: List[WorkflowStep] = field(default_factory=list)
    status: str = "pending"
    created_at: str = None
    executed_at: Optional[str] = None
    results: List[Dict[str, Any]] = field(default_factory=list)

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()


class SwarmIntelligenceAgent:
    """Central swarm coordination system"""

    def __init__(self, workspace_dir: str = None):
        self.workspace_dir = Path(workspace_dir) if workspace_dir else Path.cwd()
        self.agents: Dict[str, Agent] = {}
        self.tasks: Dict[str, Task] = {}
        self.task_queue: asyncio.Queue = asyncio.Queue()
        self.workflows: Dict[str, Workflow] = {}
        self.models: Dict[str, ModelProfile] = {}
        self.execution_log = self.workspace_dir / "action_logs" / "swarm_execution.log"
        self.execution_log.parent.mkdir(parents=True, exist_ok=True)

        logger.info(f"Swarm Intelligence Agent initialized at {self.workspace_dir}")
        self._register_default_models()

    def register_agent(self, agent_id: str, name: str, role: AgentRole,
                      capabilities: List[str]) -> Agent:
        """Register a new agent in the swarm"""
        agent = Agent(
            agent_id=agent_id,
            name=name,
            role=role,
            capabilities=capabilities
        )
        self.agents[agent_id] = agent
        logger.info(f"Agent registered: {name} ({role.value})")
        agent_dict = asdict(agent)
        agent_dict['role'] = role.value
        self._log_action("agent_registered", {"agent": agent_dict})
        return agent

    def create_task(self, task_id: str, description: str, priority: int = 1) -> Task:
        """Create a new task"""
        task = Task(
            task_id=task_id,
            description=description,
            priority=priority
        )
        self.tasks[task_id] = task
        logger.info(f"Task created: {task_id} (Priority: {priority})")
        self._log_action("task_created", {"task": asdict(task)})
        return task

    def assign_task(self, task_id: str, agent_id: str) -> bool:
        """Assign a task to an agent"""
        if task_id not in self.tasks or agent_id not in self.agents:
            logger.error(f"Invalid task or agent: {task_id}, {agent_id}")
            return False

        task = self.tasks[task_id]
        agent = self.agents[agent_id]

        # Check if agent has required capabilities
        task_keywords = set(task.description.lower().split())
        agent_capabilities = {cap.lower() for cap in agent.capabilities}
        match_score = len(task_keywords & agent_capabilities)
        if match_score == 0:
            logger.warning(f"Agent {agent.name} may not match task keywords: {task.description}")

        task.assigned_to = agent_id
        task.status = "assigned"

        logger.info(f"Task {task_id} assigned to {agent.name}")
        self._log_action("task_assigned", {
            "task_id": task_id,
            "agent_id": agent_id,
            "agent_name": agent.name
        })
        return True

    def execute_task(self, task_id: str) -> Dict[str, Any]:
        """Execute an assigned task"""
        if task_id not in self.tasks:
            logger.error(f"Task not found: {task_id}")
            return {"success": False, "error": "Task not found"}

        task = self.tasks[task_id]
        if not task.assigned_to:
            logger.error(f"Task not assigned: {task_id}")
            return {"success": False, "error": "Task not assigned"}

        agent = self.agents[task.assigned_to]
        task.status = "executing"

        logger.info(f"Executing task {task_id} with {agent.name}")

        # Simulate task execution
        result = {
            "success": True,
            "task_id": task_id,
            "agent_id": agent.agent_id,
            "agent_name": agent.name,
            "executed_at": datetime.now().isoformat(),
            "description": task.description
        }

        task.status = "completed"
        task.completed_at = datetime.now().isoformat()
        task.result = result
        agent.tasks_completed += 1

        self._log_action("task_executed", result)
        return result

    def get_swarm_status(self) -> Dict[str, Any]:
        """Get overall swarm status"""
        total_agents = len(self.agents)
        active_agents = sum(1 for a in self.agents.values() if a.status == "active")
        total_tasks = len(self.tasks)
        completed_tasks = sum(1 for t in self.tasks.values() if t.status == "completed")
        total_workflows = len(self.workflows)
        completed_workflows = sum(
            1 for w in self.workflows.values() if w.status == "completed"
        )

        status = {
            "timestamp": datetime.now().isoformat(),
            "total_agents": total_agents,
            "active_agents": active_agents,
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "completion_rate": completed_tasks / total_tasks if total_tasks > 0 else 0,
            "total_workflows": total_workflows,
            "completed_workflows": completed_workflows,
            "models_available": len(self.models),
            "agents": [
                {
                    "id": a.agent_id,
                    "name": a.name,
                    "role": a.role.value,
                    "status": a.status,
                    "tasks_completed": a.tasks_completed
                }
                for a in self.agents.values()
            ]
        }

        logger.info(f"Swarm Status: {completed_tasks}/{total_tasks} tasks completed")
        return status

    def register_model(self, model_id: str, name: str, provider: str,
                       strengths: List[str], endpoint: Optional[str] = None,
                       status: str = "available") -> ModelProfile:
        """Register a new model for routing"""
        model = ModelProfile(
            model_id=model_id,
            name=name,
            provider=provider,
            strengths=strengths,
            endpoint=endpoint,
            status=status
        )
        self.models[model_id] = model
        self._log_action("model_registered", {"model": asdict(model)})
        return model

    def list_models(self) -> List[Dict[str, Any]]:
        """List registered models"""
        return [asdict(model) for model in self.models.values()]

    def route_model(self, query: str) -> Dict[str, Any]:
        """Route query to best-fit model based on strengths"""
        if not self.models:
            return {"success": False, "error": "No models registered"}
        available_models = list(self.models.values())
        query_lower = query.lower()
        best_model = None
        best_score = -1
        matched_strengths = []

        for model in available_models:
            strengths = [strength.lower() for strength in model.strengths]
            score = sum(1 for strength in strengths if strength in query_lower)
            if score > best_score:
                best_score = score
                best_model = model
                matched_strengths = [s for s in strengths if s in query_lower]

        if best_model is None:
            if not available_models:
                return {"success": False, "error": "No models registered"}
            best_model = available_models[0]

        reason = (
            f"Matched strengths: {', '.join(matched_strengths)}"
            if matched_strengths
            else f"No direct match, defaulting to {best_model.name}"
        )

        return {
            "success": True,
            "model": asdict(best_model),
            "score": best_score,
            "reason": reason
        }

    def select_agent_for_task(self, description: str) -> Optional[str]:
        """Select best-fit agent for task description"""
        if not self.agents:
            return None

        keywords = set(re.findall(r"\w+", description.lower()))
        best_agent = None
        best_score = -1

        for agent in self.agents.values():
            capabilities = {cap.lower() for cap in agent.capabilities}
            score = len(keywords & capabilities)
            if score > best_score:
                best_score = score
                best_agent = agent

        if best_score <= 0 and "analyzer_01" in self.agents:
            return "analyzer_01"

        return best_agent.agent_id if best_agent else None

    def create_workflow(self, workflow_id: str, name: str, description: str,
                        steps: List[Any]) -> Workflow:
        """Create a new workflow"""
        workflow_steps = []
        for idx, step in enumerate(steps, start=1):
            if isinstance(step, WorkflowStep):
                workflow_steps.append(step)
            else:
                workflow_steps.append(WorkflowStep(
                    step_id=f"{workflow_id}_step_{idx}",
                    description=step.get("description", ""),
                    priority=step.get("priority", 5),
                    assigned_to=step.get("assigned_to")
                ))

        workflow = Workflow(
            workflow_id=workflow_id,
            name=name,
            description=description,
            steps=workflow_steps
        )
        self.workflows[workflow_id] = workflow
        self._log_action("workflow_created", {"workflow": self._workflow_to_dict(workflow)})
        return workflow

    def list_workflows(self) -> List[Dict[str, Any]]:
        """List workflows"""
        return [self._workflow_to_dict(workflow) for workflow in self.workflows.values()]

    def execute_workflow(self, workflow_id: str) -> Dict[str, Any]:
        """Execute workflow steps sequentially"""
        workflow = self.workflows.get(workflow_id)
        if not workflow:
            return {"success": False, "error": "Workflow not found"}

        workflow.status = "executing"
        workflow.executed_at = datetime.now().isoformat()
        workflow.results = []

        run_suffix = datetime.now().strftime("%H%M%S")
        for idx, step in enumerate(workflow.steps, start=1):
            task_id = f"{workflow.workflow_id}_{idx}_{run_suffix}"
            step.status = "executing"
            task = self.create_task(task_id, step.description, priority=step.priority)

            agent_id = step.assigned_to or self.select_agent_for_task(step.description)
            if not agent_id:
                step.status = "failed"
                step.result = {"success": False, "error": "No agent available"}
                workflow.results.append(step.result)
                continue

            if not self.assign_task(task.task_id, agent_id):
                step.status = "failed"
                step.result = {"success": False, "error": "Task assignment failed"}
                workflow.results.append(step.result)
                continue

            step.assigned_to = agent_id
            result = self.execute_task(task.task_id)
            step.result = result
            step.status = "completed" if result.get("success") else "failed"
            workflow.results.append(result)

        workflow.status = (
            "completed"
            if all(step.status == "completed" for step in workflow.steps)
            else "partial"
        )
        self._log_action("workflow_executed", {"workflow": self._workflow_to_dict(workflow)})

        return {
            "success": workflow.status == "completed",
            "workflow": self._workflow_to_dict(workflow)
        }

    def _workflow_to_dict(self, workflow: Workflow) -> Dict[str, Any]:
        workflow_dict = asdict(workflow)
        workflow_dict["steps"] = [
            {
                **asdict(step),
                "assigned_to": step.assigned_to
            }
            for step in workflow.steps
        ]
        return workflow_dict

    def _register_default_models(self):
        defaults = [
            ModelProfile(
                model_id="gpt_4",
                name="GPT-4",
                provider="OpenAI",
                strengths=["code", "analysis", "reasoning", "planning"]
            ),
            ModelProfile(
                model_id="claude_3_5",
                name="Claude 3.5",
                provider="Anthropic",
                strengths=["writing", "analysis", "summarize", "strategy"]
            ),
            ModelProfile(
                model_id="gemini_1_5",
                name="Gemini 1.5",
                provider="Google",
                strengths=["multimodal", "long-context", "research", "vision"]
            ),
            ModelProfile(
                model_id="perplexity",
                name="Perplexity",
                provider="Perplexity AI",
                strengths=["search", "citations", "research", "browsing"]
            ),
            ModelProfile(
                model_id="minimax",
                name="Minimax",
                provider="Minimax",
                strengths=["planning", "workflow", "coordination", "automation"]
            )
        ]

        for model in defaults:
            self.models[model.model_id] = model

    def get_agent_model_info(self, agent_id: str = None) -> Dict[str, Any]:
        """Get model and version information for agents"""
        if agent_id and agent_id in self.agents:
            agent = self.agents[agent_id]
            return {
                "agent_id": agent.agent_id,
                "name": agent.name,
                "model": "Swarm Intelligence Agent v2.0",
                "role": agent.role.value,
                "capabilities": agent.capabilities,
                "framework": "Python Multi-Agent System",
                "version": "2.0.0",
                "architecture": "Autonomous Task Execution",
                "status": agent.status
            }
        else:
            # Return all agents' model info
            return {
                "system_model": "Swarm Intelligence Engine v2.0",
                "framework": "Multi-Agent Coordination System",
                "version": "2.0.0",
                "total_agents": len(self.agents),
                "agents": [
                    {
                        "agent_id": a.agent_id,
                        "name": a.name,
                        "model": "Swarm Intelligence Agent v2.0",
                        "role": a.role.value,
                        "version": "2.0.0"
                    }
                    for a in self.agents.values()
                ]
            }

    def _log_action(self, action: str, data: Dict[str, Any]):
        """Log swarm action"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "data": data
        }
        with open(self.execution_log, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')


class CodeAnalysisAgent(Agent):
    """Specialized agent for code analysis"""

    def __init__(self):
        super().__init__(
            agent_id="code_analyzer_01",
            name="Code Analyzer",
            role=AgentRole.ANALYZER,
            capabilities=["analyze", "lint", "security_check", "performance_review"]
        )

    def analyze_code(self, file_path: str) -> Dict[str, Any]:
        """Analyze Python code"""
        try:
            with open(file_path, 'r') as f:
                content = f.read()

            analysis = {
                "file": file_path,
                "lines_of_code": len(content.split('\n')),
                "has_docstrings": '"""' in content or "'''" in content,
                "has_type_hints": '->' in content or ': ' in content,
                "issues": []
            }

            if 'TODO' in content:
                analysis["issues"].append("Contains TODO comments")
            if 'FIXME' in content:
                analysis["issues"].append("Contains FIXME comments")
            if 'import *' in content:
                analysis["issues"].append("Uses wildcard imports")

            return analysis
        except Exception as e:
            logger.error(f"Error analyzing {file_path}: {e}")
            return {"error": str(e)}


class TestGenerationAgent(Agent):
    """Specialized agent for test generation"""

    def __init__(self):
        super().__init__(
            agent_id="test_generator_01",
            name="Test Generator",
            role=AgentRole.ANALYZER,
            capabilities=["generate_tests", "unit_testing", "coverage_analysis"]
        )

    def generate_tests(self, function_name: str, file_path: str) -> Dict[str, Any]:
        """Generate test cases for a function"""
        return {
            "function": function_name,
            "file": file_path,
            "tests_generated": 5,
            "test_template": f"""
import pytest
from {Path(file_path).stem} import {function_name}

def test_{function_name}_basic():
    result = {function_name}()
    assert result is not None

def test_{function_name}_error_handling():
    with pytest.raises(Exception):
        {function_name}(None)
"""
        }


class MonitoringAgent(Agent):
    """Specialized agent for system monitoring"""

    def __init__(self):
        super().__init__(
            agent_id="monitor_01",
            name="System Monitor",
            role=AgentRole.MONITOR,
            capabilities=["monitor", "alert", "health_check", "performance_tracking"]
        )

    def check_system_health(self) -> Dict[str, Any]:
        """Check system health"""
        try:
            import psutil
            return {
                "cpu_percent": psutil.cpu_percent(interval=1),
                "memory_percent": psutil.virtual_memory().percent,
                "disk_percent": psutil.disk_usage('/').percent,
                "status": "healthy"
            }
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return {"status": "error", "error": str(e)}


def demonstrate_swarm():
    """Demonstrate swarm intelligence capabilities"""
    print("\n🤖 Swarm Intelligence Agent - Demonstration")
    print("=" * 50)

    swarm = SwarmIntelligenceAgent(
        workspace_dir="c:\\Users\\rhuam\\Documents\\GitHub\\apex-trade"
    )

    # Register agents
    coordinator = swarm.register_agent(
        "coordinator_01", "Coordinator", AgentRole.COORDINATOR,
        ["coordinate", "delegate", "optimize"]
    )
    analyzer = swarm.register_agent(
        "analyzer_01", "Analyzer", AgentRole.ANALYZER,
        ["analyze", "review", "audit"]
    )
    monitor = swarm.register_agent(
        "monitor_01", "Monitor", AgentRole.MONITOR,
        ["monitor", "alert", "health_check"]
    )

    # Create tasks
    task1 = swarm.create_task("task_001", "analyze codebase", priority=1)
    task2 = swarm.create_task("task_002", "generate tests", priority=2)
    task3 = swarm.create_task("task_003", "check system health", priority=1)

    # Assign and execute tasks
    swarm.assign_task("task_001", "analyzer_01")
    swarm.assign_task("task_002", "analyzer_01")
    swarm.assign_task("task_003", "monitor_01")

    result1 = swarm.execute_task("task_001")
    result2 = swarm.execute_task("task_002")
    result3 = swarm.execute_task("task_003")

    # Display swarm status
    status = swarm.get_swarm_status()

    print(f"\n✓ Agents registered: {status['total_agents']}")
    print(f"✓ Tasks completed: {status['completed_tasks']}/{status['total_tasks']}")
    print(f"✓ Completion rate: {status['completion_rate']:.0%}")

    print("\n" + "=" * 50)
    print("Swarm demonstration complete")

    return swarm


if __name__ == "__main__":
    swarm = demonstrate_swarm()
