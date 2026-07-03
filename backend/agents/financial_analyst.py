import os
from typing import List, Optional
from pydantic import BaseModel, Field
from google import genai
from google.genai import types
from config import GEMINI_API_KEY, DEFAULT_MODEL

class UnitEconomics(BaseModel):
    customer_acquisition_cost: str = Field(description="Evaluation of Customer Acquisition Cost (CAC).")
    lifetime_value: str = Field(description="Evaluation of Customer Lifetime Value (LTV) or LTV:CAC ratio.")
    payback_period_months: int = Field(description="Estimated months required to recover acquisition costs.")

class FinancialAnalysisReport(BaseModel):
    pricing_model_assessment: str = Field(description="Analysis of current pricing architecture (e.g. SaaS tiers, usage-based).")
    revenue_scalability_score: int = Field(description="Rating from 1 to 10 on how scalable the revenue model is.")
    unit_economics: UnitEconomics
    cash_burn_risks: List[str] = Field(description="Identified key risks related to operational cash burn or capital intensity.")
    financial_recommendations: List[str] = Field(description="Actionable advice to improve financial margins and monetization.")

class FinancialAnalystAgent:
    def __init__(self, api_key: Optional[str] = None, model_name: str = DEFAULT_MODEL):
        self.api_key = api_key or GEMINI_API_KEY
        self.model_name = model_name
        if self.api_key:
            self.client = genai.Client(api_key=self.api_key)
        else:
            self.client = None

    def analyze_financials(
        self, 
        startup_name: str, 
        pricing_details: str, 
        funding_raised: str, 
        monthly_expenses: str
    ) -> FinancialAnalysisReport:
        if not self.client:
            return self._generate_mock_report()

        prompt = f"""
        You are a seasoned CFO and Venture Capital Financial Analyst. 
        Evaluate the financial viability, unit economics, and cash burn dynamics of this startup.

        Startup Name: {startup_name}
        Pricing & Monetization Details: {pricing_details}
        Funding Raised to Date: {funding_raised}
        Estimated Monthly Operating Expenses: {monthly_expenses}
        """

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=FinancialAnalysisReport,
                temperature=0.3
            )
        )

        return FinancialAnalysisReport.model_validate_json(response.text)

    def _generate_mock_report(self) -> FinancialAnalysisReport:
        return FinancialAnalysisReport(
            pricing_model_assessment="[MOCK MODE] Tiered subscription model aligns well with SMB and Enterprise segments.",
            revenue_scalability_score=9,
            unit_economics=UnitEconomics(
                customer_acquisition_cost="Estimated at $450 per enterprise deal through digital channels.",
                lifetime_value="Estimated at $5,400 assuming 36-month average retention, yielding a healthy ~12x LTV:CAC.",
                payback_period_months=5
            ),
            cash_burn_risks=[
                "High early engineering overhead prior to achieving scalable self-serve onboarding.",
                "Potential sales cycle drag for enterprise tier implementations."
            ],
            financial_recommendations=[
                "Introduce annual billing discounts to upfront lock cash flow.",
                "Implement automated self-service tier to lower mid-market acquisition costs."
            ]
        )
