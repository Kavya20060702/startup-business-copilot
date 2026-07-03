import os
from typing import List, Optional
from pydantic import BaseModel, Field
from google import genai
from google.genai import types
from config import GEMINI_API_KEY, DEFAULT_MODEL

class MarketFeasibility(BaseModel):
    score: int = Field(description="Score from 1 to 10 evaluating market viability and growth potential.")
    reasoning: str = Field(description="Explanation behind the market feasibility score.")
    target_market_size: str = Field(description="Estimated TAM/SAM market size analysis.")

class RiskFactor(BaseModel):
    risk_type: str = Field(description="Category of risk e.g. Regulatory, Competition, Execution, Financial.")
    description: str = Field(description="Detailed explanation of the risk.")
    mitigation_strategy: str = Field(description="Actionable advice to minimize or mitigate this risk.")

class BusinessAnalysisReport(BaseModel):
    startup_name: str = Field(description="Name or working title of the startup project.")
    executive_summary: str = Field(description="High-level evaluation summary of the business concept.")
    core_value_prop: str = Field(description="Analysis of the unique value proposition.")
    competitive_advantage: str = Field(description="Key moats or differentiators against existing market players.")
    market_feasibility: MarketFeasibility
    top_risks: List[RiskFactor] = Field(description="Top 3 to 5 key risks identified.")
    strategic_recommendations: List[str] = Field(description="Immediate actionable recommendations for the founders.")

class BusinessAnalystAgent:
    def __init__(self, api_key: Optional[str] = None, model_name: str = DEFAULT_MODEL):
        self.api_key = api_key or GEMINI_API_KEY
        self.model_name = model_name
        if self.api_key:
            self.client = genai.Client(api_key=self.api_key)
        else:
            self.client = None

    def analyze_startup(
        self, 
        startup_name: str, 
        description: str, 
        target_industry: str, 
        business_model: str
    ) -> BusinessAnalysisReport:
        if not self.client:
            # Fallback mock report if API key is not yet configured in environment
            return self._generate_mock_report(startup_name, description)

        prompt = f"""
        You are an expert Senior Venture Capitalist and Startup Business Analyst. 
        Evaluate the following startup concept thoroughly and produce a structured strategic business analysis report.

        Startup Name: {startup_name}
        Target Industry: {target_industry}
        Business Model: {business_model}
        Description: {description}
        """

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=BusinessAnalysisReport,
                temperature=0.3
            )
        )

        return BusinessAnalysisReport.model_validate_json(response.text)

    def _generate_mock_report(self, startup_name: str, description: str) -> BusinessAnalysisReport:
        return BusinessAnalysisReport(
            startup_name=startup_name,
            executive_summary=f"[MOCK MODE - Configure GEMINI_API_KEY to run live model] The concept '{startup_name}' presents an innovative solution in its domain.",
            core_value_prop="Automated decision intelligence and streamlined operations for target customers.",
            competitive_advantage="Proprietary AI workflow integration and first-mover niche automation.",
            market_feasibility=MarketFeasibility(
                score=8,
                reasoning="Strong industry tailwinds around AI adoption and efficiency optimization.",
                target_market_size="Multi-billion dollar global total addressable market (TAM)."
            ),
            top_risks=[
                RiskFactor(
                    risk_type="Execution",
                    description="Customer acquisition cost (CAC) might be high during early scaling phases.",
                    mitigation_strategy="Focus on product-led growth (PLG) and targeted outbound enterprise trials."
                ),
                RiskFactor(
                    risk_type="Competition",
                    description="Incumbents adding fast-follow features into existing software suites.",
                    mitigation_strategy="Build deep customer workflow locks and specialized agent tools."
                )
            ],
            strategic_recommendations=[
                "Validate core unit economics with a 10-customer pilot cohort.",
                "Set up Gemini API keys to unlock dynamic live LLM business reports.",
                "Develop proprietary data loops to strengthen long-term moats."
            ]
        )
