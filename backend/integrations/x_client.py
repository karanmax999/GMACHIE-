"""X/Twitter API client for real posting with fallback to simulation."""

import httpx
from typing import Optional, Dict, Any
from loguru import logger


class XClient:
    """Client for X (Twitter) API v2."""

    def __init__(self, access_token: str):
        self.access_token = access_token
        self.base_url = "https://api.twitter.com/2"
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

    async def post_tweet(self, text: str, reply_to_id: Optional[str] = None) -> Optional[str]:
        """
        Post a tweet.
        Returns tweet ID if successful, None otherwise.
        """
        payload = {"text": text}
        if reply_to_id:
            payload["reply"] = {"in_reply_to_tweet_id": reply_to_id}

        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                response = await client.post(
                    f"{self.base_url}/tweets",
                    headers=self.headers,
                    json=payload,
                )
                response.raise_for_status()
                data = response.json()
                tweet_id = data.get("data", {}).get("id")
                logger.info(f"Tweet posted successfully: {tweet_id}")
                return tweet_id
            except httpx.HTTPError as e:
                logger.error(f"Failed to post tweet: {e}")
                return None
            except Exception as e:
                logger.error(f"Unexpected error posting tweet: {e}")
                return None

    async def get_tweet_metrics(self, tweet_id: str) -> Optional[Dict[str, Any]]:
        """
        Fetch public engagement metrics for a tweet.
        Requires matching user context (the same token or appropriate permissions).
        """
        # The v2 tweets endpoint can return public metrics if expansions are used.
        # For simplicity, we'll try to get non-promoted data, but many metrics require additional permissions.
        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                response = await client.get(
                    f"{self.base_url}/tweets/{tweet_id}",
                    headers=self.headers,
                    params={"tweet.fields": "public_metrics"},
                )
                response.raise_for_status()
                data = response.json()
                metrics = data.get("data", {}).get("public_metrics", {})
                return metrics
            except Exception as e:
                logger.warning(f"Could not fetch tweet metrics: {e}")
                return None