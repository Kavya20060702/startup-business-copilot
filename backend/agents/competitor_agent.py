import os
from typing import List, Optional
from pydantic import BaseModel, Field
from google import genai
from google.genai import types
from config import GEMINI_API_KEY, DEFAULT_MODEL
from tools.web_search import perform_live_web_search

class CompetitorProfile(BaseModel):
    name: str = Field(description="Name of key competitor or alternative solution.")
    market_share_tier: str = Field(description="Dominance level (e.g. Market Leader, Challenger, Niche Player).")
    key_advantages: List[str] = Field(description="Primary strengths of this competitor.")
    vulnerabilities: List[str] = Field(description="Gaps or weaknesses this startup can exploit.")

class CompetitorIntelligenceReport(BaseModel):
    key_competitors: List[CompetitorProfile] = Field(description="Profile of top competitors in this space.")
    defensibility_score: int = Field(description="Score from 1 to 10 on defensibility and moat creation.")
    defensive_moats: List[str] = Field(description="Moats (network effects, switching costs, proprietary tech).")
    positioning_strategy: str = Field(description="Recommended strategic market positioning.")

class CompetitorAgent:
    def __init__(self, api_key: Optional[str] = None, model_name: str = DEFAULT_MODEL):
        self.api_key = api_key or GEMINI_API_KEY
        self.model_name = model_name
        if self.api_key:
            self.client = genai.Client(api_key=self.api_key)
        else:
            self.client = None

    def analyze_competition(
        self, 
        startup_name: str, 
        description: str, 
        known_competitors: str
    ) -> CompetitorIntelligenceReport:
        # Trigger live web search to discover real-time competitor signals
        web_results = perform_live_web_search(query=f"{known_competitors} competitors market news")
        web_context = "\n".join([f"- {r['title']}: {r['snippet']}" for r in web_results])

        if not self.client:
            return self._generate_mock_report()

        prompt = f"""
        You are a Competitive Intelligence and Market Strategy Specialist.
        Analyze the competitive landscape and defensive moats for this startup, utilizing the live market signals provided.

        Startup Name: {startup_name}
        Description: {description}
        Known Competitors / Incumbents: {known_competitors}

        Live Web Market Intelligence Snippets:
        {web_context}
        """

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=CompetitorIntelligenceReport,
                temperature=0.3
            )
        )

        return CompetitorIntelligenceReport.model_validate_json(response.text)

    def _generate_mock_report(self) -> CompetitorIntelligenceReport:
        return CompetitorIntelligenceReport(
            key_competitors=[
                CompetitorProfile(
                    name="LegacyLogistics Corp",
                    market_share_tier="Market Leader",
                    key_advantages=["Established enterprise sales networks", "Deep carrier integrations"],
                    vulnerabilities=["Slow manual dispatch workflows", "Lack of real-time AI predictive routing"]
                ),
                CompetitorProfile(
                    name="FleetTech Solutions",
                    market_share_tier="Challenger",
                    key_advantages=["Modern telemetry hardware tracking"],
                    vulnerabilities=["Rigid pricing", "No automated re-routing engine"]
                )
            ],
            defensibility_score=8,
            defensive_moats=[
                "Proprietary AI routing algorithms improving with network fleet mileage data.",
                "High customer workflow integration creating strong switching costs."
            ],
            positioning_strategy="Position as the intelligent real-time AI layer sitting on top of existing telematics, avoiding direct hardware replacement battles."
        )
