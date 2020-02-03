try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'

def ocr(file):
    """
    This function will convert an image into a string.
    """
    text = pytesseract.image_to_string(Image.open(file))
    return text

#print(ocr(r"images\firestones_h.png"))
print(ocr(r"images\firestones_f.png"))