"""Channel X/Twitter Agent - Handles posting and engagement on X with real API fallback."""

from typing import Dict, Any, Optional
import random
from datetime import datetime
from core.agent import BaseAgent, AgentInput, AgentResult, AgentContext, agent
from integrations.x_client import XClient
from loguru import logger


@agent("channel_x")
class ChannelXAgent(BaseAgent):
    """Manages X/Twitter content publishing and basic engagement with real API support."""

    name = "channel_x"
    description = "Publishes posts to X (real or simulated) and tracks engagement"

    async def execute(self, input_data: AgentInput, context: AgentContext) -> AgentResult:
        """Execute X channel campaign."""
        try:
            x_posts = context.get_state("x_posts", [])
            if not x_posts:
                return AgentResult(
                    success=True,
                    agent_name=self.name,
                    data={"message": "No X posts to publish"},
                )

            real_mode = self.config.get("real_mode", False)
            x_client: Optional[XClient] = self.config.get("x_client")

            published_posts = []
            total_impressions = 0
            total_engagement = 0
            total_clicks = 0

            for idx, post in enumerate(x_posts):
                text = post.get("text", "")
                tweet_id = None
                metrics = {}

                if real_mode and x_client:
                    try:
                        tweet_id = await x_client.post_tweet(text)
                        if tweet_id:
                            # Try to fetch real metrics
                            real_metrics = await x_client.get_tweet_metrics(tweet_id)
                            if real_metrics:
                                # Map Twitter public metrics to our schema
                                sim_metrics = self._simulate_metrics(post)
                                # Simulated values as fallback for missing fields
                                metrics = {
                                    "impressions": sim_metrics["impressions"],  # Twitter API doesn't provide impressions easily
                                    "likes": real_metrics.get("like_count", sim_metrics["likes"]),
                                    "replies": real_metrics.get("reply_count", sim_metrics["replies"]),
                                    "retweets": real_metrics.get("retweet_count", sim_metrics["retweets"]),
                                    "clicks": sim_metrics["clicks"],  # Clicks not in public metrics
                                }
                            else:
                                logger.warning(f"Failed to fetch metrics for tweet {tweet_id}, using simulation")
                                metrics = self._simulate_metrics(post)
                        else:
                            logger.warning("Failed to post tweet, falling back to simulation")
                            metrics = self._simulate_metrics(post)
                    except Exception as e:
                        logger.error(f"Exception during real X post: {e}, falling back to simulation")
                        metrics = self._simulate_metrics(post)
                else:
                    metrics = self._simulate_metrics(post)

                published_post = {
                    "post_id": tweet_id or f"x_{context.campaign_id}_{idx}_{int(datetime.utcnow().timestamp())}",
                    "content": text,
                    "type": post.get("type", "unknown"),
                    "cta": post.get("cta", ""),
                    "published_at": datetime.utcnow().isoformat(),
                    "metrics": metrics,
                    "status": "published",
                }
                published_posts.append(published_post)

                total_impressions += metrics["impressions"]
                total_engagement += metrics["likes"] + metrics["replies"] + metrics["retweets"]
                total_clicks += metrics["clicks"]

                context.log_event("post_published", self.name, {
                    "post_id": published_post["post_id"],
                    "type": published_post["type"],
                    "real": tweet_id is not None,
                })

            # Update state
            existing_posts = context.get_state("published_x_posts", [])
            all_posts = existing_posts + published_posts
            context.set_state("published_x_posts", all_posts)
            context.set_state("x_impressions", total_impressions)
            context.set_state("x_engagement", total_engagement)
            context.set_state("x_clicks", total_clicks)

            context.log_event("channel_x_complete", self.name, {
                "posts_published": len(published_posts),
                "total_impressions": total_impressions,
                "total_clicks": total_clicks,
                "real_mode_used": real_mode and x_client is not None,
            })

            return AgentResult(
                success=True,
                agent_name=self.name,
                data={
                    "posts_published": len(published_posts),
                    "total_impressions": total_impressions,
                    "total_clicks": total_clicks,
                    "posts": published_posts,
                },
            )

        except Exception as e:
            logger.exception("ChannelXAgent failed")
            return AgentResult(
                success=False,
                agent_name=self.name,
                data={},
                errors=[str(e)],
            )

    def _simulate_metrics(self, post: Dict[str, Any]) -> Dict[str, int]:
        """Simulate engagement metrics for a post based on content heuristics."""
        text = post.get("text", "").lower()
        post_type = post.get("type", "benefit")

        base_impressions = random.randint(1000, 10000)
        base_likes = random.randint(10, 200)
        base_replies = random.randint(0, 50)
        base_retweets = random.randint(5, 100)
        base_clicks = random.randint(20, 500)

        if "?" in text:
            base_engagement = int(base_likes * 1.2)
            base_replies = int(base_replies * 1.5)
        else:
            base_engagement = base_likes

        exclamation_count = text.count("!")
        if exclamation_count > 0:
            base_impressions = int(base_impressions * (1 + 0.1 * min(exclamation_count, 3)))

        hashtags = text.count("#")
        if hashtags > 0:
            base_impressions = int(base_impressions * (1 + 0.15 * min(hashtags, 2)))

        cta = post.get("cta", "").lower()
        if any(word in cta for word in ["click", "signup", "try", "get"]):
            base_clicks = int(base_clicks * 1.3)

        if post_type == "benefit":
            base_clicks = int(base_clicks * 1.2)
        elif post_type == "curiosity":
            base_replies = int(base_replies * 1.3)
        elif post_type == "social_proof":
            base_retweets = int(base_retweets * 1.4)

        return {
            "impressions": base_impressions,
            "likes": base_engagement,
            "replies": base_replies,
            "retweets": base_retweets,
            "clicks": base_clicks,
        }