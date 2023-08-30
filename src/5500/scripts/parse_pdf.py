import PyPDF2

def split_pdf(file_path):
    pdf_file = open(file_path, 'rb')
    pdf_reader = PyPDF2.PdfFileReader(pdf_file)
    num_pages = pdf_reader.numPages

    pdf_writer = PyPDF2.PdfFileWriter()
    for page_num in range(0, 3):
        page = pdf_reader.getPage(page_num)
        pdf_writer.addPage(page)
    with open('first_3_pages.pdf', 'wb') as f:
        pdf_writer.write(f)

    for i in range(3, num_pages, 4):
        pdf_writer = PyPDF2.PdfFileWriter()
        for page_num in range(i, i + 4):
            if page_num < num_pages:
                page = pdf_reader.getPage(page_num)
                pdf_writer.addPage(page)
        with open(f'other_pages_{i}.pdf', 'wb') as f:
            pdf_writer.write(f)

    pdf_file.close()

split_pdf('/Users/nzozaya@sitetracker.com/Desktop/Dropbox_5500.pdf')
