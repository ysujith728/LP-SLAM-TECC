import json
import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class RAGEngine:
    def __init__(self, db_path="slam_engine/tecc_db.json"):
        self.db_path = db_path

        # Embedding model
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        # Load DB
        self.data = self.load_database()

        # Build FAISS index
        self.index, self.vectors = self.build_faiss_index()

    def load_database(self):
        if not os.path.exists(self.db_path):
            raise FileNotFoundError("❌ tecc_db.json not found!")

        with open(self.db_path, "r") as f:
            return json.load(f)

    def build_faiss_index(self):
        # Create embeddings
        texts = [item["text"] for item in self.data]
        vectors = self.model.encode(texts)

        # Convert to float32 numpy
        vectors = np.array(vectors).astype("float32")

        # Create FAISS index
        dim = vectors.shape[1]
        index = faiss.IndexFlatL2(dim)
        index.add(vectors)

        return index, vectors

    def query(self, user_text, top_k=1):
        emb = self.model.encode([user_text]).astype("float32")
        distances, indices = self.index.search(emb, top_k)

        result = self.data[indices[0][0]]
        return {
            "matched_text": result["text"],
            "meaning": result.get("meaning", "No meaning provided"),
            "distance": float(distances[0][0]),
        }
