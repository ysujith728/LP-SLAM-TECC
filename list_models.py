import os
from dotenv import load_dotenv
from google import genai

# Load .env file
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("❌ GEMINI_API_KEY missing from .env")

client = genai.Client(api_key=API_KEY)

print("\n=== AVAILABLE GEMINI MODELS ===")

models = client.models.list()

for m in models:
    print("-", m.name)
