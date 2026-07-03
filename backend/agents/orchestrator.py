import concurrent.futures
from typing import Optional
from pydantic import BaseModel, Field
from agents.business_analyst import BusinessAnalystAgent, BusinessAnalysisReport
from agents.financial_analyst import FinancialAnalystAgent, FinancialAnalysisReport
from agents.competitor_agent import CompetitorAgent, CompetitorIntelligenceReport

class StartupDossier(BaseModel):
    startup_name: str = Field(description="Name of the evaluated startup.")
    overall_investment_grade: str = Field(description="Synthesized investment rating (e.g. Strongly Recommended, Strong Potential with Risks, High Risk).")
    executive_dossier_summary: str = Field(description="Unified summary synthesising business, financial, and competitive insights.")
    business_analysis: BusinessAnalysisReport
    financial_analysis: FinancialAnalysisReport
    competitor_intelligence: CompetitorIntelligenceReport

class AgentOrchestrator:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.business_agent = BusinessAnalystAgent(api_key=self.api_key)
        self.financial_agent = FinancialAnalystAgent(api_key=self.api_key)
        self.competitor_agent = CompetitorAgent(api_key=self.api_key)

    def generate_full_dossier(
        self,
        startup_name: str,
        description: str,
        target_industry: str,
        business_model: str,
        pricing_details: str,
        funding_raised: str,
        monthly_expenses: str,
        known_competitors: str
    ) -> StartupDossier:
        # Run agent evaluations in parallel for optimal performance
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_business = executor.submit(
                self.business_agent.analyze_startup,
                startup_name=startup_name,
                description=description,
                target_industry=target_industry,
                business_model=business_model
            )
            future_financial = executor.submit(
                self.financial_agent.analyze_financials,
                startup_name=startup_name,
                pricing_details=pricing_details,
                funding_raised=funding_raised,
                monthly_expenses=monthly_expenses
            )
            future_competitor = executor.submit(
                self.competitor_agent.analyze_competition,
                startup_name=startup_name,
                description=description,
                known_competitors=known_competitors
            )

            business_report = future_business.result()
            financial_report = future_financial.result()
            competitor_report = future_competitor.result()

        # Synthesize investment grade rating based on composite scores
        avg_score = (
            business_report.market_feasibility.score + 
            financial_report.revenue_scalability_score + 
            competitor_report.defensibility_score
        ) / 3.0

        if avg_score >= 8.0:
            investment_grade = "Grade A - Strongly Recommended for Investment"
        elif avg_score >= 6.0:
            investment_grade = "Grade B - Strong Potential with Manageable Risks"
        else:
            investment_grade = "Grade C - High Risk / Requires Pivoting"

        summary = f"Synthesized analysis for '{startup_name}'. Composite evaluation score: {avg_score:.1f}/10. The company shows strong market viability combined with scalable unit economics."

        return StartupDossier(
            startup_name=startup_name,
            overall_investment_grade=investment_grade,
            executive_dossier_summary=summary,
            business_analysis=business_report,
            financial_analysis=financial_report,
            competitor_intelligence=competitor_report
        )
