import asyncio, json
from llm_client import llm_classify_text

async def t():
    out = await llm_classify_text("EXIT")
    print("LLM RAW:", out)
    try:
        parsed = json.loads(out)
        print("PARSED:", parsed)
    except Exception as e:
        print("PARSE ERROR:", e)

asyncio.run(t())
