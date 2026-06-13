"""State management for GMACHIE campaign execution."""

from typing import Any, Dict
from dataclasses import dataclass, field
from datetime import datetime
import uuid


@dataclass
class CampaignState:
    """State for a single campaign execution."""
    campaign_id: str
    business_info: Dict[str, Any]
    goal: str
    created_at: datetime = None
    current_phase: str = "initial"
    data: Dict[str, Any] = field(default_factory=dict)
    history: list[Dict[str, Any]] = field(default_factory=list)

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow()

    def get(self, key: str, default: Any = None) -> Any:
        """Get value from state data."""
        return self.data.get(key, default)

    def set(self, key: str, value: Any):
        """Set value in state data."""
        self.data[key] = value

    def log_event(self, event_type: str, agent: str, data: Dict[str, Any]):
        """Log an event to history."""
        self.history.append({
            "timestamp": datetime.utcnow(),
            "agent": agent,
            "event": event_type,
            "data": data
        })


class StateStore:
    """In-memory state store for campaign execution."""

    def __init__(self):
        self._states: Dict[str, CampaignState] = {}
        self.logger = None

    def create_campaign(self, business_info: Dict[str, Any], goal: str) -> str:
        """Create a new campaign state and return its ID."""
        campaign_id = str(uuid.uuid4())[:8]
        state = CampaignState(
            campaign_id=campaign_id,
            business_info=business_info,
            goal=goal
        )
        self._states[campaign_id] = state
        return campaign_id

    def add_campaign(self, state: CampaignState):
        """Manually add a campaign state."""
        self._states[state.campaign_id] = state

    def get_campaign(self, campaign_id: str) -> CampaignState:
        """Get campaign state by ID."""
        if campaign_id not in self._states:
            raise KeyError(f"Campaign {campaign_id} not found")
        return self._states[campaign_id]

    def get(self, campaign_id: str, key: str, default: Any = None) -> Any:
        """Get value from a campaign's state."""
        campaign = self.get_campaign(campaign_id)
        return campaign.get(key, default)

    def set(self, campaign_id: str, key: str, value: Any):
        """Set value in a campaign's state."""
        campaign = self.get_campaign(campaign_id)
        campaign.set(key, value)

    def exists(self, campaign_id: str) -> bool:
        """Check if campaign exists."""
        return campaign_id in self._states

    def list_campaigns(self) -> list[str]:
        """List all campaign IDs."""
        return list(self._states.keys())

    def cleanup_old_campaigns(self, max_age_hours: int = 24):
        """Remove old campaigns to prevent memory leaks."""
        # Implementation left for demo simplicity
        pass