from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
import numpy as np
import cv2
import aiohttp
import json

from slam_engine.text_detection import extract_text_from_image
from slam_engine.tecc_model import rag_lookup
from llm_client import llm_classify_text  # LLM now working

app = FastAPI()

# GLOBAL SEMANTIC MAP
global_semantic_map = []

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Root -> serve UI
@app.get("/", response_class=HTMLResponse)
async def serve_home():
    return FileResponse("templates/index.html")


# ------------------------------------------------
# Utility: Load image from URL
# ------------------------------------------------
async def load_image_from_url(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers={"User-Agent": "Mozilla/5.0"}) as resp:
            if resp.status != 200:
                raise ValueError(f"Unable to download: HTTP {resp.status}")
            data = await resp.read()

    img_array = np.frombuffer(data, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Image decode failed")
    return img


# ------------------------------------------------
# ANALYZE ENDPOINT (OCR → RAG → LLM → MAP)
# ------------------------------------------------
@app.post("/analyze")
async def analyze_image(request: Request, file: UploadFile = File(None)):

    # Parse JSON if available
    data = {}
    if "application/json" in request.headers.get("content-type", ""):
        data = await request.json()

    image_url = data.get("image_url")
    img = None

    # File upload
    if file:
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img is None:
            return {"error": "Failed to decode uploaded image"}

    # URL upload
    elif image_url:
        try:
            img = await load_image_from_url(image_url)
        except Exception as e:
            return {"error": f"URL load failed: {e}"}

    else:
        return {"error": "Provide either file upload or image_url"}

    # ---------------------------
    # OCR
    # ---------------------------
    detected = extract_text_from_image(img)

    extracted = []
    for d in detected:
        try:
            _, txt, conf = d
            extracted.append((txt, float(conf)))
        except:
            extracted.append((str(d), 1.0))

    annotations = []

    # ---------------------------
    # RAG + LLM TECC
    # ---------------------------
    for txt, conf in extracted:

        # RAG
        rag_res = rag_lookup(txt)

        # LLM TECC
        try:
            llm_raw = await llm_classify_text(txt)
            llm = json.loads(llm_raw)
        except Exception as e:
            llm = {
                "corrected": txt,
                "label": rag_res["matched_text"],
                "explanation": f"LLM error: {e}"
            }

        out = {
            "orig_text": txt,
            "conf": conf,
            "corrected": llm.get("corrected", txt),
            "llm": {
                "label": llm.get("label", rag_res["matched_text"]),
                "explanation": llm.get("explanation", rag_res["meaning"])
            },
            "retrieved": [{
                "id": rag_res["matched_text"],
                "distance": rag_res["distance"]
            }]
        }

        annotations.append(out)

        # Semantic map
        global_semantic_map.append({
            "text": out["corrected"],
            "label": out["llm"]["label"],
            "meaning": out["llm"]["explanation"]
        })

    return JSONResponse({
        "annotations": annotations,
        "semantic_map_size": len(global_semantic_map)
    })


# ------------------------------------------------
# Semantic map endpoint
# ------------------------------------------------
@app.get("/semantic_map")
def get_map():
    return {"semantic_map": global_semantic_map}


# Run server
if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
