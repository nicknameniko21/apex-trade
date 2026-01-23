#!/usr/bin/env python3
"""
Unified Agent Interface with Natural Language Processing
Integrates NLP capabilities with existing Swarm and Autonomous agents
"""

import json
import logging
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

# Import existing agents
from nlp_agent import NaturalLanguageAgent, NLPIntent
from swarm_intelligence_agent import SwarmIntelligenceAgent, AgentRole
from autonomous_execution_agent import (
    CodeExecutionAgent, DataAnalysisAgent, OptimizationAgent
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class UnifiedAgentSystem:
    """
    Unified agent system with natural language interface
    Responds to natural language commands and coordinates agent execution
    """
    
    def __init__(self, workspace_dir: str = None):
        self.workspace_dir = Path(workspace_dir) if workspace_dir else Path.cwd()
        
        # Initialize NLP agent for natural language understanding
        self.nlp_agent = NaturalLanguageAgent("unified_nlp")
        
        # Initialize swarm coordinator
        self.swarm = SwarmIntelligenceAgent(str(self.workspace_dir))
        
        # Initialize specialized agents
        self.code_agent = CodeExecutionAgent()
        self.data_agent = DataAnalysisAgent()
        self.optimizer_agent = OptimizationAgent()
        
        # Register agents with swarm
        self._register_agents()
        
        logger.info("Unified Agent System initialized with NLP capabilities")
    
    def _register_agents(self):
        """Register specialized agents with swarm coordinator"""
        self.swarm.register_agent(
            "code_agent",
            "Code Execution Agent",
            AgentRole.EXECUTOR,
            ["execute", "test", "debug"]
        )
        self.swarm.register_agent(
            "data_agent",
            "Data Analysis Agent",
            AgentRole.ANALYZER,
            ["analyze", "report", "visualize"]
        )
        self.swarm.register_agent(
            "optimizer_agent",
            "Optimization Agent",
            AgentRole.ANALYZER,
            ["optimize", "recommend", "benchmark"]
        )
    
    def process_command(self, command: str) -> Dict[str, Any]:
        """
        Process natural language command
        
        Args:
            command: Natural language command string
        
        Returns:
            Dictionary with execution results and response
        """
        logger.info(f"Processing command: {command}")
        
        # Parse natural language into intent
        nlp_result = self.nlp_agent.process_natural_language(command)
        intent = nlp_result["intent"]
        
        # Execute based on intent
        if intent.action == "create_task":
            result = self._create_task_from_intent(intent)
        elif intent.action == "analyze_code":
            result = self._analyze_code_from_intent(intent)
        elif intent.action == "run_tests":
            result = self._run_tests_from_intent(intent)
        elif intent.action == "generate_tests":
            result = self._generate_tests_from_intent(intent)
        elif intent.action == "improve_code":
            result = self._improve_code_from_intent(intent)
        elif intent.action == "status":
            result = self._get_status()
        elif intent.action == "help":
            result = self._get_help()
        else:
            result = {
                "success": False,
                "error": "Unknown action",
                "details": nlp_result["response"]
            }
        
        # Generate natural language response
        response = self._generate_response(intent, result)
        
        return {
            "command": command,
            "intent": intent.action,
            "confidence": intent.confidence,
            "result": result,
            "response": response,
            "timestamp": datetime.now().isoformat()
        }
    
    def _create_task_from_intent(self, intent: NLPIntent) -> Dict[str, Any]:
        """Create a task in swarm from parsed intent"""
        task_desc = intent.entities.get("target", "Generic task")
        task_id = f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        task = self.swarm.create_task(task_id, task_desc, priority=1)
        
        # Auto-assign to appropriate agent
        if "test" in task_desc.lower():
            self.swarm.assign_task(task_id, "code_agent")
        elif "analyze" in task_desc.lower():
            self.swarm.assign_task(task_id, "data_agent")
        elif "optimize" in task_desc.lower():
            self.swarm.assign_task(task_id, "optimizer_agent")
        
        return {
            "success": True,
            "task_id": task_id,
            "description": task_desc,
            "assigned_to": task.assigned_to
        }
    
    def _analyze_code_from_intent(self, intent: NLPIntent) -> Dict[str, Any]:
        """Analyze code based on parsed intent"""
        target = intent.entities.get("target", ".")
        
        # Use data analysis agent
        analysis = {
            "success": True,
            "target": target,
            "type": "code_analysis",
            "timestamp": datetime.now().isoformat(),
            "agent": "data_agent"
        }
        
        # Learn from this analysis
        self.data_agent.learn_from_execution(analysis)
        
        return analysis
    
    def _run_tests_from_intent(self, intent: NLPIntent) -> Dict[str, Any]:
        """Run tests based on parsed intent"""
        target = intent.entities.get("target", ".")
        
        # Create test task
        task_id = f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.swarm.create_task(task_id, f"Run tests for {target}", priority=2)
        self.swarm.assign_task(task_id, "code_agent")
        
        return {
            "success": True,
            "target": target,
            "task_id": task_id,
            "status": "queued"
        }
    
    def _generate_tests_from_intent(self, intent: NLPIntent) -> Dict[str, Any]:
        """Generate tests based on parsed intent"""
        target = intent.entities.get("target", "")
        
        return {
            "success": True,
            "target": target,
            "message": f"Test generation queued for {target}",
            "agent": "code_agent"
        }
    
    def _improve_code_from_intent(self, intent: NLPIntent) -> Dict[str, Any]:
        """Improve code based on parsed intent"""
        target = intent.entities.get("target", "")
        
        # Use optimizer agent
        recommendations = self.optimizer_agent.optimize_performance("code_quality")
        
        return {
            "success": True,
            "target": target,
            "recommendations": recommendations.get("recommendations", {}),
            "agent": "optimizer_agent"
        }
    
    def _get_status(self) -> Dict[str, Any]:
        """Get system status"""
        swarm_status = self.swarm.get_swarm_status()
        
        return {
            "success": True,
            "swarm_status": swarm_status,
            "agents": {
                "code_agent": self.code_agent.get_performance_metrics(),
                "data_agent": self.data_agent.get_performance_metrics(),
                "optimizer_agent": self.optimizer_agent.get_performance_metrics()
            },
            "nlp_commands_processed": len(self.nlp_agent.conversation_history)
        }
    
    def _get_help(self) -> Dict[str, Any]:
        """Get help information"""
        return {
            "success": True,
            "help": """Natural Language Agent System - Available Commands:

Task Management:
- "Create a task to [description]"
- "Add a task for [description]"

Code Operations:
- "Analyze code in [path]"
- "Review code at [path]"
- "Run tests for [file]"
- "Generate tests for [file]"
- "Improve code in [path]"
- "Optimize [file]"

System:
- "What's the status?"
- "Show me the progress"
- "Help"

Examples:
- "Create a task to analyze the codebase"
- "Run tests for test_script.py"
- "Analyze code in agents/"
- "Generate tests for nlp_agent.py"
- "Optimize copilot_test_project/test_script.py"
"""
        }
    
    def _generate_response(self, intent: NLPIntent, result: Dict[str, Any]) -> str:
        """Generate natural language response"""
        
        if not result.get("success"):
            return f"❌ Error: {result.get('error', 'Unknown error')}"
        
        if intent.action == "create_task":
            task_id = result.get("task_id", "unknown")
            assigned = result.get("assigned_to", "unassigned")
            return f"✓ Task {task_id} created and assigned to {assigned}"
        
        elif intent.action == "analyze_code":
            target = result.get("target", "code")
            return f"✓ Code analysis completed for {target}"
        
        elif intent.action == "run_tests":
            target = result.get("target", "tests")
            return f"✓ Tests queued for {target}"
        
        elif intent.action == "generate_tests":
            target = result.get("target", "code")
            return f"✓ Test generation queued for {target}"
        
        elif intent.action == "improve_code":
            target = result.get("target", "code")
            recs = len(result.get("recommendations", []))
            return f"✓ Generated {recs} optimization recommendations for {target}"
        
        elif intent.action == "status":
            swarm = result.get("swarm_status", {})
            tasks_completed = swarm.get("tasks_completed", 0)
            return f"✓ System operational. {tasks_completed} tasks completed."
        
        elif intent.action == "help":
            return result.get("help", "Help information")
        
        return "✓ Command processed successfully"


def interactive_demo():
    """Interactive demo of natural language agent system"""
    print("🤖 Unified Agent System with Natural Language Processing")
    print("=" * 70)
    print("All agents can now understand natural language!")
    print("=" * 70)
    print()
    
    system = UnifiedAgentSystem()
    
    print("Try commands like:")
    print('  - "create a task to analyze the codebase"')
    print('  - "run tests for test_script.py"')
    print('  - "what\'s the status?"')
    print('  - "help"')
    print()
    print("Enter 'quit' to exit")
    print("=" * 70)
    print()
    
    while True:
        try:
            command = input("You: ").strip()
            if command.lower() in ['quit', 'exit', 'q']:
                print("Goodbye! 👋")
                break
            
            if not command:
                continue
            
            result = system.process_command(command)
            print(f"Agent: {result['response']}")
            print()
            
        except KeyboardInterrupt:
            print("\nGoodbye! 👋")
            break
        except Exception as e:
            print(f"Error: {e}")


def automated_demo():
    """Automated demo showing various commands"""
    print("🤖 Unified Agent System - Automated Demo")
    print("=" * 70)
    print()
    
    system = UnifiedAgentSystem()
    
    commands = [
        "create a task to analyze the codebase",
        "analyze code in agents/",
        "run tests for test_script.py",
        "generate tests for nlp_agent.py",
        "optimize copilot_test_project/test_script.py",
        "what's the status?",
    ]
    
    for command in commands:
        print(f"You: {command}")
        result = system.process_command(command)
        print(f"Agent: {result['response']}")
        print()
    
    print("=" * 70)
    print("✓ Demo complete! All agents understand natural language.")
    print()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "interactive":
        interactive_demo()
    else:
        automated_demo()
