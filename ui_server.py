#!/usr/bin/env python3
"""
Swarm Intelligence UI - Web Interface for Agent Management
"""

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List
import threading
import time

from agents.swarm_intelligence_agent import SwarmIntelligenceAgent, AgentRole
from agents.autonomous_execution_agent import (
    CodeExecutionAgent, DataAnalysisAgent, OptimizationAgent
)
from agents.autonomous_task_generator import AutonomousTaskGenerator
from agents.pine_scripts_manager import PineScriptsManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Global swarm instance
workspace = Path(__file__).parent
swarm = None
autonomous_agents = {}
pine_manager = None
task_generator = None
learning_thread = None
learning_active = False


@app.route('/')
def index():
    """Serve main UI"""
    return render_template('index.html')


def start_continuous_learning():
    """Start background learning loop"""
    global learning_thread, learning_active
    
    if learning_active:
        logger.warning("Learning loop already running")
        return
    
    learning_active = True
    learning_thread = threading.Thread(target=_continuous_learning_worker, daemon=True)
    learning_thread.start()
    logger.info("Background learning loop started")


def _continuous_learning_worker():
    """Background worker for continuous learning"""
    global learning_active, task_generator
    
    learning_cycle = 0
    while learning_active:
        try:
            learning_cycle += 1
            logger.info(f"Learning cycle {learning_cycle} starting...")
            
            # Generate learning tasks
            task_ids = task_generator.generate_learning_tasks()
            logger.info(f"Cycle {learning_cycle}: Generated {len(task_ids)} tasks")
            
            # Execute tasks
            results = task_generator.execute_all_tasks()
            logger.info(f"Cycle {learning_cycle}: Executed {len(results['executed'])} tasks")
            
            # Generate adaptive tasks based on patterns
            adaptive_ids = task_generator.generate_adaptive_tasks()
            if adaptive_ids:
                # Execute adaptive tasks
                adaptive_results = task_generator.execute_all_tasks()
                logger.info(f"Cycle {learning_cycle}: {len(adaptive_ids)} adaptive tasks executed")
            
            # Save learning state
            _save_learning_state()
            
            # Wait before next cycle
            time.sleep(60)  # 60 second interval
            
        except Exception as e:
            logger.error(f"Learning cycle error: {e}")
            time.sleep(10)  # Shorter wait on error


def _save_learning_state():
    """Persist learned patterns to disk"""
    try:
        learning_state = {
            "timestamp": datetime.now().isoformat(),
            "agents": {}
        }
        
        for agent_id, agent in autonomous_agents.items():
            if hasattr(agent, 'learned_patterns'):
                learning_state["agents"][agent_id] = {
                    "id": agent.agent_id,
                    "patterns": agent.learned_patterns,
                    "task_history_size": len(agent.task_history)
                }
        
        # Save to file
        state_file = workspace / "action_logs" / "learning_state.json"
        with open(state_file, 'w') as f:
            json.dump(learning_state, f, indent=2)
        
        logger.info(f"Learning state saved with {len(learning_state['agents'])} agents")
    except Exception as e:
        logger.error(f"Failed to save learning state: {e}")


def stop_continuous_learning():
    """Stop background learning loop"""
    global learning_active
    learning_active = False
    logger.info("Background learning loop stopping...")
    
    
def initialize_swarm():
    """Initialize swarm on startup"""
    global swarm, autonomous_agents, pine_manager, task_generator
    swarm = SwarmIntelligenceAgent(str(workspace))
    
    # Create autonomous agents with GitHub integration
    autonomous_agents = {
        "code_executor": CodeExecutionAgent(str(workspace)),
        "data_analyst": DataAnalysisAgent(),
        "optimizer": OptimizationAgent()
    }
    
    # Register agents with swarm
    for agent_id, agent in autonomous_agents.items():
        swarm.register_agent(
            agent_id=agent_id,
            name=agent.agent_id,
            role=AgentRole.EXECUTOR,
            capabilities=agent.capabilities
        )
    
    # Initialize Pine Scripts Manager
    pine_manager = PineScriptsManager(str(workspace))
    scripts = pine_manager.discover_scripts()
    
    if scripts:
        logger.info(f"Loaded {len(scripts)} Pine Scripts")
        # Auto-fix broken scripts
        for script in scripts:
            validation = pine_manager.validate_script(script)
            if not validation["valid"]:
                logger.warning(f"Fixing broken script: {script.name}")
                pine_manager.fix_broken_script(script.name)
        pine_manager.cache_scripts()
    
    # Initialize task generator for autonomous learning
    task_generator = AutonomousTaskGenerator(swarm, str(workspace))
    
    # Generate initial learning tasks
    task_ids = task_generator.generate_learning_tasks()
    logger.info(f"Generated {len(task_ids)} learning tasks")
    
    # Execute initial tasks
    results = task_generator.execute_all_tasks()
    logger.info(f"Executed {len(results['executed'])} initial tasks, failed: {len(results['failed'])}")
    
    # Start continuous background learning
    start_continuous_learning()
    
    logger.info("Swarm and autonomous agents initialized with continuous learning")


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
        agent_id, agent_name = route_natural_language(user_message)
        
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
            "user_message": user_message,
            "task_id": task_id,
            "status": "completed",
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


@app.route('/api/pine-scripts', methods=['GET'])
def get_pine_scripts():
    """Get all Pine Scripts"""
    if not pine_manager:
        return jsonify({"scripts": [], "error": "Pine manager not initialized"}), 503
    
    scripts = pine_manager.get_all_scripts()
    return jsonify({
        "scripts": [
            {
                "name": s.name,
                "status": s.status,
                "version": s.version,
                "path": s.path,
                "last_updated": s.last_updated
            }
            for s in scripts
        ],
        "total": len(scripts)
    })


@app.route('/api/pine-scripts/<script_name>', methods=['GET'])
def get_pine_script(script_name):
    """Get specific Pine Script"""
    if not pine_manager:
        return jsonify({"error": "Pine manager not initialized"}), 503
    
    script = pine_manager.get_script(script_name)
    if not script:
        return jsonify({"error": "Script not found"}), 404
    
    return jsonify({
        "name": script.name,
        "content": script.content,
        "status": script.status,
        "version": script.version,
        "path": script.path
    })


@app.route('/api/pine-scripts/<script_name>/validate', methods=['POST'])
def validate_pine_script(script_name):
    """Validate Pine Script"""
    if not pine_manager:
        return jsonify({"error": "Pine manager not initialized"}), 503
    
    script = pine_manager.get_script(script_name)
    if not script:
        return jsonify({"error": "Script not found"}), 404
    
    validation = pine_manager.validate_script(script)
    return jsonify(validation)


@app.route('/api/pine-scripts/<script_name>/fix', methods=['POST'])
def fix_pine_script(script_name):
    """Fix broken Pine Script"""
    if not pine_manager:
        return jsonify({"error": "Pine manager not initialized"}), 503
    
    success = pine_manager.fix_broken_script(script_name)
    if success:
        pine_manager.cache_scripts()
        return jsonify({"success": True, "message": f"Fixed {script_name}"})
    
    return jsonify({"success": False, "error": "Could not fix script"}), 400


@app.route('/api/github/push', methods=['POST'])
def github_push():
    """Push code to GitHub"""
    data = request.json
    file_path = data.get("file_path", ".")
    commit_message = data.get("message", f"Auto-commit from UI - {datetime.now().isoformat()}")
    
    code_agent = autonomous_agents.get("code_executor")
    if not code_agent:
        return jsonify({"error": "Code executor not initialized"}), 503
    
    result = code_agent.push_to_github(file_path, commit_message)
    return jsonify(result), (200 if result["success"] else 400)


@app.route('/api/github/pull', methods=['POST'])
def github_pull():
    """Pull from GitHub"""
    code_agent = autonomous_agents.get("code_executor")
    if not code_agent:
        return jsonify({"error": "Code executor not initialized"}), 503
    
    result = code_agent.pull_from_github()
    return jsonify(result), (200 if result["success"] else 400)


@app.route('/api/github/branch', methods=['POST'])
def github_branch():
    """Create GitHub branch"""
    data = request.json
    branch_name = data.get("branch_name")
    
    if not branch_name:
        return jsonify({"error": "branch_name required"}), 400
    
    code_agent = autonomous_agents.get("code_executor")
    if not code_agent:
        return jsonify({"error": "Code executor not initialized"}), 503
    
    result = code_agent.create_github_branch(branch_name)
    return jsonify(result), (200 if result["success"] else 400)


@app.route('/api/swarm/learning-status', methods=['GET'])
def get_learning_status():
    """Get swarm learning progress"""
    if not task_generator:
        return jsonify({"error": "Task generator not initialized"}), 503
    
    status = task_generator.get_agent_learning_status()
    
    # Add task statistics
    status["task_statistics"] = {
        "total_tasks": len(swarm.tasks) if swarm else 0,
        "executed_tasks": sum(1 for t in (swarm.tasks.values() if swarm else []) if t.status == "completed"),
        "pending_tasks": sum(1 for t in (swarm.tasks.values() if swarm else []) if t.status in ["pending", "assigned"])
    }
    
    return jsonify(status)


@app.route('/api/swarm/generate-tasks', methods=['POST'])
def generate_tasks():
    """Generate new learning tasks"""
    if not task_generator:
        return jsonify({"error": "Task generator not initialized"}), 503
    
    data = request.json or {}
    task_type = data.get("type", "learning")
    
    if task_type == "adaptive":
        task_ids = task_generator.generate_adaptive_tasks()
    else:
        task_ids = task_generator.generate_learning_tasks()
    
    # Execute tasks
    results = task_generator.execute_all_tasks()
    
    return jsonify({
        "success": True,
        "tasks_generated": len(task_ids),
        "tasks_executed": len(results["executed"]),
        "results": results
    })


@app.route('/api/swarm/learning/start', methods=['POST'])
def start_learning():
    """Start background learning loop"""
    global learning_active
    
    if learning_active:
        return jsonify({"success": False, "error": "Learning already running"}), 400
    
    start_continuous_learning()
    return jsonify({"success": True, "message": "Background learning started"})


@app.route('/api/swarm/learning/stop', methods=['POST'])
def stop_learning():
    """Stop background learning loop"""
    global learning_active
    
    if not learning_active:
        return jsonify({"success": False, "error": "Learning not running"}), 400
    
    stop_continuous_learning()
    return jsonify({"success": True, "message": "Background learning stopped"})


@app.route('/api/swarm/learning/status', methods=['GET'])
def learning_status():
    """Get learning loop status"""
    global learning_active
    
    status_file = workspace / "action_logs" / "learning_state.json"
    last_update = None
    learning_data = None
    
    if status_file.exists():
        try:
            with open(status_file) as f:
                learning_data = json.load(f)
                last_update = learning_data.get("timestamp")
        except:
            pass
    
    return jsonify({
        "learning_active": learning_active,
        "last_update": last_update,
        "learning_data": learning_data
    })


@app.route('/api/chat', methods=['POST'])
def chat():
    """Chat with agents - converts user queries into learning tasks"""
    if not task_generator or not swarm:
        return jsonify({"error": "System not initialized"}), 503
    
    data = request.json or {}
    user_message = data.get("message", "").strip()
    
    if not user_message:
        return jsonify({"error": "Empty message"}), 400
    
    logger.info(f"User query: {user_message}")
    
    # Create a custom task from the user query
    custom_task_id = f"user_query_{int(time.time())}"
    task_description = f"User asked: {user_message}"
    
    try:
        # Create and execute the task
        task = swarm.create_task(
            task_id=custom_task_id,
            description=task_description,
            priority=1,  # User queries get high priority
            task_type="user_query"
        )
        
        # Assign to an available agent
        available_agents = [aid for aid in autonomous_agents.keys() 
                          if autonomous_agents[aid].status == 'idle']
        
        if not available_agents:
            available_agents = [list(autonomous_agents.keys())[0]]
        
        agent_id = available_agents[0]
        swarm.assign_task(task, agent_id)
        result = swarm.execute_task(task, agent_id)
        
        # Log the interaction
        logger.info(f"Task {custom_task_id} assigned to {agent_id}: {result}")
        
        # Record learning from this interaction
        agent = autonomous_agents[agent_id]
        if result.get("success"):
            agent.learned_patterns.setdefault("user_query", {"successes": 0, "failures": 0})
            agent.learned_patterns["user_query"]["successes"] += 1
        else:
            agent.learned_patterns.setdefault("user_query", {"successes": 0, "failures": 0})
            agent.learned_patterns["user_query"]["failures"] += 1
        
        return jsonify({
            "success": True,
            "agent": agent_id,
            "task_id": custom_task_id,
            "message": f"Task processed by {agent_id}",
            "result": result.get("message", "Task completed")
        })
    
    except Exception as e:
        logger.error(f"Error processing chat: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/chat/history', methods=['GET'])
def get_chat_history():
    """Get chat history and interactions"""
    history_file = workspace / "action_logs" / "chat_history.json"
    
    if history_file.exists():
        try:
            with open(history_file) as f:
                history = json.load(f)
                return jsonify({"success": True, "history": history})
        except:
            pass
    
    return jsonify({"success": True, "history": []})


@app.route('/api/agents/<agent_id>/chat', methods=['POST'])
def agent_chat(agent_id):
    """Chat directly with a specific agent"""
    if agent_id not in autonomous_agents:
        return jsonify({"error": f"Agent {agent_id} not found"}), 404
    
    data = request.json or {}
    message = data.get("message", "").strip()
    
    if not message:
        return jsonify({"error": "Empty message"}), 400
    
    agent = autonomous_agents[agent_id]
    
    # Execute the message as a task for this agent
    try:
        result = agent.execute_code(message)
        logger.info(f"Agent {agent_id} processed: {message}")
        
        return jsonify({
            "success": True,
            "agent": agent_id,
            "message": message,
            "response": result.get("message", "Task completed"),
            "learning_stats": agent.learned_patterns
        })
    except Exception as e:
        logger.error(f"Error in agent chat: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    initialize_swarm()
    logger.info("Starting Swarm Intelligence UI on http://localhost:5000")
    app.run(debug=False, host='0.0.0.0', port=5000)
