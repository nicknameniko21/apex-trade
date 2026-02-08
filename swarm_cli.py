#!/usr/bin/env python3
"""
Swarm Intelligence Command-Line Interface
Interactive chat/command interface for controlling the apex-trade swarm system
"""

import requests
import json
import sys
import os
from pathlib import Path
from datetime import datetime

# Fix Windows encoding
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    os.environ['PYTHONIOENCODING'] = 'utf-8'

BASE_URL = "http://localhost:5000"

class SwarmCLI:
    def __init__(self):
        self.base_url = BASE_URL
        self.commands = {
            'status': 'Show swarm status and agent information',
            'agents': 'List all registered agents',
            'tasks': 'Show current tasks',
            'learning': 'Show learning status',
            'generate': 'Generate new learning tasks',
            'start-learning': 'Start continuous learning loop',
            'stop-learning': 'Stop continuous learning loop',
            'scripts': 'List Pine Script trading strategies',
            'validate-script': 'Validate a Pine Script',
            'github-status': 'Show GitHub integration status',
            'execute': 'Execute a custom task (advanced)',
            'help': 'Show this help message',
            'quit': 'Exit the CLI'
        }

    def print_header(self):
        print("\n" + "="*70)
        print("  APEX TRADE SWARM INTELLIGENCE CONTROL CENTER  ".center(70, "="))
        print("="*70 + "\n")

    def print_help(self):
        print("\nAvailable Commands:")
        print("-" * 70)
        for cmd, desc in self.commands.items():
            print(f"  {cmd:20} - {desc}")
        print("-" * 70 + "\n")

    def check_server(self):
        """Check if server is running"""
        try:
            resp = requests.get(f"{self.base_url}/api/agents", timeout=2)
            return resp.status_code == 200
        except:
            return False

    def get_swarm_status(self):
        """Get current swarm status"""
        try:
            resp = requests.get(f"{self.base_url}/api/agents")
            if resp.status_code == 200:
                data = resp.json()
                print("\n[*] SWARM STATUS:")
                print("-" * 70)
                print(f"Server: [OK] ONLINE ({self.base_url})")
                print(f"Agents Registered: {len(data.get('agents', []))}")
                
                for agent in data.get('agents', []):
                    status = "[OK]" if agent.get('status') == 'idle' else "[*]"
                    print(f"  {status} {agent.get('id'):20} | Role: {agent.get('role'):10} | Status: {agent.get('status')}")
                print("-" * 70 + "\n")
            else:
                print("[!] Failed to get swarm status")
        except Exception as e:
            print(f"[!] Error: {e}")

    def list_agents(self):
        """List all agents with details"""
        try:
            resp = requests.get(f"{self.base_url}/api/agents")
            if resp.status_code == 200:
                data = resp.json()
                print("\n[*] REGISTERED AGENTS:")
                print("-" * 70)
                for agent in data.get('agents', []):
                    print(f"\n  ID: {agent.get('id')}")
                    print(f"  Name: {agent.get('name')}")
                    print(f"  Role: {agent.get('role')}")
                    print(f"  Status: {agent.get('status')}")
                    print(f"  Capabilities: {', '.join(agent.get('capabilities', []))}")
                print("-" * 70 + "\n")
            else:
                print("[!] Failed to list agents")
        except Exception as e:
            print(f"[!] Error: {e}")

    def show_tasks(self):
        """Show current tasks"""
        try:
            resp = requests.get(f"{self.base_url}/api/tasks")
            if resp.status_code == 200:
                data = resp.json()
                tasks = data.get('tasks', [])
                print("\n[*] TASKS:")
                print("-" * 70)
                if not tasks:
                    print("  No active tasks")
                else:
                    for task in tasks:
                        print(f"\n  ID: {task.get('id')}")
                        print(f"  Description: {task.get('description')}")
                        print(f"  Status: {task.get('status')}")
                        print(f"  Priority: {task.get('priority')}")
                print("-" * 70 + "\n")
            else:
                print("[!] Failed to get tasks")
        except Exception as e:
            print(f"[!] Error: {e}")

    def show_learning_status(self):
        """Show learning status and metrics"""
        try:
            resp = requests.get(f"{self.base_url}/api/swarm/learning-status")
            if resp.status_code == 200:
                data = resp.json()
                print("\n[*] LEARNING STATUS:")
                print("-" * 70)
                print(f"Total Tasks: {data.get('total_tasks', 0)}")
                print(f"Completed: {data.get('completed_tasks', 0)}")
                print(f"Failed: {data.get('failed_tasks', 0)}")
                print(f"Success Rate: {data.get('success_rate', '0')}%")
                
                print("\nAgent Learning Patterns:")
                for agent_id, patterns in data.get('agent_patterns', {}).items():
                    print(f"  {agent_id}:")
                    for task_type, counts in patterns.items():
                        print(f"    {task_type}: {counts['successes']} successes, {counts['failures']} failures")
                print("-" * 70 + "\n")
            else:
                print("[!] Failed to get learning status")
        except Exception as e:
            print(f"[!] Error: {e}")

    def generate_tasks(self, task_type="learning"):
        """Generate new learning tasks"""
        try:
            resp = requests.post(f"{self.base_url}/api/swarm/generate-tasks", 
                               json={"type": task_type})
            if resp.status_code == 200:
                data = resp.json()
                print(f"\n[+] TASKS GENERATED:")
                print("-" * 70)
                print(f"Generated: {data.get('tasks_generated', 0)}")
                print(f"Executed: {data.get('tasks_executed', 0)}")
                print(f"Success: {data.get('results', {}).get('success', False)}")
                print("-" * 70 + "\n")
            else:
                print("[!] Failed to generate tasks")
        except Exception as e:
            print(f"[!] Error: {e}")

    def start_learning(self):
        """Start continuous learning loop"""
        try:
            resp = requests.post(f"{self.base_url}/api/swarm/learning/start")
            if resp.status_code == 200:
                print("\n[+] Learning loop started")
                print("   Tasks will be generated and executed every 60 seconds")
                print("   (Run 'learning' command to monitor progress)\n")
            else:
                print("[!] Failed to start learning")
        except Exception as e:
            print(f"[!] Error: {e}")

    def stop_learning(self):
        """Stop continuous learning loop"""
        try:
            resp = requests.post(f"{self.base_url}/api/swarm/learning/stop")
            if resp.status_code == 200:
                print("\n[+] Learning loop stopped\n")
            else:
                print("[!] Failed to stop learning")
        except Exception as e:
            print(f"[!] Error: {e}")

    def list_scripts(self):
        """List Pine Script trading strategies"""
        try:
            resp = requests.get(f"{self.base_url}/api/pine-scripts")
            if resp.status_code == 200:
                data = resp.json()
                print("\n[*] PINE SCRIPTS:")
                print("-" * 70)
                for script in data.get('scripts', []):
                    status = "[OK]" if script.get('valid') else "[!]"
                    print(f"  {status} {script.get('name'):20} | Type: {script.get('type')}")
                print("-" * 70 + "\n")
            else:
                print("[!] Failed to list scripts")
        except Exception as e:
            print(f"[!] Error: {e}")

    def validate_script(self, script_name):
        """Validate a Pine Script"""
        try:
            resp = requests.get(f"{self.base_url}/api/pine-scripts/validate/{script_name}")
            if resp.status_code == 200:
                data = resp.json()
                print(f"\n[*] VALIDATION RESULT for {script_name}:")
                print("-" * 70)
                print(f"Valid: {'[OK] Yes' if data.get('valid') else '[!] No'}")
                if data.get('errors'):
                    print(f"Errors: {', '.join(data.get('errors', []))}")
                print("-" * 70 + "\n")
            else:
                print(f"[!] Script '{script_name}' not found")
        except Exception as e:
            print(f"[!] Error: {e}")

    def run(self):
        """Main CLI loop"""
        if not self.check_server():
            print("\n[!] ERROR: Cannot connect to Swarm server at", self.base_url)
            print("   Start the server with: python ui_server.py\n")
            return

        self.print_header()
        print("Welcome to Swarm Intelligence Control Center!")
        print("Type 'help' for available commands or 'quit' to exit.\n")

        while True:
            try:
                user_input = input("[swarm]> ").strip().lower()
                
                if not user_input:
                    continue

                if user_input == 'help':
                    self.print_help()
                elif user_input == 'quit' or user_input == 'exit':
                    print("\n[*] Goodbye!\n")
                    break
                elif user_input == 'status':
                    self.get_swarm_status()
                elif user_input == 'agents':
                    self.list_agents()
                elif user_input == 'tasks':
                    self.show_tasks()
                elif user_input == 'learning':
                    self.show_learning_status()
                elif user_input == 'generate':
                    self.generate_tasks("learning")
                elif user_input == 'start-learning':
                    self.start_learning()
                elif user_input == 'stop-learning':
                    self.stop_learning()
                elif user_input == 'scripts':
                    self.list_scripts()
                elif user_input.startswith('validate-script '):
                    script_name = user_input.split('validate-script ', 1)[1]
                    self.validate_script(script_name)
                elif user_input == 'github-status':
                    print("\n[+] GitHub Integration: Active")
                    print("   CodeExecutionAgent has native GitHub support")
                    print("   Endpoints: /api/github/push, /api/github/pull, /api/github/branch\n")
                else:
                    print(f"[!] Unknown command: '{user_input}'")
                    print("   Type 'help' for available commands\n")

            except KeyboardInterrupt:
                print("\n\n[*] Goodbye!\n")
                break
            except Exception as e:
                print(f"[!] Error: {e}\n")

if __name__ == '__main__':
    cli = SwarmCLI()
    cli.run()
