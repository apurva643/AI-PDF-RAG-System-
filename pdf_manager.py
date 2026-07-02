uploaded_pdfs = set()


def add_pdf(filename):

    uploaded_pdfs.add(
        filename
    )


def get_uploaded_pdfs():

    return list(
        uploaded_pdfs
    )


def clear_pdfs():

    uploaded_pdfs.clear()