from slam_engine.rag_engine import RAGEngine

rag = RAGEngine()

query = "exit door"
result = rag.query(query)

print("\n=== RAG RESULT ===")
print(result)
