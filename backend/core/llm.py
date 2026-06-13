"""LLM client for agent communication. Supports IRONLABS (default) and OpenAI-compatible endpoints."""

import os
from typing import Optional, Dict, Any, List
import httpx
from pydantic import BaseModel
from loguru import logger


class LLMConfig(BaseModel):
    """Configuration for LLM client."""
    api_key: str
    base_url: str = "https://api.ironlabs.ai/v1"
    model: str = "claude-3-opus"  # or whatever model name Iron Labs uses
    max_tokens: int = 2000
    temperature: float = 0.7
    timeout: float = 60.0


class LLMResponse(BaseModel):
    """Response from LLM."""
    content: str
    usage: Optional[Dict[str, int]] = None
    model: Optional[str] = None


class LLMClient:
    """Client for making LLM calls. Designed for agent use."""

    def __init__(self, config: Optional[LLMConfig] = None):
        self.config = config or LLMConfig(
            api_key=os.getenv("IRONLABS_API_KEY", ""),
            base_url=os.getenv("IRONLABS_BASE_URL", "https://api.ironlabs.ai/v1"),
            model=os.getenv("IRONLABS_MODEL", "claude-3-opus"),
        )
        if not self.config.api_key:
            logger.warning("No IRONLABS_API_KEY set. LLM calls will fail.")

    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> LLMResponse:
        """
        Generate text from the LLM.

        Args:
            prompt: User message
            system_prompt: Optional system message
            temperature: Override config temperature
            max_tokens: Override config max_tokens

        Returns:
            LLMResponse with generated content
        """
        if not self.config.api_key:
            # Return mock response for testing if no API key
            logger.warning("No API key - returning mock response")
            return LLMResponse(
                content="This is a mock LLM response. Set IRONLABS_API_KEY to use real LLM.",
                usage={"prompt_tokens": 10, "completion_tokens": 20},
                model=self.config.model,
            )

        headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json",
        }

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.config.model,
            "messages": messages,
            "temperature": temperature or self.config.temperature,
            "max_tokens": max_tokens or self.config.max_tokens,
        }

        async with httpx.AsyncClient(timeout=self.config.timeout) as client:
            try:
                response = await client.post(
                    f"{self.config.base_url}/chat/completions",
                    headers=headers,
                    json=payload,
                )
                response.raise_for_status()
                data = response.json()

                content = data["choices"][0]["message"]["content"]
                usage = data.get("usage", {})
                model = data.get("model", self.config.model)

                return LLMResponse(content=content, usage=usage, model=model)

            except Exception as e:
                logger.error(f"LLM API error: {e}")
                raise

    async def generate_with_tools(
        self,
        prompt: str,
        tools: List[Dict[str, Any]],
        system_prompt: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Generate with function/tool calling capability.

        Args:
            prompt: User message
            tools: List of tool definitions (OpenAI function format)
            system_prompt: Optional system message

        Returns:
            Dict with 'content' and optionally 'tool_calls'
        """
        # For now, just use regular generate. Tool calling can be added later.
        response = await self.generate(prompt, system_prompt)
        return {"content": response.content, "tool_calls": []}


# Global LLM client instance (to be configured at startup)
_llm_client: Optional[LLMClient] = None


def get_llm_client() -> LLMClient:
    """Get or create the global LLM client."""
    global _llm_client
    if _llm_client is None:
        _llm_client = LLMClient()
    return _llm_client


def set_llm_client(client: LLMClient):
    """Set the global LLM client (used for testing or custom config)."""
    global _llm_client
    _llm_client = client