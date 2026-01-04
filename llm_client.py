import os
from dotenv import load_dotenv
from google import genai
import json

load_dotenv(".env")

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("Missing GEMINI_API_KEY in .env")

client = genai.Client(api_key=API_KEY)


async def llm_classify_text(text: str):
    """
    Uses Gemini to correct OCR, classify text, and provide meaning.
    Always returns clean JSON.
    """

    prompt = f"""
You are TECC, a text correction + classification model.

Given OCR text: "{text}"

1. Correct OCR mistakes (only if CLEARLY wrong).
2. Choose the label ONLY from:
   - exit_sign
   - room_number
   - lab
   - direction
   - unknown
3. Do NOT guess. If uncertain → label = "unknown".
4. Return STRICT JSON only. No explanations outside JSON.

Format:
{{
  "corrected": "<corrected text>",
  "label": "<label>",
  "explanation": "<short explanation>"
}}
"""

    try:
        response = client.models.generate_content(
            model="models/gemini-2.5-flash",
            contents=prompt
        )

        raw = response.text.strip()

        # Extract only JSON (remove anything before/after)
        json_start = raw.find("{")
        json_end = raw.rfind("}")

        if json_start == -1 or json_end == -1:
            raise ValueError("No JSON found in LLM output")

        clean = raw[json_start:json_end + 1]
        return clean

    except Exception as e:
        return json.dumps({
            "corrected": text,
            "label": "unknown",
            "explanation": f"LLM error: {str(e)}"
        })
