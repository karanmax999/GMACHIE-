"""Channel LinkedIn Agent - Publishes posts and simulates engagement on LinkedIn with real API fallback."""

from typing import Dict, Any, Optional
import random
from datetime import datetime
from core.agent import BaseAgent, AgentInput, AgentResult, AgentContext, agent
from integrations.linkedin_client import LinkedInClient
from loguru import logger


@agent("channel_linkedin")
class ChannelLinkedInAgent(BaseAgent):
    """Manages LinkedIn content publishing and engagement metrics with real API support."""

    name = "channel_linkedin"
    description = "Publishes LinkedIn posts (real or simulated) and tracks engagement"

    async def execute(self, input_data: AgentInput, context: AgentContext) -> AgentResult:
        """Execute LinkedIn campaign."""
        try:
            linkedin_posts = context.get_state("linkedin_posts", [])
            if not linkedin_posts:
                return AgentResult(
                    success=True,
                    agent_name=self.name,
                    data={"message": "No LinkedIn posts to publish"},
                )

            real_mode = self.config.get("real_mode", False)
            linkedin_client: Optional[LinkedInClient] = self.config.get("linkedin_client")

            published_posts = []
            total_impressions = 0
            total_likes = 0
            total_comments = 0
            total_clicks = 0

            for idx, post in enumerate(linkedin_posts):
                text = post.get("text", "")
                post_urn = None
                metrics = {}

                if real_mode and linkedin_client:
                    try:
                        post_urn = await linkedin_client.create_post(text)
                        if post_urn:
                            real_metrics = await linkedin_client.get_post_metrics(post_urn)
                            if real_metrics:
                                # Map LinkedIn metrics to our schema; structure is TBD by API response.
                                # For now, we'll simulate primary metrics and merge any real ones.
                                sim_metrics = self._simulate_linkedin_metrics(post)
                                metrics = sim_metrics
                                # If LinkedIn returns counts, they could override simulated ones.
                                # Example: real_metrics might have "count" fields; adjust mapping as needed.
                                if isinstance(real_metrics, dict):
                                    if "likes" in real_metrics:
                                        metrics["likes"] = real_metrics["likes"]
                                    if "comments" in real_metrics:
                                        metrics["comments"] = real_metrics["comments"]
                                    # Impressions not always available, keep simulated
                            else:
                                logger.warning(f"No metrics for LinkedIn post {post_urn}, using simulation")
                                metrics = self._simulate_linkedin_metrics(post)
                        else:
                            logger.warning("Failed to create LinkedIn post, falling back to simulation")
                            metrics = self._simulate_linkedin_metrics(post)
                    except Exception as e:
                        logger.error(f"Exception during real LinkedIn post: {e}, falling back to simulation")
                        metrics = self._simulate_linkedin_metrics(post)
                else:
                    metrics = self._simulate_linkedin_metrics(post)

                published_post = {
                    "post_id": post_urn or f"li_{context.campaign_id}_{idx}_{int(datetime.utcnow().timestamp())}",
                    "content": text,
                    "topic": post.get("topic", ""),
                    "cta": post.get("cta", ""),
                    "published_at": datetime.utcnow().isoformat(),
                    "metrics": metrics,
                    "status": "published",
                }
                published_posts.append(published_post)

                total_impressions += metrics["impressions"]
                total_likes += metrics["likes"]
                total_comments += metrics["comments"]
                total_clicks += metrics["clicks"]

                context.log_event("linkedin_post_published", self.name, {
                    "post_id": published_post["post_id"],
                    "topic": post.get("topic"),
                    "real": post_urn is not None,
                })

            # Update context state
            existing = context.get_state("published_linkedin_posts", [])
            all_posts = existing + published_posts
            context.set_state("published_linkedin_posts", all_posts)
            context.set_state("linkedin_impressions", total_impressions)
            context.set_state("linkedin_likes", total_likes)
            context.set_state("linkedin_comments", total_comments)
            context.set_state("linkedin_clicks", total_clicks)

            context.log_event("channel_linkedin_complete", self.name, {
                "posts_published": len(published_posts),
                "total_impressions": total_impressions,
                "total_clicks": total_clicks,
                "real_mode_used": real_mode and linkedin_client is not None,
            })

            return AgentResult(
                success=True,
                agent_name=self.name,
                data={
                    "posts_published": len(published_posts),
                    "total_impressions": total_impressions,
                    "total_likes": total_likes,
                    "total_comments": total_comments,
                    "total_clicks": total_clicks,
                    "posts": published_posts,
                },
            )

        except Exception as e:
            logger.exception("ChannelLinkedInAgent failed")
            return AgentResult(
                success=False,
                agent_name=self.name,
                data={},
                errors=[str(e)],
            )

    def _simulate_linkedin_metrics(self, post: Dict[str, Any]) -> Dict[str, int]:
        """Simulate LinkedIn engagement metrics."""
        text = post.get("text", "").lower()
        topic = post.get("topic", "").lower()

        base_impressions = random.randint(300, 3000)
        base_likes = random.randint(5, 100)
        base_comments = random.randint(0, 20)
        base_clicks = random.randint(10, 200)

        if len(text) > 200:
            base_impressions = int(base_impressions * 1.2)
            base_clicks = int(base_clicks * 1.1)

        professional_keywords = ["growth", "revenue", "strategy", "b2b", "saas", "marketing"]
        if any(kw in text for kw in professional_keywords):
            base_impressions = int(base_impressions * 1.3)
            base_engagement = base_likes + base_comments
            base_engagement = int(base_engagement * 1.2)

        cta = post.get("cta", "").lower()
        if any(word in cta for word in ["comment", "share", "connect"]):
            base_comments = int(base_comments * 1.5)
            base_clicks = int(base_clicks * 1.2)

        return {
            "impressions": base_impressions,
            "likes": base_likes,
            "comments": base_comments,
            "shares": random.randint(0, 30),
            "clicks": base_clicks,
        }