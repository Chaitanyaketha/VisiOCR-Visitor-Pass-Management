import cv2
import pytesseract
import re
import pytesseract

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class Aadhar_OCR:
    def __init__(self, img_path):
        self.user_aadhar_no = ''
        self.user_gender = ''
        self.user_dob = ''
        self.user_name = ''
        self.img_name = img_path
    
    def extract_data(self):
        # Reading the image, extracting text from it, and storing the text into a list.
        img = cv2.imread(self.img_name)
        text = pytesseract.image_to_string(img)
        all_text_list = re.split(r'[\n]', text)
        
        # Process the text list to remove all whitespace elements in the list.
        text_list = [i for i in all_text_list if re.search(r'\S', i)]

        # Extracting all the necessary details from the pruned text list.
        # 1) Aadhar Card No.
        aadhar_no_pat = r'^[0-9]{4}\s[0-9]{4}\s[0-9]{4}$'
        for i in text_list:
            if re.match(aadhar_no_pat, i):
                self.user_aadhar_no = i
                break  # Break out once Aadhar number is found

        # 2) Gender
        aadhar_gender_pat = r'(Male|MALE|male|Female|FEMALE|female)'
        for i in text_list:
            if re.search(aadhar_gender_pat, i):
                if re.search(r'(Male|MALE|male)', i):
                    self.user_gender = 'MALE'
                elif re.search(r'(Female|FEMALE|female)', i):
                    self.user_gender = 'FEMALE'
                break  # Break out once gender is found

        #  3) DOB
        aadhar_dob_pat = r'(Year|Birth|irth|YoB|YOB:|DOB:|DOB)'
        date_ele = str()
        for idx, i in enumerate(text_list):
            if re.search(aadhar_dob_pat, i):
                index = re.search(aadhar_dob_pat, i).span()[1]
                date_ele = i
                dob_idx = idx
            else:
                continue

        date_str=''
        for i in date_ele[index:]:
            if re.match(r'\d', i):
                date_str = date_str+i
            elif re.match(r'/', i):
                date_str = date_str+i
            else:
                continue
        self.user_dob = date_str
    
        if dob_idx > 0:
            self.user_name = text_list[dob_idx - 1]
        
        # Print extracted details to console
        print("Extracted Data:")
        print("Aadhar Number:", self.user_aadhar_no)
        print("Gender:", self.user_gender)
        print("Date of Birth:", self.user_dob)
        print("Name:", self.user_name)
        
        return [self.user_aadhar_no, self.user_gender, self.user_dob, self.user_name]
