import easyocr

reader = easyocr.Reader(["en"], gpu=False)

def extract_text_local(image_path):
    result = reader.readtext(image_path, detail=0)
    if result:
        return result[0]  # return first detected text
    return None
