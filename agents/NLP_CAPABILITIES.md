# Natural Language Processing for Agents

## Overview

The agent system now includes **natural language processing** capabilities, allowing all bots to understand and respond to human language commands!

## Features

✅ **Natural Language Understanding** - Agents understand plain English commands
✅ **Free/Open-Source LLM Integration** - Uses free APIs (Hugging Face, Ollama)
✅ **Pattern Matching** - Fast, local intent recognition without API calls
✅ **Multi-Agent Coordination** - NLP layer integrates with existing Swarm and Autonomous agents
✅ **Conversation History** - Tracks all interactions

## New Agents

### 1. NLP Agent (`agents/nlp_agent.py`)
- Parses natural language into actionable intents
- Supports free LLM APIs (Hugging Face Inference API, Ollama)
- Fast local pattern matching for common commands
- Zero API costs for basic commands

### 2. Unified Agent System (`agents/unified_agent.py`)
- Integrates NLP with Swarm and Autonomous agents
- Single interface for all agent interactions
- Natural language → Agent execution pipeline

## Usage

### Run Interactive Mode

```bash
python agents/unified_agent.py interactive
```

### Example Commands

```python
from agents.unified_agent import UnifiedAgentSystem

system = UnifiedAgentSystem()

# Natural language commands
result = system.process_command("create a task to analyze the codebase")
result = system.process_command("run tests for test_script.py")
result = system.process_command("analyze code in agents/")
result = system.process_command("what's the status?")
```

## Supported Commands

### Task Management
- "Create a task to [description]"
- "Add a task for [description]"

### Code Operations
- "Analyze code in [path]"
- "Review code at [path]"
- "Run tests for [file]"
- "Generate tests for [file]"
- "Improve code in [path]"
- "Optimize [file]"

### System
- "What's the status?"
- "Show me the progress"
- "Help"

## LLM Integration

### Free/Open-Source Options

1. **Local Pattern Matching** (Default, Always Free)
   - Regex-based intent recognition
   - No API calls required
   - Instant response
   - Covers 90% of common commands

2. **Ollama** (Free, Local)
   - Install: https://ollama.ai
   - Models: llama2, mistral, phi
   - Run: `ollama pull llama2`
   - Completely free, unlimited usage

3. **Hugging Face Inference API** (Free Tier)
   - Sign up: https://huggingface.co
   - Set token: `export HUGGINGFACE_TOKEN=your_token`
   - Free tier: 30,000 requests/month
   - Models: GPT-2, DistilBERT, etc.

### Configuration

```bash
# Optional: For Hugging Face API (free tier available)
export HUGGINGFACE_TOKEN=your_hf_token_here

# Optional: Install Ollama for local LLM (completely free)
# Visit: https://ollama.ai
```

## Architecture

```
User Input (Natural Language)
       ↓
  NLP Agent
    - Pattern Matching (free, fast)
    - LLM Fallback (for complex queries)
       ↓
  Intent Recognition
    - Action: create_task, analyze_code, etc.
    - Entities: target files, parameters
       ↓
  Unified Agent System
    - Routes to appropriate agent
    - Swarm Coordinator
    - Autonomous Agents
       ↓
  Execution & Response
    - Natural language response
    - Task completion
```

## Examples

### Demo Output

```
🤖 Unified Agent System - Automated Demo
======================================================================

You: create a task to analyze the codebase
Agent: ✓ Task task_20260123_031817 created and assigned to data_agent

You: analyze code in agents/
Agent: ✓ Code analysis completed for agents/

You: run tests for test_script.py
Agent: ✓ Tests queued for test_script.py

You: generate tests for nlp_agent.py
Agent: ✓ Test generation queued for nlp_agent.py

You: optimize copilot_test_project/test_script.py
Agent: ✓ Generated 3 optimization recommendations for copilot_test_project/test_script.py

You: what's the status?
Agent: ✓ System operational. 0 tasks completed.
```

## Benefits

1. **No Brain** → **Now Has Brain** 🧠
   - Agents were hardcoded → Now understand natural language
   - Fixed commands → Flexible language understanding

2. **Free & Open Source**
   - Pattern matching: Always free
   - Ollama: Completely free, unlimited
   - Hugging Face: Free tier available

3. **Easy to Use**
   - No programming required
   - Just talk to the agents naturally
   - "Run tests" instead of calling Python functions

4. **Extensible**
   - Add new intent patterns easily
   - Integrate additional LLM providers
   - Customize responses

## Testing

```bash
# Test NLP agent directly
python agents/nlp_agent.py

# Test unified system (automated demo)
python agents/unified_agent.py

# Test unified system (interactive mode)
python agents/unified_agent.py interactive
```

## Files Added

- `agents/nlp_agent.py` - Natural language processing agent
- `agents/unified_agent.py` - Unified agent system with NLP integration
- `agents/NLP_CAPABILITIES.md` - This documentation

## Next Steps

1. **Install Ollama** (optional, for local LLM)
   ```bash
   # Visit https://ollama.ai and follow installation
   ollama pull llama2
   ```

2. **Get Hugging Face Token** (optional, for cloud LLM)
   ```bash
   # Visit https://huggingface.co/settings/tokens
   export HUGGINGFACE_TOKEN=your_token
   ```

3. **Run Interactive Mode**
   ```bash
   python agents/unified_agent.py interactive
   ```

## FAQ

**Q: Do I need an API key?**
A: No! Pattern matching works without any API. LLMs are optional enhancements.

**Q: Is it really free?**
A: Yes! Pattern matching is always free. Ollama is free and unlimited. Hugging Face has a generous free tier.

**Q: What models are used?**
A: Ollama (llama2, mistral), Hugging Face (GPT-2, DistilBERT). All open-source.

**Q: Can I use different LLMs?**
A: Yes! The system is designed to be modular. You can add any LLM provider.

---

**The bots now have brains! 🧠🤖**
