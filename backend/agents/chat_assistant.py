import os
from typing import Optional, List, Dict
from google import genai
from config import GEMINI_API_KEY, DEFAULT_MODEL

class ChatAssistantAgent:
    def __init__(self, api_key: Optional[str] = None, model_name: str = DEFAULT_MODEL):
        self.api_key = api_key or GEMINI_API_KEY
        self.model_name = model_name
        if self.api_key:
            self.client = genai.Client(api_key=self.api_key)
        else:
            self.client = None

    def answer_vc_question(
        self, 
        user_question: str, 
        startup_context: str
    ) -> str:
        if not self.client:
            return f"[MOCK CHAT COPILOT] In response to your question ('{user_question}'): Based on our analysis of this startup, unit economics show strong resilience, but we recommend monitoring CAC payback periods closely."

        prompt = f"""
        You are an expert VC Investment Director and Business Copilot.
        The user (Venture Capital Investor or Founder) is asking a follow-up question regarding an evaluated startup.

        Startup Context & Evaluation Summary:
        {startup_context}

        User Question:
        {user_question}

        Provide a concise, sharp, professional VC-level advice and analysis in response.
        """

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt
        )

        return response.text
