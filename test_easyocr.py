import easyocr
import cv2

image_path = r"D:\PROJECTS\LP-SLAM-TECC\exit.jpg"

img = cv2.imread(image_path)

if img is None:
    print("❌ Image not found.")
    exit()

print("✔ Image loaded successfully.")

reader = easyocr.Reader(['en'], gpu=False)
result = reader.readtext(img)

print("\n=== OCR RESULT ===")
print(result)
