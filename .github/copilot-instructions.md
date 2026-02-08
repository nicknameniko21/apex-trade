# GitHub Copilot Instructions for apex-trade

This is a **multi-agent AI orchestration platform** built to coordinate multiple specialized AI models and autonomous agents for task execution, learning, and continuous evolution.

## Architecture Overview

**Core Philosophy**: Swarm intelligence with autonomous learning and cross-session persistence.

```
Mobile/Termux Interface
    ↓
SwarmIntelligenceAgent (central coordinator) → agents/ directory
    ↓
AutonomousExecutionAgents (specialized learners)
    ↓
Pine Scripts Trading Strategies → pine_scripts/ directory
    ↓
MCP Server Integration (external AI models)
    ↓
UI Server (Flask REST API + web dashboard)
```

**Key Components**:
- `agents/swarm_intelligence_agent.py` - Core orchestrator managing agent registry, task queues, and execution
- `agents/autonomous_execution_agent.py` - Individual agents with decision-making and pattern learning; **CodeExecutionAgent now has GitHub integration**
- `agents/pine_scripts_manager.py` - Pine Script loading, validation, and auto-repair
- `agents/pine_scripts_auto_sync.py` - Automatic syncing from external Pine repository
- `mcp_server.py` - Model Context Protocol server for external integrations
- `ui_server.py` - Flask web server exposing REST endpoints for agent, script, and GitHub management
- `pine_scripts/` - Trading strategies in Pine Script format
- `templates/index.html` - Web dashboard for monitoring agents, tasks, and trading strategies

## Critical Design Patterns

### 1. Agent Registration & Task Assignment
Agents are registered with specific **roles** (COORDINATOR, ANALYZER, EXECUTOR, MONITOR, COMMUNICATOR) and capabilities lists. Tasks are created as dataclass objects with priority, status, and result fields. The swarm assigns tasks based on agent capabilities—not random distribution.

**Example pattern** (from `swarm_intelligence_agent.py`):
```python
agent = swarm.register_agent(agent_id, name, role=AgentRole.EXECUTOR, 
                             capabilities=["task_analysis", "data_processing"])
task = Task(task_id="t1", description="...", priority=1)
swarm.assign_task(task, agent_id)  # capability-aware assignment
```

### 2. Autonomous Learning Loop
Agents learn from execution results by storing patterns (success/failure counts) and adjusting strategy. **Do NOT create new learning mechanisms**—extend the existing `learned_patterns` dict and `learn_from_execution()` method. ExecutionStrategy defaults to ADAPTIVE (evaluates past patterns before deciding).

### 3. Persistent Memory Across Sessions
The codebase prioritizes cross-session persistence. Auto-backup (`auto_backup.sh`/`auto_backup.ps1`) commits decisions to git. New features should preserve state in `action_logs/` or filesystem paths defined in `__init__`.

### 4. Permission Framework
CEO authority is implicit in the codebase (`CEO: HomicidalRage` in README). Autonomous operations are pre-authorized in `automation_config.json`. Do NOT add new operations requiring approval—extend existing ones.

## Project-Specific Conventions

- **Logging**: Always use `logging.basicConfig(level=logging.INFO)` at module import and `logger = logging.getLogger(__name__)`
- **Paths**: Use `pathlib.Path` for all file operations; workspace_dir defaults to `Path.cwd()`
- **Dataclasses**: Use `@dataclass` with `__post_init__` for timestamps (e.g., `created_at = datetime.now().isoformat()`)
- **Enums**: Define role/strategy enums before classes (AgentRole, ExecutionStrategy)
- **Async**: Use `asyncio.Queue` for task queues (already initialized in SwarmIntelligenceAgent)
- **Web API**: Flask routes return `jsonify()` dicts; agents are serialized via `asdict()`

## Workflows & Build Commands

**Starting the system**:
```bash
# Option 1: Auto-startup (if available)
python cto_self_sustaining_startup.py

# Option 2: Direct execution
python ui_server.py  # Starts Flask on port 5000
python mcp_server.py  # Starts MCP server (if needed)
```

**Testing**: No test runner configured. Validation is manual or through integration_test.py.

**Logging**: Check `action_logs/swarm_execution.log` and `action_logs/session_report.md` for decision trails.

## Integration Points

- **Pine Scripts**: Located in `pine_scripts/` directory. Auto-discovered, validated, and repaired on startup via `PineScriptsManager`. Broken scripts (like volatility indicator) are fixed automatically.
- **Pine Scripts Auto-Sync**: `PineScriptsAutoSync` monitors external repository and syncs updates hourly. Configured in `automation_config.json`.
- **REST Endpoints**: Flask routes in `ui_server.py` expose `/api/pine-scripts/` endpoints for listing, validating, and fixing scripts.
- **GitHub Integration**: `CodeExecutionAgent` now has native GitHub support via `/api/github/` endpoints (push, pull, branch creation). All code execution auto-commits to GitHub.
- **MCP Servers**: External AI models are integrated via `MCPServer.get_tools()`. New tools should follow the `{"name", "description", "parameters"}` dict format.
- **GitHub Auto-Sync**: Automated via `auto_backup.sh` (5-minute interval default in config). CodeExecutionAgent provides programmatic GitHub access.
- **Decision Logging**: All autonomous decisions logged to `action_logs/autonomous_decisions.md` and `action_logs/code_execution.log`.

## When Extending This Codebase

1. **Adding new agent types**: Create subclass of `AutonomousAgent`, override `make_decision()` and `learn_from_execution()`
2. **Adding new roles/strategies**: Extend `AgentRole` or `ExecutionStrategy` enums
3. **Adding new tools/capabilities**: Update MCP tool list in `mcp_server.py` and swarm agent capabilities list
4. **Modifying task processing**: Update `SwarmIntelligenceAgent.execute_task()` logic; preserve existing task queue structure

## Files to Understand Before Major Changes

- [CORE_STORY.md](CORE_STORY.md) - High-level vision and system capabilities
- [integration_frameworks/multi_agent_collaboration_framework.md](integration_frameworks/multi_agent_collaboration_framework.md) - Swarm parallelization strategy
- [agents/NLP_CAPABILITIES.md](agents/NLP_CAPABILITIES.md) - Natural language interaction design
- [automation_config.json](automation_config.json) - Operational parameters (intervals, auto-features)

## Known Constraints

- **Python 3.11+** required for typing features
- **No external ML libraries**: Agent learning is pattern-based (count aggregation), not model-based
- **Single-machine coordination**: Swarm orchestrator runs on one host (PC or Termux)
- **Synchronous task execution**: Despite `asyncio.Queue`, actual task execution is sequential unless explicitly parallelized in strategy

---

*Last Updated: February 8, 2026*  
*For questions, reference the decision logs in `action_logs/autonomous_decisions.md`*
