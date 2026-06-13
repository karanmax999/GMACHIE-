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
                logger.warning("LLM API is unreachable or failed. Falling back to local simulated response...")
                simulated_content = self._get_simulated_response(prompt, system_prompt)
                return LLMResponse(
                    content=simulated_content,
                    usage={"prompt_tokens": 0, "completion_tokens": 0},
                    model="simulated-fallback",
                )

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

    def _get_simulated_response(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Return a simulated JSON string for testing or offline environments."""
        system_prompt_str = system_prompt.lower() if system_prompt else ""
        prompt_str = prompt.lower()

        # 1. Strategy Agent fallback
        if "positioning" in system_prompt_str or "campaign_themes" in system_prompt_str:
            return """
{
  "positioning": "AI-powered marketing automation for small businesses and developers looking to scale their distribution.",
  "target_audience": "Indie hackers, startup founders, and small B2B teams.",
  "channels": [
    {"name": "x", "primary": true, "why": "High density of tech audience and founders.", "expected_reach": "10000"},
    {"name": "linkedin", "primary": true, "why": "B2B professional network with high organic reach.", "expected_reach": "5000"},
    {"name": "email", "primary": true, "why": "Direct channel with the highest conversion rate.", "expected_reach": "1000"}
  ],
  "campaign_themes": ["Automate Your Distribution", "Build in Public", "AI Marketing Assistant"],
  "kpi_targets": {
    "week1": {"impressions": 1000, "clicks": 100, "signups": 10},
    "week2": {"impressions": 2500, "clicks": 300, "signups": 35},
    "week3": {"impressions": 6000, "clicks": 800, "signups": 90}
  },
  "north_star_metric": "Weekly Active Campaigns"
}
"""

        # 2. Research Agent fallback
        elif "updated_personas" in system_prompt_str or "competitor_insights" in system_prompt_str:
            return """
{
  "updated_personas": [
    {
      "name": "Busy Developer Ben",
      "description": "Building a SaaS alone, has no time for copywriting or social scheduling.",
      "pain_points": ["Marketing is tedious", "Writing copy is hard", "Low organic engagement"],
      "triggers": ["Product launch day is coming", "Needs first 100 users"],
      "objections": ["AI content sounds fake", "Too expensive"],
      "language": ["#indiehackers", "buildinpublic", "SaaS", "bootstrap"]
    },
    {
      "name": "Growth Lead Grace",
      "description": "Solo marketer at a B2B startup, needs to publish across multiple platforms daily.",
      "pain_points": ["Content creation burnout", "Context switching", "Hard to measure ROI"],
      "triggers": ["Needs to scale content production", "Campaign performance is dropping"],
      "objections": ["Security compliance", "Integration with existing CRM"],
      "language": ["growth marketing", "conversion rate", "funnel", "MarTech"]
    }
  ],
  "competitor_insights": [
    {
      "competitor": "AdAgency Co",
      "strategy": "High-end manual campaign setup and execution",
      "strengths": ["Strong creative direction", "Enterprise scale"],
      "weaknesses": ["Extremely expensive", "Slow execution"],
      "opportunity": "Provide instant, affordable self-serve AI campaign drafts"
    },
    {
      "competitor": "SchedulerPro",
      "strategy": "Simple scheduling across social channels",
      "strengths": ["Reliable automation", "Low cost"],
      "weaknesses": ["No AI generation", "No strategy advice"],
      "opportunity": "Combine strategic planning, content creation, and scheduling"
    }
  ],
  "trending_topics": [
    {"topic": "AI Marketing Automation", "relevance": "Direct match for GMACHIE value prop", "hashtags": ["#AIMarketing", "#SaaS"]},
    {"topic": "Building B2B Products", "relevance": "Targets indie hackers and SaaS founders", "hashtags": ["#B2B", "#IndieHackers"]}
  ],
  "recommended_keywords": ["ai marketing engine", "autonomous marketing", "gtm workflow", "social media scheduler"],
  "content_gaps": ["Detailed guides on how to scale startup marketing with zero budget"]
}
"""

        # 3. Content Agent - X/Twitter fallback
        elif "x/twitter posts" in prompt_str or "benefit-driven" in prompt_str or "x_posts" in prompt_str or "280 characters" in prompt_str:
            return """
[
  {"text": "Solo founders: Stop spending hours on marketing. Orchestrate and schedule your GTM campaigns in minutes with our AI assistant. #IndieHackers #AIMarketing", "type": "benefit", "cta": "Join the waitlist"},
  {"text": "What if you had an autonomous marketing team working 24/7 to draft social posts, research trends, and write emails? GMACHIE does exactly that. #MarTech #SaaS", "type": "curiosity", "cta": "Learn how it works"},
  {"text": "We helped 12 B2B startups launch their campaigns last week with zero manual copywriting. Setup takes less than 15 minutes. #GrowthHacking #MarTech", "type": "social_proof", "cta": "Get early access"}
]
"""

        # 4. Content Agent - LinkedIn fallback
        elif "linkedin posts" in prompt_str or "linkedin growth hacker" in system_prompt_str:
            return """
[
  {
    "text": "Are you a bootstrap founder spending more time writing posts and outreach emails than building your product?\\n\\nMarketing is the lifeblood of startup growth, but context-switching kills momentum. That's why we created GMACHIE. It serves as your autonomous go-to-market agent, drafting posts, planning distribution strategy, and sending newsletters while you focus on code.\\n\\nLet AI handle your distribution.",
    "topic": "SaaS Growth",
    "cta": "Join the beta program"
  },
  {
    "text": "The major bottleneck for most SaaS startups isn't building the product—it's distribution. \\n\\nWithout a dedicated marketing team, scaling content and social presence is a full-time job. GMACHIE bridges that gap. It researches competitor strategies, updates your buyer personas, and drafts high-engagement copy tailored specifically to your product positioning.\\n\\nStop manual social scheduling. Switch to autonomous distribution.",
    "topic": "B2B Marketing",
    "cta": "Start your campaign free"
  }
]
"""

        # 5. Content Agent - Email welcome sequence fallback
        elif "welcome sequence" in prompt_str or "emails" in prompt_str or "subject" in prompt_str:
            return """
{
  "emails": [
    {
      "subject": "Welcome to GMACHIE - Let's launch your GTM campaign",
      "body": "Hey there,\\n\\nWelcome to GMACHIE! We are excited to help you automate your go-to-market execution.\\n\\nOur AI-powered orchestrator has already started analyzing your target audience and positioning. Click below to review your GTM plan and approve your first campaign drafts.",
      "cta_text": "Launch Campaign",
      "cta_link": "#",
      "day": 0
    },
    {
      "subject": "How GMACHIE automates your B2B growth",
      "body": "Hey again,\\n\\nYesterday we drafted your first campaign. But how does GMACHIE actually work?\\n\\nIt continuously researches competitor strategies and social trends, updates your buyer personas, and dynamically adapts your messaging so you always stay ahead of the curve. No manual research required.",
      "cta_text": "View Insights",
      "cta_link": "#",
      "day": 2
    },
    {
      "subject": "Startups are scaling 3x faster with autonomous marketing",
      "body": "Hey,\\n\\nFounders using GMACHIE have seen a 3x increase in weekly impressions and saved over 15 hours of manual content writing.\\n\\nDon't let distribution hold your product back. Approve your campaign drafts today and start publishing live.",
      "cta_text": "Approve & Publish",
      "cta_link": "#",
      "day": 5
    }
  ]
}
"""
        return '{"content": "Simulated mock response content"}'


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