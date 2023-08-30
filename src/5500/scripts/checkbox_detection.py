import pdfplumber
import cv2
import numpy as np
import os

def contains_blue_x(image):
    # Convert to the RGB color space
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Define the lower and upper bounds for blue color
    lower_blue = np.array([90, 50, 50])
    upper_blue = np.array([140, 255, 255])
    
    # Threshold the image to keep only blue regions
    hsv_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2HSV)
    mask = cv2.inRange(hsv_image, lower_blue, upper_blue)
    
    # Count non-zero pixels in the mask
    non_zero_count = np.count_nonzero(mask)
    
    return non_zero_count > 0

CHECKBOX_COORDINATES_DICT = {
    'Annual_Return_Report__Annual_Report_Identification_Information__A_MultiEmployer_Plan': {'x0': 154.03, 'y0': 189.31, 'x1': 161.03, 'y1':201.31},
    'Annual_Return_Report__Annual_Report_Identification_Information__A_Multiple_Employer_Plan': {'x0': 295.03, 'y0': 189.31, 'x1': 303.03, 'y1':201.31},
    'Annual_Return_Report__Annual_Report_Identification_Information__A_Single_Employer_Plan': {'x0': 154.03, 'y0': 212.31, 'x1': 161.03, 'y1': 224.31},
    'Annual_Return_Report__Annual_Report_Identification_Information__A_DFE': {'x0': 295.03, 'y0': 212.31, 'x1': 303.03, 'y1': 224.31},
    'Annual_Return_Report__Annual_Report_Identification_Information__The_First_Return_Report': {'x0': 154.03, 'y0': 222.31, 'x1': 161.03, 'y1':238.31},
    'Annual_Return_Report__Annual_Report_Identification_Information__The_Final_Return_Report': {'x0': 295.03, 'y0': 222.31, 'x1': 303.03, 'y1':238.31},
    'Annual_Return_Report__Annual_Report_Identification_Information__An_Amended_Return_Report': {'x0': 154.03, 'y0': 241.31, 'x1': 161.03, 'y1':252.31},
    'Annual_Return_Report__Annual_Report_Identification_Information__A_Short_Plan_Year_Return_Report': {'x0': 295.03, 'y0': 241.31, 'x1': 303.03, 'y1':252.31}
}

import os

def extract_all_fields(pdf_page, CHECKBOX_COORDINATES_DICT):
    extracted_data = {}
    for field_label, coords in CHECKBOX_COORDINATES_DICT.items():
        x0, y0, x1, y1 = coords['x0'], coords['y0'], coords['x1'], coords['y1']
        
        # Convert to image and check for blue "X"
        img = pdf_page.crop((x0, y0, x1, y1)).to_image()
        
        # Save the image with a unique name
        img_path = f"{field_label}_temp_image.png"
        img.save(img_path, format='PNG')
        
        # Read the image using OpenCV
        np_img = cv2.imread(img_path)
        
        # Check for blue "X"
        is_checked = contains_blue_x(np_img)
        
        # Store the result
        extracted_data[field_label] = is_checked
        
        # Remove the temporary image, unless it's for a specific label
        if field_label != 'Annual_Report_Identification_Information__A_DFE':
            os.remove(img_path)

    return extracted_data


# File path to your PDF
pdf_path = '/Users/nzozaya@sitetracker.com/Desktop/20191011155705P030069089841001.pdf'

# Open the PDF file
with pdfplumber.open(pdf_path) as pdf:
    pdf_page = pdf.pages[0]
    extracted_data_dict = extract_all_fields(pdf_page, CHECKBOX_COORDINATES_DICT)

for key in CHECKBOX_COORDINATES_DICT.keys():
    print(f"{key}: {extracted_data_dict[key]}")
