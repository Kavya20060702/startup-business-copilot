import os
from fastapi import APIRouter, HTTPException, status, Query, UploadFile, File
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from typing import List, Dict, Any
from agents.business_analyst import BusinessAnalystAgent, BusinessAnalysisReport
from agents.orchestrator import AgentOrchestrator, StartupDossier
from agents.chat_assistant import ChatAssistantAgent
from memory.vector_store import StartupVectorStore
from reports.pdf_generator import generate_dossier_pdf
from tools.file_parser import parse_uploaded_file, UPLOADS_DIR

router = APIRouter(prefix="/api/v1", tags=["AI Agents"])
vector_store = StartupVectorStore()

class AnalyzeStartupRequest(BaseModel):
    startup_name: str = Field(..., example="SupplyChain AI")
    description: str = Field(..., example="Autonomous logistics optimization platform for mid-sized freight companies.")
    target_industry: str = Field(default="Logistics & Supply Chain", example="Logistics & Supply Chain")
    business_model: str = Field(default="B2B SaaS", example="B2B SaaS Subscription")

class FullDossierRequest(BaseModel):
    startup_name: str = Field(..., example="FreightFlow AI")
    description: str = Field(..., example="An autonomous AI platform that predicts shipping delays and re-routes regional freight vehicles.")
    target_industry: str = Field(default="Logistics & Supply Chain", example="Logistics & Supply Chain")
    business_model: str = Field(default="B2B SaaS Subscription", example="B2B SaaS Subscription")
    pricing_details: str = Field(..., example="$500/month per fleet hub + tiered usage based on miles tracked.")
    funding_raised: str = Field(default="$1.2M Seed", example="$1.2M Seed")
    monthly_expenses: str = Field(default="$45,000/month", example="$45,000/month")
    known_competitors: str = Field(default="LegacyLogistics, FleetTech, manual dispatchers", example="LegacyLogistics, FleetTech")

class ChatRequest(BaseModel):
    question: str = Field(..., example="What is the biggest risk for this startup?")
    context: str = Field(default="", example="Startup FreightFlow AI evaluation summary.")

@router.post("/analyze", response_model=BusinessAnalysisReport)
def analyze_startup(request: AnalyzeStartupRequest):
    try:
        agent = BusinessAnalystAgent()
        report = agent.analyze_startup(
            startup_name=request.startup_name,
            description=request.description,
            target_industry=request.target_industry,
            business_model=request.business_model
        )
        return report
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error running Business Analyst Agent: {str(e)}"
        )

@router.post("/dossier", response_model=StartupDossier)
def generate_dossier(request: FullDossierRequest):
    try:
        orchestrator = AgentOrchestrator()
        dossier = orchestrator.generate_full_dossier(
            startup_name=request.startup_name,
            description=request.description,
            target_industry=request.target_industry,
            business_model=request.business_model,
            pricing_details=request.pricing_details,
            funding_raised=request.funding_raised,
            monthly_expenses=request.monthly_expenses,
            known_competitors=request.known_competitors
        )

        vector_store.save_dossier_benchmark(
            startup_name=dossier.startup_name,
            industry=request.target_industry,
            summary=dossier.executive_dossier_summary,
            grade=dossier.overall_investment_grade
        )

        return dossier
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error running Multi-Agent Orchestrator: {str(e)}"
        )

@router.post("/dossier/pdf")
def generate_dossier_pdf_endpoint(request: FullDossierRequest):
    try:
        orchestrator = AgentOrchestrator()
        dossier = orchestrator.generate_full_dossier(
            startup_name=request.startup_name,
            description=request.description,
            target_industry=request.target_industry,
            business_model=request.business_model,
            pricing_details=request.pricing_details,
            funding_raised=request.funding_raised,
            monthly_expenses=request.monthly_expenses,
            known_competitors=request.known_competitors
        )

        pdf_path = generate_dossier_pdf(dossier.model_dump())
        filename = os.path.basename(pdf_path)
        media_type = "application/pdf" if pdf_path.endswith(".pdf") else "text/plain"

        return FileResponse(path=pdf_path, filename=filename, media_type=media_type)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating PDF dossier: {str(e)}"
        )

@router.get("/memory/similar")
def get_similar_benchmarks(query: str = Query(..., example="Logistics SaaS AI")):
    try:
        benchmarks = vector_store.search_similar_benchmarks(query=query)
        return {"query": query, "results": benchmarks}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error querying memory store: {str(e)}"
        )

@router.post("/upload")
async def upload_pitch_file(file: UploadFile = File(...)):
    try:
        os.makedirs(UPLOADS_DIR, exist_ok=True)
        file_path = os.path.join(UPLOADS_DIR, file.filename)
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        parsed_data = parse_uploaded_file(file_path)
        return {"status": "success", "data": parsed_data}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing uploaded file: {str(e)}"
        )

@router.post("/chat")
def chat_with_copilot(request: ChatRequest):
    try:
        assistant = ChatAssistantAgent()
        reply = assistant.answer_vc_question(
            user_question=request.question,
            startup_context=request.context
        )
        return {"reply": reply}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error in Chat Copilot: {str(e)}"
        )
