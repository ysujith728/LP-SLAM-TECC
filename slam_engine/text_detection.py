import easyocr
import cv2
import numpy as np

# Load OCR model once
reader = easyocr.Reader(['en'], gpu=False)

def extract_text_from_image(img):
    """
    Accepts an OpenCV BGR image (numpy array)
    Returns EasyOCR-style results: [ [bbox, text, conf], ... ]
    """

    if img is None:
        return []

    # Convert BGR → RGB (EasyOCR expects RGB)
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    results = reader.readtext(rgb)  # returns [ [bbox, text, conf], ... ]

    return results

