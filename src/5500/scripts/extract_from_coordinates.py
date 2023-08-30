def extract_text_from_coordinates(pdf_page, coordinates):
    cropped_area = pdf_page.within_bbox(coordinates)
    text = cropped_area.extract_text()
    return text
