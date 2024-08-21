import cv2
import pytesseract
import re
from PIL import Image
from tkinter import Tk
from tkinter.filedialog import askopenfilename

def capture_image():
    # Initialize camera capture
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Unable to access camera")
        return None

    # Capture a frame
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture image")
        return None

    # Release the camera
    cap.release()

    return frame

def preprocess_image(image):
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply thresholding or other preprocessing techniques as needed
    # For example:
    # _, binary_image = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    return gray

def extract_text(image):
    # Use Tesseract OCR to extract text
    extracted_text = pytesseract.image_to_string(image)
    return extracted_text

def extract_name_dob(text):
    # Extract name and DOB using regular expressions
    name_pattern = r"(?i)(?:Name|Full Name)[:|\s]*(.*?)(?=\n|$)"
    dob_pattern = r"(?i)(?:DOB|Date\s*of\s*Birth)[:|\s]*((?:0?[1-9]|[12][0-9]|3[01])[- /.](?:0?[1-9]|1[0-2])[- /.](?:19|20)?\d{2})"

    name_match = re.search(name_pattern, text)
    dob_match = re.search(dob_pattern, text)

    name = name_match.group(1).strip() if name_match else None
    dob = dob_match.group(1).strip() if dob_match else None

    return name, dob

def upload_image():
    # Open file dialog for image selection
    Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
    filename = askopenfilename()  # show an "Open" dialog box and return the path to the selected file
    if filename:
        image = cv2.imread(filename)
        return image
    else:
        print("Error: No file selected")
        return None

def main():
    # Option to capture image or upload from file
    print("Choose an option:")
    print("1. Capture Image")
    print("2. Upload Image")
    choice = input("Enter your choice (1/2): ")

    if choice == '1':
        # Capture image
        captured_image = capture_image()
        if captured_image is None:
            return
    elif choice == '2':
        # Upload image
        captured_image = upload_image()
        if captured_image is None:
            return
    else:
        print("Invalid choice")
        return

    # Preprocess image
    preprocessed_image = preprocess_image(captured_image)

    # Extract text
    extracted_text = extract_text(preprocessed_image)

    # Display the extracted text
    print("Extracted Text:")
    print(extracted_text)

    # Extract name and DOB
    name, dob = extract_name_dob(extracted_text)

    # Display the extracted name and DOB
    print("Extracted Name:", name)
    print("Extracted DOB:", dob)

if __name__ == "__main__":
    main()
print()