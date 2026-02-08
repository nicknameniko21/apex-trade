# Swarm Intelligence REST API Reference

## Quick Start

### 1. **Interactive CLI** (Easiest)
```bash
python swarm_cli.py
```

Then type commands:
```
swarm> status          # See swarm status
swarm> agents          # List all agents
swarm> learning        # Show learning progress
swarm> generate        # Generate new tasks
swarm> start-learning  # Start continuous learning
swarm> help            # See all commands
```

### 2. **Web Dashboard**
Open in browser: `http://localhost:5000`

### 3. **Direct REST API Calls**

---

## REST API Endpoints

### Swarm Status & Control

#### Get Swarm Status
```bash
curl http://localhost:5000/api/agents
```

**Response:**
```json
{
  "agents": [
    {
      "id": "code_executor_01",
      "name": "Code Executor",
      "role": "EXECUTOR",
      "status": "idle",
      "capabilities": ["code_analysis", "code_execution"]
    }
  ]
}
```

#### Get Learning Status
```bash
curl http://localhost:5000/api/swarm/learning-status
```

**Response:**
```json
{
  "total_tasks": 12,
  "completed_tasks": 12,
  "failed_tasks": 0,
  "success_rate": "100%",
  "agent_patterns": {
    "code_executor_01": {
      "learn_analyze_code": {
        "successes": 2,
        "failures": 0
      }
    }
  }
}
```

#### Generate Learning Tasks
```bash
curl -X POST http://localhost:5000/api/swarm/generate-tasks \
  -H "Content-Type: application/json" \
  -d '{"type": "learning"}'
```

#### Start Learning Loop
```bash
curl -X POST http://localhost:5000/api/swarm/learning/start
```

**Response:**
```json
{
  "success": true,
  "message": "Background learning started"
}
```

#### Stop Learning Loop
```bash
curl -X POST http://localhost:5000/api/swarm/learning/stop
```

#### Check Learning Status
```bash
curl http://localhost:5000/api/swarm/learning/status
```

**Response:**
```json
{
  "learning_active": true,
  "last_update": "2026-02-08T12:34:56.789Z",
  "learning_data": {
    "agents": 3,
    "cycles_completed": 5
  }
}
```

---

### Tasks

#### Get All Tasks
```bash
curl http://localhost:5000/api/tasks
```

**Response:**
```json
{
  "tasks": [
    {
      "id": "learn_analyze_code",
      "description": "Analyze codebase structure",
      "status": "completed",
      "priority": 1
    }
  ]
}
```

#### Create New Task
```bash
curl -X POST http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Custom analysis task",
    "priority": 1
  }'
```

---

### Pine Scripts

#### List All Pine Scripts
```bash
curl http://localhost:5000/api/pine-scripts
```

**Response:**
```json
{
  "scripts": [
    {
      "name": "rsi_strategy",
      "type": "strategy",
      "valid": true,
      "path": "/pine_scripts/rsi_strategy.pine"
    }
  ]
}
```

#### Validate Script
```bash
curl http://localhost:5000/api/pine-scripts/validate/rsi_strategy
```

**Response:**
```json
{
  "name": "rsi_strategy",
  "valid": true,
  "errors": []
}
```

#### Fix Broken Script
```bash
curl -X POST http://localhost:5000/api/pine-scripts/fix \
  -H "Content-Type: application/json" \
  -d '{"script_name": "volatility"}'
```

---

### GitHub Integration

#### Push to GitHub
```bash
curl -X POST http://localhost:5000/api/github/push \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Auto-update from swarm learning"
  }'
```

#### Pull from GitHub
```bash
curl -X POST http://localhost:5000/api/github/pull
```

#### Create GitHub Branch
```bash
curl -X POST http://localhost:5000/api/github/branch \
  -H "Content-Type: application/json" \
  -d '{"branch_name": "feature/new-strategy"}'
```

---

## Python Examples

### Using requests library
```python
import requests

BASE_URL = "http://localhost:5000"

# Get swarm status
response = requests.get(f"{BASE_URL}/api/agents")
agents = response.json()['agents']
print(f"Active agents: {len(agents)}")

# Start learning
response = requests.post(f"{BASE_URL}/api/swarm/learning/start")
print(response.json())

# Generate tasks
response = requests.post(f"{BASE_URL}/api/swarm/generate-tasks",
                        json={"type": "learning"})
print(f"Tasks generated: {response.json()['tasks_generated']}")

# Check learning progress
response = requests.get(f"{BASE_URL}/api/swarm/learning-status")
status = response.json()
print(f"Success rate: {status['success_rate']}")
```

---

## Command-Line Examples

### Monitor Learning in Real-Time
```bash
# Every 10 seconds, show learning progress
watch -n 10 'curl -s http://localhost:5000/api/swarm/learning-status | python -m json.tool'
```

### Get Agent Info
```bash
curl http://localhost:5000/api/agents | python -m json.tool
```

### Start Continuous Learning (background)
```bash
curl -X POST http://localhost:5000/api/swarm/learning/start &
```

### Generate Tasks Every 30 Seconds
```bash
while true; do
  curl -X POST http://localhost:5000/api/swarm/generate-tasks \
    -d '{"type": "learning"}'
  echo "Tasks generated at $(date)"
  sleep 30
done
```

---

## Architecture Overview

```
┌─────────────────────────────────────┐
│   Flask REST API Server (port 5000) │
└─────────────────────────────────────┘
            ↓
┌─────────────────────────────────────┐
│   SwarmIntelligenceAgent            │
│   - Orchestrates 3 agents           │
│   - Manages task queue              │
│   - Coordinates execution           │
└─────────────────────────────────────┘
            ↓
┌──────────────────────────────────────────────────────┐
│  Autonomous Agents (3 running in parallel)           │
│  - CodeExecutor       (code analysis/execution)      │
│  - DataAnalyst        (data processing)              │
│  - Optimizer          (performance optimization)     │
└──────────────────────────────────────────────────────┘
            ↓
┌──────────────────────────────────────────────────────┐
│  Task Generator                                      │
│  - Generates 6 learning task types every cycle       │
│  - Adaptive tasks based on success rates             │
│  - Runs in background thread (60s cycles)            │
└──────────────────────────────────────────────────────┘
            ↓
┌──────────────────────────────────────────────────────┐
│  Learning Engine                                     │
│  - Tracks success/failure patterns                   │
│  - Adapts execution strategies                       │
│  - Persists state to action_logs/                    │
└──────────────────────────────────────────────────────┘
```

---

## Status Codes

| Code | Meaning |
|------|---------|
| 200  | Success |
| 201  | Created |
| 400  | Bad request |
| 404  | Not found |
| 500  | Server error |
| 503  | Service unavailable |

---

## Useful Tips

1. **Monitor in Real-Time**: Use the CLI with `swarm> learning` command
2. **Check Server Status**: `curl http://localhost:5000/api/agents`
3. **View Logs**: Check `action_logs/swarm_execution.log`
4. **Stop Learning**: `swarm> stop-learning` to pause autonomous operation
5. **Manual Tasks**: Use `swarm> generate` to trigger immediate task generation

---

**Last Updated**: 2026-02-08
