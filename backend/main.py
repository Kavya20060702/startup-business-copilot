import os
import sys
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# Ensure backend directory is in python path
SYS_BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(SYS_BACKEND_DIR)

from api.agent_router import router as agent_router

app = FastAPI(
    title="Startup Business Copilot API",
    description="Multi-agent AI business analysis powered by Google ADK & Gemini",
    version="0.1.0"
)

# Include API Router
app.include_router(agent_router)

# Mount Static Files for Modern Frontend Web Dashboard
FRONTEND_DIR = os.path.join(os.path.dirname(SYS_BACKEND_DIR), "frontend")
if os.path.exists(FRONTEND_DIR):
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="static_frontend")
