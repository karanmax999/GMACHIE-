from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Type
from pydantic import BaseModel
import uuid
from loguru import logger


class AgentResult(BaseModel):
    """Standard output from any agent."""
    success: bool
    agent_name: str
    data: Dict[str, Any]
    errors: Optional[list[str]] = None
    metadata: Optional[Dict[str, Any]] = None

    def model_dump(self, **kwargs) -> Dict[str, Any]:
        return super().model_dump(**kwargs)


class AgentInput(BaseModel):
    """Standard input to any agent."""
    context: Dict[str, Any] = {}
    agent_inputs: Optional[Dict[str, Any]] = None
    task_id: Optional[str] = None

    def model_dump(self, **kwargs) -> Dict[str, Any]:
        return super().model_dump(**kwargs)


class AgentContext:
    """Shared state and utilities for agents during a campaign."""

    def __init__(self, campaign_id: str, state_store: "StateStore"):
        self.campaign_id = campaign_id
        self.state_store = state_store
        self.logger = logger.bind(agent_context=True, campaign_id=campaign_id)

    def get_state(self, key: str, default: Any = None) -> Any:
        """Get value from shared state."""
        return self.state_store.get(self.campaign_id, key, default)

    def set_state(self, key: str, value: Any):
        """Set value in shared state."""
        self.state_store.set(self.campaign_id, key, value)

    def log(self, message: str, level: str = "info", **kwargs):
        """Log with context."""
        getattr(self.logger, level)(message, **kwargs)


class BaseAgent(ABC):
    """Base class for all GTM agents."""

    name: str = "base_agent"
    description: str = ""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.logger = logger.bind(agent_name=self.name)

    @abstractmethod
    async def execute(self, input_data: AgentInput, context: AgentContext) -> AgentResult:
        """Execute the agent's main logic."""
        pass

    def validate_input(self, input_data: AgentInput) -> bool:
        """Validate input before execution."""
        return True

    def get_prompt(self, input_data: AgentInput) -> str:
        """Construct the LLM prompt for this agent."""
        raise NotImplementedError("Agents must implement get_prompt")

    async def call_llm(self, prompt: str, **kwargs) -> str:
        """Call the LLM with the given prompt."""
        # This will be implemented with actual LLM call
        raise NotImplementedError("Must be implemented by subclass or injected")

    def __repr__(self):
        return f"<{self.name}>"


class AgentRegistry:
    """Registry for managing and instantiating agents."""

    def __init__(self):
        self._agents: Dict[str, Type[BaseAgent]] = {}

    def register(self, agent_class: Type[BaseAgent]):
        """Register an agent class."""
        self._agents[agent_class.name] = agent_class
        return agent_class

    def get_agent(self, name: str, config: Optional[Dict] = None) -> BaseAgent:
        """Instantiate an agent by name."""
        if name not in self._agents:
            raise ValueError(f"Agent '{name}' not registered")
        return self._agents[name](config)

    def list_agents(self) -> list[str]:
        """List all registered agent names."""
        return list(self._agents.keys())


# Global registry
registry = AgentRegistry()


def agent(name: str):
    """Decorator to register agents."""
    def decorator(cls):
        registry.register(cls)
        cls.name = name
        return cls
    return decorator