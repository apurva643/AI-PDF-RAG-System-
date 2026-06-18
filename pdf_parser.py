from PyPDF2 import PdfReader
from io import BytesIO


def extract_text_from_pdf(contents):

    pdf_file = BytesIO(contents)

    reader = PdfReader(pdf_file)

    pages = []

    for i, page in enumerate(reader.pages):

        text = page.extract_text()

        if text:

            pages.append(

                {
                    "text": text,
                    "page": i + 1
                }

            )

    return pages