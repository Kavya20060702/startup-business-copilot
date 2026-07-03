# 🚀 Startup Business Copilot

### AI-Powered Multi-Agent Business Intelligence Platform

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![Google Gemini](https://img.shields.io/badge/Google-Gemini-orange)
![ChromaDB](https://img.shields.io/badge/RAG-ChromaDB-red)
![License](https://img.shields.io/badge/License-MIT-yellow)

Startup Business Copilot is an AI-powered business intelligence platform that helps founders, investors, and business analysts evaluate startups through a collaborative multi-agent workflow.

The platform combines specialized AI agents, Google Gemini, vector memory (RAG), real-time market intelligence, and automated executive reporting to generate comprehensive startup analyses and strategic recommendations.

---

# 🎯 Problem Statement

Evaluating a startup requires expertise across multiple domains including business strategy, financial planning, competitive analysis, and market research. This process is often time-consuming, expensive, and requires multiple specialists.

Startup Business Copilot simplifies this workflow by coordinating multiple AI agents that collaborate to analyze business information, generate insights, and produce professional reports within minutes.

---

# ✨ Features

- 🤖 Multi-Agent AI Architecture
- 💼 Business Analyst Agent
- 💰 Financial Analyst Agent
- 📈 Competitor Intelligence Agent
- 💬 AI Chat Copilot
- 🧠 Vector Memory (RAG) using ChromaDB
- 🌐 Real-Time Market Intelligence
- 📄 Executive PDF Report Generator
- 📁 PDF & CSV Document Parsing
- 📊 Interactive Business Dashboard
- ⚡ FastAPI REST API
- 🎨 Modern Responsive Web Interface

---

# 🌟 Why This Project Stands Out

Unlike traditional AI assistants that rely on a single prompt-response workflow, Startup Business Copilot distributes responsibilities across specialized AI agents.

Each agent focuses on a specific domain—business strategy, financial analysis, competitor intelligence, and user interaction—resulting in more structured analysis and clearer decision support.

## Key Highlights

- 🤖 **Multi-Agent Collaboration** — Specialized Business, Financial, Competitor, and Chat Assistant agents coordinated through an orchestration layer.
- 🧠 **Retrieval-Augmented Generation (RAG)** — ChromaDB stores previous startup evaluations and retrieves similar companies for contextual recommendations.
- 📊 **Business Intelligence** — Generates structured insights covering business models, financial health, market opportunities, and strategic risks.
- 📄 **Executive Reports** — Automatically produces professional PDF reports suitable for founders, investors, and stakeholders.
- 🌐 **Real-Time Market Intelligence** — Uses web search capabilities to enrich competitor analysis with current market information.
- 📁 **Document Processing** — Extracts and analyzes information from uploaded PDF pitch decks and CSV financial data.
- 💬 **Interactive AI Assistant** — Supports follow-up questions after analysis without restarting the workflow.
- ⚡ **Modern Full-Stack Platform** — Built with FastAPI and a responsive frontend for a seamless user experience.
- 🏗️ **Modular Architecture** — Agents, tools, memory, APIs, and reporting modules are independently organized for scalability and maintenance.

---

# 🏢 Real-World Applications

- Startup Due Diligence
- Venture Capital Screening
- Investment Research
- Business Consulting
- Market Analysis
- Founder Decision Support
- Strategic Business Evaluation

---

# 🏗️ System Architecture

> **Architecture Diagram**

<img width="1284" height="832" alt="Image" src="https://github.com/user-attachments/assets/203a6f49-8a3d-42bb-b278-09424ba3255e" />

---

# 🔄 Workflow

```
                User
                  │
                  ▼
        Upload PDF / CSV / Startup Details
                  │
                  ▼
          Business Analyst Agent
                  │
                  ▼
         Financial Analyst Agent
                  │
                  ▼
      Competitor Intelligence Agent
                  │
                  ▼
         Vector Memory (ChromaDB)
                  │
                  ▼
      Executive PDF Report Generator
                  │
                  ▼
        Interactive Dashboard & Chat
```

---

# 🤖 AI Agents

## 💼 Business Analyst

Analyzes:

- Business Model
- Value Proposition
- Product-Market Fit
- Risks
- Strategic Recommendations

---

## 💰 Financial Analyst

Evaluates:

- Revenue Model
- Burn Rate
- Unit Economics
- Pricing Strategy
- Financial Health

---

## 📈 Competitor Intelligence Agent

Performs:

- Competitor Discovery
- SWOT Analysis
- Market Positioning
- Competitive Moat Evaluation

---

## 💬 Chat Copilot

Allows users to ask follow-up questions after the initial analysis.

Example:

> "What are the biggest financial risks for this startup?"

---

# 🧠 Vector Memory (RAG)

The platform stores previous startup evaluations in ChromaDB and retrieves similar startups to provide contextual recommendations.

This enables:

- Historical Comparisons
- Semantic Search
- Context-Aware Recommendations

---

# 📄 Executive Reports

Automatically generates professional PDF reports including:

- Executive Summary
- Business Analysis
- Financial Review
- Competitor Analysis
- Investment Score
- Strategic Recommendations

---

# 🚀 Technology Stack

## Backend

- Python
- FastAPI
- Google Gemini API
- ChromaDB
- ReportLab
- Pandas

## Frontend

- HTML
- CSS
- JavaScript

## AI Technologies

- Multi-Agent Architecture
- Retrieval-Augmented Generation (RAG)
- Semantic Vector Search
- Real-Time Web Search

---

# 🌐 REST API

| Endpoint | Description |
|----------|-------------|
| GET / | Application Status |
| POST /api/v1/analyze | Startup Analysis |
| POST /api/v1/dossier | Multi-Agent Evaluation |
| POST /api/v1/dossier/pdf | Generate Executive Report |
| GET /api/v1/memory/similar | Search Similar Startups |

---

# 📁 Project Structure

```
startup-business-copilot/
│
├── backend/
│   ├── agents/
│   ├── api/
│   ├── memory/
│   ├── reports/
│   ├── skills/
│   ├── tools/
│   ├── uploads/
│   ├── config.py
│   ├── main.py
│   └── requirements.txt
│
├── frontend/
│
├── docs/
│
├── screenshots/
│
├── README.md
├── LICENSE
└── .gitignore
```

---

# 📸 Screenshots

> Add screenshots inside the **screenshots/** folder.

Suggested screenshots:

- Dashboard
- Startup Analysis
- AI Chat
- Executive PDF
- Vector Memory Search

---

# 🚀 Installation

```bash
git clone https://github.com/Kavya20060702/startup-business-copilot.git

cd startup-business-copilot

cd backend

python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate

pip install -r requirements.txt

uvicorn main:app --reload
```

---

# 🎯 Future Improvements

- Google ADK Integration
- MCP Server Support
- Cloud Deployment
- Multi-Language Support
- Investor CRM Integration
- Team Collaboration
- Advanced Business Analytics

---

# 🏆 Project Highlights

- 🤖 Multi-Agent AI Workflow
- 🧠 Vector Memory with ChromaDB
- 🌐 Real-Time Market Intelligence
- 📄 Automated Executive Reports
- 📊 Interactive Dashboard
- 💬 AI Chat Assistant
- ⚡ FastAPI Backend
- 🎨 Modern Responsive UI

---

# 🙏 Acknowledgements

This project was developed as part of Kaggle's **AI Agents: Intensive Vibe Coding Capstone Project with Google**.

It demonstrates practical applications of multi-agent AI, retrieval-augmented generation (RAG), business intelligence, and intelligent workflow orchestration for startup evaluation.

---

# 📄 License

This project is licensed under the MIT License.
