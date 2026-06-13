"""Market & Audience Research Agent - Continuously refines targeting and messaging."""

from typing import Dict, Any, List
from core.agent import BaseAgent, AgentInput, AgentResult, AgentContext, agent
from core.llm import get_llm_client
from loguru import logger
import json


@agent("research")
class ResearchAgent(BaseAgent):
    """Gathers audience insights, competitor intel, and trending topics."""

    name = "research"
    description = "Researches audience, competitors, and trends to refine messaging"

    async def execute(self, input_data: AgentInput, context: AgentContext) -> AgentResult:
        """Conduct market research."""
        try:
            icp = context.get_state("icp", "")
            campaign_themes = context.get_state("campaign_themes", [])
            personas = context.get_state("personas", [])
            business_info = context.get_state("business_info", {})

            llm = get_llm_client()

            prompt = self._build_prompt(business_info, icp, campaign_themes, personas)
            system_prompt = """You are an expert market researcher specializing in Gen Z and digital product launches.
Your task: provide deep audience insights, competitor analysis, and trending topics relevant to the product.

Output format: valid JSON with these keys:
{
  "updated_personas": [
    {
      "name": "string",
      "description": "string",
      "pain_points": ["string"],
      "triggers": ["string"],
      "objections": ["string"],
      "language": ["string"]  // slang, hashtags, tone
    }
  ],
  "competitor_insights": [
    {
      "competitor": "string",
      "strategy": "string",
      "strengths": ["string"],
      "weaknesses": ["string"],
      "opportunity": "string"
    }
  ],
  "trending_topics": [
    {"topic": "string", "relevance": "string", "hashtags": ["string"]}
  ],
  "recommended_keywords": ["string"],
  "content_gaps": ["string"]  // what competitors are missing
}

Be specific, actionable, and tailored to the audience. Use real-sounding but generic competitor names if needed."""

            response = await llm.generate(prompt, system_prompt=system_prompt, temperature=0.8)

            # Parse JSON
            try:
                content = response.content.strip()
                if "```json" in content:
                    content = content.split("```json")[1].split("```")[0].strip()
                elif "```" in content:
                    content = content.split("```")[1].split("```")[0].strip()

                research_data = json.loads(content)
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse research JSON: {e}")
                return AgentResult(
                    success=False,
                    agent_name=self.name,
                    data={},
                    errors=[f"JSON parse error: {e}"],
                )

            # Update state with research findings
            context.set_state("personas", research_data.get("updated_personas", personas))
            context.set_state("competitor_insights", research_data.get("competitor_insights", []))
            context.set_state("trending_topics", research_data.get("trending_topics", []))
            context.set_state("recommended_keywords", research_data.get("recommended_keywords", []))
            context.set_state("content_gaps", research_data.get("content_gaps", []))

            context.log_event("research_complete", self.name, research_data)

            return AgentResult(
                success=True,
                agent_name=self.name,
                data=research_data,
                metadata={"model": response.model, "tokens": response.usage},
            )

        except Exception as e:
            logger.exception("ResearchAgent failed")
            return AgentResult(
                success=False,
                agent_name=self.name,
                data={},
                errors=[str(e)],
            )

    def _build_prompt(
        self,
        business_info: Dict[str, Any],
        icp: str,
        campaign_themes: List[str],
        personas: List[Dict],
    ) -> str:
        product = business_info.get("name", "Product")
        industry = business_info.get("industry", "")

        prompt = f"""As a market researcher, analyze the following scenario:

Product: {product}
Industry: {industry}
ICP: {icp}
Campaign Themes: {', '.join(campaign_themes) if campaign_themes else 'Not yet defined'}

Existing Personas (if any):
{json.dumps(personas, indent=2) if personas else 'None'}

Please provide:
1. 2-3 refined audience personas with detailed psychographics
2. Analysis of 3-5 relevant competitors (real or hypothetical in this space)
3. 5-7 trending topics/hashtags that this audience is engaging with right now
4. Recommended keywords for content and SEO
5. Content gaps - what are competitorsmissing that we can own

Make this specific to the product and audience."""

        return prompt