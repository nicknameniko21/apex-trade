# CONTROL YOUR SWARM - Complete Guide

## TL;DR - 30 Second Start

```bash
# Terminal 1: Start the swarm system
python ui_server.py

# Terminal 2: Control it with CLI
python swarm_cli.py

# Then in CLI:
[swarm]> status        # See what's running
[swarm]> learning      # Monitor learning progress
[swarm]> generate      # Create tasks
[swarm]> help          # See all commands
```

---

## The Three Ways to Control Your Swarm

### 1️⃣ **Interactive CLI (EASIEST - Start Here!)**
```bash
python swarm_cli.py
```

This is your **dashboard and control center** in the terminal.

**Commands:**
```
status              → See agent status
agents              → List all agents
learning            → Show learning progress
generate            → Create new tasks
start-learning      → Resume auto-learning
stop-learning       → Pause auto-learning
scripts             → List Pine Scripts
tasks               → Current tasks
github-status       → GitHub integration info
help                → Show all commands
quit                → Exit
```

**Example:**
```
[swarm]> status
[*] SWARM STATUS:
Server: [OK] ONLINE (http://localhost:5000)
Agents Registered: 3
  [OK] code_executor_01  | Role: EXECUTOR | Status: idle
  [OK] data_analyst_01   | Role: EXECUTOR | Status: idle
  [OK] optimizer_01      | Role: EXECUTOR | Status: idle
```

---

### 2️⃣ **Web Dashboard (Visual)**
Open browser: `http://localhost:5000`

Shows:
- Live agent status
- Learning metrics
- Task queue
- Pine Scripts
- Real-time updates

---

### 3️⃣ **REST API (Programmatic)**

```bash
# Check status
curl http://localhost:5000/api/agents

# Start learning
curl -X POST http://localhost:5000/api/swarm/learning/start

# Generate tasks
curl -X POST http://localhost:5000/api/swarm/generate-tasks \
  -H "Content-Type: application/json" \
  -d '{"type": "learning"}'

# Check progress
curl http://localhost:5000/api/swarm/learning-status
```

Full API docs: See [SWARM_API_REFERENCE.md](SWARM_API_REFERENCE.md)

---

## What's Actually Running?

```
┌─────────────────────────────┐
│  Your Commands              │
│  (CLI / Web / API)          │
└──────────────┬──────────────┘
               ↓
┌─────────────────────────────────────────────┐
│  Flask Server (port 5000)                   │
│  - Receives your commands                   │
│  - Manages REST endpoints                   │
└──────────────┬──────────────────────────────┘
               ↓
┌──────────────────────────────────────────────┐
│  Swarm Intelligence Agent (Orchestrator)     │
│  - Coordinates 3 specialized agents          │
│  - Assigns tasks based on capabilities       │
│  - Tracks execution and learning             │
└──────────────┬───────────────────────────────┘
               ↓
┌───────────────────────────────────────────────┐
│  Three Autonomous Agents (Background)         │
│  - CodeExecutor    → Analyzes code            │
│  - DataAnalyst     → Processes data           │
│  - Optimizer       → Optimizes performance    │
│  Each learns from every task executed        │
└───────────────────────────────────────────────┘
               ↓
┌───────────────────────────────────────────────┐
│  Continuous Learning Loop (Every 60 seconds)  │
│  - Generates 6 learning tasks                │
│  - Assigns to agents                         │
│  - Executes sequentially                     │
│  - Records success/failure patterns          │
│  - Saves state to disk                       │
│  - Repeats forever (autonomous)              │
└───────────────────────────────────────────────┘
```

---

## Complete Workflow

### Step 1: Start the Server
```bash
cd c:\Users\rhuam\Documents\GitHub\apex-trade
python ui_server.py
```

**You should see:**
```
INFO:__main__:Swarm and autonomous agents initialized
INFO:__main__:Background learning loop started
INFO:__main__:Starting Swarm Intelligence UI on http://localhost:5000
 * Running on http://127.0.0.1:5000

INFO:__main__:Learning cycle 1 starting...
INFO:__main__:Cycle 1: Generated 6 tasks
INFO:__main__:Cycle 1: Executed 6 tasks
INFO:__main__:Learning state saved with 3 agents
```

✅ **The swarm is now running autonomously in the background!**

### Step 2: In Another Terminal, Start the CLI
```bash
python swarm_cli.py
```

**You'll see:**
```
======================================================================
===========  APEX TRADE SWARM INTELLIGENCE CONTROL CENTER  ===========
======================================================================

Welcome to Swarm Intelligence Control Center!
Type 'help' for available commands or 'quit' to exit.

[swarm]>
```

### Step 3: Control It
```bash
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
```

---

## Real Examples

### Monitor Learning Progress
```bash
[swarm]> learning      # Run every 60 seconds to watch it learn
```

### See All Agents and Capabilities
```bash
[swarm]> agents

[*] REGISTERED AGENTS:
----------------------------------------------------------------------

  ID: code_executor_01
  Name: Code Executor
  Role: EXECUTOR
  Status: idle
  Capabilities: code_analysis, code_execution

  ID: data_analyst_01
  Name: Data Analyst
  Role: EXECUTOR
  Status: idle
  Capabilities: data_analysis, reporting

  ID: optimizer_01
  Name: Optimizer
  Role: EXECUTOR
  Status: idle
  Capabilities: performance_optimization, metrics_analysis
----------------------------------------------------------------------
```

### Check Trading Strategies
```bash
[swarm]> scripts

[*] PINE SCRIPTS:
----------------------------------------------------------------------
  [OK] rsi_strategy            | Type: strategy
  [OK] ma_crossover            | Type: strategy
  [OK] volatility              | Type: indicator
----------------------------------------------------------------------
```

### Pause/Resume Learning
```bash
[swarm]> stop-learning
[+] Learning loop stopped

[swarm]> start-learning
[+] Learning loop started
   Tasks will be generated and executed every 60 seconds
   (Run 'learning' command to monitor progress)
```

---

## Monitoring Tools

### In CLI (Recommended)
```bash
python swarm_cli.py
[swarm]> learning
[swarm]> learning    # Run again after 60 seconds
```

### Via Web Browser
```
http://localhost:5000
```
Real-time dashboard with agent status and metrics.

### Via Log Files
```bash
# View execution log
cat action_logs/swarm_execution.log

# View learning state
cat action_logs/learning_state.json | python -m json.tool

# View code execution log
cat action_logs/code_execution.log
```

### Via REST API
```bash
curl http://localhost:5000/api/swarm/learning-status | python -m json.tool
```

---

## What's Happening Automatically

**Right now, while you read this, your swarm is:**

✓ Generating 6 learning tasks every 60 seconds
✓ Assigning them to 3 specialized agents
✓ Executing them in sequence
✓ Recording which tasks succeed/fail
✓ Learning patterns to improve strategy
✓ Saving all decisions to disk
✓ Repeating this cycle indefinitely
✓ Listening for your REST API commands
✓ Ready to be controlled via CLI/Web/API

**No manual intervention needed** - it's completely autonomous!

---

## Python Code Integration

```python
import requests

BASE_URL = "http://localhost:5000"

# Get swarm status
response = requests.get(f"{BASE_URL}/api/agents")
agents = response.json()
print(f"Running agents: {len(agents['agents'])}")

# Start learning
requests.post(f"{BASE_URL}/api/swarm/learning/start")

# Check progress
response = requests.get(f"{BASE_URL}/api/swarm/learning-status")
status = response.json()
print(f"Success rate: {status['success_rate']}")

# Generate tasks
response = requests.post(f"{BASE_URL}/api/swarm/generate-tasks",
                        json={"type": "learning"})
print(f"Tasks created: {response.json()['tasks_generated']}")
```

---

## Quick Commands Reference

| Command | What It Does |
|---------|------------|
| `status` | Show swarm health and agent status |
| `agents` | List all agents with capabilities |
| `tasks` | Show current task queue |
| `learning` | Display learning progress metrics |
| `generate` | Create and execute tasks immediately |
| `start-learning` | Resume autonomous 60-second cycles |
| `stop-learning` | Pause autonomous operation |
| `scripts` | List Pine Script trading strategies |
| `validate-script rsi_strategy` | Check if a script is valid |
| `github-status` | Show GitHub integration info |
| `help` | Show all commands |
| `quit` | Exit the CLI |

---

## Troubleshooting

### CLI says "Cannot connect to Swarm server"
```bash
# Start the server first!
python ui_server.py
```

### CLI shows 0 agents
```bash
# Wait 5 seconds for initialization, then:
[swarm]> status
```

### Learning seems stuck
```bash
# Check if loop is running:
[swarm]> learning

# If not updating, restart:
[swarm]> stop-learning
[swarm]> start-learning
```

### Port 5000 in use
```bash
# Find and kill process on port 5000:
# PowerShell: Get-NetTCPConnection -LocalPort 5000 | Stop-Process -Force
```

---

## Files You Need

```
.
├── ui_server.py                   # Start this: python ui_server.py
├── swarm_cli.py                   # Run this: python swarm_cli.py
├── QUICK_START_GUIDE.md           # You're reading this!
├── SWARM_API_REFERENCE.md         # API documentation
├── agents/
│   ├── swarm_intelligence_agent.py
│   ├── autonomous_execution_agent.py
│   ├── autonomous_task_generator.py
│   └── pine_scripts_manager.py
├── pine_scripts/                  # Trading strategies
│   ├── rsi_strategy.pine
│   ├── ma_crossover.pine
│   └── volatility.pine
├── action_logs/                   # Where decisions are saved
├── templates/
│   └── index.html                 # Web dashboard
```

---

## Next Steps

1. **Start the system**: `python ui_server.py`
2. **Open CLI**: `python swarm_cli.py` (in another terminal)
3. **Check status**: `[swarm]> status`
4. **Watch learning**: `[swarm]> learning`
5. **Try commands**: `[swarm]> help`
6. **Explore dashboard**: `http://localhost:5000`
7. **Read API docs**: See [SWARM_API_REFERENCE.md](SWARM_API_REFERENCE.md)

---

## Summary

You now have **complete control** over your autonomous swarm system through:

✅ **Interactive CLI** - `python swarm_cli.py`
✅ **Web Dashboard** - `http://localhost:5000`
✅ **REST API** - Full programmatic access
✅ **Autonomous Learning** - Runs continuously in background
✅ **Complete Logging** - All decisions saved

**The swarm is ready. Take command!**

```bash
python ui_server.py &
python swarm_cli.py
```

Then type: `[swarm]> status`

---

*Last Updated: 2026-02-08*
*For API details see: SWARM_API_REFERENCE.md*
*For advanced setup see: .github/copilot-instructions.md*
