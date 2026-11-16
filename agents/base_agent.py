"""
Base Agentic AI Architecture for Cyber Security Operations.

Implements an OODA (Observe-Orient-Decide-Act) deliberation loop,
stateful context memory, and structured reasoning schema for autonomous SOC agents.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, List, Optional


@dataclass
class AgentMessage:
    """Represents a structured communication message between SOC agents."""
    sender_agent: str
    recipient_agent: str
    timestamp: str
    message_type: str  # 'EVALUATION', 'QUERY', 'FORENSIC_EVIDENCE', 'COMMAND', 'SYNTHESIS'
    thought: str
    content: Dict[str, Any]


class BaseSOCAgent(ABC):
    """Abstract Base Class for autonomous security agents."""

    def __init__(self, name: str, role: str, expertise: str):
        self.name = name
        self.role = role
        self.expertise = expertise
        self.memory: List[AgentMessage] = []

    def log_thought(self, recipient: str, message_type: str, thought: str, content: Dict[str, Any]) -> AgentMessage:
        msg = AgentMessage(
            sender_agent=self.name,
            recipient_agent=recipient,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            message_type=message_type,
            thought=thought,
            content=content
        )
        self.memory.append(msg)
        return msg

    @abstractmethod
    def process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the agent's core reasoning and decision process."""
        pass
