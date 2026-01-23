#!/usr/bin/env python3
"""
Natural Language Processing Agent
Provides natural language understanding capabilities for agent interactions
Uses free/open-source LLM APIs for language processing
"""

import json
import logging
import os
import requests
from typing import Dict, List, Any, Optional
from datetime import datetime
from dataclasses import dataclass
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class NLPIntent:
    """Represents a parsed natural language intent"""
    action: str
    entities: Dict[str, Any]
    confidence: float
    raw_text: str
    timestamp: str = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()


class FreeNLPProvider:
    """Free/Open-source NLP API provider"""
    
    def __init__(self):
        self.providers = {
            "huggingface": {
                "url": "https://api-inference.huggingface.co/models/{model}",
                "models": {
                    "text-generation": "gpt2",
                    "sentiment": "distilbert-base-uncased-finetuned-sst-2-english",
                    "question-answering": "distilbert-base-cased-distilled-squad"
                },
                "token": os.environ.get("HUGGINGFACE_TOKEN", "")
            },
            "ollama": {
                "url": "http://localhost:11434/api/generate",
                "models": ["llama2", "mistral", "phi"],
                "available": self._check_ollama_available()
            }
        }
    
    def _check_ollama_available(self) -> bool:
        """Check if local Ollama is available"""
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def query_huggingface(self, text: str, task: str = "text-generation") -> Dict[str, Any]:
        """Query Hugging Face Inference API (free tier)"""
        model = self.providers["huggingface"]["models"].get(task, "gpt2")
        url = self.providers["huggingface"]["url"].format(model=model)
        
        headers = {}
        if self.providers["huggingface"]["token"]:
            headers["Authorization"] = f"Bearer {self.providers['huggingface']['token']}"
        
        try:
            response = requests.post(
                url,
                headers=headers,
                json={"inputs": text},
                timeout=10
            )
            if response.status_code == 200:
                return {"success": True, "result": response.json()}
            else:
                return {"success": False, "error": f"HTTP {response.status_code}"}
        except Exception as e:
            logger.warning(f"Hugging Face API error: {e}")
            return {"success": False, "error": str(e)}
    
    def query_ollama(self, text: str, model: str = "llama2") -> Dict[str, Any]:
        """Query local Ollama instance (completely free)"""
        if not self.providers["ollama"]["available"]:
            return {"success": False, "error": "Ollama not available"}
        
        try:
            response = requests.post(
                self.providers["ollama"]["url"],
                json={"model": model, "prompt": text, "stream": False},
                timeout=30
            )
            if response.status_code == 200:
                return {"success": True, "result": response.json()}
            else:
                return {"success": False, "error": f"HTTP {response.status_code}"}
        except Exception as e:
            logger.warning(f"Ollama API error: {e}")
            return {"success": False, "error": str(e)}


class NaturalLanguageAgent:
    """Agent that understands and responds to natural language"""
    
    def __init__(self, agent_id: str = "nlp_agent_01"):
        self.agent_id = agent_id
        self.nlp_provider = FreeNLPProvider()
        self.intent_patterns = self._load_intent_patterns()
        self.conversation_history: List[Dict[str, Any]] = []
        logger.info(f"Natural Language Agent {agent_id} initialized")
    
    def _load_intent_patterns(self) -> Dict[str, List[str]]:
        """Load intent recognition patterns"""
        return {
            "create_task": [
                r"create (?:a )?task (?:to |for )?(.+)",
                r"add (?:a )?task (?:to |for )?(.+)",
                r"new task[:\s]+(.+)",
                r"task[:\s]+(.+)"
            ],
            "analyze_code": [
                r"analyze (?:the )?code (?:in |at )?(.+)",
                r"review (?:the )?code (?:in |at )?(.+)",
                r"check (?:the )?code (?:in |at )?(.+)"
            ],
            "run_tests": [
                r"run (?:the )?tests?(?: for| on)? (.+)",
                r"test (.+)",
                r"execute tests?(?: for| on)? (.+)"
            ],
            "generate_tests": [
                r"generate tests?(?: for)? (.+)",
                r"create tests?(?: for)? (.+)",
                r"write tests?(?: for)? (.+)"
            ],
            "improve_code": [
                r"improve (?:the )?code (?:in |at )?(.+)",
                r"optimize (.+)",
                r"refactor (.+)",
                r"fix (.+)"
            ],
            "status": [
                r"status",
                r"what(?:'s| is) (?:the )?status",
                r"show (?:me )?(?:the )?progress",
                r"how(?:'s| is) it going"
            ],
            "help": [
                r"help",
                r"what can you do",
                r"commands",
                r"capabilities"
            ]
        }
    
    def parse_intent(self, text: str) -> NLPIntent:
        """Parse natural language text into actionable intent"""
        text = text.lower().strip()
        
        # Try pattern matching first (fast, free, no API needed)
        for action, patterns in self.intent_patterns.items():
            for pattern in patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    entities = {}
                    if match.groups():
                        entities["target"] = match.group(1).strip()
                    
                    return NLPIntent(
                        action=action,
                        entities=entities,
                        confidence=0.9,
                        raw_text=text
                    )
        
        # Fallback to LLM for complex queries
        llm_result = self._llm_parse(text)
        if llm_result["success"]:
            return llm_result["intent"]
        
        # Unknown intent
        return NLPIntent(
            action="unknown",
            entities={"text": text},
            confidence=0.3,
            raw_text=text
        )
    
    def _llm_parse(self, text: str) -> Dict[str, Any]:
        """Use LLM to parse complex natural language"""
        # Try Ollama first (free, local, no limits)
        if self.nlp_provider.providers["ollama"]["available"]:
            prompt = f"""Parse this command and extract the action and entities.
Command: {text}

Respond with JSON:
{{"action": "action_name", "entities": {{}}, "confidence": 0.0-1.0}}

Available actions: create_task, analyze_code, run_tests, generate_tests, improve_code, status, help, unknown"""
            
            result = self.nlp_provider.query_ollama(prompt, model="llama2")
            if result["success"]:
                try:
                    # Parse LLM response
                    response_text = result["result"].get("response", "")
                    parsed = json.loads(response_text)
                    return {
                        "success": True,
                        "intent": NLPIntent(
                            action=parsed["action"],
                            entities=parsed["entities"],
                            confidence=parsed["confidence"],
                            raw_text=text
                        )
                    }
                except:
                    pass
        
        return {"success": False}
    
    def generate_response(self, intent: NLPIntent, result: Dict[str, Any]) -> str:
        """Generate natural language response"""
        
        responses = {
            "create_task": f"✓ Task created: {intent.entities.get('target', 'task')}",
            "analyze_code": f"✓ Analyzing code at {intent.entities.get('target', 'specified location')}...",
            "run_tests": f"✓ Running tests for {intent.entities.get('target', 'project')}...",
            "generate_tests": f"✓ Generating tests for {intent.entities.get('target', 'code')}...",
            "improve_code": f"✓ Improving code at {intent.entities.get('target', 'specified location')}...",
            "status": "All systems operational. Ready to assist.",
            "help": """I understand natural language commands! Try:
- "Create a task to analyze the codebase"
- "Run tests for test_script.py"
- "Analyze code in agents/"
- "Generate tests for swarm_intelligence_agent.py"
- "What's the status?"
- "Improve code in copilot_test_project/"
""",
            "unknown": f"I didn't understand: '{intent.raw_text}'. Try 'help' for available commands."
        }
        
        base_response = responses.get(intent.action, "Command processed.")
        
        # Add result details if available
        if result.get("details"):
            base_response += f"\n{result['details']}"
        
        return base_response
    
    def process_natural_language(self, text: str) -> Dict[str, Any]:
        """Process natural language command and return result"""
        logger.info(f"Processing natural language: {text}")
        
        # Parse intent
        intent = self.parse_intent(text)
        logger.info(f"Parsed intent: {intent.action} (confidence: {intent.confidence})")
        
        # Execute action
        result = self._execute_intent(intent)
        
        # Generate response
        response = self.generate_response(intent, result)
        
        # Store in history
        self.conversation_history.append({
            "timestamp": datetime.now().isoformat(),
            "input": text,
            "intent": intent.action,
            "confidence": intent.confidence,
            "response": response,
            "result": result
        })
        
        return {
            "intent": intent,
            "result": result,
            "response": response,
            "success": result.get("success", False)
        }
    
    def _execute_intent(self, intent: NLPIntent) -> Dict[str, Any]:
        """Execute the parsed intent"""
        
        if intent.action == "create_task":
            return {
                "success": True,
                "task_id": f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "description": intent.entities.get("target", ""),
                "details": f"Task created with ID: task_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            }
        
        elif intent.action == "status":
            return {
                "success": True,
                "status": "operational",
                "tasks_completed": len(self.conversation_history),
                "details": f"Processed {len(self.conversation_history)} commands"
            }
        
        elif intent.action == "help":
            return {
                "success": True,
                "details": "Help text provided"
            }
        
        elif intent.action in ["analyze_code", "run_tests", "generate_tests", "improve_code"]:
            return {
                "success": True,
                "action": intent.action,
                "target": intent.entities.get("target", ""),
                "details": f"Action '{intent.action}' queued for execution"
            }
        
        else:
            return {
                "success": False,
                "error": "Unknown action",
                "details": "Try 'help' to see available commands"
            }
    
    def get_conversation_history(self) -> List[Dict[str, Any]]:
        """Get conversation history"""
        return self.conversation_history


# Demonstration
def demo():
    """Demonstrate NLP capabilities"""
    print("🤖 Natural Language Processing Agent Demo")
    print("=" * 60)
    print()
    
    agent = NaturalLanguageAgent()
    
    # Test commands
    test_commands = [
        "create a task to analyze the codebase",
        "run tests for test_script.py",
        "what's the status?",
        "help",
        "analyze code in agents/",
        "improve code in copilot_test_project/"
    ]
    
    for command in test_commands:
        print(f"User: {command}")
        result = agent.process_natural_language(command)
        print(f"Agent: {result['response']}")
        print()
    
    print("=" * 60)
    print(f"✓ Processed {len(agent.conversation_history)} commands")
    print()


if __name__ == "__main__":
    demo()
