from slam_engine.text_detection import extract_text_from_image
from slam_engine.tecc_model import rag_lookup

print("\n=== Testing Full Pipeline (OCR → RAG) ===")

# image generated earlier
image_path = "exit.jpg"

# run OCR
ocr_texts = extract_text_from_image(image_path)
print("\nOCR OUTPUT:", ocr_texts)

# if OCR found text
if ocr_texts:
    text = ocr_texts[0]
    rag_result = rag_lookup(text)
    print("\nRAG RESULT:", rag_result)
else:
    print("\n❌ No text detected by OCR.")
