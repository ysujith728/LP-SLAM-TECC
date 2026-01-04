import json

print("\n=== Checking rag_data.jsonl ===")

try:
    with open("knowledge_base/rag_data.jsonl", "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            print(f"Line {i+1}: {line.strip()}")

    print("\n✔ File loaded successfully.\n")

except Exception as e:
    print("\n❌ Error reading file:", e)
