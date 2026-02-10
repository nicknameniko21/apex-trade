# Local Development Guide

This guide covers running the Swarm Intelligence Control Center locally for development.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git

## Setup

### 1. Clone and Install

```bash
# Clone the repository
git clone https://github.com/nicknameniko21/apex-trade.git
cd apex-trade

# Install dependencies
pip install -r requirements.txt
```

### 2. Verify Installation

```bash
# Check Python version
python --version  # Should be 3.8+

# Check installed packages
pip list | grep -E "(Flask|flask-cors)"
```

## Running the Application

### Start the Server

```bash
python ui_server.py
```

Expected output:
```
INFO:agents.swarm_intelligence_agent:Swarm and autonomous agents initialized
INFO:ui_server:Starting Swarm Intelligence UI on http://localhost:5000
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://[your-ip]:5000
```

### Access the Application

Open your browser to:
- **Web UI**: http://localhost:5000
- **API Status**: http://localhost:5000/api/status
- **Agent List**: http://localhost:5000/api/agents

## Development Workflow

### Making Changes

1. **Edit Files**: Modify Python files, templates, or agents
2. **Restart Server**: Stop (Ctrl+C) and restart `python ui_server.py`
3. **Test Changes**: Refresh browser or test API endpoints
4. **Check Logs**: View console output for errors

### Project Structure

```
apex-trade/
├── api/
│   └── index.py          # Vercel serverless entrypoint
├── agents/
│   ├── swarm_intelligence_agent.py
│   └── autonomous_execution_agent.py
├── templates/
│   └── index.html        # Web UI
├── ui_server.py          # Main Flask application
├── requirements.txt      # Python dependencies
└── vercel.json          # Vercel configuration
```

### Key Files for Development

- **`ui_server.py`**: Main Flask app with all routes
- **`agents/swarm_intelligence_agent.py`**: Core agent coordination
- **`agents/autonomous_execution_agent.py`**: Autonomous execution agents
- **`templates/index.html`**: Web interface
- **`api/index.py`**: Vercel deployment wrapper

## Testing

### Manual Testing

```bash
# Test API endpoints
curl http://localhost:5000/api/status
curl http://localhost:5000/api/agents
curl http://localhost:5000/api/tasks

# Test agent registration
curl -X POST http://localhost:5000/api/agents/register \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Agent", "role": "EXECUTOR", "capabilities": ["test"]}'

# Test task creation
curl -X POST http://localhost:5000/api/tasks/create \
  -H "Content-Type: application/json" \
  -d '{"description": "Test task", "priority": 5}'
```

### Run Tests

```bash
# Run pytest tests (if available)
pytest copilot_test_project/

# Run specific test file
pytest copilot_test_project/test_script.py -v
```

## Debugging

### Enable Debug Mode

Edit `ui_server.py` (line 358):

```python
# Change from:
app.run(debug=False, host='0.0.0.0', port=5000)

# To:
app.run(debug=True, host='0.0.0.0', port=5000)
```

**Benefits**:
- Auto-reload on file changes
- Detailed error pages
- Interactive debugger

**Warning**: Never use `debug=True` in production!

### View Logs

The application creates logs in:
- **Action Logs**: `action_logs/swarm_execution.log`
- **Console**: Real-time output in terminal

```bash
# Tail logs in real-time
tail -f action_logs/swarm_execution.log

# View recent log entries
tail -20 action_logs/swarm_execution.log
```

### Common Issues

#### Port Already in Use

```bash
# Error: Address already in use
# Solution: Kill the process using port 5000
lsof -ti:5000 | xargs kill -9

# Or use a different port
# Edit ui_server.py line 358: port=5000 -> port=5001
```

#### Import Errors

```bash
# Error: ModuleNotFoundError: No module named 'flask'
# Solution: Reinstall dependencies
pip install -r requirements.txt

# Or install individually
pip install Flask flask-cors
```

#### Template Not Found

```bash
# Error: TemplateNotFound: index.html
# Solution: Ensure templates/ directory exists with index.html
ls -la templates/index.html
```

## Environment Setup

### Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate (macOS/Linux)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Deactivate when done
deactivate
```

### IDE Configuration

#### VS Code

Create `.vscode/settings.json`:

```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/venv/bin/python",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "python.formatting.provider": "black"
}
```

#### PyCharm

1. File → Settings → Project → Python Interpreter
2. Add Interpreter → Virtualenv Environment
3. Select existing environment: `./venv`

## API Development

### Test API with Python

```python
import requests

# Base URL
BASE_URL = "http://localhost:5000"

# Get status
response = requests.get(f"{BASE_URL}/api/status")
print(response.json())

# Create task
task_data = {
    "description": "Test automated task",
    "priority": 3
}
response = requests.post(f"{BASE_URL}/api/tasks/create", json=task_data)
print(response.json())
```

### Test API with JavaScript

```javascript
// Fetch status
fetch('http://localhost:5000/api/status')
  .then(res => res.json())
  .then(data => console.log(data));

// Create agent
fetch('http://localhost:5000/api/agents/register', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    name: 'JS Test Agent',
    role: 'EXECUTOR',
    capabilities: ['javascript', 'testing']
  })
})
  .then(res => res.json())
  .then(data => console.log(data));
```

## Hot Reload Setup

For automatic reloading during development:

```bash
# Install watchdog for file watching
pip install watchdog

# Run with auto-reload (Flask debug mode handles this)
python ui_server.py
```

With debug mode enabled, Flask automatically reloads when files change.

## Performance Testing

### Load Testing

```bash
# Install apache bench
sudo apt-get install apache2-utils  # Linux
brew install httpd  # macOS

# Test with 100 requests, 10 concurrent
ab -n 100 -c 10 http://localhost:5000/api/status

# Load test specific endpoint
ab -n 1000 -c 50 http://localhost:5000/api/agents
```

## Next Steps

1. **Read the Code**: Start with `ui_server.py` to understand routes
2. **Modify Agents**: Customize agents in `agents/` directory
3. **Update UI**: Edit `templates/index.html` for interface changes
4. **Add Features**: Create new routes and agent capabilities
5. **Test Thoroughly**: Test locally before deploying

## Resources

- Flask Documentation: https://flask.palletsprojects.com/
- Python Documentation: https://docs.python.org/3/
- REST API Best Practices: https://restfulapi.net/

---

**Happy Developing!**
