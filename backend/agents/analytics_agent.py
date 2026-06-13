"""Analytics & Optimization Agent - Measures performance and generates insights."""

from typing import Dict, Any
from core.agent import BaseAgent, AgentInput, AgentResult, AgentContext, agent
from loguru import logger


@agent("analytics")
class AnalyticsAgent(BaseAgent):
    """Aggregates metrics and generates recommendations."""

    name = "analytics"
    description = "Collects metrics from all channels and provides optimization insights"

    async def execute(self, input_data: AgentInput, context: AgentContext) -> AgentResult:
        """Analyze campaign performance and generate recommendations."""
        try:
            # Gather metrics from context
            x_impressions = context.get_state("x_impressions", 0)
            x_clicks = context.get_state("x_clicks", 0)
            x_engagement = context.get_state("x_engagement", 0)

            linkedin_impressions = context.get_state("linkedin_impressions", 0)
            linkedin_clicks = context.get_state("linkedin_clicks", 0)
            linkedin_likes = context.get_state("linkedin_likes", 0)

            email_opens = context.get_state("email_opens", 0)
            email_clicks = context.get_state("email_clicks", 0)
            email_conversions = context.get_state("email_conversions", 0)
            email_ctr = context.get_state("email_ctr", 0)

            # Compute totals
            total_impressions = x_impressions + linkedin_impressions
            total_clicks = x_clicks + linkedin_clicks
            total_signups = email_conversions  # assuming signups from email

            # Rates
            ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
            email_open_rate = (email_opens / context.get_state("email_sent_count", 1) * 100) if context.get_state("email_sent_count", 0) > 0 else 0

            # Generate recommendations
            recommendations = self._generate_recommendations(
                x_impressions, x_clicks,
                linkedin_impressions, linkedin_clicks,
                email_open_rate, email_ctr, email_conversions
            )

            analytics_data = {
                "totalImpressions": total_impressions,
                "totalClicks": total_clicks,
                "totalSignups": total_signups,
                "ctr": round(ctr, 2),
                "emailOpenRate": round(email_open_rate, 2),
                "emailCtr": email_ctr,
                "recommendations": recommendations,
                "channelBreakdown": {
                    "x": {"impressions": x_impressions, "clicks": x_clicks},
                    "linkedin": {"impressions": linkedin_impressions, "clicks": linkedin_clicks},
                    "email": {"opens": email_opens, "clicks": email_clicks, "conversions": email_conversions},
                }
            }

            # Store in context
            context.set_state("total_impressions", total_impressions)
            context.set_state("total_clicks", total_clicks)
            context.set_state("signups", total_signups)
            context.set_state("ctr", round(ctr, 2))
            context.set_state("recommendations", recommendations)

            context.log_event("analytics_complete", self.name, analytics_data)

            return AgentResult(
                success=True,
                agent_name=self.name,
                data=analytics_data,
            )

        except Exception as e:
            logger.exception("AnalyticsAgent failed")
            return AgentResult(
                success=False,
                agent_name=self.name,
                data={},
                errors=[str(e)],
            )

    def _generate_recommendations(
        self,
        x_imp: int, x_clicks: int,
        li_imp: int, li_clicks: int,
        email_open: float, email_ctr: float, email_conv: int,
    ) -> list[str]:
        """Simple rule-based recommendations."""
        recs = []

        # X channel
        x_ctr = (x_clicks / x_imp * 100) if x_imp > 0 else 0
        if x_ctr < 0.5:
            recs.append("X posts have low CTR. Try stronger CTAs or more engaging copy.")
        elif x_ctr > 2:
            recs.append("X is performing well. Consider increasing posting frequency.")

        # LinkedIn
        li_ctr = (li_clicks / li_imp * 100) if li_imp > 0 else 0
        if li_ctr < 0.3:
            recs.append("LinkedIn engagement is low. Refine professional messaging and post timing.")
        elif li_ctr > 1:
            recs.append("LinkedIn driving good clicks. Double down on top-performing topics.")

        # Email
        if email_open < 15:
            recs.append("Email open rate low. Improve subject lines and sender reputation.")
        if email_ctr < 3:
            recs.append("Email click-through low. Review email content and CTA placement.")
        if email_conv > 0:
            recs.append("Email conversions detected. Scale email list and test send times.")

        if not recs:
            recs.append("All channels showing baseline metrics. Continue monitoring and iterate.")

        return recs