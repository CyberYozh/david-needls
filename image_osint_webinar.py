# python3 -m venv env   
# source env/bin/activate  
# pip install pillow exifread requests opencv-python pytesseract

# sudo apt update                                               
# sudo apt install tesseract-ocr -y


import sys
import exifread
import cv2
import pytesseract
from PIL import Image

def exif_data(path):
    print("\n[EXIF]")
    with open(path, "rb") as f:
        tags = exifread.process_file(f)

    gps_found = False
    for tag in tags:
        if "GPS" in tag:
            print(tag, tags[tag])
            gps_found = True

    if not gps_found:
        print("No GPS metadata found")

def ocr_text(path):
    print("\n[OCR TEXT DETECTION]")
    img = cv2.imread(path)
    text = pytesseract.image_to_string(img)

    if text.strip():
        print("Detected text:")
        print(text)
    else:
        print("No readable text found")

def basic_image_analysis(path):
    print("\n[IMAGE ANALYSIS]")

    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    edges = cv2.Canny(gray, 100, 200)
    edge_density = edges.mean()

    print(f"Edge density: {edge_density}")

    if edge_density < 20:
        print("Likely smooth environment (indoor / sky / blur)")
    elif edge_density < 60:
        print("Possibly urban or mixed environment")
    else:
        print("Highly detailed scene (urban / dense objects)")

def reverse_search_hint():
    print("\n[REVERSE IMAGE SEARCH MANUAL]")
    print("- https://images.google.com")
    print("- https://yandex.com/images/")
    print("- https://tineye.com")

def main():
    if len(sys.argv) < 2:
        print("Usage: python osint.py image.jpg")
        return

    path = sys.argv[1]

    exif_data(path)
    ocr_text(path)
    basic_image_analysis(path)
    reverse_search_hint()

if __name__ == "__main__":
    main()
