"""Convex client for Python backend to interact with Convex database via REST."""

import httpx
from typing import Any, Dict, Optional
from datetime import datetime
import os
from loguru import logger


class ConvexClient:
    """HTTP client for Convex mutations and queries."""

    def __init__(
        self,
        base_url: str = "http://localhost:3001",
        auth_token: Optional[str] = None,
    ):
        self.base_url = base_url.rstrip("/")
        self.headers = {"Content-Type": "application/json"}
        if auth_token:
            self.headers["Authorization"] = f"Bearer {auth_token}"

    async def call_mutation(self, name: str, args: Dict[str, Any]) -> Any:
        """Call a Convex mutation."""
        url = f"{self.base_url}/api/mutations/{name}"
        payload = {"args": args}
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.post(url, json=payload, headers=self.headers)
                response.raise_for_status()
                return response.json()
            except Exception as e:
                logger.error(f"Convex mutation {name} failed: {e}")
                raise

    async def call_query(self, name: str, args: Optional[Dict[str, Any]] = None) -> Any:
        """Call a Convex query."""
        url = f"{self.base_url}/api/queries/{name}"
        params = {}
        if args:
            # For simple query parameters, use GET params.
            # For complex objects, should use POST with body, but Convex expects GET with query params for simple types.
            # We'll use GET with query params for now, assuming args are simple.
            params = args
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.get(url, params=params, headers=self.headers)
                response.raise_for_status()
                return response.json()
            except Exception as e:
                logger.error(f"Convex query {name} failed: {e}")
                raise

    # Convenience methods

    async def create_campaign(self, business_info: Dict[str, Any], goal: str) -> str:
        """Create a new campaign and return its Convex ID."""
        result = await self.call_mutation("createCampaign", {
            "businessInfo": business_info,
            "goal": goal,
        })
        return result["campaignId"]

    async def update_campaign(self, campaign_id: str, updates: Dict[str, Any]):
        """Update campaign fields."""
        await self.call_mutation("updateCampaign", {
            "campaignId": campaign_id,
            "updates": updates,
        })

    async def log_agent_run(
        self,
        campaign_id: str,
        agent_name: str,
        phase: str,
        input_data: Any,
        output: Any,
        status: str,
        started_at: datetime,
        completed_at: Optional[datetime] = None,
        errors: Optional[list[str]] = None,
    ):
        """Log an agent execution run."""
        await self.call_mutation("logAgentRun", {
            "campaignId": campaign_id,
            "agentName": agent_name,
            "phase": phase,
            "input": input_data,
            "output": output,
            "status": status,
            "startedAt": started_at.isoformat(),
            "completedAt": completed_at.isoformat() if completed_at else None,
            "errors": errors,
        })

    async def create_content(
        self,
        campaign_id: str,
        channel: str,
        type: str,
        body: str,
        status: str,
        title: Optional[str] = None,
        variant: Optional[str] = None,
        published_at: Optional[datetime] = None,
        scheduled_at: Optional[datetime] = None,
        metrics: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Create a content record."""
        result = await self.call_mutation("createContent", {
            "campaignId": campaign_id,
            "channel": channel,
            "type": type,
            "title": title,
            "body": body,
            "variant": variant,
            "status": status,
            "publishedAt": published_at.isoformat() if published_at else None,
            "scheduledAt": scheduled_at.isoformat() if scheduled_at else None,
            "metrics": metrics,
        })
        return result["contentId"]

    async def create_metric(
        self,
        campaign_id: str,
        channel: str,
        metric_type: str,
        value: int,
        recorded_at: datetime,
        content_id: Optional[str] = None,
    ):
        """Create a metric record."""
        await self.call_mutation("createMetric", {
            "campaignId": campaign_id,
            "contentId": content_id,
            "channel": channel,
            "metricType": metric_type,
            "value": value,
            "recordedAt": recorded_at.isoformat(),
        })

    # Queries

    async def get_campaign(self, campaign_id: str) -> Dict[str, Any]:
        """Get campaign by ID."""
        return await self.call_query("getCampaign", {"campaignId": campaign_id})

    async def list_campaigns(self) -> list[Dict[str, Any]]:
        """List all campaigns."""
        return await self.call_query("listCampaigns", {})

    async def get_campaign_content(self, campaign_id: str) -> list[Dict[str, Any]]:
        """Get all content for a campaign."""
        return await self.call_query("getCampaignContent", {"campaignId": campaign_id})

    async def get_campaign_metrics(self, campaign_id: str) -> list[Dict[str, Any]]:
        """Get all metrics for a campaign."""
        return await self.call_query("getCampaignMetrics", {"campaignId": campaign_id})

    async def get_campaign_agent_runs(self, campaign_id: str) -> list[Dict[str, Any]]:
        """Get agent run history for a campaign."""
        return await self.call_query("getCampaignAgentRuns", {"campaignId": campaign_id})


# Global client
_convex_client: Optional[ConvexClient] = None


def get_convex_client() -> ConvexClient:
    global _convex_client
    if _convex_client is None:
        _convex_client = ConvexClient(
            base_url=os.getenv("CONVEX_BASE_URL", "http://localhost:3001"),
            auth_token=os.getenv("CONVEX_AUTH_TOKEN"),
        )
    return _convex_client


def set_convex_client(client: ConvexClient):
    global _convex_client
    _convex_client = client