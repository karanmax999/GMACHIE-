"""GMACHIE Backend - FastAPI application."""

import os
from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any
import uvicorn

from core.state_store import StateStore
from core.orchestrator import Orchestrator
from integrations.convex_client import ConvexClient, get_convex_client
from integrations.x_client import XClient
from integrations.linkedin_client import LinkedInClient
from integrations.email_client import EmailClient

# Import agents to register them with the global registry
import agents.strategy_agent
import agents.research_agent
import agents.content_agent
import agents.channel_x_agent
import agents.channel_email_agent
import agents.channel_linkedin_agent
import agents.analytics_agent

from loguru import logger

app = FastAPI(title="GMACHIE Backend")

# CORS middleware to allow Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize core components
state_store = StateStore()
convex_client = get_convex_client()

# Build agent configuration from environment variables
agent_config: Dict[str, Any] = {"real_mode": os.getenv("REAL_MODE", "false").lower() == "true"}

if agent_config["real_mode"]:
    # X/Twitter
    twitter_token = os.getenv("TWITTER_ACCESS_TOKEN")
    if twitter_token:
        agent_config["x_client"] = XClient(twitter_token)
        logger.info("X client initialized in real mode")
    else:
        logger.warning("TWITTER_ACCESS_TOKEN not set; X agent will simulate")

    # LinkedIn
    linkedin_token = os.getenv("LINKEDIN_ACCESS_TOKEN")
    linkedin_urn = os.getenv("LINKEDIN_AUTHOR_URN")
    if linkedin_token and linkedin_urn:
        agent_config["linkedin_client"] = LinkedInClient(linkedin_token, linkedin_urn)
        logger.info("LinkedIn client initialized in real mode")
    else:
        logger.warning("LinkedIn credentials missing; LinkedIn agent will simulate")

    # Email (SMTP)
    smtp_host = os.getenv("SMTP_HOST")
    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASSWORD")
    if smtp_host and smtp_user and smtp_pass:
        agent_config["email_client"] = EmailClient(smtp_host, username=smtp_user, password=smtp_pass)
        logger.info("Email client initialized in real mode (SMTP)")
    else:
        logger.warning("SMTP credentials missing; email agent will simulate")

# Create orchestrator with agent_config
orchestrator = Orchestrator(state_store, convex_client, agent_config)


class StartCampaignRequest(BaseModel):
    business_info: Dict[str, Any]
    goal: str
    icp: str = ""


@app.post("/api/campaigns")
async def start_campaign(request: StartCampaignRequest, background_tasks: BackgroundTasks):
    """Start a new GTM campaign."""
    business_info = request.business_info
    goal = request.goal
    icp = request.icp or ""
    business_info_with_icp = {**business_info, "icp": icp}

    try:
        # Create campaign record in Convex and get its ID
        campaign_id = await convex_client.create_campaign(business_info_with_icp, goal)
    except Exception as e:
        logger.error(f"Failed to create campaign in Convex: {e}")
        raise HTTPException(status_code=500, detail="Convex error")

    # Run the campaign in background
    background_tasks.add_task(
        orchestrator.run_campaign,
        business_info_with_icp,
        goal,
        campaign_id=campaign_id
    )

    return {"campaign_id": campaign_id, "status": "started"}


@app.post("/api/campaigns/{campaign_id}/run")
async def run_campaign_cycle(campaign_id: str, background_tasks: BackgroundTasks):
    """Trigger a new GTM cycle for an existing campaign."""
    try:
        campaign = await convex_client.get_campaign(campaign_id)
        if not campaign:
            raise HTTPException(status_code=404, detail="Campaign not found")
        
        # Mark status as running in Convex
        await convex_client.update_campaign(campaign_id, {"status": "running"})
        
        # Trigger background execution
        background_tasks.add_task(
            orchestrator.run_campaign,
            campaign["businessInfo"],
            campaign["goal"],
            campaign_id=campaign_id
        )
        return {"status": "started"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error triggering campaign run {campaign_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to start campaign cycle: {str(e)}")


@app.get("/api/campaigns")
async def list_campaigns():
    """List all campaigns."""
    try:
        return await convex_client.list_campaigns()
    except Exception as e:
        logger.error(f"Error listing campaigns: {e}")
        raise HTTPException(status_code=500, detail="Error fetching campaigns")


@app.get("/api/campaigns/{campaign_id}")
async def get_campaign(campaign_id: str):
    """Get campaign details."""
    try:
        return await convex_client.get_campaign(campaign_id)
    except Exception as e:
        logger.error(f"Error fetching campaign {campaign_id}: {e}")
        raise HTTPException(status_code=404, detail="Campaign not found")


@app.get("/api/campaigns/{campaign_id}/content")
async def get_campaign_content(campaign_id: str):
    """Get content for a campaign."""
    try:
        return await convex_client.get_campaign_content(campaign_id)
    except Exception as e:
        logger.error(f"Error fetching content: {e}")
        raise HTTPException(status_code=500, detail="Error fetching content")


@app.get("/api/campaigns/{campaign_id}/metrics")
async def get_campaign_metrics(campaign_id: str):
    """Get metrics for a campaign."""
    try:
        return await convex_client.get_campaign_metrics(campaign_id)
    except Exception as e:
        logger.error(f"Error fetching metrics: {e}")
        raise HTTPException(status_code=500, detail="Error fetching metrics")


@app.get("/api/campaigns/{campaign_id}/agent-runs")
async def get_campaign_agent_runs(campaign_id: str):
    """Get agent run history for a campaign."""
    try:
        return await convex_client.get_campaign_agent_runs(campaign_id)
    except Exception as e:
        logger.error(f"Error fetching agent runs: {e}")
        raise HTTPException(status_code=500, detail="Error fetching agent runs")


if __name__ == "__main__":
    uvicorn.run(app, host=os.getenv("HOST", "0.0.0.0"), port=int(os.getenv("PORT", 8082)))