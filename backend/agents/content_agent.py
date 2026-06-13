"""Content Engine Agent - Generates channel-specific content."""

from typing import Dict, Any, List
from core.agent import BaseAgent, AgentInput, AgentResult, AgentContext, agent
from core.llm import get_llm_client
from loguru import logger
import json
import uuid


@agent("content")
class ContentAgent(BaseAgent):
    """Generates multi-format GTM content for different channels."""

    name = "content"
    description = "Creates posts, emails, and ad copy tailored to personas and channels"

    async def execute(self, input_data: AgentInput, context: AgentContext) -> AgentResult:
        """Generate content assets for the campaign."""
        try:
            campaign_themes = context.get_state("campaign_themes", [])
            personas = context.get_state("personas", [])
            channels = context.get_state("channels", [])
            positioning = context.get_state("positioning", "")

            llm = get_llm_client()

            # Generate content for each channel
            generated_content = {}

            # Generate X/Twitter content
            x_content = await self._generate_x_content(llm, campaign_themes, personas, positioning)
            generated_content["x_posts"] = x_content

            # Generate LinkedIn content
            linkedin_content = await self._generate_linkedin_content(llm, campaign_themes, personas, positioning)
            generated_content["linkedin_posts"] = linkedin_content

            # Generate Email campaigns
            email_content = await self._generate_email_content(llm, campaign_themes, personas, positioning)
            generated_content["email_campaigns"] = email_content

            # Store in state
            context.set_state("generated_content", generated_content)
            context.set_state("x_posts", x_content)
            context.set_state("linkedin_posts", linkedin_content)
            context.set_state("email_campaigns", email_content)

            context.log_event("content_generation_complete", self.name, {
                "x_count": len(x_content),
                "linkedin_count": len(linkedin_content),
                "email_count": len(email_content)
            })

            return AgentResult(
                success=True,
                agent_name=self.name,
                data=generated_content,
                metadata={"total_assets": len(x_content) + len(linkedin_content) + len(email_content)},
            )

        except Exception as e:
            logger.exception("ContentAgent failed")
            return AgentResult(
                success=False,
                agent_name=self.name,
                data={},
                errors=[str(e)],
            )

    async def _generate_x_content(
        self,
        llm,
        themes: List[str],
        personas: List[Dict],
        positioning: str,
    ) -> List[Dict[str, Any]]:
        """Generate X/Twitter posts (short, punchy)."""
        persona_summary = self._summarize_personas(personas)
        theme_list = ", ".join(themes) if themes else "product launch"

        prompt = f"""Create 3 engaging X/Twitter posts for a product launch.

Product Positioning: {positioning}
Target Audience: {persona_summary}
Campaign Themes: {theme_list}

Requirements:
- Each post under 280 characters
- Use relevant hashtags (2-3 per post)
- Include a clear call-to-action (CTA)
- Mix of: benefit-driven, curiosity-driven, social proof
- Format: JSON array of objects with keys: "text" (string), "type" (one of: "benefit", "curiosity", "social_proof"), "cta" (string)

Example:
[
  {{"text": "Struggling to budget as a student? Our AI app categorizes expenses instantly. Try it free!", "type": "benefit", "cta": "Sign up for early access"}},
  ...
]"""

        system_prompt = "You are an expert social media copywriter for Gen Z audiences. Write concise, trendy, high-engagement posts."

        response = await llm.generate(prompt, system_prompt=system_prompt, temperature=0.8)

        try:
            content = response.content.strip()
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            posts = json.loads(content)
            # Validate structure
            for p in posts:
                if not isinstance(p, dict) or "text" not in p:
                    raise ValueError("Invalid post structure")
            return posts
        except Exception as e:
            logger.error(f"Failed to parse X content: {e}")
            # Return placeholder
            return [
                {"text": f"Launch alert: {themes[0] if themes else 'Our product'} is coming soon! #GTM", "type": "curiosity", "cta": "Stay tuned"},
                {"text": "Budgeting made stupid simple. AI-powered expense tracking for Gen Z. #FinTech", "type": "benefit", "cta": "Join waitlist"},
            ]

    async def _generate_linkedin_content(
        self,
        llm,
        themes: List[str],
        personas: List[Dict],
        positioning: str,
    ) -> List[Dict[str, Any]]:
        """Generate LinkedIn posts (more professional, longer)."""
        persona_summary = self._summarize_personas(personas)

        prompt = f"""Create 2 LinkedIn posts for a B2B/B2C product launch.

Positioning: {positioning}
Audience: {persona_summary}
Themes: {', '.join(themes) if themes else 'N/A'}

Requirements:
- 1-2 paragraphs (150-300 words)
- Professional but engaging tone
- Include a hook, value prop, and CTA
- Add 3-5 relevant hashtags
- Format: JSON array with objects: {{"text": "...", "topic": "...", "cta": "..."}}"""

        system_prompt = "You are a LinkedIn growth hacker. Write posts that drive engagement and conversions."

        response = await llm.generate(prompt, system_prompt=system_prompt, temperature=0.7)

        try:
            content = response.content.strip()
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            posts = json.loads(content)
            return posts
        except Exception as e:
            logger.error(f"Failed to parse LinkedIn content: {e}")
            return [
                {"text": "We're building something new to solve expense tracking for Gen Z. DM us if you'd like early access.", "topic": "FinTech Innovation", "cta": "Comment your biggest budgeting pain"},
            ]

    async def _generate_email_content(
        self,
        llm,
        themes: List[str],
        personas: List[Dict],
        positioning: str,
    ) -> List[Dict[str, Any]]:
        """Generate email campaign sequences."""
        persona_summary = self._summarize_personas(personas)
        theme = themes[0] if themes else "product launch"

        prompt = f"""Create a 3-email welcome sequence for a new product.

Product Positioning: {positioning}
Target Audience: {persona_summary}
Main Theme: {theme}

Sequence:
1. Welcome / Introduction (day 0)
2. Value deep dive / Story (day 2)
3. Social proof / CTA to convert (day 5)

For each email, provide:
- subject (short, compelling)
- body (HTML-like plain text, ~200 words)
- cta_text (button text)
- cta_link (placeholder "#")

Return as JSON: {{"emails": [{{"subject": "...", "body": "...", "cta_text": "...", "cta_link": "#", "day": number}}, ...]}}"""

        system_prompt = "You are an email marketing specialist. Write concise, conversion-focused emails."

        response = await llm.generate(prompt, system_prompt=system_prompt, temperature=0.7)

        try:
            content = response.content.strip()
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            data = json.loads(content)
            return data.get("emails", [])
        except Exception as e:
            logger.error(f"Failed to parse email content: {e}")
            return [
                {"subject": "Welcome to FinSmart!", "body": "We're excited to have you. Here's what we do...", "cta_text": "Get Started", "cta_link": "#", "day": 0},
            ]

    def _summarize_personas(self, personas: List[Dict]) -> str:
        """Create a short text summary of personas for prompts."""
        if not personas:
            return "General audience interested in budgeting/financial management"
        summary = []
        for p in personas[:2]:  # Just top 2
            name = p.get("name", "Persona")
            desc = p.get("description", "")
            summary.append(f"{name}: {desc}")
        return " | ".join(summary)