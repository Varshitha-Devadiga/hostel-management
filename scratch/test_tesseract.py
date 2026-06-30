from PIL import Image
import pytesseract
import os

try:
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    
    # Create a dummy image
    img = Image.new('RGB', (100, 30), color = (73, 109, 137))
    
    # Extract text
    text = pytesseract.image_to_string(img)
    print("Tesseract works! Output:", text)
except Exception as e:
    print("Error:", type(e), e)
