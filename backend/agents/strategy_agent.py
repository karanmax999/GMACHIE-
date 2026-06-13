"""GTM Strategy Agent - Creates the overall GTM plan."""

from typing import Dict, Any
from core.agent import BaseAgent, AgentInput, AgentResult, AgentContext, agent
from core.llm import get_llm_client
from loguru import logger
import json


@agent("strategy")
class StrategyAgent(BaseAgent):
    """Creates GTM strategy plan based on product and ICP."""

    name = "strategy"
    description = "Creates GTM strategy, channel selection, messaging pillars, and KPI targets"

    async def execute(self, input_data: AgentInput, context: AgentContext) -> AgentResult:
        """Generate GTM strategy."""
        try:
            business_info = context.get_state("business_info", {})
            goal = context.get_state("goal", "")
            icp = context.get_state("icp", "")

            llm = get_llm_client()

            prompt = self._build_prompt(business_info, goal, icp)
            system_prompt = """You are an expert GTM strategist for AI-powered products.
Your task: design a go-to-market plan that is specific, actionable, and metrics-driven.

Output format: valid JSON with these keys:
{
  "positioning": "string - clear value proposition",
  "target_audience": "string - refined audience description",
  "channels": [
    {"name": "string", "primary": bool, "why": "string", "expected_reach": "string"}
  ],
  "campaign_themes": ["string"],
  "kpi_targets": {
    "week1": {"impressions": number, "clicks": number, "signups": number},
    "week2": {...}
  },
  "north_star_metric": "string - primary success metric"
}

Be concrete: include numbers, specific platforms, and clear reasoning."""

            response = await llm.generate(prompt, system_prompt=system_prompt, temperature=0.7)

            # Parse JSON from response
            try:
                content = response.content.strip()
                if "```json" in content:
                    content = content.split("```json")[1].split("```")[0].strip()
                elif "```" in content:
                    content = content.split("```")[1].split("```")[0].strip()

                strategy_data = json.loads(content)
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse strategy JSON: {e}")
                return AgentResult(
                    success=False,
                    agent_name=self.name,
                    data={},
                    errors=[f"JSON parse error: {e}", f"Response was: {response.content[:500]}"],
                )

            # Store results in state
            context.set_state("gtm_plan", strategy_data)
            context.set_state("positioning", strategy_data.get("positioning"))
            context.set_state("channels", strategy_data.get("channels", []))
            context.set_state("campaign_themes", strategy_data.get("campaign_themes", []))
            context.set_state("kpi_targets", strategy_data.get("kpi_targets", {}))
            context.set_state("north_star_metric", strategy_data.get("north_star_metric"))

            context.log_event("strategy_complete", self.name, strategy_data)

            return AgentResult(
                success=True,
                agent_name=self.name,
                data=strategy_data,
                metadata={"model": response.model, "tokens": response.usage},
            )

        except Exception as e:
            logger.exception("StrategyAgent failed")
            return AgentResult(
                success=False,
                agent_name=self.name,
                data={},
                errors=[str(e)],
            )

    def _build_prompt(self, business_info: Dict[str, Any], goal: str, icp: str) -> str:
        """Construct the prompt for the strategy agent."""
        name = business_info.get("name", "Product")
        description = business_info.get("description", "")
        industry = business_info.get("industry", "")
        website = business_info.get("website", "")

        prompt = f"""Create a GTM strategy for the following:

Product Name: {name}
Description: {description}
Industry: {industry}
Website: {website}

Target Audience (ICP): {icp}

Goal: {goal}

Please provide a detailed GTM strategy in JSON format as specified."""

        return prompt