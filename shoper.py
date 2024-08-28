import sys
import cv2
import pytesseract
from PIL import Image
import numpy as np
import json
import re

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def preprocess_image(image_path):
    print("Loading image...")
    img = cv2.imread(image_path)
    cv2.imshow('Original Image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    print("Applying Gaussian blur...")
    img = cv2.GaussianBlur(img, (5, 5), 0)
    cv2.imshow('Blurred Image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


    print("Converting to grayscale...")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imshow('Grayscale Image', gray)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    print("Applying binary thresholding...")
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    cv2.imshow('Binary Image', binary)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    print("Applying binary thresholding...")
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    cv2.imshow('Binary Image', binary)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return binary

def extract_text(image):
    custom_config = r'--oem 3 --psm 6'
    lang = 'eng'
    text = pytesseract.image_to_string(image, config=custom_config, lang=lang)
    return text

def parse_receipt_text(text):
    lines = text.splitlines()
    all_data = []
    items = []

    for line in lines:
        parts = line.split()
        
        # Store each line's raw text for general information
        all_data.append(line)
        
        # Check if the line contains a quantity and a price
        if len(parts) > 2:
            for i in range(len(parts) - 1):
                if parts[i].isdigit() and re.search(r'\d+(?:\.\d+)?', parts[i+1]):
                    quantity = int(parts[i])
                    price = parts[i+1]
                    name = ' '.join(parts[:i])
                    # Check if the name is not empty and does not contain keywords like "Tabte", "Bis", etc.
                    if name and not any(keyword in name for keyword in ["Tabte", "Bis", "Sub Total", "Cast", "Change", "Thank", "Proase"]):
                        items.append({"name": name, "quantity": quantity, "price": price})
                        break
                
                
                elif re.search(r'\d+(?:\.\d+)?', parts[i]):
                    price = parts[i]
                    quantity = 1
                    name = ' '.join(parts[:i] + parts[i+1:])
                    # Check if the name is not empty and does not contain keywords like "Tabte", "Bis", etc.
                    if name and not any(keyword in name for keyword in ["Tabte", "Bis", "Sub Total", "Cast", "Change", "Thank", "Proase"]):
                        items.append({"name": name, "quantity": quantity, "price": price})
                        break

    return {"all_data": all_data, "items": items}

def save_to_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def main(image_path):
    processed_image = preprocess_image(image_path)
    text = extract_text(processed_image)
    parsed_data = parse_receipt_text(text)
    save_to_json(parsed_data, 'sales_data.json')

    print("\nExtracted Items:")
    for item in parsed_data["items"]:
        print(f"{item['name']}: {item['quantity']}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python shoper.py <image_path>")
        sys.exit(1)
    
    image_path = sys.argv[1]
    main(image_path)
