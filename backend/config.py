import os
from dotenv import load_dotenv

# Explicitly load .env file from config.py directory
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
load_dotenv(dotenv_path=env_path)

PROJECT_NAME = "Startup Business Copilot"
VERSION = "0.1.0"

# Gemini API Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
DEFAULT_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
