"""Email client stub. Real implementation would integrate with SendGrid, Mailgun, or SMTP."""

from typing import Optional, Dict, Any, List
from loguru import logger


class EmailClient:
    """Email sending client. Currently a stub for simulation with optional SMTP."""

    def __init__(self, smtp_host: Optional[str] = None, smtp_port: int = 587,
                 username: Optional[str] = None, password: Optional[str] = None):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.real_mode = bool(smtp_host and username and password)

    async def send_campaign(self, subject: str, body: str, recipients: List[str]) -> Optional[Dict[str, Any]]:
        """
        Send an email campaign.
        Returns a dict with sent count and message IDs if real, None otherwise.
        """
        if not self.real_mode:
            logger.info("Email client in simulation mode (no SMTP configured).")
            return None

        # Real implementation would use aiosmtplib or SendGrid API
        # For now, log the intent and return simulated result
        logger.info(f"Simulating email send to {len(recipients)} recipients with subject: {subject}")
        return {
            "sent": len(recipients),
            "message_ids": [f"sim_{i}" for i in range(len(recipients))],
        }