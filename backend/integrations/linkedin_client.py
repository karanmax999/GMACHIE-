"""LinkedIn API client for real post creation with fallback to simulation."""

import httpx
from typing import Optional, Dict, Any, List
from loguru import logger


class LinkedInClient:
    """Client for LinkedIn REST API (UGC posts)."""

    def __init__(self, access_token: str, author_urn: str):
        """
        Initialize LinkedIn client.
        author_urn: e.g., "urn:li:person:{person_id}" or "urn:li:organization:{org_id}"
        """
        self.access_token = access_token
        self.author_urn = author_urn
        self.base_url = "https://api.linkedin.com/rest"
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0",
        }

    async def create_post(self, text: str, topic: Optional[str] = None) -> Optional[str]:
        """
        Create a UGC post on LinkedIn.
        Returns post URN (e.g., "urn:li:ugcPost:123") if successful, None otherwise.
        """
        # Build the post content
        post_data = {
            "author": self.author_urn,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {"text": text},
                    "shareMediaCategory": "NONE",
                }
            },
            "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"},
        }

        if topic:
            # Optionally add a topic via headline or in the text; LinkedIn doesn't have a simple topic field.
            pass

        async with httpx.AsyncClient(timeout=15.0) as client:
            try:
                response = await client.post(
                    f"{self.base_url}/ugcPosts",
                    headers=self.headers,
                    json=post_data,
                )
                response.raise_for_status()
                # Location header contains the post URN
                location = response.headers.get("Location", "")
                post_urn = location.split("/")[-1] if location else None
                logger.info(f"LinkedIn post created: {post_urn}")
                return post_urn
            except httpx.HTTPError as e:
                logger.error(f"Failed to create LinkedIn post: {e}")
                return None
            except Exception as e:
                logger.error(f"Unexpected error creating LinkedIn post: {e}")
                return None

    async def get_post_metrics(self, post_urn: str) -> Optional[Dict[str, Any]]:
        """
        Fetch metrics for a post. Requires organization page or appropriate permissions.
        For personal posts, metrics are limited.
        """
        # The endpoint for stats is /socialActions/{ugcPostUrn}/stats
        # But that requires specific permissions. We'll try to get available metrics.
        try:
            encoded_urn = post_urn.replace(":", "%3A")
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    f"{self.base_url}/socialActions/{encoded_urn}/stats",
                    headers=self.headers,
                )
                response.raise_for_status()
                data = response.json()
                return data
        except Exception as e:
            logger.warning(f"Could not fetch LinkedIn post metrics: {e}")
            return None