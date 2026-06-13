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
        self.logs = []

    def get_state(self, key: str, default: Any = None) -> Any:
        """Get value from shared state."""
        return self.state_store.get(self.campaign_id, key, default)

    def set_state(self, key: str, value: Any):
        """Set value in shared state."""
        self.state_store.set(self.campaign_id, key, value)

    def log(self, message: str, level: str = "info", **kwargs):
        """Log with context."""
        getattr(self.logger, level)(message, **kwargs)
        tag = level.upper()
        if tag == "INFO":
            self.logs.append(f"[INFO] {message}")
        elif tag == "WARNING":
            self.logs.append(f"[INFO] WARNING: {message}")
        elif tag == "ERROR":
            self.logs.append(f"[ERROR] {message}")
        else:
            self.logs.append(f"[{tag}] {message}")

    def log_event(self, event_type: str, agent: str, data: Dict[str, Any]):
        """Log an event to campaign history."""
        campaign = self.state_store.get_campaign(self.campaign_id)
        campaign.log_event(event_type, agent, data)
        
        # Add formatted event to detailed logs
        if event_type == "strategy_complete":
            self.logs.append("[STRATEGY] Strategy formulation completed successfully.")
            self.logs.append(f"[DECISION] Positioning defined: {data.get('positioning', '')}")
            self.logs.append(f"[DECISION] North Star Metric: {data.get('north_star_metric', '')}")
        elif event_type == "research_complete":
            self.logs.append("[RESEARCH] Competitor analysis and ICP research completed.")
            for persona in data.get("updated_personas", []):
                self.logs.append(f"[PERSONA CREATED] Mapped persona '{persona.get('name')}' - {persona.get('description', '')[:80]}...")
            for comp in data.get("competitor_insights", []):
                self.logs.append(f"[COMPETITOR ANALYSES] Scanned competitor '{comp.get('competitor')}' - Strengths: {', '.join(comp.get('strengths', []))}")
        elif event_type == "content_generation_complete":
            self.logs.append("[COPYWRITING] Multi-channel copy generation completed.")
            self.logs.append(f"[DRAFT] Created {data.get('x_count', 0)} X/Twitter posts, {data.get('linkedin_count', 0)} LinkedIn posts, and {data.get('email_count', 0)} email sequences.")
        elif event_type == "post_published":
            channel_name = agent.replace("channel_", "").upper()
            self.logs.append(f"[CHANNEL] Published post {data.get('post_id')} to {channel_name} (real: {data.get('real')})")
        elif event_type == "email_sent":
            self.logs.append(f"[CHANNEL] Sent email '{data.get('subject')}' to contact list (real: {data.get('real')})")
        elif event_type == "analytics_complete":
            self.logs.append(f"[ANALYSIS] Aggregate metrics: {data.get('totalImpressions', 0)} impressions, {data.get('totalClicks', 0)} clicks, {data.get('totalSignups', 0)} signups (CTR: {data.get('ctr', 0):.2f}%)")
            for rec in data.get("recommendations", []):
                self.logs.append(f"[RECOMMENDATION] {rec}")
        else:
            self.logs.append(f"[INFO] Event {event_type} logged by {agent}")


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