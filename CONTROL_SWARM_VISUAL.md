# HOW TO CONTROL YOUR SWARM - Visual Summary

## The Problem You Had
> "I don't see how to control or chat with codex or swarm"

## The Solution (Three Options)

---

## OPTION 1: Interactive CLI ⭐ START HERE

```
┌─────────────────────────────────────────────────┐
│ python swarm_cli.py                             │
├─────────────────────────────────────────────────┤
│                                                 │
│ ======= SWARM INTELLIGENCE CONTROL =======   │
│                                                 │
│ [swarm]> status                                 │
│ [*] SWARM STATUS:                               │
│ Agents Registered: 3                            │
│   [OK] code_executor_01    │ EXECUTOR │ idle   │
│   [OK] data_analyst_01     │ EXECUTOR │ idle   │
│   [OK] optimizer_01        │ EXECUTOR │ idle   │
│                                                 │
│ [swarm]> learning                               │
│ [*] LEARNING STATUS:                            │
│ Success Rate: 100%                              │
│ Total Tasks: 12                                 │
│ Completed: 12                                   │
│ Failed: 0                                       │
│                                                 │
│ [swarm]> generate                               │
│ [+] TASKS GENERATED: 6                          │
│ [+] TASKS EXECUTED: 6/6                         │
│                                                 │
│ [swarm]> quit                                   │
│                                                 │
└─────────────────────────────────────────────────┘

FEATURES:
✓ 12 commands (status, agents, learning, generate, etc)
✓ Real-time monitoring
✓ Easy to use
✓ Windows PowerShell compatible
✓ Perfect for beginners
```

### Available Commands:
```
status         - See swarm health
agents         - List all agents  
tasks          - Current task queue
learning       - Learning progress
generate       - Create tasks now
start-learning - Resume auto-mode
stop-learning  - Pause auto-mode
scripts        - Trading strategies
help           - Show all commands
quit           - Exit
```

---

## OPTION 2: Web Dashboard 🌐

```
Open in browser:
http://localhost:5000

SHOWS:
✓ Live agent status
✓ Learning metrics
✓ Task queue
✓ Pine Scripts
✓ Real-time updates
✓ Pretty interface
```

---

## OPTION 3: REST API 🔌

```bash
# Get status
curl http://localhost:5000/api/agents

# Start learning
curl -X POST http://localhost:5000/api/swarm/learning/start

# Check progress  
curl http://localhost:5000/api/swarm/learning-status

# Generate tasks
curl -X POST http://localhost:5000/api/swarm/generate-tasks \
  -H "Content-Type: application/json" \
  -d '{"type": "learning"}'

# In Python:
import requests
requests.get("http://localhost:5000/api/agents")
```

---

## Quick Start (30 seconds)

### Terminal 1:
```bash
python ui_server.py
# Server starts and runs autonomously
```

### Terminal 2:
```bash
python swarm_cli.py

[swarm]> status         # See it
[swarm]> learning       # Monitor it
[swarm]> generate       # Control it
[swarm]> help          # Learn commands
```

---

## What Happens Automatically

```
BACKGROUND (Running 24/7)
├─ Every 60 seconds:
│  ├─ Generate 6 learning tasks
│  ├─ Assign to 3 agents
│  ├─ Execute sequentially
│  ├─ Record success/failure
│  ├─ Learn patterns
│  └─ Save to disk
│
└─ Continuously improving
   ├─ Agent success rates increase
   ├─ Pattern recognition improves
   ├─ Better task strategies
   └─ NO manual work needed
```

---

## Real Example Session

```
$ python ui_server.py
INFO:__main__:Background learning loop started
INFO:__main__:Starting Swarm Intelligence UI on http://localhost:5000
 * Running on http://127.0.0.1:5000
INFO:__main__:Learning cycle 1 starting...
INFO:__main__:Cycle 1: Generated 6 tasks
INFO:__main__:Cycle 1: Executed 6 tasks
INFO:__main__:Learning state saved with 3 agents

$ python swarm_cli.py

[swarm]> status
[*] SWARM STATUS:
Server: [OK] ONLINE (http://localhost:5000)
Agents Registered: 3
  [OK] code_executor_01  | Role: EXECUTOR | Status: idle
  [OK] data_analyst_01   | Role: EXECUTOR | Status: idle
  [OK] optimizer_01      | Role: EXECUTOR | Status: idle

[swarm]> learning
[*] LEARNING STATUS:
Total Tasks: 12
Completed: 12
Failed: 0
Success Rate: 100%

Agent Learning Patterns:
  code_executor_01:
    learn_analyze_code: 2 successes, 0 failures
    learn_generate_docs: 2 successes, 0 failures
    learn_optimize_performance: 2 successes, 0 failures
    learn_test_coverage: 2 successes, 0 failures
    learn_refactor_code: 2 successes, 0 failures
    learn_security_audit: 2 successes, 0 failures

[swarm]> generate
[+] TASKS GENERATED:
Generated: 6
Executed: 6
Success: True

[swarm]> scripts
[*] PINE SCRIPTS:
  [OK] rsi_strategy            | Type: strategy
  [OK] ma_crossover            | Type: strategy
  [OK] volatility              | Type: indicator

[swarm]> agents
[*] REGISTERED AGENTS:

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

[swarm]> quit
[*] Goodbye!
```

---

## Architecture Overview

```
┌────────────────────────────────────────────────────────┐
│                YOUR COMMANDS                           │
│          (CLI / Web / API / Python code)               │
└─────────────────────────┬──────────────────────────────┘
                          │
┌─────────────────────────▼──────────────────────────────┐
│         FLASK REST API SERVER (port 5000)              │
│  ✓ 12+ endpoints                                       │
│  ✓ Task management                                     │
│  ✓ Agent control                                       │
│  ✓ Learning status                                     │
│  ✓ Pine Script validation                              │
│  ✓ GitHub integration                                  │
└─────────────────────────┬──────────────────────────────┘
                          │
┌─────────────────────────▼──────────────────────────────┐
│      SWARM INTELLIGENCE AGENT (Orchestrator)           │
│  ✓ Registers agents                                    │
│  ✓ Creates tasks                                       │
│  ✓ Assigns to capabilities                             │
│  ✓ Tracks execution                                    │
│  ✓ Aggregates learning                                 │
└─────────────────────────┬──────────────────────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
┌───────▼───────┐  ┌──────▼──────┐  ┌──────▼──────┐
│   AGENT 1     │  │   AGENT 2   │  │   AGENT 3   │
│ CodeExecutor  │  │ DataAnalyst │  │ Optimizer   │
│               │  │             │  │             │
│ Capabilities: │  │ Capabilit:  │  │ Capabilit:  │
│ - code anal.  │  │ - data anal.│  │ - perf opt. │
│ - execution   │  │ - reporting │  │ - metrics   │
│               │  │             │  │             │
│ Learns from:  │  │ Learns from:│  │ Learns from:│
│ 6 tasks/cycle │  │ 6 tasks/cyc │  │ 6 tasks/cy │
└───────┬───────┘  └──────┬──────┘  └──────┬──────┘
        │                 │                 │
        └─────────────────┼─────────────────┘
                          │
        ┌─────────────────▼─────────────────┐
        │   BACKGROUND LEARNING LOOP        │
        │   (60-second cycles)              │
        │                                   │
        │  Every cycle:                     │
        │  ① Generate 6 learning tasks      │
        │  ② Assign to agents               │
        │  ③ Execute sequentially           │
        │  ④ Record success/failure         │
        │  ⑤ Learn patterns                 │
        │  ⑥ Save state to disk             │
        │  ⑦ Sleep 60 seconds               │
        │  ⑧ Repeat forever                 │
        │                                   │
        │  AUTONOMOUS & CONTINUOUS          │
        └───────────────────────────────────┘
```

---

## File Guide

| File | Purpose |
|------|---------|
| `swarm_cli.py` | **⭐ START HERE** - Interactive CLI |
| `ui_server.py` | Start this first - REST API server |
| `CONTROL_YOUR_SWARM.md` | Detailed control guide |
| `QUICK_START_GUIDE.md` | Step-by-step tutorial |
| `SWARM_API_REFERENCE.md` | REST API documentation |
| `CONTINUOUS_LEARNING_STATUS.md` | Learning system status |
| `templates/index.html` | Web dashboard |
| `action_logs/` | Where decisions are saved |

---

## TL;DR

**You asked**: "How do I control the swarm?"

**Answer**: Three ways!

1. **CLI (Easiest)**: `python swarm_cli.py`
2. **Web**: `http://localhost:5000`  
3. **API**: `curl http://localhost:5000/api/agents`

**Right now** the swarm is running autonomously in the background, learning and improving every 60 seconds.

**You** now have complete control to:
- Monitor its progress
- Trigger tasks
- Start/stop learning
- View metrics
- All via CLI, web, or code

**Start with**: `python ui_server.py` then `python swarm_cli.py`

---

## Next Command to Run

```bash
python swarm_cli.py
```

Then type:
```
[swarm]> status
[swarm]> help
```

That's it. You're in control! 🚀
