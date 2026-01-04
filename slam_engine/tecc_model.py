from sentence_transformers import SentenceTransformer
import faiss
import json
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

# Load KB
records = []
with open("knowledge_base/rag_data.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        records.append(json.loads(line))

texts = [r["text"] for r in records]
ids = [r["id"] for r in records]

embeddings = model.encode(texts, convert_to_numpy=True)

index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)


def rag_lookup(query_text):
    q_emb = model.encode([query_text], convert_to_numpy=True)

    distance, idx = index.search(q_emb, 1)

    best = records[idx[0][0]]
    return {
        "matched_text": best["id"],
        "meaning": best["text"],
        "distance": float(distance[0][0])
    }
global_semantic_map = []
