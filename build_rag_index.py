# build_rag_index.py
import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

DOCS_PATH = "rag_docs.jsonl"
INDEX_PATH = "rag_index.faiss"


def load_docs(docs_path):
    docs = []
    with open(docs_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            docs.append(json.loads(line))
    return docs


def build_index(docs):
    print("Loading embedding model: all-MiniLM-L6-v2 ...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    print(f"Encoding {len(docs)} documents...")
    texts = [d["text"] for d in docs]
    embeddings = model.encode(texts, convert_to_numpy=True)

    # FAISS requires float32
    embeddings = embeddings.astype("float32")

    dim = embeddings.shape[1]
    print(f"Embedding dimension = {dim}")

    print("Creating FAISS index...")
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    print(f"Saving index to {INDEX_PATH} ...")
    faiss.write_index(index, INDEX_PATH)

    print("Done! RAG index built successfully.")


if __name__ == "__main__":
    print("Reading documents...")
    docs = load_docs(DOCS_PATH)
    if not docs:
        print("ERROR: rag_docs.jsonl is empty!")
        exit(1)

    build_index(docs)
