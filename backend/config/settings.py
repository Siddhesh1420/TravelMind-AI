import os
from dotenv import load_dotenv

load_dotenv()

# ── LLM ──────────────────────────────────────────
USE_LOCAL = os.getenv("USE_LOCAL", "false").lower() == "true"
GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:7b")
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.1"))
LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "6000"))
LLM_SLEEP_SECONDS = int(os.getenv("LLM_SLEEP_SECONDS", "15"))

# ── API Keys ──────────────────────────────────────
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
SERPAPI_KEY = os.getenv("SERPAPI_KEY")
OPENWEATHERMAP_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")

# ── Agent Behavior ────────────────────────────────
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
RETRY_BACKOFF = float(os.getenv("RETRY_BACKOFF", "15.0"))

# ── Data Limits ───────────────────────────────────
MAX_HOTELS = int(os.getenv("MAX_HOTELS", "2"))
MAX_FLIGHTS = int(os.getenv("MAX_FLIGHTS", "2"))
MAX_TRAINS = int(os.getenv("MAX_TRAINS", "2"))
MAX_ATTRACTIONS = int(os.getenv("MAX_ATTRACTIONS", "3"))
MAX_TIPS = int(os.getenv("MAX_TIPS", "2"))
ATTRACTION_CONTENT_LENGTH = int(os.getenv("ATTRACTION_CONTENT_LENGTH", "100"))
TIP_CONTENT_LENGTH = int(os.getenv("TIP_CONTENT_LENGTH", "150"))

# ── Auth ──────────────────────────────────────────
SECRET_KEY = os.getenv("SECRET_KEY", "travelmind-secret-key-change-in-production")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("TOKEN_EXPIRE", "30"))

# ── Rate Limiting ─────────────────────────────────
RATE_LIMIT = os.getenv("RATE_LIMIT", "5/minute")

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:8000/auth/callback")

SECRET_KEY = os.getenv("SECRET_KEY", "travelmind-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30