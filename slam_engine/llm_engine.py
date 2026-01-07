# slam_engine/llm_engine.py
import os, json
import asyncio

OPENAI_KEY = os.environ.get("OPENAI_API_KEY")
USE_OPENAI = bool(OPENAI_KEY)

if USE_OPENAI:
    import openai
    openai.api_key = OPENAI_KEY

class LLM:
    def __init__(self):
        pass

    async def interpret(self, corrected_text, retrieved_docs, pose=None, conf=0.0):
        # build a short, bounded prompt that asks for JSON
        docs_text = "\n\n".join([f"[{d.get('id','')}] {d.get('text','')}" for d in retrieved_docs]) if retrieved_docs else ""
        prompt = f"""
You are a mapping assistant. Use ONLY the provided context (if any).

Context:
{docs_text}

Detected text: "{corrected_text}"
Pose: {pose}
OCR confidence: {conf}

Return a JSON object with keys:
- label (short)
- explanation (one sentence)
- action (what to annotate on the map)
- sources (list of doc ids)
"""
        # fallback local answer if no API key
        if not USE_OPENAI:
            return {"label": corrected_text.upper(), "explanation": "Local fallback (no OpenAI key)", "action": f"annotate:{corrected_text}", "sources": [d.get("id") for d in retrieved_docs]}

        # call OpenAI completion (simple)
        try:
            resp = openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=200, temperature=0.0)
            text = resp.choices[0].text.strip()
            # extract JSON substring
            jstart = text.find("{"); jend = text.rfind("}")
            if jstart!=-1 and jend!=-1:
                return json.loads(text[jstart:jend+1])
            # fallback wrap
            return {"label": corrected_text.upper(), "explanation": text, "action": f"annotate:{corrected_text}", "sources": [d.get("id") for d in retrieved_docs]}
        except Exception as e:
            return {"label": corrected_text.upper(), "explanation": f"LLM error: {str(e)}", "action": f"annotate:{corrected_text}", "sources": [d.get("id") for d in retrieved_docs]}

