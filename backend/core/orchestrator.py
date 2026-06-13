"""Orchestrator manages agent execution cycles for GTM campaigns."""

from typing import Dict, Any, Optional
from datetime import datetime
from core.agent import BaseAgent, AgentInput, AgentResult, AgentContext, registry
from core.state_store import StateStore, CampaignState
from integrations.convex_client import ConvexClient, get_convex_client
from loguru import logger


class Orchestrator:
    """Orchestrates multi-agent GTM campaign execution."""

    def __init__(self, state_store: StateStore, convex_client: Optional[ConvexClient] = None,
                 agent_config: Optional[Dict] = None):
        self.state_store = state_store
        self.convex_client = convex_client or get_convex_client()
        self.agent_config = agent_config or {}
        self.registry = registry

    async def run_campaign(
        self,
        business_info: Dict[str, Any],
        goal: str,
        max_cycles: int = 3,
        campaign_id: Optional[str] = None,
        stage: str = "draft",  # "draft", "publish", or "all"
    ) -> Dict[str, Any]:
        """
        Run a GTM campaign cycle.

        Args:
            business_info: Product/company details
            goal: High-level GTM goal
            max_cycles: Max cycles (unused for single stages)
            campaign_id: Optional existing campaign ID (from Convex)
            stage: Stage of campaign execution ("draft", "publish", "all")

        Returns:
            Final campaign state summary
        """
        logger.info(f"Running campaign: {business_info.get('name', 'Unnamed')} - Goal: {goal} - Stage: {stage}")

        # Create campaign in Convex if not provided
        if campaign_id is None:
            campaign_id = await self.convex_client.create_campaign(business_info, goal)
            logger.info(f"Created campaign in Convex with ID: {campaign_id}")
        else:
            logger.info(f"Using provided campaign ID: {campaign_id}")

        # Create local state
        campaign_state = CampaignState(
            campaign_id=campaign_id,
            business_info=business_info,
            goal=goal,
        )
        self.state_store.add_campaign(campaign_state)

        # Create agent context
        context = AgentContext(campaign_id, self.state_store)
        context.set_state("goal", goal)
        context.set_state("business_info", business_info)

        # Set up stage and load details if publishing
        current_cycle = 0
        if stage == "publish":
            campaign_data = await self.convex_client.get_campaign(campaign_id)
            if campaign_data:
                current_cycle = campaign_data.get("currentCycle", 0)
                # Recover campaign state from Convex
                context.set_state("gtmPlan", campaign_data.get("gtmPlan", {}))
                context.set_state("positioning", campaign_data.get("positioning"))
                context.set_state("channels", campaign_data.get("channels", []))
                context.set_state("campaignThemes", campaign_data.get("campaignThemes", []))
                context.set_state("kpiTargets", campaign_data.get("kpiTargets", {}))
                context.set_state("northStarMetric", campaign_data.get("northStarMetric"))
                context.set_state("personas", campaign_data.get("personas", []))
                context.set_state("competitorInsights", campaign_data.get("competitorInsights", []))
                context.set_state("trendingTopics", campaign_data.get("trendingTopics", []))
                context.set_state("recommendedKeywords", campaign_data.get("recommendedKeywords", []))
                context.set_state("contentGaps", campaign_data.get("contentGaps", []))
                
            # Load generated/edited content from Convex
            content_items = await self.convex_client.get_campaign_content(campaign_id)
            x_posts = []
            linkedin_posts = []
            email_campaigns = []
            
            for item in content_items:
                if item.get("status") == "generated":
                    channel = item.get("channel")
                    body = item.get("body", "")
                    variant = item.get("variant")
                    title = item.get("title")
                    
                    if channel == "x":
                        x_posts.append({"text": body, "type": variant or "unknown"})
                    elif channel == "linkedin":
                        linkedin_posts.append({"text": body, "topic": title or "unknown"})
                    elif channel == "email":
                        subject = title or ""
                        email_body = body
                        if subject and body.startswith(f"Subject: {subject}\n\n"):
                            email_body = body[len(f"Subject: {subject}\n\n"):]
                        
                        day = 1
                        if variant and variant.startswith("day"):
                            try:
                                day = int(variant[3:])
                            except ValueError:
                                pass
                        email_campaigns.append({"subject": subject, "body": email_body, "day": day})
            
            context.set_state("x_posts", x_posts)
            context.set_state("linkedin_posts", linkedin_posts)
            context.set_state("email_campaigns", email_campaigns)
            logger.info(f"Recovered {len(x_posts)} X posts, {len(linkedin_posts)} LinkedIn posts, {len(email_campaigns)} emails from Convex.")

        context.set_state("current_cycle", current_cycle)
        context.set_state("current_phase", "agents_running")
        context.set_state("status", "running")

        # Define agent pipeline based on stage
        if stage == "draft":
            agent_sequence = [
                ("strategy", "Strategy Agent"),
                ("research", "Research Agent"),
                ("content", "Content Agent"),
            ]
        elif stage == "publish":
            agent_sequence = [
                ("channel_x", "Channel Agent - X/Twitter"),
                ("channel_linkedin", "Channel Agent - LinkedIn"),
                ("channel_email", "Channel Agent - Email"),
                ("analytics", "Analytics Agent"),
            ]
        else:  # "all"
            agent_sequence = [
                ("strategy", "Strategy Agent"),
                ("research", "Research Agent"),
                ("content", "Content Agent"),
                ("channel_x", "Channel Agent - X/Twitter"),
                ("channel_linkedin", "Channel Agent - LinkedIn"),
                ("channel_email", "Channel Agent - Email"),
                ("analytics", "Analytics Agent"),
            ]

        try:
            # Execute each agent in the sequence
            for agent_name, display_name in agent_sequence:
                start_time = datetime.utcnow()
                context.set_state("current_agent", agent_name)

                # Clear and initialize logs for this agent execution
                context.logs = []
                context.logs.append(f"[INFO] Initializing {display_name}...")

                # Update currentPhase in state and Convex dynamically
                phase_map = {
                    "strategy": "strategy",
                    "research": "research",
                    "content": "content",
                    "channel_x": "executing",
                    "channel_linkedin": "executing",
                    "channel_email": "executing",
                    "analytics": "analytics",
                }
                current_phase = phase_map.get(agent_name, "idle")
                context.set_state("current_phase", current_phase)

                await self.convex_client.update_campaign(campaign_id, {
                    "status": "running",
                    "currentPhase": current_phase,
                })

                # Get agent instance with config (real_mode, clients)
                agent = self.registry.get_agent(agent_name, self.agent_config)

                # Prepare input
                input_data = AgentInput(
                    context=context.state_store.get_campaign(campaign_id).data,
                    task_id=campaign_id,
                )

                result: Optional[AgentResult] = None
                try:
                    result = await agent.execute(input_data, context)
                    if result.success:
                        logger.info(f"{display_name} completed successfully")
                        context.log_event("complete", agent_name, result.data)
                        # Update state with agent output
                        for key, value in result.data.items():
                            context.set_state(key, value)
                    else:
                        logger.error(f"{display_name} failed: {result.errors}")
                        context.log_event("error", agent_name, {"error": result.errors})
                except Exception as e:
                    logger.exception(f"Exception in {display_name}")
                    context.log_event("exception", agent_name, {"error": str(e)})
                    result = AgentResult(
                        success=False,
                        agent_name=agent_name,
                        data={},
                        errors=[str(e)],
                    )
                finally:
                    # Persist agent run and updates to Convex
                    await self._persist_agent_run(campaign_id, agent_name, result, start_time, context)

            if stage == "draft":
                # Halt campaign cycle for human review
                context.set_state("status", "needs_review")
                context.set_state("current_phase", "review")
                await self.convex_client.update_campaign(campaign_id, {
                    "status": "needs_review",
                    "currentPhase": "review",
                })
                logger.info(f"Campaign {campaign_id} drafted. Paused for human review.")
            else:
                # Finalize publishing stage
                context.set_state("status", "completed")
                context.set_state("current_phase", "idle")
                context.log_event("campaign_complete", "orchestrator", {"cycles": current_cycle + 1})

                # Generate final report
                report = await self._generate_report(campaign_state)
                context.set_state("final_report", report)

                # Update Convex with final report, status, and increment cycle
                await self.convex_client.update_campaign(campaign_id, {
                    "finalReport": report,
                    "status": "completed",
                    "currentPhase": "idle",
                    "currentCycle": current_cycle + 1,
                })

        except Exception as e:
            logger.exception("Campaign execution failed")
            context.set_state("status", "failed")
            context.set_state("error", str(e))
            context.log_event("campaign_failed", "orchestrator", {"error": str(e)})
            await self.convex_client.update_campaign(campaign_id, {"status": "failed", "error": str(e)})

        finally:
            final_state = self.state_store.get_campaign(campaign_id)
            return {
                "campaign_id": campaign_id,
                "status": final_state.data.get("status", "unknown"),
                "cycles_completed": final_state.data.get("current_cycle", 0),
                "report": final_state.data.get("final_report", {}),
                "history": final_state.history,
            }

    async def _persist_agent_run(
        self,
        campaign_id: str,
        agent_name: str,
        result: Optional[AgentResult],
        start_time: datetime,
        context: AgentContext,
    ):
        """Log agent execution to Convex and apply updates if successful."""
        if result is None:
            status = "failed"
            errors = ["No result (exception before execution)"]
            output_data = {}
            completed_at = datetime.utcnow()
        else:
            status = "success" if result.success else "failed"
            errors = result.errors
            output_data = result.data
            completed_at = datetime.utcnow()

        # Append final status log
        if status == "success":
            context.logs.append(f"[SUCCESS] {agent_name.upper()} Agent completed successfully.")
        else:
            context.logs.append(f"[ERROR] {agent_name.upper()} Agent failed: {', '.join(errors or [])}")

        # Package output with logs
        output_with_logs = {
            "data": output_data,
            "logs": getattr(context, "logs", [])
        }

        # Log agent run
        await self.convex_client.log_agent_run(
            campaign_id=campaign_id,
            agent_name=agent_name,
            phase=context.get_state("current_phase", agent_name),
            input_data={},  # Could enrich if needed
            output=output_with_logs,
            status=status,
            started_at=start_time.isoformat(),
            completed_at=completed_at.isoformat() if completed_at else None,
            errors=errors,
        )

        # If success, apply agent-specific updates to campaign/content/metrics
        if result and result.success:
            await self._apply_agent_updates(campaign_id, agent_name, result.data, context)

    async def _apply_agent_updates(
        self,
        campaign_id: str,
        agent_name: str,
        data: Dict[str, Any],
        context: AgentContext,
    ):
        """Apply data from an agent to Convex database."""
        try:
            if agent_name == "strategy":
                updates = {
                    "gtmPlan": data,
                    "positioning": data.get("positioning"),
                    "channels": data.get("channels", []),
                    "campaignThemes": data.get("campaign_themes", []),
                    "kpiTargets": data.get("kpi_targets", {}),
                    "northStarMetric": data.get("north_star_metric"),
                }
                await self.convex_client.update_campaign(campaign_id, updates)

            elif agent_name == "research":
                updates = {
                    "personas": data.get("updated_personas", []),
                    "competitorInsights": data.get("competitor_insights", []),
                    "trendingTopics": data.get("trending_topics", []),
                    "recommendedKeywords": data.get("recommended_keywords", []),
                    "contentGaps": data.get("content_gaps", []),
                }
                await self.convex_client.update_campaign(campaign_id, updates)

            elif agent_name == "content":
                # Create content items for each channel
                x_posts = data.get("x_posts", [])
                for post in x_posts:
                    await self.convex_client.create_content(
                        campaign_id=campaign_id,
                        channel="x",
                        type="post",
                        body=post.get("text", ""),
                        status="generated",
                        title=None,
                        variant=post.get("type"),
                    )
                linkedin_posts = data.get("linkedin_posts", [])
                for post in linkedin_posts:
                    await self.convex_client.create_content(
                        campaign_id=campaign_id,
                        channel="linkedin",
                        type="post",
                        body=post.get("text", ""),
                        status="generated",
                        title=post.get("topic"),
                        variant=None,
                    )
                emails = data.get("email_campaigns", [])
                for email in emails:
                    body = f"Subject: {email.get('subject', '')}\n\n{email.get('body', '')}"
                    await self.convex_client.create_content(
                        campaign_id=campaign_id,
                        channel="email",
                        type="email",
                        body=body,
                        status="generated",
                        title=email.get("subject"),
                        variant=f"day{email.get('day')}",
                    )

            elif agent_name == "channel_x":
                posts = data.get("posts", [])
                for post in posts:
                    content_id = await self.convex_client.create_content(
                        campaign_id=campaign_id,
                        channel="x",
                        type="post",
                        body=post.get("content", ""),
                        status="published",
                        title=None,
                        variant=post.get("type"),
                        published_at=post.get("published_at"),
                        metrics=post.get("metrics", {}),
                    )
                    metrics = post.get("metrics", {})
                    for metric_type, value in metrics.items():
                        await self.convex_client.create_metric(
                            campaign_id=campaign_id,
                            channel="x",
                            metric_type=metric_type,
                            value=value,
                            recorded_at=datetime.utcnow().isoformat(),
                            content_id=content_id,
                        )

            elif agent_name == "channel_linkedin":
                posts = data.get("posts", [])
                for post in posts:
                    content_id = await self.convex_client.create_content(
                        campaign_id=campaign_id,
                        channel="linkedin",
                        type="post",
                        body=post.get("content", ""),
                        status="published",
                        title=None,
                        variant=post.get("type"),
                        published_at=post.get("published_at"),
                        metrics=post.get("metrics", {}),
                    )
                    metrics = post.get("metrics", {})
                    for metric_type, value in metrics.items():
                        await self.convex_client.create_metric(
                            campaign_id=campaign_id,
                            channel="linkedin",
                            metric_type=metric_type,
                            value=value,
                            recorded_at=datetime.utcnow().isoformat(),
                            content_id=content_id,
                        )

            elif agent_name == "channel_email":
                emails = data.get("sent_emails", [])
                for email in emails:
                    content_id = await self.convex_client.create_content(
                        campaign_id=campaign_id,
                        channel="email",
                        type="email",
                        body="",  # We don't store full body here, just metrics
                        title=email.get("subject"),
                        status="sent",
                        published_at=email.get("sent_at"),
                        metrics={
                            "opens": email.get("metrics", {}).get("opens"),
                            "clicks": email.get("metrics", {}).get("clicks"),
                            "conversions": email.get("metrics", {}).get("conversions"),
                        },
                    )
                    metrics = email.get("metrics", {})
                    for metric_type in ["opens", "clicks", "conversions"]:
                        if metric_type in metrics:
                            await self.convex_client.create_metric(
                                campaign_id=campaign_id,
                                channel="email",
                                metric_type=metric_type,
                                value=metrics[metric_type],
                                recorded_at=datetime.utcnow().isoformat(),
                                content_id=content_id,
                            )

            elif agent_name == "analytics":
                updates = {}
                for key in ["totalImpressions", "totalClicks", "totalSignups", "ctr", "recommendations"]:
                    if key in data:
                        updates[key] = data[key]
                if updates:
                    await self.convex_client.update_campaign(campaign_id, updates)

        except Exception as e:
            logger.error(f"Failed to apply updates for agent {agent_name}: {e}")

    async def _should_continue_campaign(self, context: AgentContext, campaign: CampaignState) -> bool:
        """Determine if campaign should continue to another cycle."""
        metrics = context.get_state("metrics", {})
        if not metrics:
            return True
        return True  # For demo, always run all cycles

    async def _adapt_strategy(self, context: AgentContext):
        """Adapt strategy based on analytics."""
        insights = context.get_state("insights", [])
        if insights:
            context.set_state("adaptations", insights)
            context.log_event("strategy_adapted", "orchestrator", {"insights": insights})

    async def _generate_report(self, campaign: CampaignState) -> Dict[str, Any]:
        """Generate human-readable campaign report."""
        data = campaign.data
        return {
            "summary": f"Campaign {campaign.campaign_id} completed",
            "goal": campaign.goal,
            "business": campaign.business_info.get("name"),
            "metrics": {
                "total_impressions": data.get("total_impressions", 0),
                "total_clicks": data.get("total_clicks", 0),
                "signups": data.get("signups", 0),
                "ctr": data.get("ctr", 0),
            },
            "recommendations": data.get("recommendations", []),
            "content_generated": {
                "x_posts": len(data.get("x_posts", [])),
                "linkedin_posts": len(data.get("linkedin_posts", [])),
                "emails": len(data.get("email_campaigns", [])),
            }
        }

    def get_campaign_state(self, campaign_id: str) -> Dict[str, Any]:
        """Get current state of a campaign."""
        campaign = self.state_store.get_campaign(campaign_id)
        return {
            "campaign_id": campaign.campaign_id,
            "status": campaign.data.get("status", "unknown"),
            "current_phase": campaign.data.get("current_phase", "unknown"),
            "metrics": campaign.data.get("metrics", {}),
        }