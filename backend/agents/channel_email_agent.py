"""Channel Email Agent - Manages email campaign sending and tracking with real API stub."""

from typing import Dict, Any, Optional
import random
from datetime import datetime
from core.agent import BaseAgent, AgentInput, AgentResult, AgentContext, agent
from integrations.email_client import EmailClient
from loguru import logger


@agent("channel_email")
class ChannelEmailAgent(BaseAgent):
    """Manages email campaign sending and metrics (real or simulated)."""

    name = "channel_email"
    description = "Sends email sequences and tracks opens/clicks/conversions"

    async def execute(self, input_data: AgentInput, context: AgentContext) -> AgentResult:
        """Execute email campaign."""
        try:
            email_campaigns = context.get_state("email_campaigns", [])
            if not email_campaigns:
                return AgentResult(
                    success=True,
                    agent_name=self.name,
                    data={"message": "No email campaigns to send"},
                )

            real_mode = self.config.get("real_mode", False)
            email_client: Optional[EmailClient] = self.config.get("email_client")
            lead_count = self.config.get("lead_count", 1000)

            # For real email, we'd need a list of recipient emails. For demo, we'll simulate recipients.
            simulated_recipients = [f"lead{i}@example.com" for i in range(lead_count)]

            sent_emails = []
            total_opens = 0
            total_clicks = 0
            total_conversions = 0

            for idx, email in enumerate(email_campaigns):
                subject = email.get("subject", "")
                body = email.get("body", "")
                day = email.get("day", 0)

                if real_mode and email_client:
                    try:
                        result = await email_client.send_campaign(subject, body, simulated_recipients)
                        if result:
                            # Real send attempted; we'd need webhooks/statistics to get opens/clicks. For now, fall back to simulation for metrics.
                            logger.info(f"Email campaign sent (simulated receipt): {subject}")
                            metrics = self._simulate_email_metrics(email, lead_count, day)
                        else:
                            logger.warning("Email client returned no result, using simulated metrics")
                            metrics = self._simulate_email_metrics(email, lead_count, day)
                    except Exception as e:
                        logger.error(f"Error sending email: {e}, using simulation")
                        metrics = self._simulate_email_metrics(email, lead_count, day)
                else:
                    metrics = self._simulate_email_metrics(email, lead_count, day)

                sent_email = {
                    "email_id": f"email_{context.campaign_id}_{idx}",
                    "subject": subject,
                    "day": day,
                    "recipient_count": lead_count,
                    "metrics": metrics,
                    "sent_at": datetime.utcnow().isoformat(),
                }
                sent_emails.append(sent_email)

                total_opens += metrics["opens"]
                total_clicks += metrics["clicks"]
                total_conversions += metrics["conversions"]

                context.log_event("email_sent", self.name, {
                    "subject": subject,
                    "recipients": lead_count,
                })

            existing_emails = context.get_state("sent_emails", [])
            all_emails = existing_emails + sent_emails
            context.set_state("sent_emails", all_emails)

            context.set_state("email_opens", total_opens)
            context.set_state("email_clicks", total_clicks)
            context.set_state("email_conversions", total_conversions)
            context.set_state("email_sent_count", len(sent_emails) * lead_count)

            if total_opens > 0:
                context.set_state("email_ctr", round((total_clicks / total_opens) * 100, 2))
                context.set_state("email_conversion_rate", round((total_conversions / total_opens) * 100, 2))
            else:
                context.set_state("email_ctr", 0)
                context.set_state("email_conversion_rate", 0)

            context.log_event("channel_email_complete", self.name, {
                "emails_sent": len(sent_emails),
                "total_recipients": len(sent_emails) * lead_count,
                "total_conversions": total_conversions,
                "real_mode_used": real_mode and email_client is not None,
            })

            return AgentResult(
                success=True,
                agent_name=self.name,
                data={
                    "emails_sent": len(sent_emails),
                    "total_recipients": len(sent_emails) * lead_count,
                    "total_opens": total_opens,
                    "total_clicks": total_clicks,
                    "total_conversions": total_conversions,
                    "sent_emails": sent_emails,
                },
            )

        except Exception as e:
            logger.exception("ChannelEmailAgent failed")
            return AgentResult(
                success=False,
                agent_name=self.name,
                data={},
                errors=[str(e)],
            )

    def _simulate_email_metrics(self, email: Dict[str, Any], recipient_count: int, day: int) -> Dict[str, int]:
        """Simulate email campaign metrics."""
        subject = email.get("subject", "").lower()

        base_open_rate = 0.18
        base_click_rate = 0.05
        base_conversion_rate = 0.10

        if day == 0:
            base_open_rate = 0.25
            base_click_rate = 0.08
        elif day == 2:
            base_open_rate = 0.15
            base_click_rate = 0.04
        elif day >= 5:
            base_open_rate = 0.12
            base_click_rate = 0.03

        if "{{" in subject:
            base_open_rate *= 1.15
        if "?" in subject:
            base_open_rate *= 1.10

        urgency_words = ["limited", "last chance", "closing", "expire", "today"]
        if any(word in subject for word in urgency_words):
            base_open_rate *= 1.20
            base_click_rate *= 1.15

        variation = random.uniform(0.8, 1.2)
        open_rate = min(0.5, max(0.05, base_open_rate * variation))
        click_rate = min(0.3, max(0.01, base_click_rate * variation))
        conversion_rate = min(0.5, max(0.01, base_conversion_rate * variation))

        opens = int(recipient_count * open_rate)
        clicks = int(opens * click_rate)
        conversions = int(clicks * conversion_rate)

        return {
            "opens": opens,
            "clicks": clicks,
            "conversions": conversions,
            "open_rate": round(open_rate * 100, 2),
            "ctr": round(click_rate * 100, 2),
            "conversion_rate": round(conversion_rate * 100, 2),
        }