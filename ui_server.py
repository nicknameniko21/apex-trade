#!/usr/bin/env python3
"""
Swarm Intelligence UI - Web Interface for Agent Management
"""

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import json
import logging
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List
import threading
import time

from agents.swarm_intelligence_agent import SwarmIntelligenceAgent, AgentRole
from agents.autonomous_execution_agent import (
    CodeExecutionAgent, DataAnalysisAgent, OptimizationAgent
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Global swarm instance
workspace = Path(__file__).parent
swarm = None
autonomous_agents = {}


def initialize_swarm():
    """Initialize swarm on startup"""
    global swarm, autonomous_agents
    swarm = SwarmIntelligenceAgent(str(workspace))
    
    # Create autonomous agents
    autonomous_agents = {
        "code_executor": CodeExecutionAgent(),
        "data_analyst": DataAnalysisAgent(),
        "optimizer": OptimizationAgent()
    }
    if not swarm.agents:
        swarm.register_agent(
            "coordinator_01",
            "Coordinator",
            AgentRole.COORDINATOR,
            ["coordinate", "delegate", "workflow", "plan"]
        )
        swarm.register_agent(
            "analyzer_01",
            "Analyzer",
            AgentRole.ANALYZER,
            ["analyze", "review", "audit", "code"]
        )
        swarm.register_agent(
            "executor_01",
            "Executor",
            AgentRole.EXECUTOR,
            ["execute", "run", "deploy", "test"]
        )
        swarm.register_agent(
            "monitor_01",
            "Monitor",
            AgentRole.MONITOR,
            ["monitor", "health", "status", "metrics"]
        )
        swarm.register_agent(
            "communicator_01",
            "Communicator",
            AgentRole.COMMUNICATOR,
            ["communicate", "summarize", "report"]
        )
    logger.info("Swarm and autonomous agents initialized")


@app.route('/')
def index():
    """Serve main UI"""
    return render_template('index.html')


@app.route('/api/agents', methods=['GET'])
def get_agents():
    """Get all registered agents"""
    agents = []
    for agent_id, agent in swarm.agents.items():
        agents.append({
            "id": agent_id,
            "name": agent.name,
            "role": agent.role.value,
            "status": agent.status,
            "capabilities": agent.capabilities,
            "tasks_completed": agent.tasks_completed,
            "created_at": agent.created_at
        })
    return jsonify({"agents": agents, "total": len(agents)})


@app.route('/api/agents/register', methods=['POST'])
def register_agent():
    """Register a new agent"""
    data = request.json
    try:
        agent_id = data.get("agent_id", f"agent_{len(swarm.agents)}")
        name = data.get("name", "Unnamed Agent")
        role = AgentRole[data.get("role", "EXECUTOR").upper()]
        capabilities = data.get("capabilities", [])
        
        agent = swarm.register_agent(agent_id, name, role, capabilities)
        
        return jsonify({
            "success": True,
            "agent": {
                "id": agent.agent_id,
                "name": agent.name,
                "role": agent.role.value
            }
        }), 201
    except Exception as e:
        logger.error(f"Error registering agent: {e}")
        return jsonify({"success": False, "error": str(e)}), 400


@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """Get all tasks"""
    tasks = []
    for task_id, task in swarm.tasks.items():
        tasks.append({
            "id": task.task_id,
            "description": task.description,
            "priority": task.priority,
            "status": task.status,
            "assigned_to": task.assigned_to,
            "created_at": task.created_at,
            "completed_at": task.completed_at,
            "result": task.result
        })
    return jsonify({"tasks": tasks, "total": len(tasks)})


@app.route('/api/tasks/create', methods=['POST'])
def create_task():
    """Create a new task"""
    data = request.json
    try:
        task_id = data.get("task_id", f"task_{len(swarm.tasks)}")
        description = data.get("description", "")
        priority = data.get("priority", 5)
        
        if not description:
            return jsonify({"success": False, "error": "Description required"}), 400
        
        task = swarm.create_task(task_id, description, priority)
        
        return jsonify({
            "success": True,
            "task": {
                "id": task.task_id,
                "description": task.description,
                "priority": task.priority,
                "status": task.status
            }
        }), 201
    except Exception as e:
        logger.error(f"Error creating task: {e}")
        return jsonify({"success": False, "error": str(e)}), 400


@app.route('/api/tasks/<task_id>/assign', methods=['POST'])
def assign_task(task_id):
    """Assign task to agent"""
    data = request.json
    agent_id = data.get("agent_id")
    
    if not agent_id:
        return jsonify({"success": False, "error": "Agent ID required"}), 400
    
    try:
        success = swarm.assign_task(task_id, agent_id)
        if success:
            return jsonify({
                "success": True,
                "message": f"Task {task_id} assigned to {agent_id}"
            })
        else:
            return jsonify({"success": False, "error": "Assignment failed"}), 400
    except Exception as e:
        logger.error(f"Error assigning task: {e}")
        return jsonify({"success": False, "error": str(e)}), 400


@app.route('/api/tasks/<task_id>/execute', methods=['POST'])
def execute_task(task_id):
    """Execute a task"""
    try:
        result = swarm.execute_task(task_id)
        if result.get("success"):
            return jsonify({
                "success": True,
                "result": result
            })
        else:
            return jsonify({"success": False, "error": result.get("error")}), 400
    except Exception as e:
        logger.error(f"Error executing task: {e}")
        return jsonify({"success": False, "error": str(e)}), 400


@app.route('/api/status', methods=['GET'])
def get_status():
    """Get overall swarm status"""
    try:
        status = swarm.get_swarm_status()
        return jsonify(status)
    except Exception as e:
        logger.error(f"Error getting status: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/models', methods=['GET'])
def get_models():
    """Get all registered models"""
    try:
        return jsonify({"models": swarm.list_models(), "total": len(swarm.models)})
    except Exception as e:
        logger.error(f"Error getting models: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/models/register', methods=['POST'])
def register_model():
    """Register a new model"""
    data = request.json or {}
    try:
        model_id = data.get("model_id")
        name = data.get("name")
        provider = data.get("provider")
        strengths = data.get("strengths", [])
        endpoint = data.get("endpoint")
        status = data.get("status", "available")

        if not model_id or not name or not provider:
            return jsonify({"success": False, "error": "model_id, name, provider required"}), 400

        model = swarm.register_model(
            model_id=model_id,
            name=name,
            provider=provider,
            strengths=strengths,
            endpoint=endpoint,
            status=status
        )
        return jsonify({"success": True, "model": asdict(model)}), 201
    except Exception as e:
        logger.error(f"Error registering model: {e}")
        return jsonify({"success": False, "error": str(e)}), 400


@app.route('/api/models/route', methods=['POST'])
def route_model():
    """Route query to best-fit model"""
    data = request.json or {}
    query = data.get("query", "").strip()
    if not query:
        return jsonify({"success": False, "error": "Query required"}), 400
    try:
        return jsonify(swarm.route_model(query))
    except Exception as e:
        logger.error(f"Error routing model: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/workflows', methods=['GET'])
def get_workflows():
    """Get all workflows"""
    try:
        return jsonify({"workflows": swarm.list_workflows(), "total": len(swarm.workflows)})
    except Exception as e:
        logger.error(f"Error getting workflows: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/workflows/create', methods=['POST'])
def create_workflow():
    """Create a workflow"""
    data = request.json or {}
    try:
        workflow_id = data.get("workflow_id", f"workflow_{len(swarm.workflows)}")
        name = data.get("name", "Unnamed Workflow")
        description = data.get("description", "")
        steps = data.get("steps", [])
        if not steps:
            return jsonify({"success": False, "error": "Workflow steps required"}), 400

        workflow = swarm.create_workflow(workflow_id, name, description, steps)
        return jsonify({"success": True, "workflow": asdict(workflow)}), 201
    except Exception as e:
        logger.error(f"Error creating workflow: {e}")
        return jsonify({"success": False, "error": str(e)}), 400


@app.route('/api/workflows/<workflow_id>/execute', methods=['POST'])
def execute_workflow(workflow_id):
    """Execute workflow"""
    try:
        result = swarm.execute_workflow(workflow_id)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error executing workflow: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/autonomous/execute', methods=['POST'])
def execute_autonomous():
    """Execute autonomous agent task"""
    data = request.json
    agent_type = data.get("agent_type", "code_executor")
    task_type = data.get("task_type", "analyze")
    target = data.get("target", "")
    
    try:
        if agent_type == "code_executor":
            result = autonomous_agents["code_executor"].execute_code(target)
        elif agent_type == "data_analyst":
            result = autonomous_agents["data_analyst"].analyze_logs(target)
        elif agent_type == "optimizer":
            result = autonomous_agents["optimizer"].optimize_performance(target)
        else:
            return jsonify({"success": False, "error": "Unknown agent type"}), 400
        
        return jsonify({
            "success": result.get("success", True),
            "result": result
        })
    except Exception as e:
        logger.error(f"Error executing autonomous task: {e}")
        return jsonify({"success": False, "error": str(e)}), 400


@app.route('/api/agents/<agent_id>/model', methods=['GET'])
def get_agent_model(agent_id):
    """Get agent model information"""
    try:
        model_info = swarm.get_agent_model_info(agent_id)
        return jsonify(model_info)
    except Exception as e:
        logger.error(f"Error getting agent model: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/model', methods=['GET'])
def get_system_model():
    """Get system model information"""
    try:
        model_info = swarm.get_agent_model_info()
        return jsonify(model_info)
    except Exception as e:
        logger.error(f"Error getting system model: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/logs', methods=['GET'])
def get_logs():
    """Get execution logs"""
    try:
        log_file = workspace / "action_logs" / "swarm_execution.log"
        if not log_file.exists():
            return jsonify({"logs": []})
        
        logs = []
        with open(log_file, 'r') as f:
            for line in f:
                try:
                    logs.append(json.loads(line))
                except:
                    pass
        
        # Return last 50 logs
        return jsonify({"logs": logs[-50:]})
    except Exception as e:
        logger.error(f"Error getting logs: {e}")
        return jsonify({"error": str(e)}), 500


def route_natural_language(query: str) -> tuple[str, str]:
    """Route natural language query to appropriate agent"""
    query_lower = query.lower()
    
    # Analyze keywords
    if any(word in query_lower for word in ['analyze', 'review', 'audit', 'check', 'scan', 'code']):
        return "analyzer_01", "Analyzer Agent"
    elif any(word in query_lower for word in ['optimize', 'improve', 'performance', 'speed', 'slow']):
        return "optimizer_01", "Optimizer Agent"
    elif any(word in query_lower for word in ['execute', 'run', 'test', 'deploy', 'build']):
        return "executor_01", "Executor Agent"
    elif any(word in query_lower for word in ['health', 'status', 'monitor', 'check system', 'uptime', 'metric']):
        return "monitor_01", "Monitor Agent"
    else:
        return "analyzer_01", "Analyzer Agent"  # Default


@app.route('/api/chat', methods=['POST'])
def chat():
    """Natural language chat interface for agents"""
    data = request.json
    user_message = data.get("message", "").strip()
    
    if not user_message:
        return jsonify({"success": False, "error": "Empty message"}), 400
    
    try:
        # Route to appropriate agent
        selected_agent = swarm.select_agent_for_task(user_message)
        if selected_agent:
            fallback_name = None
        else:
            selected_agent, fallback_name = route_natural_language(user_message)
        agent_id = selected_agent
        agent_name = (
            swarm.agents.get(agent_id).name
            if agent_id and agent_id in swarm.agents
            else (fallback_name or agent_id or "Unknown Agent")
        )
        model_routing = swarm.route_model(user_message)
        
        # Create task from natural language
        task_id = f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        task = swarm.create_task(task_id, user_message, priority=1)
        
        # Assign to routed agent
        swarm.assign_task(task_id, agent_id)
        
        # Execute immediately
        result = swarm.execute_task(task_id)
        
        # Format response
        response = {
            "success": True,
            "agent": agent_name,
            "agent_id": agent_id,
            "user_message": user_message,
            "task_id": task_id,
            "status": "completed",
            "model": model_routing.get("model"),
            "model_reason": model_routing.get("reason"),
            "result": {
                "task_id": result.get("task_id"),
                "description": result.get("description"),
                "executed_at": result.get("executed_at"),
                "agent": result.get("agent_name")
            }
        }
        
        return jsonify(response), 200
    
    except Exception as e:
        logger.error(f"Error in chat: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/chat/history', methods=['GET'])
def chat_history():
    """Get chat history"""
    try:
        log_file = workspace / "action_logs" / "swarm_execution.log"
        if not log_file.exists():
            return jsonify({"history": []})
        
        history = []
        with open(log_file, 'r') as f:
            for line in f:
                try:
                    log_entry = json.loads(line)
                    if log_entry.get("action") == "task_executed":
                        history.append({
                            "timestamp": log_entry.get("timestamp"),
                            "task": log_entry.get("data", {}).get("description"),
                            "agent": log_entry.get("data", {}).get("agent_name"),
                            "success": log_entry.get("data", {}).get("success")
                        })
                except:
                    pass
        
        return jsonify({"history": history[-50:]})
    except Exception as e:
        logger.error(f"Error getting chat history: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    initialize_swarm()
    logger.info("Starting Swarm Intelligence UI on http://localhost:5000")
    app.run(debug=False, host='0.0.0.0', port=5000)
