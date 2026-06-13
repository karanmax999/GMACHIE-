"""X/Twitter API client using tweepy for real posting with fallback to simulation."""

import asyncio
from typing import Optional, Dict, Any
import tweepy
from loguru import logger


class XClient:
    """Client for X (Twitter) API v2 using tweepy."""

    def __init__(
        self,
        consumer_key: str,
        consumer_secret: str,
        access_token: str,
        access_token_secret: str,
    ):
        self.client = tweepy.Client(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            access_token=access_token,
            access_token_secret=access_token_secret,
        )

    async def post_tweet(self, text: str, reply_to_id: Optional[str] = None) -> Optional[str]:
        """
        Post a tweet.
        Returns tweet ID if successful, None otherwise.
        """
        try:
            kwargs = {"text": text}
            if reply_to_id:
                kwargs["in_reply_to_tweet_id"] = reply_to_id

            # Run the synchronous tweepy call in a separate thread to avoid blocking the async loop
            response = await asyncio.to_thread(self.client.create_tweet, **kwargs)
            
            if response and response.data:
                tweet_id = response.data.get("id")
                logger.info(f"Tweet posted successfully via tweepy: {tweet_id}")
                return str(tweet_id)
            else:
                logger.error("Failed to post tweet: Empty response from Twitter API")
                return None
        except Exception as e:
            logger.error(f"Failed to post tweet: {e}")
            return None

    async def get_tweet_metrics(self, tweet_id: str) -> Optional[Dict[str, Any]]:
        """
        Fetch public engagement metrics for a tweet.
        """
        try:
            # Run the synchronous tweepy call in a separate thread
            response = await asyncio.to_thread(
                self.client.get_tweet,
                id=tweet_id,
                tweet_fields=["public_metrics"],
            )
            if response and response.data:
                tweet_data = response.data
                if hasattr(tweet_data, "public_metrics") and tweet_data.public_metrics is not None:
                    return tweet_data.public_metrics
                elif isinstance(tweet_data, dict):
                    return tweet_data.get("public_metrics")
            return None
        except Exception as e:
            logger.warning(f"Could not fetch tweet metrics: {e}")
            return None