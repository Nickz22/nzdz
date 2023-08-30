import pdfplumber
import cv2
import numpy as np
import os
import pytesseract
import time  # Import the time module at the top of your script

# Function to check for blue "X" in image
def contains_blue_x(image):
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    lower_blue = np.array([90, 50, 50])
    upper_blue = np.array([140, 255, 255])
    hsv_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2HSV)
    mask = cv2.inRange(hsv_image, lower_blue, upper_blue)
    non_zero_count = np.count_nonzero(mask)
    return non_zero_count > 0

# Coordinates for checkbox detection
ARR_CHECKBOX_COORDINATES = {
    'Annual_Return_Report__Annual_Report_Identification_Information__A_MultiEmployer_Plan': {'x0': 154.03, 'y0': 189.31, 'x1': 161.03, 'y1':201.31},
    'Annual_Return_Report__Annual_Report_Identification_Information__A_Multiple_Employer_Plan': {'x0': 295.03, 'y0': 189.31, 'x1': 303.03, 'y1':201.31},
    'Annual_Return_Report__Annual_Report_Identification_Information__A_Single_Employer_Plan': {'x0': 154.03, 'y0': 212.31, 'x1': 161.03, 'y1': 224.31},
    'Annual_Return_Report__Annual_Report_Identification_Information__A_DFE': {'x0': 295.03, 'y0': 212.31, 'x1': 303.03, 'y1': 224.31},
    'Annual_Return_Report__Annual_Report_Identification_Information__The_First_Return_Report': {'x0': 154.03, 'y0': 222.31, 'x1': 161.03, 'y1':238.31},
    'Annual_Return_Report__Annual_Report_Identification_Information__The_Final_Return_Report': {'x0': 295.03, 'y0': 222.31, 'x1': 303.03, 'y1':238.31},
    'Annual_Return_Report__Annual_Report_Identification_Information__An_Amended_Return_Report': {'x0': 154.03, 'y0': 241.31, 'x1': 161.03, 'y1':252.31},
    'Annual_Return_Report__Annual_Report_Identification_Information__A_Short_Plan_Year_Return_Report': {'x0': 295.03, 'y0': 241.31, 'x1': 303.03, 'y1':252.31},
    'Annual_Return_Report__Annual_Report_Identification_Information__Form5558' : {'x0': 148.00, 'y0': 273.31, 'x1': 156.03, 'y1':286.31},
    'Annual_Return_Report__Annual_Report_Identification_Information__Automatic_Extension' : {'x0': 292.00, 'y0': 273.31, 'x1': 300.03, 'y1':286.31},
    'Annual_Return_Report__Annual_Report_Identification_Information__the_DVFC_program' : {'x0': 471, 'y0': 273.31, 'x1': 478.03, 'y1':286.31},
    'Annual_Return_Report__Annual_Report_Identification_Information__Collectively_Bargained' : {'x0': 500, 'y0': 256.31, 'x1': 507, 'y1':268.31},
    # 'title__Insurance_Information': {'x0': 225.03, 'y0': 50.31, 'x1': 370.03, 'y1':70.31}
    # 'Annual_Return_Report__Annual_Report_Identification_Information__Plan_Year_Ending' : {'x0': 425.03, 'y0': 177.31, 'x1': 485.03, 'y1':187.31},
}

ARR_TEXT_COORDINATES = {
    'Annual_Return_Report__Annual_Report_Identification_Information__Plan_Year_Beginning' : {'x0': 225.03, 'y0': 177.31, 'x1': 285.03, 'y1':187.31},
    'Annual_Return_Report__Annual_Report_Identification_Information__Plan_Year_Ending' : {'x0': 425.03, 'y0': 177.31, 'x1': 485.03, 'y1':187.31},
    'Annual_Return_Report__Basic_Plan_Information__Name_of_plan' : {'x0': 15.03, 'y0': 325.31, 'x1': 460.03, 'y1':355.31}
}

II_CHECKBOX_COORDINATES = {
    
}

II_TEXT_COORDINATES = {
    'Insurance_Information__Plan_Year_Beginning' : { 'x0': 220.03, 'y0': 148, 'x1': 300, 'y1':157},
    'Insurance_Information__Plan_Year_Ending' : { 'x0': 420.03, 'y0': 148, 'x1': 500, 'y1':157},
    'Insurance_Information__Name_of_Plan' : { 'x0': 15.03, 'y0': 168, 'x1': 350, 'y1':200},
    'Insurance_Information__Plan_Sponsors_Name__c' : { 'x0': 15.03, 'y0': 213, 'x1': 350, 'y1':235},
    'Insurance_Information__Three_Digit_PN' : { 'x0': 495, 'y0': 160, 'x1': 600, 'y1':180}
}

field_label_to_preserve = 'Annual_Return_Report__Annual_Report_Identification_Information__Plan_Year_Ending'

# Coordinates for text extraction
PAGE_TITLE_COORDINATES = {
    'title__Annual_Return_Report': {'x0': 160.03, 'y0': 70.31, 'x1': 300.03, 'y1':85.31},
    'title__Insurance_Information': {'x0': 225.03, 'y0': 50.31, 'x1': 370.03, 'y1':70.31}
}

NO_OCR_TEXT_COORDINATES = {
    'Insurance_Information__Three_Digit_PN' : { 'x0': 495, 'y0': 160, 'x1': 600, 'y1':180},
    'Annual_Return_Report__Annual_Report_Identification_Information__Plan_Year_Beginning' : {'x0': 225.03, 'y0': 177.31, 'x1': 285.03, 'y1':187.31},
    'Annual_Return_Report__Annual_Report_Identification_Information__Plan_Year_Ending' : {'x0': 425.03, 'y0': 177.31, 'x1': 485.03, 'y1':187.31},
    'Insurance_Information__Plan_Year_Beginning' : { 'x0': 220.03, 'y0': 148, 'x1': 300, 'y1':157},
    'Insurance_Information__Plan_Year_Ending' : { 'x0': 420.03, 'y0': 148, 'x1': 500, 'y1':157},
}

# Function for checkbox detection
def extract_checkbox_fields(pdf_page, coords_dict):
    extracted_data = {}
    for field_label, coords in coords_dict.items():
        x0, y0, x1, y1 = coords['x0'], coords['y0'], coords['x1'], coords['y1']
        img = pdf_page.crop((x0, y0, x1, y1)).to_image()
        img_path = f"{field_label}_temp_image.png"
        img.save(img_path, format='PNG')
        np_img = cv2.imread(img_path)
        is_checked = contains_blue_x(np_img)
        extracted_data[field_label] = is_checked
        if field_label != field_label_to_preserve:
            os.remove(img_path)
    return extracted_data

def scale_and_ocr(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    return pytesseract.image_to_string(img)

# Function for text extraction
def extract_text_fields(pdf_page, coords_dict):
    extracted_data = {}
    for field_label, coords in coords_dict.items():
        x0, y0, x1, y1 = coords['x0'], coords['y0'], coords['x1'], coords['y1']
        cropped = pdf_page.crop((x0, y0, x1, y1))
        
        if field_label in NO_OCR_TEXT_COORDINATES:
            extracted_text = cropped.extract_text()
        else:
            img = cropped.to_image()
            img_path = f"{field_label}_temp_ocr_image.png"
            img.save(img_path, format='PNG')
            extracted_text = scale_and_ocr(img_path)
            os.remove(img_path)
            
        extracted_data[field_label] = extracted_text
    return extracted_data


# File path to your PDF
pdf_path = '/Users/nzozaya@sitetracker.com/Desktop/20180921073157P030207269121001.pdf'

# Open the PDF file and process it
with pdfplumber.open(pdf_path) as pdf:
    for page_number, pdf_page in enumerate(pdf.pages):
        print(f"------------------------------------------")
        page_titles = extract_text_fields(pdf_page, PAGE_TITLE_COORDINATES)
        
        if page_titles.get('title__Annual_Return_Report', '').startswith("Annual Return/Report"):
            print(f"Processing 'Annual Return/Report' on page {page_number + 1}...")
            checkbox_data = extract_checkbox_fields(pdf_page, ARR_CHECKBOX_COORDINATES)
            text_data = extract_text_fields(pdf_page, ARR_TEXT_COORDINATES)
            
            print(f"Checkbox Data for page {page_number + 1}:")
            for key in checkbox_data.keys():
                print(f"{key}: {checkbox_data[key]}")

            print(f"\nText Data for page {page_number + 1}:")
            for key in text_data.keys():
                print(f"{key}: {text_data[key]}")

        elif page_titles.get('title__Insurance_Information', '').startswith("Insurance Information"):
            print(f"Processing 'Insurance Information' on page {page_number + 1}...")
            checkbox_data = extract_checkbox_fields(pdf_page, II_CHECKBOX_COORDINATES)
            text_data = extract_text_fields(pdf_page, II_TEXT_COORDINATES)

            print(f"Checkbox Data for page {page_number + 1}:")
            for key in checkbox_data.keys():
                print(f"{key}: {checkbox_data[key]}")

            print(f"\nText Data for page {page_number + 1}:")
            for key in text_data.keys():
                print(f"{key}: {text_data[key]}")

        time.sleep(1)  # Pause for 2 seconds before moving to the next page