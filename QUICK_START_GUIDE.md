# QUICK START: Controlling Your Swarm

## How to Chat with the Swarm

You now have **three ways** to control and interact with the apex-trade swarm system:

---

## Option 1: Interactive CLI (RECOMMENDED - Easiest)

### Start the CLI:
```bash
python swarm_cli.py
```

### Example Session:
```
======================================================================
===========  APEX TRADE SWARM INTELLIGENCE CONTROL CENTER  ===========
======================================================================

Welcome to Swarm Intelligence Control Center!
Type 'help' for available commands or 'quit' to exit.

[swarm]> status
[*] SWARM STATUS:
----------------------------------------------------------------------
Server: [OK] ONLINE (http://localhost:5000)
Agents Registered: 3
  [OK] code_executor_01       | Role: EXECUTOR    | Status: idle
  [OK] data_analyst_01        | Role: EXECUTOR    | Status: idle
  [OK] optimizer_01           | Role: EXECUTOR    | Status: idle
----------------------------------------------------------------------

[swarm]> learning
[*] LEARNING STATUS:
----------------------------------------------------------------------
Total Tasks: 12
Completed: 12
Failed: 0
Success Rate: 100%

Agent Learning Patterns:
  code_executor_01:
    learn_analyze_code: 2 successes, 0 failures
    learn_generate_docs: 2 successes, 0 failures
----------------------------------------------------------------------

[swarm]> generate
[+] TASKS GENERATED:
----------------------------------------------------------------------
Generated: 6
Executed: 6
Success: True
----------------------------------------------------------------------

[swarm]> quit
[*] Goodbye!
```

### Available Commands in CLI:
```
status               - Show swarm status and agent information
agents               - List all registered agents
tasks                - Show current tasks
learning             - Show learning status
generate             - Generate new learning tasks
start-learning       - Start continuous learning loop
stop-learning        - Stop continuous learning loop
scripts              - List Pine Script trading strategies
validate-script      - Validate a Pine Script (usage: validate-script rsi_strategy)
github-status        - Show GitHub integration status
help                 - Show this help message
quit                 - Exit the CLI
```

---

## Option 2: Web Dashboard

### Open in Browser:
```
http://localhost:5000
```

The web dashboard shows:
- Real-time agent status
- Learning progress metrics
- Current task list
- Pine Script validation status
- GitHub integration status

---

## Option 3: REST API (For Programmatic Access)

### Quick Examples:

#### Get Swarm Status:
```bash
curl http://localhost:5000/api/agents
```

#### Start Learning:
```bash
curl -X POST http://localhost:5000/api/swarm/learning/start
```

#### Check Learning Progress:
```bash
curl http://localhost:5000/api/swarm/learning-status
```

#### Generate Tasks Immediately:
```bash
curl -X POST http://localhost:5000/api/swarm/generate-tasks \
  -H "Content-Type: application/json" \
  -d '{"type": "learning"}'
```

#### List Pine Scripts:
```bash
curl http://localhost:5000/api/pine-scripts
```

For full API reference, see [SWARM_API_REFERENCE.md](SWARM_API_REFERENCE.md)

---

## Complete Workflow Example

### 1. Start the Server (in one terminal):
```bash
python ui_server.py
```

You'll see:
```
INFO:__main__:Starting Swarm Intelligence UI on http://localhost:5000
INFO:__main__:Background learning loop started
 * Running on http://127.0.0.1:5000
```

The system now automatically:
- Initializes 3 agents (CodeExecutor, DataAnalyst, Optimizer)
- Loads Pine Scripts
- Generates 6 learning tasks
- Starts continuous background learning (60-second cycles)

### 2. In Another Terminal, Use the CLI:
```bash
python swarm_cli.py
```

### 3. Common Commands to Try:

```bash
# Check system health
[swarm]> status

# See all agents
[swarm]> agents

# Monitor learning progress
[swarm]> learning

# Generate immediate tasks
[swarm]> generate

# See trading strategies
[swarm]> scripts

# Stop/start learning loop
[swarm]> stop-learning
[swarm]> start-learning

# Get help
[swarm]> help
```

---

## What the Swarm Does Automatically

Once `python ui_server.py` starts, the system:

1. **Registers 3 Agents**:
   - CodeExecutor - Executes code analysis tasks
   - DataAnalyst - Processes data
   - Optimizer - Optimizes performance

2. **Loads 3 Pine Scripts**:
   - rsi_strategy - RSI indicator strategy
   - ma_crossover - Moving average crossover
   - volatility - ATR volatility strategy

3. **Starts Learning Cycles** (Every 60 seconds):
   - Generate 6 learning tasks
   - Assign to agents based on capabilities
   - Execute sequentially
   - Record success/failure patterns
   - Save state to disk
   - Repeat

4. **Provides REST API** on port 5000 for:
   - Agent control and monitoring
   - Task generation
   - Learning status
   - Pine Script validation
   - GitHub integration

---

## Monitoring Learning in Real-Time

### Option A: Use CLI
```bash
python swarm_cli.py
[swarm]> learning     # Run every 10 seconds to see progress
```

### Option B: Watch REST Endpoint
```bash
# Continuously check learning status (PowerShell)
while ($true) {
  curl http://localhost:5000/api/swarm/learning-status | ConvertFrom-Json
  Start-Sleep -Seconds 10
}
```

### Option C: Check Log Files
```bash
# Windows PowerShell
Get-Content -Path action_logs/swarm_execution.log -Wait

# or
cat action_logs/learning_state.json | python -m json.tool
```

---

## Python Integration Example

```python
import requests

BASE_URL = "http://localhost:5000"

# Get agent status
agents = requests.get(f"{BASE_URL}/api/agents").json()
print(f"Active agents: {len(agents['agents'])}")

# Start learning
requests.post(f"{BASE_URL}/api/swarm/learning/start")

# Check progress
learning = requests.get(f"{BASE_URL}/api/swarm/learning-status").json()
print(f"Success rate: {learning['success_rate']}")

# Generate tasks
response = requests.post(f"{BASE_URL}/api/swarm/generate-tasks",
                        json={"type": "learning"})
print(f"Tasks generated: {response.json()['tasks_generated']}")
```

---

## Control vs. Automation

### Manual Control (Via CLI)
```bash
[swarm]> stop-learning         # Pause autonomous operation
[swarm]> generate              # Manually trigger tasks
[swarm]> start-learning        # Resume autonomy
```

### Automatic Control (Background)
The system continuously runs in background:
- 60-second learning cycles
- Persistent pattern learning
- Automatic state saving
- No manual intervention needed

---

## Troubleshooting

### Problem: "Cannot connect to Swarm server"
**Solution**: Start the server first:
```bash
python ui_server.py
```

### Problem: CLI shows 0 agents
**Solution**: Wait 5 seconds for swarm to initialize, then try:
```bash
[swarm]> status
```

### Problem: "Port 5000 already in use"
**Solution**: Kill the process on port 5000:
```bash
# PowerShell
Get-Process | Where-Object Port -eq 5000 | Stop-Process -Force
```

### Problem: Learning isn't happening
**Solution**: Check if learning loop is active:
```bash
[swarm]> learning              # Should show cycling tasks
# or
[swarm]> start-learning        # Re-start if stopped
```

---

## Next Steps

1. **Explore the CLI**: Run `python swarm_cli.py` and try all commands
2. **Monitor Learning**: Use `[swarm]> learning` every 60s to see progress
3. **Check Logs**: Review `action_logs/` directory for decision trails
4. **Integrate with Code**: Use REST API in your own scripts
5. **Extend Agents**: Add new agent types to handle specialized tasks

---

## Files Reference

- **swarm_cli.py** - Interactive CLI for control and monitoring
- **ui_server.py** - Flask REST API server (start with `python ui_server.py`)
- **SWARM_API_REFERENCE.md** - Complete REST API documentation
- **action_logs/** - Where learning decisions and execution logs are stored
- **templates/index.html** - Web dashboard

---

**Start with**: `python ui_server.py` in one terminal, then `python swarm_cli.py` in another!
